# N-08 — Third-Party Vendor Risk Management

> **Route:** `/legal/vendor-risk/`
> **Division:** N — Legal & Compliance
> **Primary Role:** Compliance Lead (Role 76, Level 5) · Legal Counsel (Role 75, Level 4)
> **Read Access:** CTO (Role 3) · Finance Manager (Role 69) · Security Engineer (Role 16) · DPDP Officer (Role 77)
> **File:** `n-08-vendor-risk.md`
> **Priority:** P1 — EduForge depends on 18+ vendors; any vendor failure = platform failure
> **Status:** ✅ New page — vendor concentration risk undocumented until now

---

## 1. Purpose

EduForge's platform depends on external vendors for critical functions: AWS (compute + storage), Razorpay (payments), Cloudflare (CDN + R2), Twilio/MSG91 (SMS/OTP), AWS SES (email), DigiSign (e-signatures), IDFY (BGV), iThenticate (plagiarism), Google/Meta (ads), and others. A vendor outage, pricing change, data breach, or contract termination directly impacts EduForge's ability to serve 2,050 institutions and 7.6M students.

This page provides: (1) vendor registry with contract details, SLA commitments, and renewal dates, (2) vendor risk scoring (operational, financial, compliance, concentration), (3) vendor incident tracking (their outages affecting our platform), (4) DPDPA data processing agreements (DPA) status for vendors handling personal data, (5) vendor concentration analysis (single points of failure), and (6) exit strategy documentation for each critical vendor.

---

## 2. Page Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  Third-Party Vendor Risk Management     [Add Vendor] [Export]       │
├─────────────────────────────────────────────────────────────────────┤
│  RISK KPI STRIP (5 tiles)                                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ │
│  │ 18       │ │ 3        │ │ 14/18    │ │ 2        │ │ 4        │ │
│  │ Active   │ │ Critical │ │ DPA      │ │ Vendor   │ │ Contracts│ │
│  │ Vendors  │ │ (Single  │ │ Signed   │ │ Incidents│ │ Renewing │ │
│  │          │ │ PoF) ⚠️  │ │ ✅ 77.8% │ │ This Qtr │ │ in 90d   │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│  [Vendor Registry] [Risk Matrix] [DPA Tracker] [Incidents] [Exit Plans] │
├─────────────────────────────────────────────────────────────────────┤
│  VENDOR REGISTRY                                                    │
│                                                                     │
│  Vendor          │ Category     │ Risk  │ DPA  │ Contract   │ Spend│
│  ─────────────────────────────────────────────────────────────────  │
│  AWS             │ Infra        │ 🟡 Med│ ✅   │ Mar 2028   │ ₹28L/m│
│  Razorpay        │ Payments     │ 🔴 High│ ✅  │ Sep 2027   │ 1.8% │
│  Cloudflare      │ CDN/Storage  │ 🟡 Med│ ✅   │ Dec 2027   │ ₹4L/m│
│  MSG91           │ SMS/OTP      │ 🟡 Med│ ✅   │ Jun 2027   │ ₹2L/m│
│  Twilio          │ SMS Backup   │ 🟢 Low│ ✅   │ Annual     │ ₹20K │
│  AWS SES         │ Email        │ 🟢 Low│ ✅   │ (AWS)      │ ₹8K/m│
│  IDFY            │ BGV          │ 🟡 Med│ ✅   │ Mar 2027 ⚠│ ₹3L/m│
│  DigiSign        │ E-signatures │ 🟢 Low│ ⬜   │ Jul 2027   │ ₹40K │
│  iThenticate     │ Plagiarism   │ 🟢 Low│ ⬜   │ Annual     │ ₹1.2L│
│  Google Ads      │ Marketing    │ 🟢 Low│ N/A  │ Self-serve │ ₹8L/m│
│                                                                     │
│  ⚠️ IDFY contract expiring 31 March 2027 — renewal in progress     │
│  🔴 Razorpay = single point of failure for ALL payments             │
├─────────────────────────────────────────────────────────────────────┤
│  CONCENTRATION RISK ANALYSIS                                        │
│                                                                     │
│  SINGLE POINTS OF FAILURE:                                          │
│  🔴 AWS (Compute + DB + Queues + Email) — 78% of infrastructure    │
│     Mitigation: Multi-AZ; DR to ap-south-2 (Hyderabad); no multi-  │
│     cloud currently (cost prohibitive)                              │
│  🔴 Razorpay (100% of online payments)                              │
│     Mitigation: Backup NEFT/bank transfer process documented        │
│     Exit plan: PhonePe/Cashfree integration ready (tested quarterly)│
│  🔴 PostgreSQL (100% of transactional data)                         │
│     Mitigation: RDS Multi-AZ; daily backups; WAL streaming          │
│     Note: Not vendor-specific — managed service via AWS RDS         │
│  🟡 MSG91 (primary SMS/OTP)                                         │
│     Mitigation: Twilio as pre-configured backup; auto-failover      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Models

