# Page 23 — Test Case Repository

**URL:** `/portal/product/test-cases/`
**Permission:** `product.manage_test_cases`
**Priority:** P2
**Roles:** QA Engineer, PM Platform

---

## Purpose

Central repository for all 12,000+ test cases across the SRAV platform. Organises test cases by feature area, test type, and priority. Enables QA engineers to browse, write, review, and execute test cases; track coverage against product features; and import/export test suites for external tools. Directly feeds test runs on page 21 (QA Dashboard) and release gate requirements on the Release Manager (page 03).

Core responsibilities:
- Store and organise all test cases with full documentation
- Track which feature areas are well-covered vs gaps
- Manage test case review and approval workflow
- Link test cases to product features, user stories, and releases
- Support test case versioning (when a feature changes, test cases are updated)
- Import from Postman, Cucumber, and CSV; export in standard formats
- Provide test suite builder (group test cases into suites for targeted runs)

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  "Test Case Repository"    [New Test Case]  [Import]  [Export]  │
├─────────────────────────────────────────────────────────────────┤
│  KPI Strip — 5 cards                                            │
├─────────────────────────────────────────────────────────────────┤
│  Tab Bar:                                                       │
│  All Cases · Suites · Coverage Map · Review Queue · Archived    │
├─────────────────────────────────────────────────────────────────┤
│  Two-panel layout:                                              │
│  Left: Feature Tree (collapsible) │ Right: Test Case List/Detail│
└─────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip — 5 Cards

| # | Label | Value | Click Action |
|---|---|---|---|
| 1 | Total Test Cases | Count of all active test cases | Opens All Cases |
| 2 | Automated | Count marked as automated | Filters to automated |
| 3 | Manual Only | Count without automation | Filters to manual |
| 4 | Pending Review | Test cases in review queue | Opens Review Queue |
| 5 | Coverage Gaps | Feature areas with < 50% test coverage | Opens Coverage Map |

---

## Tab 1 — All Cases (Primary View)

### Two-Panel Layout

**Left Panel — Feature Tree (280px wide)**

Hierarchical tree of all feature areas. Expandable/collapsible.

Structure:
```
▶ Student Experience
   ▶ Authentication
      Login (24 cases)
      Registration (18 cases)
      Password Reset (12 cases)
      2FA (8 cases)
   ▶ Exam Taking
      Exam Start (15 cases)
      MCQ Questions (22 cases)
      MSQ Questions (14 cases)
      Integer Questions (10 cases)
      Section Navigation (18 cases)
      Timer Behaviour (20 cases)
      Submit Flow (16 cases)
      Proctoring (28 cases)
   ▶ Results
      Immediate Result (14 cases)
      Detailed Analysis (19 cases)
      Leaderboard (12 cases)
      Score Certificate (8 cases)
   ▶ Mobile App
      App Login (10 cases)
      Offline Mode (22 cases)
      FCM Notifications (15 cases)
▶ Institution Admin
   ▶ Exam Management
      Create Exam (30 cases)
      Schedule Exam (20 cases)
      Exam Settings (25 cases)
      Live Monitor (18 cases)
   ▶ Student Management
      Import Students (15 cases)
      Batch Management (14 cases)
      Student Profile (12 cases)
   ▶ Analytics
      Dashboard (14 cases)
      Reports (20 cases)
   ▶ Communication
      Announcements (16 cases)
      Email Templates (10 cases)
▶ Finance
   ▶ Payment Flow (22 cases)
   ▶ Invoice & GST (14 cases)
   ▶ Refunds (10 cases)
▶ Platform Admin
   ▶ Feature Flags (18 cases)
   ▶ Release Deploy (12 cases)
   ▶ Rollback (8 cases)
   ▶ Plan Config (14 cases)
▶ API & Integrations
   ▶ REST API (45 cases)
   ▶ Webhooks (20 cases)
   ▶ SSO (16 cases)
▶ Performance
   ▶ Load Tests (30 cases)
   ▶ Stress Tests (15 cases)
```

