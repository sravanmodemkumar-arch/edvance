# Module 56 — Platform Billing & GST Invoicing

## 1. Purpose & Scope

Platform Billing & GST Invoicing handles EduForge's own revenue collection — charging institutions, TSPs, and B2C students for platform access. This module is entirely separate from Module 24–26 (fee management within institutions).

Coverage:
- B2B subscription invoicing to institutions
- TSP wholesale billing (active student count × tier rate)
- B2C student payments for mock tests and AI credits
- GST-compliant tax invoices (B2B, B2C, e-invoice via IRP)
- Razorpay payment integration (UPI, Cards, Net Banking, E-NACH)
- Dunning management (retry → warning → suspension)
- Credit notes (SLA credits, refunds, adjustments)
- GSTR-1 / GSTR-3B / GSTR-9 export automation

---

## 2. GST Compliance Architecture

### 2.1 Invoice Types and GST Treatment

| Invoice Type | GST Treatment | Mandatory Fields |
|-------------|---------------|-----------------|
| B2B (inter-state) | 18% IGST | Both GSTINs, HSN, IRN, QR |
| B2B (intra-state) | 9% CGST + 9% SGST | Both GSTINs, HSN, IRN, QR |
| B2C > Rs. 2.5L | 18% IGST | Seller GSTIN, buyer address, HSN |
| B2C < Rs. 2.5L | 18% IGST | Seller GSTIN, HSN (aggregated in GSTR-1 B2CS) |
| Government exempt | Nil GST | Exemption certificate reference |
| Credit Note | Reverses tax of original invoice | Original invoice reference mandatory |

HSN code for all EduForge services: **9984** (Online Information and Database Access/Retrieval Services)

### 2.2 Place of Supply

For digital services, place of supply = location of supplier (IGST Act Section 13). This means:
- All B2C invoices → IGST (18%) regardless of student state
- B2B invoices → IGST if buyer in different state, CGST+SGST if same state as EduForge registration

### 2.3 GSTIN Validation

```python
# billing/gstin_validator.py
import httpx, re

GSTIN_REGEX = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$")
GST_API_URL = "https://api.gst.gov.in/commonapi/v1.1/taxpayerDetails"

def validate_gstin(gstin: str) -> dict:
    """
    Validate GSTIN format + verify against GST portal API.
    Returns taxpayer details if valid.
    """
    gstin = gstin.strip().upper()
    if not GSTIN_REGEX.match(gstin):
        raise ValueError(f"Invalid GSTIN format: {gstin}")
    # Verify against GST portal (non-blocking; cached for 24h)
    cache_key = f"gstin:{gstin}"
    cached = redis_get(cache_key)  # DynamoDB cache, 24h TTL
    if cached:
        return cached
    resp = httpx.get(f"{GST_API_URL}/{gstin}", timeout=5.0)
    if resp.status_code == 200:
        data = resp.json()
        set_cache(cache_key, data, ttl=86400)
        return data
    return {"gstin": gstin, "status": "unverified"}
```

---

## 3. Invoice Generation

### 3.1 Invoice PDF (WeasyPrint)

```python
# billing/invoice_generator.py
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader

jinja = Environment(loader=FileSystemLoader("templates/billing"))

def generate_invoice_pdf(invoice_id: str) -> bytes:
    invoice = get_invoice_with_lines(invoice_id)
    einvoice = get_einvoice(invoice_id)  # IRN + QR code if applicable

    html = jinja.get_template("tax_invoice.html").render(
        invoice=invoice,
        irn=einvoice["irn"] if einvoice else None,
        qr_code_b64=einvoice["signed_qr_code"] if einvoice else None,
        seller={
            "name": "EduForge Technologies Pvt. Ltd.",
            "gstin": EDUFORGE_GSTIN,
            "address": "123, Tech Park, Bandra Kurla Complex, Mumbai 400051",
            "email": "billing@eduforge.in",
            "pan": "AABCE1234F",
        },
    )
    return HTML(string=html).write_pdf()


def get_or_generate_pdf(invoice_id: str, tenant_id: str) -> str:
    """Return S3 key for invoice PDF, generating if not exists."""
    invoice = db.fetchone("SELECT * FROM billing.invoices WHERE id = %s", [invoice_id])
    if invoice["pdf_s3_key"]:
        return invoice["pdf_s3_key"]
    pdf_bytes = generate_invoice_pdf(invoice_id)
    s3_key = f"invoices/{tenant_id}/{invoice['financial_year']}/{invoice['invoice_number']}.pdf"
    s3.put_object(
        Bucket=INVOICES_BUCKET,
        Key=s3_key,
        Body=pdf_bytes,
        ContentType="application/pdf",
        ServerSideEncryption="AES256",
    )
    db.execute("UPDATE billing.invoices SET pdf_s3_key = %s WHERE id = %s", [s3_key, invoice_id])
    return s3_key
```

### 3.2 Invoice Numbering

```python
# billing/invoice_numbering.py
def next_invoice_number(tenant_id: str, financial_year: str) -> str:
    """
    Generate sequential invoice number per financial year.
    No gaps allowed (GST audit requirement).
    Uses PostgreSQL advisory lock for concurrency safety.
    """
    with db.transaction():
        # Advisory lock: prevents concurrent invoice numbering
        db.execute("SELECT pg_advisory_xact_lock(hashtext(%s))", [f"invoice_{financial_year}"])
        result = db.fetchone("""
            SELECT COALESCE(MAX(sequence_number), 0) + 1 AS next_seq
            FROM billing.invoices
            WHERE financial_year = %s
        """, [financial_year])
        seq = result["next_seq"]
        tenant_code = get_tenant_code(tenant_id)  # 4-char alphanumeric
        return f"EDU-{financial_year}-{tenant_code}-{seq:05d}"

def get_financial_year(date: date) -> str:
    """Returns FY string like '2526' for Apr 2025 – Mar 2026."""
    if date.month >= 4:
        return f"{str(date.year)[2:]}{str(date.year + 1)[2:]}"
    else:
        return f"{str(date.year - 1)[2:]}{str(date.year)[2:]}"
```

