# Module 57 — Payment Gateway — BYOG (Razorpay, PhonePe, PayU, etc.)

## 1. Purpose & Scope

Payment Gateway BYOG (Bring Your Own Gateway) is the fee collection infrastructure for institutions. It allows each institution to connect their own payment gateway account (Razorpay, PhonePe, PayU, Cashfree, Paytm, InstaMojo) for collecting fees from students and parents.

Key architectural principle: **EduForge is a gateway adapter, not a payment aggregator.** Settlement goes directly from the gateway to the institution's bank account. EduForge never holds institution money, avoiding the RBI Payment Aggregator license requirement.

This module is completely separate from Module 56 (EduForge billing institutions for SaaS subscriptions). That is EduForge's own revenue collection; this module is for institution-to-student/parent fee collection.

Integration points:
- Module 25 (Fee Collection) — calls `GatewayProvider.create_order()` to initiate payments
- Module 26 (Fee Defaulters) — bulk payment links, dunning retry payments
- Module 35 (Notifications) — payment success/failure SMS/push
- Module 36 (WhatsApp) — QR code delivery, payment links
- Module 53 (Analytics) — payment success rates, method split analytics
- Module 55 (Incident Management) — gateway downtime incidents

---

## 2. Gateway Abstraction Layer

### 2.1 GatewayProvider Interface

```python
# payments/gateway/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal

@dataclass
class PaymentOrder:
    order_id: str              # EduForge internal order ID
    gateway_order_id: str      # Gateway-assigned order/transaction ID
    amount: Decimal
    currency: str = "INR"
    gateway: str = ""
    checkout_data: dict = field(default_factory=dict)  # Gateway-specific checkout params

@dataclass
class PaymentEvent:
    event_type: str            # payment.captured | payment.failed | refund.processed
    gateway: str
    tenant_id: str
    order_id: str
    gateway_order_id: str
    payment_id: str
    amount: Decimal
    method: str                # upi | card | netbanking | wallet | emi | ach
    bank: str | None = None
    vpa: str | None = None     # UPI VPA (anonymised for privacy)
    card_network: str | None = None  # visa | mastercard | rupay | amex
    error_code: str | None = None
    error_description: str | None = None
    raw_payload: dict = field(default_factory=dict)

class GatewayProvider(ABC):
    @abstractmethod
    def create_order(self, amount: Decimal, receipt: str, notes: dict) -> PaymentOrder: ...

    @abstractmethod
    def verify_payment(self, order_id: str, payment_id: str, signature: str) -> bool: ...

    @abstractmethod
    def fetch_order_status(self, gateway_order_id: str) -> dict: ...

    @abstractmethod
    def create_refund(self, payment_id: str, amount: Decimal, reason: str) -> dict: ...

    @abstractmethod
    def parse_webhook(self, payload: bytes, headers: dict, webhook_secret: str) -> PaymentEvent: ...

    @abstractmethod
    def generate_payment_link(
        self, amount: Decimal, description: str,
        customer: dict, expire_by_unix: int,
    ) -> str: ...

    @abstractmethod
    def generate_dynamic_qr(self, amount: Decimal, reference: str, expire_by_unix: int) -> bytes: ...

    @abstractmethod
    def health_check(self) -> bool: ...
```

### 2.2 Razorpay Adapter

```python
# payments/gateway/razorpay_adapter.py
import razorpay, hmac, hashlib

class RazorpayProvider(GatewayProvider):
    def __init__(self, creds: dict):
        self.client = razorpay.Client(auth=(creds["key_id"], creds["key_secret"]))
        self.key_id = creds["key_id"]
        self.webhook_secret = creds.get("webhook_secret", "")

    def create_order(self, amount: Decimal, receipt: str, notes: dict) -> PaymentOrder:
        order = self.client.order.create({
            "amount": int(amount * 100),  # Paise
            "currency": "INR",
            "receipt": receipt,
            "notes": notes,
        })
        return PaymentOrder(
            order_id=receipt,
            gateway_order_id=order["id"],
            amount=amount,
            gateway="razorpay",
            checkout_data={
                "key": self.key_id,
                "order_id": order["id"],
                "amount": int(amount * 100),
                "currency": "INR",
            },
        )

    def verify_payment(self, order_id: str, payment_id: str, signature: str) -> bool:
        body = f"{order_id}|{payment_id}"
        expected = hmac.new(self.key_id.encode(), body.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)

    def parse_webhook(self, payload: bytes, headers: dict, webhook_secret: str) -> PaymentEvent:
        # Verify Razorpay signature
        signature = headers.get("x-razorpay-signature", "")
        expected = hmac.new(webhook_secret.encode(), payload, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, signature):
            raise ValueError("Invalid Razorpay webhook signature")
        event = json.loads(payload)
        entity = event["payload"]["payment"]["entity"]
        return PaymentEvent(
            event_type=event["event"],
            gateway="razorpay",
            tenant_id=entity["notes"].get("tenant_id", ""),
            order_id=entity["receipt"],
            gateway_order_id=entity["order_id"],
            payment_id=entity["id"],
            amount=Decimal(entity["amount"]) / 100,
            method=entity["method"],
            bank=entity.get("bank"),
            vpa=entity.get("vpa"),
            card_network=entity.get("card", {}).get("network"),
            error_code=entity.get("error_code"),
            error_description=entity.get("error_description"),
            raw_payload=event,
        )

    def generate_dynamic_qr(self, amount: Decimal, reference: str, expire_by_unix: int) -> bytes:
        qr = self.client.qrcode.create({
            "type": "upi_qr",
            "name": reference,
            "usage": "single_use",
            "fixed_amount": True,
            "payment_amount": int(amount * 100),
            "close_by": expire_by_unix,
        })
        # Fetch QR image
        import httpx
        resp = httpx.get(qr["image_url"])
        return resp.content

    def health_check(self) -> bool:
        try:
            self.client.order.all(options={"count": 1})
            return True
        except Exception:
            return False
```