Selecting any node in the tree filters the right panel to show only test cases in that area.
Node label colour: green (≥80% passing) · amber (60–79%) · red (<60%) based on last test run.

**Right Panel — Test Case List**

### Toolbar

| Control | Options |
|---|---|
| Search | Test case title, ID, tag |
| Test Type | All / Unit / Integration / E2E / API / Manual / Performance |
| Status | All / Active / Draft / Under Review / Deprecated |
| Automation | All / Automated / Manual Only / Partially Automated |
| Priority | All / P0 Critical / P1 High / P2 Medium / P3 Low |
| Pass/Fail | All / Passing / Failing / Flaky / Not Run |
| Linked Feature | Filter by roadmap feature |

### Test Case Table — 10 columns

| Column | Detail |
|---|---|
| ID | TC-NNNNN |
| Title | Full test case title |
| Feature Area | From tree |
| Type | Badge: Unit / Integration / E2E / API / Manual / Performance |
| Priority | Badge |
| Automation | ✓ Automated · ◐ Partial · ✗ Manual |
| Last Run Status | Passed (green) · Failed (red) · Flaky (amber) · Not Run (grey) |
| Last Run Date | Relative date |
| Duration | Avg run duration (seconds) |
| Actions | View · Edit · Clone · Run Isolated · Archive |

**Row expand:** Shows test case summary — preconditions, steps summary, expected result.

**Pagination:** Showing X–Y of Z cases · page pills · per-page selector (25 / 50 / 100)

---

## Test Case Detail Drawer (720px)

Opened by clicking "View" or the test case title.

### Drawer Header
- TC-NNNNN · Title · Priority badge · Type badge · Status badge
- "Edit" button · "Clone" button · "Archive" button

### Drawer Tab 1 — Details

| Field | Content |
|---|---|
| ID | TC-NNNNN |
| Title | Full descriptive title |
| Feature Area | Breadcrumb: Feature → Sub-feature |
| Test Type | Unit / Integration / E2E / API / Manual / Performance |
| Priority | P0 / P1 / P2 / P3 with justification |
| Automation Status | Automated / Manual / Partially Automated |
| Automation Script | Path to test script file (e.g. `tests/e2e/exam/test_submit.py`) or "Not automated" |
| Linked User Story | US-NNN: user story title (clickable link to roadmap item) |
| Linked Feature | Feature name in roadmap |
| Linked Release | Release version this test was added for |
| Created By | QA engineer name |
| Created On | Date |
| Last Updated | Date + by whom |
| Version | v1.x |
| Tags | Free-text tags (e.g. "exam", "mobile", "regression", "critical-path") |
| Estimated Duration | Manual: estimated minutes · Automated: avg seconds from last 10 runs |

### Drawer Tab 2 — Test Steps

Full test case documentation.

**Preconditions:**
- List of conditions that must be true before test execution
- Example: "Student is registered and verified. Institution has SSC domain enabled. At least 1 exam is in Scheduled state with future date."

**Test Data:**
- Specific input data needed for this test
- Example: "Student: test_student_01@srav.in / Pass123. Exam: TC Mock SSC CGL #1. Expected Score: 72/100."

**Steps Table:**

| Step # | Action | Expected Result | Actual Result (during run) | Pass/Fail |
|---|---|---|---|---|
| 1 | Navigate to portal URL, enter credentials, click Login | Dashboard page loads within 2 seconds | — | — |
| 2 | Click "Upcoming Exams" section | Exam list shows TC Mock SSC CGL #1 | — | — |
| 3 | Click "Start Exam" on TC Mock SSC CGL #1 | Full-screen instruction page appears | — | — |
| 4 | Read instructions, click "I Agree & Start" | Question 1 of Section 1 displayed, timer starts | — | — |
| 5 | Answer all 100 questions (using test data answer key) | Each answer saved, progress indicator updates | — | — |
| 6 | Click "Submit Exam" | Confirmation dialog appears | — | — |
| 7 | Click "Confirm Submit" | Result page loads showing score, rank, accuracy | — | — |
| 8 | Verify score matches expected: 72/100 | Score displayed: 72. Accuracy: 72%. Time taken shown. | — | — |