### 3.3 Invoice Sequence Continuity Check

```python
# Nightly Lambda: verify no gaps in invoice sequence
def check_invoice_sequence_continuity():
    for fy in get_active_financial_years():
        gaps = db.fetchall("""
            WITH numbered AS (
                SELECT sequence_number,
                       LAG(sequence_number) OVER (ORDER BY sequence_number) AS prev_seq
                FROM billing.invoices
                WHERE financial_year = %s
            )
            SELECT sequence_number, prev_seq
            FROM numbered
            WHERE sequence_number != prev_seq + 1 AND prev_seq IS NOT NULL
        """, [fy])
        if gaps:
            notify_slack(
                channel="#billing-alerts",
                message=f":warning: Invoice sequence gaps in FY {fy}: {gaps}"
            )
```

---

## 4. E-Invoicing (IRP)

### 4.1 E-Invoice JSON Builder

```python
# billing/einvoice.py
import httpx, json

IRP_BASE = "https://einvoice1.gst.gov.in"  # Production
IRP_SESSION_TTL = 1800  # 30 minutes

_irp_token: str | None = None
_irp_token_expiry: float = 0

def get_irp_token() -> str:
    global _irp_token, _irp_token_expiry
    if _irp_token and time.time() < _irp_token_expiry - 60:
        return _irp_token
    resp = httpx.post(f"{IRP_BASE}/api/login", json={
        "UserName": get_secret("irp_username"),
        "Password": get_secret("irp_password"),
        "AppKey": get_secret("irp_app_key"),
        "ForceRefreshAccessToken": "Y",
    })
    resp.raise_for_status()
    _irp_token = resp.json()["Data"]["AuthToken"]
    _irp_token_expiry = time.time() + IRP_SESSION_TTL
    return _irp_token


def build_einvoice_json(invoice: dict, line_items: list[dict]) -> dict:
    """Build NIC e-invoice JSON from EduForge invoice data."""
    return {
        "Version": "1.1",
        "TranDtls": {
            "TaxSch": "GST",
            "SupTyp": "B2B",  # B2B, SEZWP, SEZWOP, EXPWP, EXPWOP, DEXP
            "RegRev": "N",
            "EcmGstin": None,
            "IgstOnIntra": "N",
        },
        "DocDtls": {
            "Typ": "INV",
            "No": invoice["invoice_number"],
            "Dt": invoice["invoice_date"].strftime("%d/%m/%Y"),
        },
        "SellerDtls": {
            "Gstin": EDUFORGE_GSTIN,
            "LglNm": "EduForge Technologies Pvt. Ltd.",
            "TrdNm": "EduForge",
            "Addr1": "123, Tech Park, BKC",
            "Loc": "Mumbai",
            "Pin": 400051,
            "Stcd": "27",  # Maharashtra state code
        },
        "BuyerDtls": {
            "Gstin": invoice["buyer_gstin"],
            "LglNm": invoice["buyer_legal_name"],
            "TrdNm": invoice["buyer_trade_name"],
            "Pos": invoice["place_of_supply_state_code"],
            "Addr1": invoice["buyer_address"],
            "Loc": invoice["buyer_city"],
            "Pin": invoice["buyer_pin"],
            "Stcd": invoice["buyer_state_code"],
            "Ph": invoice["buyer_phone"],
            "Em": invoice["buyer_email"],
        },
        "ItemList": [
            {
                "SlNo": str(i + 1),
                "PrdDesc": item["description"],
                "IsServc": "Y",
                "HsnCd": "9984",
                "Qty": item["quantity"],
                "Unit": "OTH",
                "UnitPrice": float(item["unit_price"]),
                "TotAmt": float(item["taxable_amount"]),
                "AssAmt": float(item["taxable_amount"]),
                "GstRt": 18.0,
                "IgstAmt": float(item["igst_amount"]),
                "CgstAmt": float(item["cgst_amount"]),
                "SgstAmt": float(item["sgst_amount"]),
                "TotItemVal": float(item["total_amount"]),
            }
            for i, item in enumerate(line_items)
        ],
        "ValDtls": {
            "AssVal": float(invoice["taxable_amount"]),
            "IgstVal": float(invoice["igst_amount"]),
            "CgstVal": float(invoice["cgst_amount"]),
            "SgstVal": float(invoice["sgst_amount"]),
            "TotInvVal": float(invoice["total_amount"]),
        },
    }


def register_einvoice(invoice_id: str) -> dict:
    """
    Submit invoice to IRP and get IRN + signed QR code.
    On IRP failure: queue to SQS for retry (never block invoice issuance).
    """
    invoice = get_invoice_with_lines(invoice_id)
    # Only B2B invoices with buyer GSTIN get e-invoice
    if not invoice["buyer_gstin"] or invoice["invoice_type"] == "b2c":
        return {}
    ein_json = build_einvoice_json(invoice, invoice["line_items"])
    token = get_irp_token()
    try:
        resp = httpx.post(
            f"{IRP_BASE}/api/inv/generate",
            headers={"user_name": get_secret("irp_username"), "authtoken": token, "gstin": EDUFORGE_GSTIN},
            json={"Data": encrypt_irp_payload(json.dumps(ein_json))},
            timeout=10.0,
        )
        data = resp.json()["Data"]
        irn = data["Irn"]
        qr_code = data["SignedQRCode"]
        # Store
        db.execute("""
            INSERT INTO billing.einvoices (invoice_id, irn, signed_qr_code, registered_at)
            VALUES (%s, %s, %s, NOW())
        """, [invoice_id, irn, qr_code])
        return {"irn": irn, "signed_qr_code": qr_code}
    except Exception as e:
        # Queue for retry — don't fail invoice issuance
        sqs.send_message(
            QueueUrl=EINVOICE_RETRY_QUEUE,
            MessageBody=json.dumps({"invoice_id": invoice_id}),
            DelaySeconds=300,  # Retry in 5 minutes
        )
        logger.error(f"IRP submission failed for {invoice_id}: {e}")
        return {}
```