### 2.3 PhonePe Adapter

```python
# payments/gateway/phonepe_adapter.py
import base64, hashlib, json, httpx

class PhonePeProvider(GatewayProvider):
    BASE = "https://api.phonepe.com/apis/hermes"

    def __init__(self, creds: dict):
        self.merchant_id = creds["merchant_id"]
        self.salt_key = creds["salt_key"]
        self.salt_index = creds["salt_index"]

    def _sign(self, base64_payload: str, endpoint: str) -> str:
        data = base64_payload + endpoint + self.salt_key
        return hashlib.sha256(data.encode()).hexdigest() + "###" + str(self.salt_index)

    def create_order(self, amount: Decimal, receipt: str, notes: dict) -> PaymentOrder:
        payload = {
            "merchantId": self.merchant_id,
            "merchantTransactionId": receipt,
            "amount": int(amount * 100),
            "redirectUrl": notes.get("redirect_url"),
            "paymentInstrument": {"type": "PAY_PAGE"},
        }
        encoded = base64.b64encode(json.dumps(payload).encode()).decode()
        signature = self._sign(encoded, "/pg/v1/pay")
        resp = httpx.post(
            f"{self.BASE}/pg/v1/pay",
            json={"request": encoded},
            headers={"X-VERIFY": signature, "X-MERCHANT-ID": self.merchant_id},
        )
        data = resp.json()["data"]
        return PaymentOrder(
            order_id=receipt,
            gateway_order_id=receipt,
            amount=amount,
            gateway="phonepe",
            checkout_data={"redirect_url": data["instrumentResponse"]["redirectInfo"]["url"]},
        )

    def parse_webhook(self, payload: bytes, headers: dict, webhook_secret: str) -> PaymentEvent:
        verify_header = headers.get("x-verify", "")
        encoded_data = json.loads(payload)["response"]
        expected = hashlib.sha256(
            (encoded_data + "/pg/v1/pay" + self.salt_key).encode()
        ).hexdigest() + "###" + str(self.salt_index)
        if not hmac.compare_digest(expected, verify_header):
            raise ValueError("Invalid PhonePe webhook signature")
        decoded = json.loads(base64.b64decode(encoded_data))
        return PaymentEvent(
            event_type="payment.captured" if decoded["code"] == "PAYMENT_SUCCESS" else "payment.failed",
            gateway="phonepe",
            tenant_id=decoded.get("merchantId", ""),
            order_id=decoded["merchantTransactionId"],
            gateway_order_id=decoded["transactionId"],
            payment_id=decoded["transactionId"],
            amount=Decimal(decoded["amount"]) / 100,
            method=decoded.get("paymentInstrument", {}).get("type", "upi").lower(),
            raw_payload=decoded,
        )
```

### 2.4 Gateway Factory

```python
# payments/gateway/factory.py
import boto3, json

sm = boto3.client("secretsmanager")
_cred_cache: dict[str, tuple[dict, float]] = {}
CRED_CACHE_TTL = 300  # 5 minutes

def _get_creds(tenant_id: str, provider: str) -> dict:
    cache_key = f"{tenant_id}:{provider}"
    cached = _cred_cache.get(cache_key)
    if cached and time.time() - cached[1] < CRED_CACHE_TTL:
        return cached[0]
    secret = json.loads(sm.get_secret_value(
        SecretId=f"/eduforge/{tenant_id}/gateway/{provider}"
    )["SecretString"])
    _cred_cache[cache_key] = (secret, time.time())
    return secret

PROVIDERS = {
    "razorpay":  RazorpayProvider,
    "phonepe":   PhonePeProvider,
    "payu":      PayUProvider,
    "cashfree":  CashfreeProvider,
    "paytm":     PaytmProvider,
    "instamojo": InstamojoProvider,
}

class GatewayFactory:
    @staticmethod
    def get(tenant_id: str, use_fallback: bool = False) -> GatewayProvider:
        config = db.fetchone("""
            SELECT provider, fallback_provider FROM payments.gateway_configs
            WHERE tenant_id = %s AND is_active = TRUE
        """, [tenant_id])
        provider = config["fallback_provider"] if use_fallback else config["provider"]
        creds = _get_creds(tenant_id, provider)
        return PROVIDERS[provider](creds)

    @staticmethod
    def get_safe(tenant_id: str) -> GatewayProvider:
        """Try primary, fall back automatically on GatewayUnavailableError."""
        try:
            gw = GatewayFactory.get(tenant_id, use_fallback=False)
            if not gw.health_check():
                raise GatewayUnavailableError("Primary gateway unhealthy")
            return gw
        except GatewayUnavailableError:
            logger.warning(f"Primary gateway unavailable for tenant {tenant_id}, using fallback")
            return GatewayFactory.get(tenant_id, use_fallback=True)
```