**Post-conditions:**
- State the system should be in after successful test execution
- Example: "Attempt record saved in DB with submitted=true. Result page accessible. Rank computed."

### Drawer Tab 3 — Run History

Table of every time this test case was executed:

| Run ID | Date | Environment | Status | Duration | Run By | Failure Message |
|---|---|---|---|---|---|---|
| TR-2026-03-20-001 | 20 Mar 2026 | Staging | ✓ Passed | 48s | CI Pipeline | — |
| TR-2026-03-18-004 | 18 Mar 2026 | Staging | ✗ Failed | 22s | Deepa Menon | "Timeout: result page took 8.4s to load" |
| TR-2026-03-15-002 | 15 Mar 2026 | UAT | ✓ Passed | 51s | CI Pipeline | — |

Pass rate summary: X passes out of Y runs = Z%

### Drawer Tab 4 — Linked Defects

Defects that were created as a result of this test case failing.

| Defect ID | Title | Severity | Status | Linked Run |
|---|---|---|---|---|
| DEF-0482 | Result page timeout on high load | P1 | In Progress | TR-2026-03-18-004 |

"Link Existing Defect" button + "Create New Defect" button.

### Drawer Tab 5 — Reviews

Review history for this test case. Who reviewed it, what was changed, approvals.

---

## Tab 2 — Suites

Test suites are named groupings of test cases used for targeted test runs.

### Suite List Table

| Column | Detail |
|---|---|
| Suite Name | Descriptive name |
| Purpose | Regression / Smoke / Sanity / Feature-specific / Release-specific |
| Test Case Count | Total cases in suite |
| Automated % | % of cases that are automated |
| Avg Run Duration | Estimated total time to run suite |
| Last Run | Timestamp + pass rate |
| Used In Releases | Count of releases this suite is linked to |
| Actions | Run · Edit · Clone · Archive |

### Suite Detail Drawer (640px)

**Header:** Suite name · purpose · test count · avg duration

**Tab 1 — Tests:**
List of test cases in this suite with ability to reorder (drag-and-drop), remove, or add cases.

**Tab 2 — Run Config:**
- Parallel workers: 1 / 2 / 4 / 8
- Retry flaky tests: Yes (1 retry / 2 retries) / No
- Stop on first failure: Yes / No
- Environment: Staging / UAT / Pre-Prod
- Notification: who to notify on completion/failure

**Tab 3 — Run History:**
Last 10 runs of this suite with pass rate trend chart.

### Common Suites

| Suite | Cases | Purpose | Linked Releases |
|---|---|---|---|
| Full Regression | 12,000+ | Run before every major release | All |
| Smoke Test | 80 | Quick health check after deploy | All |
| Critical Path | 45 | Most important user journeys | All |
| Exam Flow | 320 | Exam-related only | Exam features |
| Mobile App | 250 | Flutter app tests | Mobile releases |
| Payment Flow | 90 | Finance features | Finance releases |
| API Regression | 480 | REST API tests only | API releases |

---

## Tab 3 — Coverage Map

Visual map of test case coverage across all feature areas.

### Coverage Summary

Same heatmap concept as QA Dashboard coverage tab, but from the test case management perspective (counts of test cases per feature area vs recommended coverage).

**Coverage Table:**