---

## 5. Subscription Billing Engine

### 5.1 Monthly Invoice Generation

```python
# billing/subscription_billing.py  (runs on 1st of each month, EventBridge)

def generate_monthly_invoices():
    today = date.today()
    financial_year = get_financial_year(today)

    active_subscriptions = db.fetchall("""
        SELECT ts.*, tp.name AS plan_name, tp.monthly_price, tp.annual_price,
               t.name AS tenant_name, t.billing_gstin, t.billing_address,
               t.billing_contact_email
        FROM subscriptions.tenant_subscriptions ts
        JOIN subscriptions.subscription_plans tp ON tp.plan_id = ts.plan_id
        JOIN tenants t ON t.id = ts.tenant_id
        WHERE ts.status = 'active'
            AND ts.billing_cycle = 'monthly'
    """)

    for sub in active_subscriptions:
        # Check no duplicate invoice for this period
        existing = db.fetchone("""
            SELECT id FROM billing.invoices
            WHERE tenant_id = %s AND billing_period_start = %s AND status != 'cancelled'
        """, [sub["tenant_id"], today.replace(day=1)])
        if existing:
            continue  # Already invoiced

        invoice_number = next_invoice_number(sub["tenant_id"], financial_year)
        taxable_amount = sub["monthly_price"]
        # GST: IGST if inter-state, CGST+SGST if intra-state
        is_inter_state = is_inter_state_supply(sub["billing_gstin"])
        igst = taxable_amount * Decimal("0.18") if is_inter_state else Decimal("0")
        cgst = taxable_amount * Decimal("0.09") if not is_inter_state else Decimal("0")
        sgst = taxable_amount * Decimal("0.09") if not is_inter_state else Decimal("0")
        total = taxable_amount + igst + cgst + sgst

        invoice_id = db.fetchone("""
            INSERT INTO billing.invoices
            (tenant_id, invoice_number, financial_year, invoice_type, invoice_date,
             billing_period_start, billing_period_end,
             buyer_gstin, buyer_legal_name, buyer_address,
             taxable_amount, igst_amount, cgst_amount, sgst_amount, total_amount,
             status, created_at)
            VALUES (%s,%s,%s,'b2b',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'pending',NOW())
            RETURNING id
        """, [
            sub["tenant_id"], invoice_number, financial_year, today,
            today.replace(day=1), (today.replace(day=1) + relativedelta(months=1) - timedelta(days=1)),
            sub["billing_gstin"], sub["tenant_name"], sub["billing_address"],
            taxable_amount, igst, cgst, sgst, total,
        ])["id"]

        # Add line item
        db.execute("""
            INSERT INTO billing.invoice_line_items
            (invoice_id, description, hsn_code, quantity, unit_price, taxable_amount, igst_amount, cgst_amount, sgst_amount, total_amount)
            VALUES (%s, %s, '9984', 1, %s, %s, %s, %s, %s, %s)
        """, [invoice_id, f"{sub['plan_name']} Subscription — {today.strftime('%B %Y')}",
              taxable_amount, taxable_amount, igst, cgst, sgst, total])

        # Apply pending SLA credits
        apply_pending_credits(invoice_id, sub["tenant_id"])

        # Register e-invoice with IRP (async, non-blocking)
        sqs.send_message(QueueUrl=EINVOICE_QUEUE, MessageBody=json.dumps({"invoice_id": invoice_id}))

        # Generate PDF + send email (async)
        sqs.send_message(QueueUrl=INVOICE_DELIVERY_QUEUE, MessageBody=json.dumps({
            "invoice_id": invoice_id,
            "email": sub["billing_contact_email"],
        }))

        # Initiate payment (Razorpay)
        if sub.get("razorpay_subscription_id"):
            # Razorpay handles auto-debit — no action needed
            pass
        else:
            # Manual payment link
            create_payment_order(invoice_id, total)
```

### 5.2 Proration

```python
def compute_proration(plan_price_monthly: Decimal, start_date: date) -> Decimal:
    """
    Compute pro-rated amount for partial first month.
    """
    first_day = start_date.replace(day=1)
    last_day = (first_day + relativedelta(months=1)) - timedelta(days=1)
    days_in_month = last_day.day
    days_remaining = (last_day - start_date).days + 1
    daily_rate = plan_price_monthly / days_in_month
    return (daily_rate * days_remaining).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def compute_upgrade_proration(
    old_price: Decimal,
    new_price: Decimal,
    upgrade_date: date,
) -> Decimal:
    """
    Charge the difference for the remaining days in the billing cycle.
    """
    last_day = (upgrade_date.replace(day=1) + relativedelta(months=1)) - timedelta(days=1)
    days_in_month = last_day.day
    days_remaining = (last_day - upgrade_date).days + 1
    daily_difference = (new_price - old_price) / days_in_month
    return (daily_difference * days_remaining).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
```