---

## 3. Webhook Handler

```python
# payments/webhook_routes.py

@router.post(
    "/webhooks/pg/{tenant_id}/{provider}/{webhook_token}",
    include_in_schema=False,
)
async def receive_webhook(
    tenant_id: str,
    provider: str,
    webhook_token: str,
    request: Request,
):
    payload = await request.body()

    # 1. Validate webhook token (constant-time comparison)
    stored_token = get_webhook_token_from_secrets(tenant_id, provider)
    if not hmac.compare_digest(webhook_token.encode(), stored_token.encode()):
        raise HTTPException(403, "Invalid webhook token")

    # 2. Parse and gateway-specific signature validation
    creds = _get_creds(tenant_id, provider)
    gw = PROVIDERS[provider](creds)
    try:
        event = gw.parse_webhook(payload, dict(request.headers), creds.get("webhook_secret", ""))
    except ValueError:
        raise HTTPException(400, "Webhook signature validation failed")

    # 3. Store raw event for audit (even before idempotency check)
    raw_event_id = db.fetchone("""
        INSERT INTO payments.webhook_events
        (tenant_id, provider, event_id_header, payload_size, received_at)
        VALUES (%s, %s, %s, %s, NOW())
        RETURNING id
    """, [tenant_id, provider, event.payment_id, len(payload)])["id"]

    # 4. Idempotency check
    dedup_key = f"{provider}:{event.payment_id}:{event.event_type}"
    dedup_hash = hashlib.md5(dedup_key.encode()).hexdigest()
    try:
        WEBHOOK_DEDUP_TABLE.put_item(
            Item={"dedup_key": dedup_hash, "ttl": int(time.time()) + 86400},
            ConditionExpression="attribute_not_exists(dedup_key)",
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return {"status": "duplicate_skipped"}
        raise

    # 5. Enqueue for async processing (return 200 immediately)
    event.raw_payload["_raw_event_id"] = raw_event_id
    sqs.send_message(
        QueueUrl=FEE_PAYMENT_QUEUE,
        MessageBody=event.json(),
    )
    return {"status": "queued"}
```

---

## 4. Payment Flow (Fee Collection)

### 4.1 Create Order

```python
# payments/order_service.py

def create_payment_order(
    tenant_id: str,
    invoice_id: str,
    amount: Decimal,
    student_id: str,
    fee_description: str,
) -> dict:
    """
    Create a payment order via tenant's configured gateway.
    Called by Module 25 (Fee Collection).
    """
    gw = GatewayFactory.get_safe(tenant_id)
    order = gw.create_order(
        amount=amount,
        receipt=invoice_id,  # Idempotency key
        notes={
            "tenant_id": tenant_id,
            "student_id": student_id,
            "fee_description": fee_description[:255],
        },
    )
    # Persist order record
    db.execute("""
        INSERT INTO payments.transactions
        (transaction_id, tenant_id, invoice_id, student_id, gateway, gateway_order_id,
         amount, currency, status, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'INR', 'created', NOW())
        ON CONFLICT (invoice_id, gateway)
        DO UPDATE SET gateway_order_id = EXCLUDED.gateway_order_id, status = 'created'
    """, [str(uuid4()), tenant_id, invoice_id, student_id, gw.__class__.__name__.lower().replace("provider",""),
          order.gateway_order_id, amount])
    return {
        "order_id": invoice_id,
        "gateway": order.gateway,
        "gateway_order_id": order.gateway_order_id,
        "checkout_data": order.checkout_data,
        "amount": float(amount),
    }
```

### 4.2 Payment Confirmation (SQS Consumer)

