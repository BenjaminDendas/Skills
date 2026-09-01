# Requirements document formats

Three structures, each with a worked example. Pick per Step 3 of SKILL.md — the shared parts (summary, actors, business rules, NFRs, out of scope, assumptions) surround whichever one you use.

## Table of contents
- [Format A: User stories + acceptance criteria](#format-a-user-stories--acceptance-criteria)
- [Format B: Numbered functional requirements (FRS-style)](#format-b-numbered-functional-requirements-frs-style)
- [Format C: Use cases](#format-c-use-cases)
- [Shared sections (use with any format)](#shared-sections-use-with-any-format)

---

## Format A: User stories + acceptance criteria

Best for a single, self-contained feature small enough to live as one or two backlog items.

```markdown
# Feature: Password reset via email

## Summary
Customers who forget their password currently have to contact support to regain
access. This adds a self-service reset flow triggered from the login page.

## Actors
- Registered customer (has an existing account with a verified email)
- Support agent (no action required, but should see fewer reset tickets)

## User Stories

### FR-01: Request a password reset
As a registered customer who has forgotten my password,
I want to request a reset link by entering my email address,
so that I can regain access without contacting support.

**Acceptance Criteria**
- Given a registered email address, when the customer submits the reset request,
  then a reset link is sent to that address within 2 minutes.
- Given an email address not associated with any account, when the customer
  submits the reset request, then the customer sees the same confirmation
  message as a successful request (no account enumeration).
- Given a customer who submits more than 5 reset requests for the same email
  within 15 minutes, when the 6th request is submitted, then it is rejected
  with a rate-limit message.

### FR-02: Complete a password reset
As a customer who has received a reset link,
I want to set a new password by following the link,
so that I can log in again.

**Acceptance Criteria**
- Given a valid, unexpired reset link, when the customer submits a new
  password meeting the account's password rules, then the password is
  updated and the customer is signed in.
- Given a reset link older than 30 minutes, when the customer opens it,
  then they see an expired-link message and an option to request a new one.
- Given a reset link that has already been used once, when it is opened
  again, then it is treated as invalid.
```

---

## Format B: Numbered functional requirements (FRS-style)

Best for a larger feature or initiative spanning multiple areas — reads as a spec to review and sign off on as a whole, and every line is independently referenceable.

```markdown
# Feature: Bulk invoice export

## Summary
Finance currently exports invoices one at a time. This adds a bulk export so
an admin can retrieve many invoices in a single action for reconciliation.

## Actors
- Finance admin (has export permission)
- Standard user (no export access)

## Functional Requirements

### Export selection
**FR-01** — The system must allow a finance admin to select a date range and
one or more invoice statuses (paid, unpaid, overdue) before exporting.
  - *Acceptance criteria:* Given a date range and at least one status is
    selected, the "Export" action becomes available; given no status is
    selected, it remains disabled.

**FR-02** — The system must limit a single export to invoices within a
24-month range.
  - *Acceptance criteria:* Selecting a range wider than 24 months shows a
    validation message and blocks the export until the range is narrowed.

### Export delivery
**FR-03** — The system must notify the finance admin when the export is
ready, rather than requiring them to wait on the page.
  - *Acceptance criteria:* For an export of any size, the admin can navigate
    away after starting it and still receive a completion notification.

**FR-04** — The system must restrict bulk export to users with the finance
admin role.
  - *Acceptance criteria:* A standard user does not see the export action;
    attempting the action directly (e.g. a stale link) is rejected.

## Non-Functional Requirements
**NFR-01** — An export of up to 50,000 invoices must complete within 10 minutes.
**NFR-02** — Exported files must be retained and downloadable for 7 days,
then removed.

## Business Rules & Edge Cases
- An export containing zero matching invoices still completes and produces
  an empty file with headers, rather than failing silently.
- If an invoice is modified after an export starts but before it finishes,
  the export reflects the invoice's state at the time the export began.

## Out of Scope
- Scheduling recurring/automatic exports (may be a future phase).
- Exporting formats other than the one currently used for single exports.

## Assumptions & Open Questions
- Assumed the existing single-invoice export file format is reused as-is;
  confirm with the product owner if a different layout is expected.
- Open: should a finance admin be able to cancel an export in progress?
```

---

## Format C: Use cases

Best for a multi-step or branching interaction where the paths matter more than a flat list would show.

```markdown
# Feature: Return authorization workflow

## Summary
Customers can currently request a return, but there's no structured approval
step for the warehouse team. This adds an authorization workflow between
request and refund.

## Actors
- Customer (requests the return)
- Warehouse reviewer (approves or rejects the request)
- System (issues the refund once goods are received)

## Use Case UC-01: Customer requests a return

**Preconditions:** Customer has a delivered order less than 30 days old.

**Main flow:**
1. Customer selects an order and chooses "Request return."
2. Customer selects the item(s) and a reason from a fixed list.
3. System creates a return request in "Pending review" status and notifies
   the warehouse reviewer.

**Alternate flows:**
- 2a. Order is older than 30 days: the "Request return" option is not
  available; customer sees the return window has closed.
- 2b. Item was marked final-sale at purchase: that item cannot be selected
  for return.

**Postcondition:** A return request exists in "Pending review" status,
visible to both the customer and the warehouse reviewer.

**Acceptance criteria (FR-01):**
- Given an eligible order, a return request can be created and is visible
  to the customer as "Pending review" immediately after submission.
- Given a final-sale item, it cannot be included in a return request.

## Use Case UC-02: Warehouse reviewer decides on the request

**Preconditions:** A return request exists in "Pending review" status.

**Main flow:**
1. Reviewer opens the request and marks it "Approved."
2. System notifies the customer with return shipping instructions.
3. Once the returned item is received and logged, system issues the refund.

**Alternate flows:**
- 1a. Reviewer marks it "Rejected" with a required reason: customer is
  notified with the reason, no shipping instructions are sent.
- 3a. Received item does not match what was authorized (wrong item, damaged
  beyond the stated reason): reviewer can flag it, which pauses the refund
  and re-notifies the customer instead of auto-refunding.

**Postcondition:** Request is in a terminal state (refunded, rejected, or
flagged for manual resolution).

**Acceptance criteria (FR-02):**
- Given an approved request and a received, matching item, a refund is
  issued automatically without further reviewer action.
- Given a rejected request, no shipping instructions or refund are ever sent.
```

---

## Shared sections (use with any format)

These accompany the chosen structure above, not replace it.

```markdown
## Business Rules & Edge Cases
- [Validation rules, boundary values, conflict handling not tied to one
  specific requirement]

## Non-Functional Requirements
**NFR-01** — [performance / security / accessibility / scalability constraint,
stated as an observable requirement, not an implementation]

## Out of Scope
- [What this explicitly does not cover]

## Assumptions & Open Questions
- [What was assumed while drafting, and what's still unresolved]
```