---

## 6. Razorpay Integration

### 6.1 Order Creation & Payment Flow

```python
# billing/razorpay_integration.py
import razorpay
import hmac, hashlib

rz_client = razorpay.Client(
    auth=(get_secret("razorpay_key_id"), get_secret("razorpay_key_secret"))
)

def create_payment_order(invoice_id: str, amount: Decimal) -> dict:
    """Create Razorpay order for an invoice."""
    order = rz_client.order.create({
        "amount": int(amount * 100),  # Razorpay expects paise
        "currency": "INR",
        "receipt": invoice_id,        # Idempotency key
        "notes": {
            "invoice_number": get_invoice_number(invoice_id),
            "tenant_id": get_invoice_tenant(invoice_id),
        },
    })
    db.execute("""
        UPDATE billing.invoices SET razorpay_order_id = %s WHERE id = %s
    """, [order["id"], invoice_id])
    return order


def handle_razorpay_webhook(payload: bytes, signature: str):
    """
    Verify and process Razorpay webhook events.
    Idempotent: DynamoDB stores processed event IDs (24h TTL).
    """
    # Verify HMAC-SHA256 signature
    expected = hmac.new(
        get_secret("razorpay_webhook_secret").encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise ValueError("Invalid Razorpay webhook signature")

    event = json.loads(payload)
    event_id = event["payload"]["payment"]["entity"]["id"]

    # Idempotency check
    try:
        WEBHOOK_DEDUP_TABLE.put_item(
            Item={"event_id": event_id, "ttl": int(time.time()) + 86400},
            ConditionExpression="attribute_not_exists(event_id)",
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return  # Already processed

    event_type = event["event"]
    if event_type == "payment.captured":
        _on_payment_captured(event["payload"]["payment"]["entity"])
    elif event_type == "payment.failed":
        _on_payment_failed(event["payload"]["payment"]["entity"])
    elif event_type == "subscription.charged":
        _on_subscription_charged(event["payload"]["subscription"]["entity"])
    elif event_type == "refund.processed":
        _on_refund_processed(event["payload"]["refund"]["entity"])


def _on_payment_captured(payment: dict):
    invoice_id = payment["receipt"]
    db.execute("""
        UPDATE billing.invoices SET status = 'paid', paid_at = NOW() WHERE id = %s
    """, [invoice_id])
    db.execute("""
        INSERT INTO billing.payments
        (invoice_id, razorpay_payment_id, method, amount, captured_at)
        VALUES (%s, %s, %s, %s, NOW())
    """, [invoice_id, payment["id"], payment["method"], Decimal(payment["amount"]) / 100])
    # Reset dunning state
    db.execute("""
        UPDATE billing.dunning_state SET status = 'cleared', cleared_at = NOW()
        WHERE invoice_id = %s
    """, [invoice_id])
    # Re-activate service if suspended
    reactivate_service_if_suspended(get_invoice_tenant(invoice_id))
    # Update tax ledger
    record_tax_entry(invoice_id)
```

### 6.2 Dunning State Machine

```python
# billing/dunning.py
from enum import Enum

class DunningStatus(str, Enum):
    ACTIVE         = "active"
    PAYMENT_FAILED = "payment_failed"
    RETRY_1        = "retry_1"         # D+3
    RETRY_2        = "retry_2"         # D+7
    OVERDUE        = "overdue"         # D+14
    SUSPENDED      = "suspended"       # D+30
    DEACTIVATED    = "deactivated"     # D+60

DUNNING_SCHEDULE = [
    (0,  "payment_failed", "Payment failed — please update payment method"),
    (3,  "retry_1",        "Reminder: payment due"),
    (7,  "retry_2",        "Warning: service may be suspended"),
    (14, "overdue",        "Final notice: payment overdue"),
    (30, "suspended",      "Service suspended due to non-payment"),
    (60, "deactivated",    "Account deactivated"),
]

def process_dunning_step(tenant_id: str):
    """
    Called daily by EventBridge scheduled rule for each tenant in dunning.
    """
    state = db.fetchone("""
        SELECT * FROM billing.dunning_state WHERE tenant_id = %s AND status != 'cleared'
    """, [tenant_id])
    if not state:
        return

    days_since_failure = (date.today() - state["failure_date"]).days
    for threshold, new_status, message in reversed(DUNNING_SCHEDULE):
        if days_since_failure >= threshold and state["status"] != new_status:
            _apply_dunning_step(tenant_id, new_status, message, state)
            break


def _apply_dunning_step(tenant_id: str, status: str, message: str, state: dict):
    db.execute("""
        UPDATE billing.dunning_state SET status = %s, updated_at = NOW() WHERE tenant_id = %s
    """, [status, tenant_id])

    if status == "suspended":
        suspend_tenant(tenant_id)

    # Attempt payment retry
    if status in ("retry_1", "retry_2"):
        retry_payment(state["invoice_id"])

    # Send notification
    send_dunning_notification(tenant_id, message, state["invoice_id"])
```

---

## 7. TSP Wholesale Billing

### 7.1 Active Student Count Computation