```python
# payments/payment_processor.py  (SQS Lambda)

def process_payment_event(event: PaymentEvent):
    if event.event_type == "payment.captured":
        # Update transaction status
        db.execute("""
            UPDATE payments.transactions
            SET status = 'captured', payment_id = %s, method = %s, captured_at = NOW()
            WHERE invoice_id = %s AND tenant_id = %s
        """, [event.payment_id, event.method, event.order_id, event.tenant_id])

        # Record gateway fee (estimated; reconciled later from settlement report)
        gateway_fee = estimate_gateway_fee(event.gateway, event.amount, event.method)
        db.execute("""
            INSERT INTO payments.gateway_fees (transaction_id, gateway, fee_amount, fee_pct, created_at)
            VALUES ((SELECT id FROM payments.transactions WHERE payment_id = %s), %s, %s, %s, NOW())
        """, [event.payment_id, event.gateway, gateway_fee["amount"], gateway_fee["pct"]])

        # Notify Module 25 to mark invoice paid
        sqs.send_message(
            QueueUrl=FEE_COLLECTION_QUEUE,
            MessageBody=json.dumps({
                "action": "mark_paid",
                "invoice_id": event.order_id,
                "tenant_id": event.tenant_id,
                "payment_id": event.payment_id,
                "amount": float(event.amount),
                "method": event.method,
            }),
        )
        # Push notification to parent (Module 35)
        trigger_payment_success_notification(event)

    elif event.event_type == "payment.failed":
        db.execute("""
            UPDATE payments.transactions
            SET status = 'failed', error_code = %s, error_description = %s, updated_at = NOW()
            WHERE invoice_id = %s AND tenant_id = %s
        """, [event.error_code, event.error_description, event.order_id, event.tenant_id])
        trigger_payment_failure_notification(event)

    # Mark raw webhook event as processed
    db.execute("""
        UPDATE payments.webhook_events SET processing_status = 'done', processed_at = NOW()
        WHERE id = %s
    """, [event.raw_payload.get("_raw_event_id")])
```

### 4.3 Limbo Detection (Nightly Reconciliation)

```python
# payments/limbo_detector.py  (runs nightly at 01:00 IST)

def detect_limbo_transactions():
    """
    Find transactions captured by gateway but not reflected in EduForge.
    Happens when webhook was missed or failed processing.
    """
    # Find all 'created' transactions older than 2 hours
    stale = db.fetchall("""
        SELECT * FROM payments.transactions
        WHERE status = 'created'
        AND created_at < NOW() - INTERVAL '2 hours'
    """)
    for txn in stale:
        gw = GatewayFactory.get(txn["tenant_id"])
        gateway_status = gw.fetch_order_status(txn["gateway_order_id"])
        if gateway_status["status"] == "paid":
            # Payment captured by gateway but not processed — replay
            event = PaymentEvent(
                event_type="payment.captured",
                gateway=txn["gateway"],
                tenant_id=txn["tenant_id"],
                order_id=txn["invoice_id"],
                gateway_order_id=txn["gateway_order_id"],
                payment_id=gateway_status["payment_id"],
                amount=txn["amount"],
                method=gateway_status["method"],
            )
            process_payment_event(event)
            logger.info(f"Limbo recovery: invoice {txn['invoice_id']} marked paid from polling")
```

---

## 5. UPI QR Code & Payment Links

### 5.1 Dynamic QR

```python
# payments/qr_service.py
from datetime import datetime, timedelta

def generate_invoice_qr(invoice_id: str, tenant_id: str) -> dict:
    """Generate a dynamic UPI QR for a specific fee invoice."""
    invoice = get_fee_invoice(invoice_id)
    gw = GatewayFactory.get_safe(tenant_id)
    expire_by = int((datetime.utcnow() + timedelta(hours=24)).timestamp())

    qr_bytes = gw.generate_dynamic_qr(
        amount=invoice["amount"],
        reference=f"FEE-{invoice_id[:8]}",
        expire_by_unix=expire_by,
    )
    # Store for retrieval
    s3_key = f"qr/{tenant_id}/{invoice_id}.png"
    s3.put_object(Bucket=ASSETS_BUCKET, Key=s3_key, Body=qr_bytes, ContentType="image/png")
    presigned_url = s3.generate_presigned_url("get_object",
        Params={"Bucket": ASSETS_BUCKET, "Key": s3_key}, ExpiresIn=86400)
    return {"qr_url": presigned_url, "expires_at": datetime.utcfromtimestamp(expire_by).isoformat()}
```

### 5.2 Payment Links

```python
# payments/link_service.py
import secrets, string

SHORT_CODE_CHARS = string.ascii_letters + string.digits

def generate_short_code() -> str:
    return "".join(secrets.choice(SHORT_CODE_CHARS) for _ in range(6))


def create_payment_link(
    tenant_id: str,
    invoice_id: str,
    amount: Decimal,
    student_name: str,
    fee_description: str,
    expire_days: int = 7,
) -> str:
    """Generate a payment link for a fee invoice. Returns short URL."""
    gw = GatewayFactory.get_safe(tenant_id)
    expire_by = int((datetime.utcnow() + timedelta(days=expire_days)).timestamp())

    gateway_link_url = gw.generate_payment_link(
        amount=amount,
        description=f"{fee_description} — {student_name}",
        customer={"name": student_name},
        expire_by_unix=expire_by,
    )
    # Create short code
    short_code = generate_short_code()
    db.execute("""
        INSERT INTO payments.payment_links
        (short_code, tenant_id, invoice_id, gateway_link_url, amount,
         expires_at, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """, [short_code, tenant_id, invoice_id, gateway_link_url, amount,
          datetime.utcfromtimestamp(expire_by)])
    # Also store in DynamoDB for sub-millisecond resolution
    LINK_TABLE.put_item(Item={
        "short_code": short_code,
        "gateway_link_url": gateway_link_url,
        "tenant_id": tenant_id,
        "invoice_id": invoice_id,
        "ttl": expire_by,
    })
    return f"https://pay.ef.in/{short_code}"


# Short link resolution (CloudFront Lambda@Edge or Lambda function URL)
def resolve_short_link(short_code: str):
    item = LINK_TABLE.get_item(Key={"short_code": short_code}).get("Item")
    if not item:
        return None  # 404
    if int(item["ttl"]) < time.time():
        return None  # Expired
    return item["gateway_link_url"]
```