| Feature Area | Total Cases | Automated | Manual Only | Coverage Score | Recommendation |
|---|---|---|---|---|---|
| Authentication | 62 | 58 | 4 | 94% | Good |
| Exam Taking | 143 | 130 | 13 | 92% | Good |
| Proctoring | 28 | 10 | 18 | 65% | Need more automation |
| Mobile App | 97 | 45 | 52 | 71% | Add automated E2E |
| API Endpoints | 480 | 480 | 0 | 98% | Excellent |
| Payment Flow | 90 | 70 | 20 | 85% | Good |
| Analytics Dashboard | 48 | 20 | 28 | 58% | Needs more cases |
| Admin Settings | 34 | 12 | 22 | 45% | Under-covered |

### Gap Identification

Below the coverage table: "Coverage Gaps" list showing feature areas that need more test cases. For each gap:
- Feature area
- Current case count
- Recommended minimum
- Gap count
- "Create Test Cases" button → pre-fills new test case form with the feature area

---

## Tab 4 — Review Queue

Test cases that have been written or updated and are awaiting peer review before becoming "Active."

### Review Queue Table

| Column | Detail |
|---|---|
| TC ID | TC-NNNNN |
| Title | Test case title |
| Written By | QA engineer |
| Submitted On | Date |
| Type | Test type |
| Priority | Badge |
| Assigned Reviewer | Name or "Unassigned" |
| Days in Queue | Count (amber if > 3) |
| Actions | Review · Assign Reviewer |

### Review Drawer (640px)

Shows test case in read mode with review action panel on the right:

**Reviewer can:**
- Approve: test case marked as Active
- Request Changes: opens text field for change description
- Add comment per test step

**Review criteria checklist:**
- [ ] Steps are clear and unambiguous
- [ ] Preconditions are complete
- [ ] Expected results are verifiable
- [ ] Test data is specified
- [ ] Priority is appropriate
- [ ] Feature area is correctly categorised

---

## Tab 5 — Archived

Test cases no longer in active use. Kept for historical reference.

Archived test cases can be:
- Restored to Active
- Permanently deleted (with confirmation)
- Used as reference when writing new cases for similar functionality

---

## New Test Case Modal (multi-step)

**Step 1 — Basics:**
- Title (required, max 120 chars)
- Feature Area (tree selector)
- Test Type: Unit / Integration / E2E / API / Manual / Performance
- Priority: P0 / P1 / P2 / P3

**Step 2 — Documentation:**
- Preconditions (required, min 1 item)
- Test data (free text)
- Steps table (minimum 2 steps required: action + expected result per step)
- Post-conditions

**Step 3 — Links:**
- Linked User Story (optional)
- Linked Feature (optional)
- Linked Release (optional)
- Automation script path (optional)
- Tags (free text, comma-separated)

**Step 4 — Review:**
- Summary of entered data
- "Submit for Review" button (creates case in "Under Review" status)
- "Save as Draft" button

---

## Import / Export

### Import Formats Supported

| Format | Source Tool | Behaviour |
|---|---|---|
| CSV (SRAV format) | Any spreadsheet | Bulk import with mapping dialog |
| Postman Collection | Postman | Imports API test cases from collection JSON |
| Cucumber/Gherkin | BDD test files | Imports Given/When/Then steps as test steps |
| JIRA XML | JIRA test export | Maps JIRA test fields to SRAV test case fields |

### Export Formats Supported

| Format | Target Tool |
|---|---|
| CSV (full export) | Spreadsheet analysis |
| JSON | API consumers, custom tooling |
| PDF | Management reporting |
| Cucumber/Gherkin | BDD test frameworks |

---

## Test Case Lifecycle

A test case moves through the following lifecycle:

| Status | Description | Transition Rules |
|---|---|---|
| Draft | Written but not reviewed | Created by QA engineer; can be freely edited |
| Under Review | Submitted for peer review | Read-only to author while in review; reviewer can approve or request changes |
| Active | Approved and in use | Included in test runs; can only be edited by creating a new version |
| Deprecated | No longer applicable | Hidden from default view; not included in runs; kept for history |
| Archived | Permanently inactive | Fully archived; searchable but not executable |