```python
# billing/tsp_billing.py
def compute_tsp_billing(tsp_id: str, billing_month: date) -> dict:
    """
    Count distinct active students (≥1 login) across TSP's tenants in billing month.
    Uses Athena analytics lake for accurate count.
    """
    month_start = billing_month.replace(day=1)
    month_end = (month_start + relativedelta(months=1)) - timedelta(days=1)

    active_students = athena_query(f"""
        SELECT COUNT(DISTINCT user_id) AS student_count
        FROM curated.fact_api_calls
        WHERE tenant_id IN (
            SELECT tenant_id FROM tsp.tsp_tenants WHERE tsp_id = '{tsp_id}'
        )
        AND user_role = 'student'
        AND date BETWEEN DATE '{month_start}' AND DATE '{month_end}'
    """)["student_count"]

    rate = get_wholesale_rate(active_students)
    net_amount = Decimal(str(active_students)) * rate
    gst_amount = net_amount * Decimal("0.18")

    return {
        "tsp_id": tsp_id,
        "billing_month": billing_month,
        "active_student_count": active_students,
        "wholesale_rate": rate,
        "net_amount": net_amount,
        "gst_amount": gst_amount,
        "total_amount": net_amount + gst_amount,
    }


WHOLESALE_RATE_TIERS = [
    (500000, Decimal("0.40")),  # > 500K students
    (50000,  Decimal("0.45")),  # > 50K students
    (10000,  Decimal("0.48")),  # > 10K students
    (1000,   Decimal("0.50")),  # > 1K students
    (0,      Decimal("0.55")),  # < 1K students
]

def get_wholesale_rate(student_count: int) -> Decimal:
    for threshold, rate in WHOLESALE_RATE_TIERS:
        if student_count > threshold:
            return rate
    return WHOLESALE_RATE_TIERS[-1][1]
```

---

## 8. Credit Notes

```python
# billing/credit_notes.py

def create_credit_note(
    tenant_id: str,
    original_invoice_id: str,
    credit_amount: Decimal,
    reason: str,
    created_by: str,
) -> str:
    original = db.fetchone("SELECT * FROM billing.invoices WHERE id = %s", [original_invoice_id])
    financial_year = get_financial_year(date.today())
    # Credit note number: CDN-2526-SMAN-00001
    cn_number = next_credit_note_number(tenant_id, financial_year)

    # GST credit note: reverses GST proportional to credit amount
    credit_ratio = credit_amount / original["taxable_amount"]
    igst_reversal = original["igst_amount"] * credit_ratio
    cgst_reversal = original["cgst_amount"] * credit_ratio
    sgst_reversal = original["sgst_amount"] * credit_ratio

    cn_id = db.fetchone("""
        INSERT INTO billing.credit_notes
        (tenant_id, credit_note_number, financial_year, original_invoice_id,
         credit_amount, igst_amount, cgst_amount, sgst_amount, total_credit_amount,
         reason, status, created_by, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'pending_application', %s, NOW())
        RETURNING id
    """, [
        tenant_id, cn_number, financial_year, original_invoice_id,
        credit_amount, igst_reversal, cgst_reversal, sgst_reversal,
        credit_amount + igst_reversal + cgst_reversal + sgst_reversal,
        reason, created_by,
    ])["id"]

    # Generate PDF credit note
    pdf_bytes = generate_credit_note_pdf(cn_id)
    s3_key = f"credit-notes/{tenant_id}/{financial_year}/{cn_number}.pdf"
    s3.put_object(Bucket=INVOICES_BUCKET, Key=s3_key, Body=pdf_bytes, ContentType="application/pdf")
    db.execute("UPDATE billing.credit_notes SET pdf_s3_key = %s WHERE id = %s", [s3_key, cn_id])

    # Email credit note
    send_credit_note_email(tenant_id, cn_id, s3_key)
    return cn_id


def apply_pending_credits(invoice_id: str, tenant_id: str):
    """Apply any pending credit notes as a discount line on the invoice."""
    pending_credits = db.fetchall("""
        SELECT * FROM billing.credit_notes
        WHERE tenant_id = %s AND status = 'pending_application'
        ORDER BY created_at ASC
    """, [tenant_id])

    invoice = db.fetchone("SELECT total_amount FROM billing.invoices WHERE id = %s", [invoice_id])
    remaining_invoice = invoice["total_amount"]

    for cn in pending_credits:
        apply_amount = min(cn["total_credit_amount"], remaining_invoice)
        db.execute("""
            INSERT INTO billing.invoice_line_items
            (invoice_id, description, hsn_code, quantity, unit_price, taxable_amount,
             igst_amount, cgst_amount, sgst_amount, total_amount)
            VALUES (%s, %s, NULL, 1, %s, %s, %s, %s, %s, %s)
        """, [invoice_id, f"Credit Note {cn['credit_note_number']}",
              -apply_amount, -apply_amount, Decimal("0"), Decimal("0"), Decimal("0"), -apply_amount])
        db.execute("""
            UPDATE billing.invoices
            SET total_amount = total_amount - %s WHERE id = %s
        """, [apply_amount, invoice_id])
        db.execute("""
            UPDATE billing.credit_notes SET status = 'applied', applied_to_invoice_id = %s, applied_at = NOW()
            WHERE id = %s
        """, [invoice_id, cn["id"]])
        remaining_invoice -= apply_amount
        if remaining_invoice <= 0:
            break
```

---

## 9. GST Filing Automation

### 9.1 GSTR-1 Generation