---

## 6. Reconciliation

```python
# payments/reconciliation.py  (runs daily at 01:30 IST via EventBridge)

def run_reconciliation(tenant_id: str, settlement_date: date):
    """
    Download gateway settlement report and match against transactions.
    """
    config = db.fetchone("SELECT * FROM payments.gateway_configs WHERE tenant_id = %s AND is_active = TRUE", [tenant_id])
    gw = GatewayFactory.get(tenant_id)
    # Download settlement (gateway-specific API)
    settlements = fetch_settlement_report(gw, settlement_date)  # List of {payment_id, amount, fee}

    run_id = db.fetchone("""
        INSERT INTO payments.reconciliation_runs
        (tenant_id, run_date, gateway, settlement_count, status, started_at)
        VALUES (%s, %s, %s, %s, 'running', NOW())
        RETURNING id
    """, [tenant_id, settlement_date, config["provider"], len(settlements)])["id"]

    reconciled = 0
    mismatches = 0
    orphans = 0

    for s in settlements:
        txn = db.fetchone("""
            SELECT * FROM payments.transactions WHERE payment_id = %s AND tenant_id = %s
        """, [s["payment_id"], tenant_id])

        if not txn:
            # Gateway has payment but EduForge doesn't — run limbo recovery
            db.execute("""
                INSERT INTO payments.orphan_transactions
                (tenant_id, gateway, payment_id, settlement_date, amount, requires_review)
                VALUES (%s, %s, %s, %s, %s, TRUE)
                ON CONFLICT (payment_id) DO NOTHING
            """, [tenant_id, config["provider"], s["payment_id"], settlement_date, s["amount"]])
            orphans += 1
        elif abs(txn["amount"] - s["amount"]) > Decimal("0.01"):
            # Amount mismatch
            db.execute("""
                INSERT INTO payments.reconciliation_mismatches
                (run_id, transaction_id, eduforge_amount, gateway_amount, difference)
                VALUES (%s, %s, %s, %s, %s)
            """, [run_id, txn["id"], txn["amount"], s["amount"], s["amount"] - txn["amount"]])
            mismatches += 1
        else:
            db.execute("""
                UPDATE payments.transactions
                SET reconciliation_status = 'reconciled', settlement_date = %s,
                    gateway_fee = %s, settlement_amount = %s - %s
                WHERE id = %s
            """, [settlement_date, s["fee"], s["amount"], s["fee"], txn["id"]])
            reconciled += 1

    db.execute("""
        UPDATE payments.reconciliation_runs
        SET status = 'completed', reconciled_count = %s, mismatch_count = %s,
            orphan_count = %s, completed_at = NOW()
        WHERE id = %s
    """, [reconciled, mismatches, orphans, run_id])

    if mismatches > 0 or orphans > 0:
        notify_finance_admin(
            tenant_id,
            f"Reconciliation alert: {mismatches} mismatches, {orphans} orphan transactions for {settlement_date}",
        )
```

---

## 7. Refunds

```python
# payments/refund_service.py

def initiate_refund(
    tenant_id: str,
    transaction_id: str,
    amount: Decimal,
    reason: str,
    initiated_by: str,
) -> str:
    txn = db.fetchone("""
        SELECT * FROM payments.transactions WHERE id = %s AND tenant_id = %s AND status = 'captured'
    """, [transaction_id, tenant_id])
    if not txn:
        raise ValueError("Transaction not found or not in captured state")
    if amount > txn["amount"]:
        raise ValueError(f"Refund amount {amount} exceeds transaction amount {txn['amount']}")

    gw = GatewayFactory.get(tenant_id)
    refund_resp = gw.create_refund(txn["payment_id"], amount, reason)

    refund_id = db.fetchone("""
        INSERT INTO payments.refunds
        (transaction_id, tenant_id, gateway_refund_id, amount, reason,
         status, initiated_by, created_at)
        VALUES (%s, %s, %s, %s, %s, 'processing', %s, NOW())
        RETURNING id
    """, [transaction_id, tenant_id, refund_resp.get("id"), amount, reason, initiated_by])["id"]

    # Notify parent
    send_refund_initiated_notification(tenant_id, txn["student_id"], amount, reason)
    return refund_id


def process_refund_webhook(event: PaymentEvent):
    """Handle refund.processed webhook from gateway."""
    db.execute("""
        UPDATE payments.refunds
        SET status = 'processed', processed_at = NOW()
        WHERE gateway_refund_id = %s
    """, [event.payment_id])
    # Re-open fee invoice in Module 25
    txn = db.fetchone("""
        SELECT invoice_id FROM payments.transactions
        JOIN payments.refunds r ON r.transaction_id = transactions.id
        WHERE r.gateway_refund_id = %s
    """, [event.payment_id])
    if txn:
        reopen_fee_invoice(txn["invoice_id"])
    # Notify parent: refund processed
    send_refund_processed_notification(event)
```