**Version control:** When an Active test case is edited, the current version is preserved as an older version. The edited test case goes back to Draft → Under Review workflow before becoming Active again. This prevents untested test case changes from silently entering the test suite.

---

## Bulk Operations

Select multiple test cases from the list panel (checkbox per row):

| Bulk Action | Detail |
|---|---|
| Add to Suite | Add all selected to an existing or new suite |
| Change Priority | Update priority for all selected |
| Submit for Review | Send all selected Drafts to review queue |
| Archive | Archive all selected (with confirmation) |
| Export Selected | Download selected test cases as CSV / JSON / PDF |
| Assign Reviewer | Assign a specific QA reviewer to all selected (Review Queue) |
| Tag | Add tags to all selected |
| Link to Release | Associate all selected with a release |

---

## Test Case Templates

New test case creation can start from a template for common patterns:

| Template | Description | Pre-filled Fields |
|---|---|---|
| CRUD Operation | Standard create/read/update/delete test | Step structure with create, verify, update, verify, delete, verify pattern |
| Authentication Test | Login/logout pattern | Precondition: user not logged in; steps: enter credentials, verify access |
| API Endpoint Test | REST API test structure | HTTP method, endpoint, request body, expected status code, expected response |
| Error State Test | Testing error handling | Steps: trigger error condition, verify error message, verify recovery |
| Permission Boundary Test | Verify access control | Steps: login as role, attempt action, verify permission enforced |
| Mobile App Test | Flutter app test | Steps: app state preconditions; native UI interaction steps |
| Performance Test | Response time check | Steps: send N concurrent requests, verify P95 response < threshold |
| E2E Workflow Test | Multi-step end-to-end | Full user journey from login to completion |

---

## Integration Points

| Page | Integration |
|---|---|
| Page 21 — QA Dashboard | Test runs reference TC-NNNNN IDs. Clicking test case in QA Dashboard run detail opens the case in this repository. Coverage heatmap in QA Dashboard pulls pass rate data per feature area from this repository. |
| Page 25 — Defect Tracker | "Create Defect from Test Failure" links defect to the test case that exposed it. Defect tracker shows linked test case in defect detail. |
| Page 03 — Release Manager | Releases can be linked to test suites. Release gate coverage % is computed from test cases linked to that release. |
| Page 26 — Automation Monitor | CI/CD pipeline test execution uses test case IDs. Automation Monitor links failed pipeline tests to their test case entries. |
| Page 24 — Performance Test Dashboard | Performance test cases (type: Performance) are part of performance test scenarios. Pass/fail is recorded back into the run history of the performance test case. |

---

## Notifications

| Event | Recipient | Channel |
|---|---|---|
| Test case submitted for review | Assigned reviewer | In-App + Email |
| Test case approved | Author | In-App |
| Test case returned with changes requested | Author | In-App |
| Test case fails in a test run for the first time | Assigned QA engineer | In-App |
| Test case flakiness threshold exceeded (< 90% pass rate over 20 runs) | Author + QA Lead | In-App |
| Coverage gap detected (feature area drops below 70% coverage) | QA Lead | In-App |
| Bulk import completed | Importing user | In-App |

---

## Key Design Decisions