```python
# compliance/gst_filing.py
import pandas as pd

def generate_gstr1(filing_month: str) -> dict:
    """
    Generate GSTR-1 JSON in NIC format for CA filing.
    Sections: B2B (inter-company), B2CL (large B2C), B2CS (small B2C).
    """
    # B2B invoices
    b2b = db.fetchall("""
        SELECT buyer_gstin, invoice_number, invoice_date, total_amount, taxable_amount,
               igst_amount, cgst_amount, sgst_amount
        FROM billing.invoices
        WHERE DATE_TRUNC('month', invoice_date) = %s::date
        AND invoice_type = 'b2b'
        AND status = 'paid'
    """, [filing_month])

    # B2CL (inter-state > Rs. 2.5L)
    b2cl = db.fetchall("""
        SELECT invoice_number, invoice_date, total_amount, taxable_amount, igst_amount
        FROM billing.invoices
        WHERE DATE_TRUNC('month', invoice_date) = %s::date
        AND invoice_type = 'b2c'
        AND total_amount >= 250000
        AND status = 'paid'
    """, [filing_month])

    # B2CS aggregate (B2C < Rs. 2.5L, aggregated)
    b2cs = db.fetchone("""
        SELECT SUM(taxable_amount) AS taxable, SUM(igst_amount) AS igst
        FROM billing.invoices
        WHERE DATE_TRUNC('month', invoice_date) = %s::date
        AND invoice_type = 'b2c'
        AND total_amount < 250000
        AND status = 'paid'
    """, [filing_month])

    return {
        "gstin": EDUFORGE_GSTIN,
        "fp": datetime.strptime(filing_month, "%Y-%m-%d").strftime("%m%Y"),
        "b2b": [{"ctin": r["buyer_gstin"], "inv": [_to_b2b_inv(r)]} for r in _group_by_gstin(b2b)],
        "b2cl": [_to_b2cl_inv(r) for r in b2cl],
        "b2cs": [{"sply_ty": "INTER", "txval": float(b2cs["taxable"]), "iamt": float(b2cs["igst"])}],
    }
```

### 9.2 Tax Ledger

```python
def record_tax_entry(invoice_id: str):
    """Record tax collected in tax ledger on payment capture."""
    invoice = db.fetchone("SELECT * FROM billing.invoices WHERE id = %s", [invoice_id])
    db.execute("""
        INSERT INTO billing.tax_ledger
        (invoice_id, period_month, supply_type, taxable_amount, igst_amount, cgst_amount, sgst_amount, total_tax)
        VALUES (%s, DATE_TRUNC('month', %s::date), %s, %s, %s, %s, %s, %s)
    """, [
        invoice_id, invoice["invoice_date"],
        "inter_state" if invoice["igst_amount"] > 0 else "intra_state",
        invoice["taxable_amount"], invoice["igst_amount"],
        invoice["cgst_amount"], invoice["sgst_amount"],
        invoice["igst_amount"] + invoice["cgst_amount"] + invoice["sgst_amount"],
    ])
```

---

## 10. Database Schema