---

## 8. BBPS Integration

```python
# payments/bbps_service.py
# BBPS (Bharat Bill Payment System) — institution registered as biller

@router.get("/bbps/fetch-bill/{roll_number}")
async def bbps_fetch_bill(roll_number: str, request: Request):
    """
    BBPS bill fetch endpoint — queried by payment apps to get outstanding fee.
    Called by Paytm, PhonePe, BHIM, bank apps, CSC kiosks.
    """
    tenant_id = resolve_tenant_from_bbps_biller_id(request.headers.get("X-BBPS-Biller-ID"))
    student = db.fetchone("""
        SELECT s.id, s.full_name, f.outstanding_amount, f.due_date
        FROM students s
        JOIN fee_invoices f ON f.student_id = s.id
        WHERE s.roll_number = %s AND s.tenant_id = %s AND f.status = 'pending'
    """, [roll_number, tenant_id])

    if not student:
        return {"status": "FAILURE", "reason": "STUDENT_NOT_FOUND"}

    return {
        "status": "SUCCESS",
        "billDetails": {
            "billAmount": str(student["outstanding_amount"]),
            "billDate": student["due_date"].isoformat(),
            "billNumber": f"FEE-{student['id'][:8].upper()}",
            "customerName": student["full_name"],
            "dueDate": student["due_date"].isoformat(),
        }
    }
```

---

## 9. PCI DSS & Security

### 9.1 Card Data Isolation

```python
# Payment page template — Razorpay.js renders the card input iframe
# EduForge server never sees raw card data

PAYMENT_PAGE_CSP = (
    "default-src 'self'; "
    "script-src 'self' https://checkout.razorpay.com https://api.razorpay.com "
    "https://js.phonepe.com https://jssdk.payu.in; "
    "frame-src https://api.razorpay.com https://secure.phonepe.com; "
    "img-src 'self' data: https:; "
    "style-src 'self' 'unsafe-inline'; "
    "connect-src 'self' https://api.razorpay.com https://api.phonepe.com"
)

@router.get("/pay/{payment_link_token}")
async def payment_page(payment_link_token: str, response: Response):
    response.headers["Content-Security-Policy"] = PAYMENT_PAGE_CSP
    link_data = resolve_short_link(payment_link_token)
    if not link_data:
        return templates.TemplateResponse("payment_link_expired.html", {})
    # Redirect to gateway's hosted payment page
    return RedirectResponse(link_data)
```

### 9.2 Amount Validation

```python
# Server-side: verify captured amount matches expected invoice amount
def verify_payment_amount(invoice_id: str, captured_amount: Decimal) -> bool:
    """
    Called on payment.captured event before marking invoice as paid.
    Prevents manipulated amounts from being accepted.
    """
    expected = db.fetchone("""
        SELECT outstanding_amount FROM fee_invoices WHERE id = %s
    """, [invoice_id])["outstanding_amount"]
    if abs(captured_amount - expected) > Decimal("0.01"):
        logger.error(f"Amount mismatch for invoice {invoice_id}: expected {expected}, got {captured_amount}")
        # Initiate automatic refund
        initiate_amount_mismatch_refund(invoice_id, captured_amount)
        return False
    return True
```

---

## 10. Database Schema