| Concern | Decision | Rationale |
|---|---|---|
| Two-panel layout | Tree + list | Feature tree gives context; list gives detail. Together faster than flat search for QA. |
| Coverage map | Separate tab | Coverage is a planning/management concern, not daily QA workflow |
| Review queue | Separate tab | Test case quality control — bad test cases cause false confidence |
| Suite builder | Separate tab | Suites are reusable configurations; separate management from individual cases |
| Run history in case drawer | Per-case history | QA needs to see if a specific test has been consistently passing or intermittently failing |
| Linked defects | In case drawer | Connects test failures to defect records without leaving the repository |
| Version control on edits | Preserve old version when editing Active test | Prevents untested changes from silently entering the test suite |
| Test case templates | Starting points for common patterns | Reduces cognitive load for new QA; ensures structural consistency across test cases |
| Lifecycle statuses | Draft → Under Review → Active → Deprecated | Full traceability; no test case goes active without review; no test case is silently deleted |
| Tree colour coding by pass rate | Green / Amber / Red nodes | Immediately identifies which feature areas have quality problems at a glance in the tree |
| Priority on test cases | P0–P3 matching defect priority | Enables prioritising which tests run first in smoke/sanity suites |

| Priority P0–P3 | Matches defect severity scale | Consistent terminology across QA Dashboard, Test Cases, and Defect Tracker |

---

## UAT (User Acceptance Testing) Program

**Purpose:** Before every major release (e.g., v3.5.0), a set of 5–10 **beta institutions** validate real-world workflows in the Pre-Production environment. This is distinct from internal QA testing — UAT is performed by actual institution admins and teachers who encounter real usability issues that internal testers miss. QA Engineer owns coordination; PM Platform owns beta institution selection.

**Why in Test Case Repository (not QA Dashboard):** UAT requires specific test scenarios (a subset of the full test case repository) to be packaged and shared with non-engineer users. The repository is the source of truth for which cases are included in any UAT plan.

---

### UAT Plan Table

| UAT ID | Release | Beta Institutions | Test Scenarios | UAT Start | UAT End | Sign-offs | Status |
|---|---|---|---|---|---|---|---|
| UAT-v3.5.0 | v3.5.0 | 8 institutions | 42 scenarios | Apr 1 | Apr 7 | 6/8 | 🟡 In Progress |
| UAT-v3.4.2 | v3.4.2 | 6 institutions | 28 scenarios | Feb 22 | Feb 28 | 6/6 | ✅ Complete |
| UAT-v3.4.0 | v3.4.0 | 10 institutions | 56 scenarios | Jan 5 | Jan 12 | 9/10 | ✅ Complete |

**[+ New UAT Plan]** button → opens UAT Plan Creation modal.

---

### UAT Plan Detail Drawer (720px)

**Trigger:** Row click on UAT Plan Table
**Header:** UAT-v3.5.0 · Release v3.5.0 · Status badge · `[×]`

**Tab A — Beta Institutions:**

Table of participating institutions:

| Institution | Type | Plan | Contact | Test Tenant | Assigned Scenarios | Sign-off Status |
|---|---|---|---|---|---|---|
| Sri Chaitanya Coaching | Coaching | Enterprise | mgr@srichaitanya.in | SCH-TEST-01 | 12 scenarios | ✅ Signed off |
| Delhi Public School (HYD) | School | Professional | admin@dps-hyd.in | DPS-TEST-01 | 8 scenarios | ✅ Signed off |
| Narayana Junior College | College | Professional | it@narayana.in | NJC-TEST-01 | 9 scenarios | ⏳ Pending |
| Resonance Coaching (RJP) | Coaching | Enterprise | qa@resonance.ac.in | RES-TEST-01 | 11 scenarios | ⏳ Pending |

**[Add Institution]:** search institutions and invite them to UAT (they receive a CSM email with pre-prod credentials for their test tenant)
**[Remove]:** removes institution from this UAT plan

**Institution selection criteria:**
- Mix of institution types (at least 1 School, 1 College, 1 Coaching)
- Mix of plan tiers (at least 1 Standard, 1 Professional, 1 Enterprise)
- Volunteer basis — institutions previously flagged as "UAT willing" in CSM system
- Maximum 10 to keep coordination manageable

**Tab B — Test Scenarios:**

Table of all test cases included in this UAT plan:

| # | Test Case ID | Feature Area | Priority | Steps | Expected Outcome | Institution | Status |
|---|---|---|---|---|---|---|---|
| 1 | TC-4821 | Exam creation (new pattern) | P0 | 7 steps | Exam created, live, 500 students can submit | Sri Chaitanya | ✅ Pass |
| 2 | TC-4822 | Result publish with rank | P1 | 5 steps | Rank list visible in 30s | Delhi PS | ⏳ Pending |
| 3 | TC-4823 | WhatsApp result notification | P1 | 3 steps | 100% students receive WhatsApp | Narayana | ❌ Fail |
| 4 | TC-4824 | Institution admin role change | P2 | 4 steps | Permission update < 30s | Resonance | ✅ Pass |

**[Add from Repository]:** opens repository search to add test cases to this UAT plan
**Scenario execution:** Institution contacts mark each scenario as Pass / Fail / Blocked via a simple form sent by QA (or via their test tenant portal's feedback widget)

**Tab C — Issues Found:**

Issues reported by beta institutions during UAT. Each issue is linked to a test case and auto-creates a draft defect in page 25 (Defect Tracker) for QA to validate.

| Issue # | Reported By | Test Case | Description | Severity | QA Verdict | Defect ID |
|---|---|---|---|---|---|---|
| UAT-I-012 | Narayana Jr College | TC-4823 | WhatsApp notification delayed 45 min | P1 | Confirmed bug | DEF-2891 |
| UAT-I-011 | Delhi PS | TC-4822 | Rank list shows wrong student name | P0 | Confirmed bug | DEF-2890 |
| UAT-I-010 | Sri Chaitanya | TC-4821 | Exam creation takes 90s on slow network | P3 | Known limitation — documented | — |

**Tab D — Sign-off:**

Institution-wise sign-off status. Each institution's contact must explicitly sign off before the institution's UAT is considered complete.

**Sign-off conditions:**
- All assigned scenarios completed (Pass or accepted exception)
- All P0/P1 issues resolved or deferred with documented reason
- Institution contact clicks [Confirm Sign-off] in their test tenant portal OR QA receives email confirmation

**Overall UAT completion rule:**
- A release can proceed to production if ≥ 80% of beta institutions have signed off and zero P0 defects from UAT are open
- If UAT sign-off rate < 80%: release blocked, flagged in Release Manager (page 03)

**Tab E — Communication Log:**

All communications with beta institutions:
- Invitation emails sent (with pre-prod tenant links)
- Scenario packages shared
- Issue follow-up emails
- Sign-off confirmations

---

### UAT Plan Creation Modal (4 steps)

**Step 1 — Select Release:** dropdown from Release Manager (page 03) — only Pre-Production or Staging releases eligible

**Step 2 — Select Beta Institutions:** search and add institutions · assign test tenants from Test Tenant Manager (page 22)

**Step 3 — Select Test Scenarios:** search repository by feature area, priority, release tag → add to UAT plan

**Step 4 — Schedule:** UAT start date · UAT end date · notification template for invitation email · [Create UAT Plan]

---

### Beta Institution Registry

**Location:** Sub-section in UAT Program (below UAT Plan Table)

Institutions that have agreed to participate in future UAT cycles. Maintained by CSM (Division J).

| Institution | Type | Plan | Contact | Total UAT Rounds | Last UAT | Preference |
|---|---|---|---|---|---|---|
| Sri Chaitanya Coaching | Coaching | Enterprise | mgr@srichaitanya.in | 8 | Mar 2026 | Major releases only |
| Narayana Jr College | College | Professional | it@narayana.in | 5 | Mar 2026 | Any release |
| Delhi Public School (HYD) | School | Professional | admin@dps-hyd.in | 3 | Feb 2026 | Any release |

**[Add to Registry]** · **[Remove]** · **[Edit Preference]**

A minimum of 3 beta institutions must be in the registry at all times. If registry drops below 3, PM Platform (Role 5) is notified to engage CSM team for recruitment.