```sql
CREATE TABLE billing.invoices (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id               UUID NOT NULL,
    invoice_number          TEXT NOT NULL UNIQUE,
    financial_year          TEXT NOT NULL,      -- e.g., '2526'
    sequence_number         INTEGER NOT NULL,
    invoice_type            TEXT NOT NULL,      -- b2b, b2c, tsp_wholesale, addon, credit_note
    invoice_date            DATE NOT NULL DEFAULT CURRENT_DATE,
    billing_period_start    DATE,
    billing_period_end      DATE,
    buyer_gstin             TEXT,
    buyer_legal_name        TEXT NOT NULL,
    buyer_trade_name        TEXT,
    buyer_address           TEXT NOT NULL,
    buyer_city              TEXT,
    buyer_pin               TEXT,
    buyer_state_code        TEXT,
    buyer_phone             TEXT,
    buyer_email             TEXT,
    place_of_supply_state_code TEXT,
    taxable_amount          NUMERIC(14,2) NOT NULL,
    igst_amount             NUMERIC(14,2) NOT NULL DEFAULT 0,
    cgst_amount             NUMERIC(14,2) NOT NULL DEFAULT 0,
    sgst_amount             NUMERIC(14,2) NOT NULL DEFAULT 0,
    total_amount            NUMERIC(14,2) NOT NULL,
    status                  TEXT NOT NULL DEFAULT 'pending',  -- pending, paid, overdue, cancelled, written_off
    razorpay_order_id       TEXT,
    pdf_s3_key              TEXT,
    paid_at                 TIMESTAMPTZ,
    notes                   TEXT,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT valid_invoice_type CHECK (invoice_type IN ('b2b','b2c','tsp_wholesale','addon','proforma')),
    CONSTRAINT valid_status CHECK (status IN ('pending','paid','overdue','cancelled','written_off'))
) PARTITION BY RANGE (invoice_date);

CREATE TABLE billing.invoices_2026
    PARTITION OF billing.invoices FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

CREATE INDEX idx_invoices_tenant ON billing.invoices (tenant_id, invoice_date DESC);
CREATE INDEX idx_invoices_status ON billing.invoices (status) WHERE status IN ('pending','overdue');
CREATE INDEX idx_invoices_gstin ON billing.invoices (buyer_gstin) WHERE buyer_gstin IS NOT NULL;

CREATE TABLE billing.invoice_line_items (
    line_id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id              UUID NOT NULL REFERENCES billing.invoices(id),
    description             TEXT NOT NULL,
    hsn_code                TEXT,
    quantity                NUMERIC(10,4) NOT NULL DEFAULT 1,
    unit_price              NUMERIC(14,2) NOT NULL,
    taxable_amount          NUMERIC(14,2) NOT NULL,
    igst_amount             NUMERIC(14,2) NOT NULL DEFAULT 0,
    cgst_amount             NUMERIC(14,2) NOT NULL DEFAULT 0,
    sgst_amount             NUMERIC(14,2) NOT NULL DEFAULT 0,
    total_amount            NUMERIC(14,2) NOT NULL
);

CREATE TABLE billing.payments (
    payment_id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id              UUID NOT NULL REFERENCES billing.invoices(id),
    razorpay_payment_id     TEXT UNIQUE,
    method                  TEXT,              -- upi, card, netbanking, neft, rtgs
    amount                  NUMERIC(14,2) NOT NULL,
    currency                TEXT NOT NULL DEFAULT 'INR',
    captured_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    refund_status           TEXT,              -- NULL, processing, refunded
    refund_amount           NUMERIC(14,2),
    refunded_at             TIMESTAMPTZ,
    razorpay_refund_id      TEXT
);

CREATE TABLE billing.payment_attempts (
    attempt_id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id              UUID NOT NULL REFERENCES billing.invoices(id),
    razorpay_order_id       TEXT,
    razorpay_payment_id     TEXT,
    attempt_number          INTEGER NOT NULL,
    method                  TEXT,
    amount                  NUMERIC(14,2) NOT NULL,
    status                  TEXT NOT NULL,     -- created, attempted, captured, failed
    error_code              TEXT,
    error_description       TEXT,
    attempted_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE billing.dunning_state (
    tenant_id               UUID PRIMARY KEY,
    invoice_id              UUID REFERENCES billing.invoices(id),
    status                  TEXT NOT NULL DEFAULT 'active',
    failure_date            DATE,
    last_retry_at           TIMESTAMPTZ,
    is_paused               BOOLEAN NOT NULL DEFAULT FALSE,
    paused_by               UUID,
    paused_reason           TEXT,
    cleared_at              TIMESTAMPTZ,
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE billing.credit_notes (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id               UUID NOT NULL,
    credit_note_number      TEXT NOT NULL UNIQUE,
    financial_year          TEXT NOT NULL,
    original_invoice_id     UUID REFERENCES billing.invoices(id),
    credit_amount           NUMERIC(14,2) NOT NULL,
    igst_amount             NUMERIC(14,2) NOT NULL DEFAULT 0,
    cgst_amount             NUMERIC(14,2) NOT NULL DEFAULT 0,
    sgst_amount             NUMERIC(14,2) NOT NULL DEFAULT 0,
    total_credit_amount     NUMERIC(14,2) NOT NULL,
    reason                  TEXT NOT NULL,
    reason_category         TEXT,  -- sla_credit, refund, pricing_adjustment, sales_concession
    status                  TEXT NOT NULL DEFAULT 'pending_application',
    pdf_s3_key              TEXT,
    applied_to_invoice_id   UUID REFERENCES billing.invoices(id),
    applied_at              TIMESTAMPTZ,
    sla_credit_id           UUID,  -- FK to incidents.sla_credits if applicable
    created_by              UUID NOT NULL,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE billing.einvoices (
    invoice_id              UUID PRIMARY KEY REFERENCES billing.invoices(id),
    irn                     TEXT NOT NULL UNIQUE,      -- 64-char IRN from IRP
    signed_qr_code          TEXT NOT NULL,             -- Base64 QR code
    irp_ack_number          TEXT,
    irp_ack_date            TIMESTAMPTZ,
    registered_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    is_cancelled            BOOLEAN NOT NULL DEFAULT FALSE,
    cancelled_at            TIMESTAMPTZ,
    cancel_reason           TEXT
);

CREATE TABLE billing.tax_ledger (
    ledger_id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id              UUID NOT NULL REFERENCES billing.invoices(id),
    period_month            DATE NOT NULL,      -- YYYY-MM-01
    supply_type             TEXT NOT NULL,      -- inter_state, intra_state
    taxable_amount          NUMERIC(14,2) NOT NULL,
    igst_amount             NUMERIC(14,2) NOT NULL DEFAULT 0,
    cgst_amount             NUMERIC(14,2) NOT NULL DEFAULT 0,
    sgst_amount             NUMERIC(14,2) NOT NULL DEFAULT 0,
    total_tax               NUMERIC(14,2) NOT NULL,
    is_reversed             BOOLEAN NOT NULL DEFAULT FALSE,  -- for credit notes
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE billing.deferred_revenue (
    deferred_id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id              UUID NOT NULL REFERENCES billing.invoices(id),
    tenant_id               UUID NOT NULL,
    total_prepaid_amount    NUMERIC(14,2) NOT NULL,
    recognized_per_month    NUMERIC(14,2) NOT NULL,
    recognition_start_month DATE NOT NULL,
    recognition_end_month   DATE NOT NULL,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE billing.tsp_billing_cycles (
    cycle_id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tsp_id                  UUID NOT NULL,
    billing_month           DATE NOT NULL,
    active_student_count    INTEGER NOT NULL,
    wholesale_rate          NUMERIC(8,4) NOT NULL,
    net_amount              NUMERIC(14,2) NOT NULL,
    gst_amount              NUMERIC(14,2) NOT NULL,
    total_amount            NUMERIC(14,2) GENERATED ALWAYS AS (net_amount + gst_amount) STORED,
    invoice_id              UUID REFERENCES billing.invoices(id),
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tsp_id, billing_month)
);

CREATE TABLE billing.tsp_disputes (
    dispute_id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cycle_id                UUID NOT NULL REFERENCES billing.tsp_billing_cycles(cycle_id),
    tsp_id                  UUID NOT NULL,
    disputed_student_count  INTEGER NOT NULL,
    claimed_student_count   INTEGER NOT NULL,
    dispute_reason          TEXT NOT NULL,
    status                  TEXT NOT NULL DEFAULT 'open',  -- open, investigating, resolved_accepted, resolved_rejected
    resolution_notes        TEXT,
    resolved_by             UUID,
    resolved_at             TIMESTAMPTZ,
    credit_note_id          UUID REFERENCES billing.credit_notes(id),
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE billing.coupons (
    coupon_id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code                    TEXT NOT NULL UNIQUE,
    discount_type           TEXT NOT NULL,   -- percent, flat
    discount_value          NUMERIC(10,2) NOT NULL,
    max_uses                INTEGER,
    current_uses            INTEGER NOT NULL DEFAULT 0,
    applicable_plans        TEXT[],          -- NULL = all plans
    valid_from              DATE NOT NULL,
    valid_until             DATE,
    is_active               BOOLEAN NOT NULL DEFAULT TRUE,
    created_by              UUID NOT NULL,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## 11. API Endpoints

```python
# billing/routes.py (FastAPI)
router = APIRouter(prefix="/billing", tags=["Billing"])