```sql
CREATE TABLE payments.gateway_configs (
    config_id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id               UUID NOT NULL UNIQUE,
    provider                TEXT NOT NULL,          -- razorpay, phonepe, payu, cashfree, paytm, instamojo
    fallback_provider       TEXT,
    webhook_token           TEXT NOT NULL,           -- stored as hash; used in webhook URL
    webhook_url             TEXT NOT NULL,           -- generated URL for institution to configure
    test_mode               BOOLEAN NOT NULL DEFAULT FALSE,
    is_active               BOOLEAN NOT NULL DEFAULT TRUE,
    last_credential_test_at TIMESTAMPTZ,
    last_successful_at      TIMESTAMPTZ,
    routing_rules           JSONB NOT NULL DEFAULT '{}',  -- method-based routing config
    enabled_methods         TEXT[] DEFAULT '{}',     -- empty = all methods; specific = restricted
    min_amount              NUMERIC(10,2) DEFAULT 1,
    max_upi_amount          NUMERIC(10,2) DEFAULT 100000,
    emi_enabled             BOOLEAN NOT NULL DEFAULT FALSE,
    emi_min_amount          NUMERIC(10,2),
    emi_tenures             INTEGER[] DEFAULT '{3,6,12}',
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE payments.transactions (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id          TEXT NOT NULL UNIQUE,   -- EduForge internal
    tenant_id               UUID NOT NULL,
    invoice_id              TEXT NOT NULL,          -- Fee invoice ID (Module 25)
    student_id              UUID,
    gateway                 TEXT NOT NULL,
    gateway_order_id        TEXT NOT NULL,
    payment_id              TEXT,                   -- populated on capture
    amount                  NUMERIC(14,2) NOT NULL,
    currency                TEXT NOT NULL DEFAULT 'INR',
    status                  TEXT NOT NULL DEFAULT 'created',
    -- payment.created, payment.attempted, payment.captured, payment.failed
    method                  TEXT,
    bank                    TEXT,
    card_network            TEXT,
    error_code              TEXT,
    error_description       TEXT,
    captured_at             TIMESTAMPTZ,
    reconciliation_status   TEXT DEFAULT 'pending',  -- pending, reconciled, mismatch
    settlement_date         DATE,
    settlement_amount       NUMERIC(14,2),
    gateway_fee             NUMERIC(14,2),
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT valid_status CHECK (status IN ('created','attempted','captured','failed','refunded'))
) PARTITION BY RANGE (created_at);

CREATE TABLE payments.transactions_2026
    PARTITION OF payments.transactions FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

CREATE INDEX idx_transactions_invoice ON payments.transactions (invoice_id, tenant_id);
CREATE INDEX idx_transactions_payment ON payments.transactions (payment_id) WHERE payment_id IS NOT NULL;
CREATE INDEX idx_transactions_status ON payments.transactions (tenant_id, status, created_at DESC);

CREATE TABLE payments.webhook_events (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id               UUID NOT NULL,
    provider                TEXT NOT NULL,
    event_id_header         TEXT,
    payload_size            INTEGER,
    processing_status       TEXT NOT NULL DEFAULT 'pending',  -- pending, done, failed
    processed_at            TIMESTAMPTZ,
    error_message           TEXT,
    received_at             TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE payments.refunds (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id          UUID NOT NULL REFERENCES payments.transactions(id),
    tenant_id               UUID NOT NULL,
    gateway_refund_id       TEXT,
    amount                  NUMERIC(14,2) NOT NULL,
    reason                  TEXT NOT NULL,
    status                  TEXT NOT NULL DEFAULT 'processing',  -- processing, processed, failed
    initiated_by            UUID NOT NULL,
    processed_at            TIMESTAMPTZ,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE payments.offline_payments (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id               UUID NOT NULL,
    invoice_id              TEXT NOT NULL,
    student_id              UUID,
    method                  TEXT NOT NULL,  -- cash, cheque, dd, neft, rtgs, imps
    amount                  NUMERIC(14,2) NOT NULL,
    reference_number        TEXT,           -- cheque no, UTR no, DD no
    bank_name               TEXT,
    payment_date            DATE NOT NULL,
    status                  TEXT NOT NULL DEFAULT 'pending',  -- pending, verified, bounced, cancelled
    verified_by             UUID,           -- maker
    approved_by             UUID,           -- checker (required for > Rs. 5000)
    receipt_s3_key          TEXT,
    notes                   TEXT,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE payments.payment_links (
    short_code              TEXT PRIMARY KEY,
    tenant_id               UUID NOT NULL,
    invoice_id              TEXT NOT NULL,
    gateway_link_url        TEXT NOT NULL,
    amount                  NUMERIC(14,2) NOT NULL,
    opened_count            INTEGER NOT NULL DEFAULT 0,
    payment_started_count   INTEGER NOT NULL DEFAULT 0,
    is_paid                 BOOLEAN NOT NULL DEFAULT FALSE,
    expires_at              TIMESTAMPTZ NOT NULL,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE payments.settlement_batches (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id               UUID NOT NULL,
    gateway                 TEXT NOT NULL,
    settlement_date         DATE NOT NULL,
    transaction_count       INTEGER NOT NULL,
    gross_amount            NUMERIC(14,2) NOT NULL,
    gateway_fees            NUMERIC(14,2) NOT NULL,
    net_amount              NUMERIC(14,2) NOT NULL,
    gateway_settlement_id   TEXT,
    downloaded_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (tenant_id, gateway, settlement_date)
);

CREATE TABLE payments.gateway_fees (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_id          UUID NOT NULL REFERENCES payments.transactions(id),
    gateway                 TEXT NOT NULL,
    fee_amount              NUMERIC(10,4) NOT NULL,
    fee_pct                 NUMERIC(6,4) NOT NULL,
    is_estimated            BOOLEAN NOT NULL DEFAULT TRUE,  -- FALSE after reconciliation
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE payments.orphan_transactions (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id               UUID NOT NULL,
    gateway                 TEXT NOT NULL,
    payment_id              TEXT NOT NULL UNIQUE,
    settlement_date         DATE NOT NULL,
    amount                  NUMERIC(14,2) NOT NULL,
    requires_review         BOOLEAN NOT NULL DEFAULT TRUE,
    resolved_at             TIMESTAMPTZ,
    resolution_notes        TEXT,
    discovered_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE payments.reconciliation_runs (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id               UUID NOT NULL,
    run_date                DATE NOT NULL,
    gateway                 TEXT NOT NULL,
    settlement_count        INTEGER NOT NULL,
    reconciled_count        INTEGER NOT NULL DEFAULT 0,
    mismatch_count          INTEGER NOT NULL DEFAULT 0,
    orphan_count            INTEGER NOT NULL DEFAULT 0,
    status                  TEXT NOT NULL DEFAULT 'running',  -- running, completed, failed
    started_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at            TIMESTAMPTZ
);

CREATE TABLE payments.reconciliation_mismatches (
    id                      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id                  UUID NOT NULL REFERENCES payments.reconciliation_runs(id),
    transaction_id          UUID REFERENCES payments.transactions(id),
    eduforge_amount         NUMERIC(14,2) NOT NULL,
    gateway_amount          NUMERIC(14,2) NOT NULL,
    difference              NUMERIC(14,2) NOT NULL,
    resolved                BOOLEAN NOT NULL DEFAULT FALSE,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## 11. API Endpoints

```python
# payments/routes.py (FastAPI)
router = APIRouter(prefix="/payments", tags=["Payments"])