```python
class Vendor(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(choices=[
        ('INFRA', 'Infrastructure'), ('PAYMENTS', 'Payments'), ('COMMS', 'Communications'),
        ('SECURITY', 'Security/BGV'), ('CONTENT', 'Content Tools'), ('MARKETING', 'Marketing'),
        ('LEGAL', 'Legal/Compliance'), ('OTHER', 'Other')
    ])
    criticality = models.CharField(choices=[
        ('CRITICAL', 'Critical — Platform cannot function'), ('HIGH', 'High — Major degradation'),
        ('MEDIUM', 'Medium — Workaround available'), ('LOW', 'Low — Non-essential')
    ])
    contract_start = models.DateField()
    contract_end = models.DateField()
    auto_renew = models.BooleanField(default=False)
    monthly_spend_paise = models.BigIntegerField()
    payment_model = models.CharField(max_length=50)  # "usage-based", "fixed", "percentage"
    sla_uptime_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    sla_response_hours = models.IntegerField(null=True)
    dpa_signed = models.BooleanField(default=False)
    dpa_document_url = models.URLField(null=True)
    handles_pii = models.BooleanField(default=False)
    pii_categories = models.JSONField(default=list)  # ["student_phone", "aadhaar", "email"]
    exit_plan_url = models.URLField(null=True)
    alternative_vendor = models.CharField(max_length=200, null=True)
    risk_score = models.IntegerField(default=0)  # 0–100 computed
    owner = models.CharField(max_length=50)  # "cto", "finance", "legal"

class VendorIncident(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    incident_date = models.DateTimeField()
    description = models.TextField()
    impact_on_eduforge = models.TextField()
    duration_minutes = models.IntegerField()
    students_affected = models.IntegerField(default=0)
    sla_breach = models.BooleanField(default=False)
    credit_claimed = models.BooleanField(default=False)
    credit_amount_paise = models.BigIntegerField(default=0)
    linked_eduforge_incident = models.ForeignKey('engineering.Incident', null=True, on_delete=models.SET_NULL)

class VendorDPA(models.Model):
    """DPDPA 2023 Data Processing Agreement tracking."""
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    dpa_version = models.CharField(max_length=20)
    signed_date = models.DateField()
    expiry_date = models.DateField(null=True)
    data_categories = models.JSONField()  # ["student PII", "exam responses", "payment data"]
    processing_purposes = models.JSONField()  # ["OTP delivery", "payment processing"]
    data_location = models.CharField(max_length=100)  # "India (Mumbai)", "Global (Cloudflare)"
    sub_processors = models.JSONField(default=list)  # Vendor's own sub-processors
    breach_notification_hours = models.IntegerField(default=72)  # DPDPA: 72h mandatory
    deletion_on_termination = models.BooleanField(default=True)
    audit_right = models.BooleanField(default=True)  # EduForge can audit vendor
```

---

## 4. Business Rules

- **Every vendor handling personal data MUST have a signed DPA (Data Processing Agreement) under DPDPA 2023.** Currently 14/18 vendors have DPAs; the 4 without (DigiSign, iThenticate, 2 others) are in negotiation. Without a DPA, EduForge is the sole liable party for any data breach by the vendor — the DPA creates shared liability and contractual obligations for data protection. Compliance Lead must escalate unsigned DPAs monthly to Legal Counsel.
- **Vendor concentration in AWS (78% of infrastructure) is the single largest platform risk.** While multi-cloud is cost-prohibitive at current scale, the mitigation must be: Multi-AZ deployment (ap-south-1a + 1b), DR capability to ap-south-2 (Hyderabad), and no AWS-proprietary services that cannot be replicated (e.g., using PostgreSQL not DynamoDB, SQS not AWS-specific queuing). This preserves the option to migrate if AWS pricing or policy changes.
- **Razorpay as the sole payment gateway means a Razorpay outage = zero fee collection.** During JNTU exam fee collection (A-06) or school admission season, payment downtime of even 30 minutes affects thousands of transactions. The backup plan (PhonePe Business / Cashfree) must be integration-tested quarterly, not just documented. A tested backup is different from a documented one.
- **SLA credits are money left on the table.** When AWS has a 4-hour outage and their SLA promises 99.99%, EduForge is entitled to service credits. The VendorIncident model tracks whether credits were claimed. Many organizations never claim SLA credits because they don't track vendor incidents systematically. At ₹28L/month AWS spend, even a 10% credit for a qualifying outage is ₹2.8L recovered.
- **Contract renewal alerts must fire 90 days before expiry.** A lapsed contract means operating without SLA protection. If IDFY (BGV vendor) contract lapses and a BGV query fails, EduForge has no contractual recourse. The 90-day alert gives Legal + Finance time to negotiate renewal terms, evaluate alternatives, or plan migration.
- **Vendor risk score combines 4 dimensions:** Operational (uptime history, incidents), Financial (vendor stability, payment model risk), Compliance (DPA status, data location, breach history), and Concentration (single point of failure). Score 0–100; >70 = High Risk (red); 40–70 = Medium (yellow); <40 = Low (green). Recalculated monthly.

---

*Last updated: 2026-03-30 · Group 1 — Platform Admin · Division N*