# Invoice management (tenant-facing)
@router.get("/invoices")
async def list_invoices(user=Depends(require_permission("billing.invoices.read"))):
    return db.fetchall("SELECT * FROM billing.invoices WHERE tenant_id = %s ORDER BY invoice_date DESC", [user.tenant_id])

@router.get("/invoices/{invoice_id}/pdf")
async def download_invoice_pdf(invoice_id: str, user=Depends(require_permission("billing.invoices.read"))):
    s3_key = get_or_generate_pdf(invoice_id, user.tenant_id)
    url = s3.generate_presigned_url("get_object",
        Params={"Bucket": INVOICES_BUCKET, "Key": s3_key}, ExpiresIn=604800)
    return RedirectResponse(url)

@router.get("/invoices/{invoice_id}/einvoice")
async def download_einvoice(invoice_id: str, user=Depends(require_permission("billing.invoices.read"))):
    ein = db.fetchone("SELECT * FROM billing.einvoices WHERE invoice_id = %s", [invoice_id])
    return ein

@router.post("/invoices/{invoice_id}/pay")
async def initiate_payment(invoice_id: str, user=Depends(require_permission("billing.invoices.pay"))):
    invoice = db.fetchone("SELECT * FROM billing.invoices WHERE id = %s AND tenant_id = %s", [invoice_id, user.tenant_id])
    order = create_payment_order(invoice_id, invoice["total_amount"])
    return {"razorpay_order_id": order["id"], "amount": invoice["total_amount"]}

@router.post("/invoices/{invoice_id}/refund")
async def request_refund(invoice_id: str, payload: RefundRequest, user=Depends(require_permission("billing.invoices.pay"))):
    payment = db.fetchone("SELECT * FROM billing.payments WHERE invoice_id = %s", [invoice_id])
    # Check 7-day refund window
    if (datetime.utcnow() - payment["captured_at"]).days > 7:
        raise HTTPException(400, "Refund window (7 days) has expired. Contact support.")
    refund = rz_client.refund.create(payment["razorpay_payment_id"], {
        "amount": int(float(payload.amount) * 100) if payload.amount else int(float(payment["amount"]) * 100),
        "notes": {"reason": payload.reason},
    })
    return {"refund_id": refund["id"], "status": "processing"}

# Webhooks
@router.post("/webhooks/razorpay", include_in_schema=False)
async def razorpay_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("X-Razorpay-Signature", "")
    handle_razorpay_webhook(payload, signature)
    return {"status": "ok"}

# Admin: credit notes
@router.post("/admin/credit-notes")
async def create_cn(payload: CreditNoteCreate, user=Depends(require_permission("billing.credit_notes.write"))):
    cn_id = create_credit_note(payload.tenant_id, payload.invoice_id, payload.amount, payload.reason, user.id)
    return {"credit_note_id": cn_id}

# Admin: GST exports
@router.get("/admin/gst/gstr1")
async def gstr1_export(month: str, user=Depends(require_permission("finance.gst.export"))):
    data = generate_gstr1(month)
    return JSONResponse(data, headers={"Content-Disposition": f"attachment; filename=GSTR1_{month}.json"})

@router.get("/admin/gst/tax-ledger")
async def tax_ledger(month: str, user=Depends(require_permission("finance.gst.export"))):
    rows = db.fetchall("SELECT * FROM billing.tax_ledger WHERE period_month = %s ORDER BY supply_type", [month])
    return rows

# TSP billing
@router.get("/tsp/billing-cycles")
async def tsp_cycles(user=Depends(require_permission("tsp.billing.read"))):
    return db.fetchall("SELECT * FROM billing.tsp_billing_cycles WHERE tsp_id = %s ORDER BY billing_month DESC", [user.tsp_id])

@router.post("/tsp/billing-cycles/{cycle_id}/dispute")
async def dispute_cycle(cycle_id: str, payload: TspDisputeCreate, user=Depends(require_permission("tsp.billing.write"))):
    return tsp_billing_service.create_dispute(cycle_id, payload, user.tsp_id)
```

---

## 12. Cost Architecture

| Component | Monthly Cost | Notes |
|-----------|-------------|-------|
| WeasyPrint (Lambda) | ~Rs. 2,500 | ~5K invoices/month × 500ms each |
| S3 (invoice PDF storage) | ~Rs. 1,200 | 7 years retention, Glacier IA after 90 days |
| SES (invoice emails) | ~Rs. 600 | ~5K emails + attachments |
| Razorpay transaction fees | ~Rs. 20,000 | 2% + Rs. 3/transaction (variable, passed to merchant) |
| Lambda (billing engine, dunning, GSTR) | ~Rs. 1,500 | Nightly scheduled jobs |
| IRP API calls | ~Rs. 0 | Free NIC API |
| DynamoDB (webhook dedup) | ~Rs. 100 | Small, TTL-purged |
| **Total fixed infra** | **~Rs. 5,900/month** | Razorpay fees are variable and pass-through |