# Order creation (called by Module 25)
@router.post("/orders")
async def create_order(
    payload: CreateOrderRequest,
    user=Depends(require_permission("payments.orders.write")),
):
    return order_service.create_payment_order(
        tenant_id=user.tenant_id,
        invoice_id=payload.invoice_id,
        amount=payload.amount,
        student_id=payload.student_id,
        fee_description=payload.description,
    )

@router.get("/orders/{order_id}/status")
async def order_status(order_id: str, user=Depends(require_permission("payments.orders.read"))):
    txn = db.fetchone("""
        SELECT status, payment_id, method, captured_at FROM payments.transactions
        WHERE invoice_id = %s AND tenant_id = %s
        ORDER BY created_at DESC LIMIT 1
    """, [order_id, user.tenant_id])
    return txn

# QR code
@router.get("/qr/{invoice_id}")
async def get_qr(invoice_id: str, user=Depends(require_permission("payments.qr.read"))):
    return qr_service.generate_invoice_qr(invoice_id, user.tenant_id)

# Payment links
@router.post("/links")
async def create_link(
    payload: CreateLinkRequest,
    user=Depends(require_permission("payments.links.write")),
):
    short_url = link_service.create_payment_link(
        tenant_id=user.tenant_id,
        invoice_id=payload.invoice_id,
        amount=payload.amount,
        student_name=payload.student_name,
        fee_description=payload.description,
        expire_days=payload.expire_days or 7,
    )
    return {"short_url": short_url}

# Refunds
@router.post("/refunds")
async def initiate_refund_endpoint(
    payload: RefundRequest,
    user=Depends(require_permission("payments.refunds.write")),
):
    refund_id = refund_service.initiate_refund(
        user.tenant_id, payload.transaction_id, payload.amount, payload.reason, user.id
    )
    return {"refund_id": refund_id, "status": "processing"}

# Admin: gateway config
@router.post("/admin/gateways")
async def configure_gateway(
    payload: GatewayConfigRequest,
    user=Depends(require_permission("admin.gateway.write")),
):
    return gateway_config_service.configure(user.tenant_id, payload)

@router.post("/admin/gateways/test")
async def test_gateway(
    payload: GatewayTestRequest,
    user=Depends(require_permission("admin.gateway.write")),
):
    """Test credentials by creating + cancelling a Rs. 1 test order."""
    return gateway_config_service.test_credentials(user.tenant_id, payload.provider, payload.credentials)

@router.get("/admin/reconciliation")
async def reconciliation_report(
    date: str,
    user=Depends(require_permission("admin.payments.read")),
):
    return reconciliation_service.get_report(user.tenant_id, date)

@router.get("/admin/analytics")
async def payment_analytics(
    from_date: str,
    to_date: str,
    user=Depends(require_permission("admin.payments.read")),
):
    return analytics_service.payment_analytics(user.tenant_id, from_date, to_date)

# Short link resolution (CloudFront Lambda@Edge for ultra-low latency)
@router.get("/s/{short_code}", include_in_schema=False)
async def resolve_link(short_code: str):
    target = link_service.resolve_short_link(short_code)
    if not target:
        return templates.TemplateResponse("payment_link_expired.html", {})
    return RedirectResponse(target, status_code=302)

# BBPS
@router.get("/bbps/fetch-bill/{roll_number}", include_in_schema=False)
async def bbps_fetch(roll_number: str, request: Request):
    return bbps_service.fetch_bill(roll_number, request)
```

---

## 12. Cost Architecture

| Component | Monthly Cost (5K tenants) | Notes |
|-----------|--------------------------|-------|
| Lambda (webhook, order, reconciliation) | ~Rs. 3,000 | ~10M invocations/month |
| DynamoDB (webhook dedup, short links) | ~Rs. 1,500 | TTL auto-purges old records |
| SQS (payment events queue) | ~Rs. 800 | ~10M messages/month |
| S3 (QR codes, reconciliation reports) | ~Rs. 600 | Small objects, short-lived |
| Secrets Manager (gateway credentials) | ~Rs. 2,500 | ~5K secrets × API calls |
| Gateway fees (Razorpay/PhonePe) | Borne by institution | 0–2% per transaction |
| **EduForge infra total** | **~Rs. 8,400/month** | ~Rs. 0.000168/student/month |

Gateway transaction fees are entirely borne by the institution (their own gateway account) — EduForge has no financial liability or revenue from student fee payments.
