# Engineering Knowledge Extraction

## Engineering Principles

### Governance Precedes Architecture Artifacts

**Principle**

當多份架構文件互相引用時，應先建立 Governance（治理規則），再建立引用 Governance 的架構文件。

**Why**

若治理規則仍存在於對話而未成為正式 artifact，後續文件將引用不存在或未批准的內容，造成自我依賴與文件漂移。

**Trade-offs**

優點：

* 建立穩定的引用基礎。
* 降低後續文件重寫成本。
* 保持 Single Source of Truth。

代價：

* 初期文件產出速度較慢。
* 需要先完成治理文件。

**When NOT to use**

* 小型一次性 prototype。
* 沒有長期維護需求的專案。

**Related Concepts**

* Single Source of Truth
* Architecture Governance
* Documentation Dependency
* Specification First

> **Metadata (Audit Only)**
>
> * Source: Current Stage
> * Evidence: 多次討論是否先寫 extraction-boundary 或 governance，最後一致決定 Governance 優先。
> * Observation Count: 6
> * Confidence: High

---

### Format Capability Must Be Separated from Source Authority

**Principle**

系統可支援哪些輸入格式，與哪些資料具有權威性（Authoritative Source）必須視為兩個獨立架構決策。

**Why**

混淆兩者容易在文件中無意間提前決定尚未批准的 Authority Policy。

**Trade-offs**

優點：

* 避免隱性 Architecture Decision。
* 保持決策可審查。

代價：

* 文件需多一層說明。
* 需要額外管理 Pending Decisions。

**When NOT to use**

* Source Authority 永遠固定且不存在選擇時。

**Related Concepts**

* Source Authority
* Architecture Decision
* Boundary Contract
* Separation of Concerns

> **Metadata (Audit Only)**
>
> * Source: Current Stage
> * Evidence: Claude 指出「Format ≠ Authority」，經討論後提升為正式 Architecture Principle。
> * Observation Count: 5
> * Confidence: High

---

### Evidence Supports Correctness; Authority Approves Adoption

**Principle**

證據可以支持某項政策是否合理，但不能自動使其成為正式政策；涉及 Authority 的決策仍需人工批准。

**Why**

觀察到現象存在，不代表應採用某種解法。

**Trade-offs**

優點：

* 防止由樣本直接推導政策。
* 保持 Architecture Governance 的決策權限。

代價：

* 決策流程增加一步 Approval。

**When NOT to use**

* 完全自動生成且無治理需求的實驗性系統。

**Related Concepts**

* Evidence-based Engineering
* Human Approval
* Governance
* ADR

> **Metadata (Audit Only)**
>
> * Source: Current Stage
> * Evidence: 多輪討論 Principle 7 與 Authority Decision 的關係。
> * Observation Count: 4
> * Confidence: High

---

## Architecture Patterns

### Governance as a Cross-cutting Meta-layer

**Principle**

Governance 應視為約束整個工程流程的 Meta-layer，而非工作流程中的第一個階段。

**Why**

若畫成線性 Pipeline，容易誤導為「Governance 完成即可結束」，忽略其持續約束 Architecture、Specification、Implementation 與 Validation。

**Trade-offs**

優點：

* 清楚區分流程與治理。
* 避免 Governance 被誤實作為 Runtime Component。

代價：

* 需要額外說明文件定位。

**When NOT to use**

* 幾乎沒有架構文件的極小型專案。

**Related Concepts**

* Meta-layer
* Architecture Governance
* Workflow
* Cross-cutting Concern

> **Metadata (Audit Only)**
>
> * Source: Current Stage
> * Evidence: 多輪討論 Governance 是否屬於 Workflow。
> * Observation Count: 4
> * Confidence: High

---

### Boundary Documents Define Contracts, Not Components

**Principle**

Boundary 文件應描述 Contract 與 Scope，而非引入新的 Runtime Component。

**Why**

將 Boundary 畫成 Component 容易導致後續實作者新增不存在的 Agent 或 Orchestrator。

**Trade-offs**

優點：

* 保持 Architecture 穩定。
* 避免 Scope Creep。

代價：

* 文件需刻意加入 Non-goals。

**When NOT to use**

* Boundary 本身就是 Runtime Module 時。

**Related Concepts**

* Contract-first
* Boundary
* Runtime Architecture
* Non-goals

> **Metadata (Audit Only)**
>
> * Source: Current Stage
> * Evidence: Extraction Boundary 是否代表新 Runtime Component 的討論。
> * Observation Count: 4
> * Confidence: High

---

## Development Workflow

### Approved Artifacts Are the Only Reference Targets

**Principle**

只有已批准並提交至 Repository 的 Artifact 可以成為其他文件的引用對象。

**Why**

避免引用尚未存在、尚未批准或僅存在於聊天內容中的規則。

**Trade-offs**

優點：

* 消除循環依賴。
* 提高文件一致性。

代價：

* 必須控制文件建立順序。

**When NOT to use**

* 一次性臨時設計討論。

**Related Concepts**

* Single Source of Truth
* Artifact-first
* Documentation Dependency
* Approval Workflow

> **Metadata (Audit Only)**
>
> * Source: Current Stage
> * Evidence: 決定 Governance commit 後才開始 Extraction Boundary。
> * Observation Count: 4
> * Confidence: High

---

### Incremental Documentation Review

**Principle**

大型架構文件應採用 Patch Review，而非每輪重寫。

**Why**

Patch Review 可降低 Drift、保留已批准內容，並使 Reviewer 聚焦於真正變更。

**Trade-offs**

優點：

* Review 成本低。
* 文件穩定性高。

代價：

* 初始文件品質需足夠。

**When NOT to use**

* 文件方向已完全錯誤時。

**Related Concepts**

* Incremental Review
* Patch
* Documentation Evolution
* Change Isolation

> **Metadata (Audit Only)**
>
> * Source: Current Stage
> * Evidence: Governance 文件多次要求「Patch only，不 Rewrite」。
> * Observation Count: 3
> * Confidence: High

---

## Repository & Git Practices

### Architecture Evidence Should Be Distinguished from Test Fixtures

**Principle**

Architecture Review 使用的 Evidence Corpus 應與 Regression Fixtures 明確分離。

**Why**

Evidence 用於發現問題；Fixture 用於驗證既定行為。兩者語義不同。

**Trade-offs**

優點：

* 降低 Repository 誤用。
* 提高資料語義清晰度。

代價：

* Repository 結構稍微增加。

**When NOT to use**

* 沒有 Architecture Review Corpus 的專案。

**Related Concepts**

* Examples
* Test Fixtures
* Corpus
* Repository Semantics

> **Metadata (Audit Only)**
>
> * Source: Current Stage
> * Evidence: `examples` 與 `fixtures` 的命名與用途討論。
> * Observation Count: 3
> * Confidence: High

---

## AI Collaboration Patterns

### Separate Author, Reviewer and Implementer Roles

**Principle**

AI 協作時，作者、獨立 Reviewer 與實作者應保持角色分離。

**Why**

角色分離降低 Authorship Bias，比依賴單一模型自我檢查更有效。

**Trade-offs**

優點：

* 更容易發現隱性假設。
* Architecture Decision 更穩健。

代價：

* Review 流程增加。

**When NOT to use**

* 一次性個人實驗。

**Related Concepts**

* Independent Review
* Authorship Bias
* Governance
* Role Separation

> **Metadata (Audit Only)**
>
> * Source: Current Stage
> * Evidence: 多次討論 GPT、Claude、Codex 的角色定位。
> * Observation Count: 6
> * Confidence: High

---

### Implementation Agents Should Render, Not Invent

**Principle**

Implementation Agent 應根據已批准 Specification 產出成果，而非新增 Architecture Policy 或 Governance Rule。

**Why**

避免 Implementation 階段越權產生新的設計決策。

**Trade-offs**

優點：

* 保持 Architecture Authority。
* 減少 Scope Creep。

代價：

* Human Review 責任增加。

**When NOT to use**

* 明確授權 AI 參與設計探索時。

**Related Concepts**

* Renderer
* Architecture Authority
* Scope Control
* Human Approval

> **Metadata (Audit Only)**
>
> * Source: Current Stage
> * Evidence: 多次強調 Codex 為 Renderer，不是 Co-author。
> * Observation Count: 5
> * Confidence: High

---

## Decision Frameworks

### Promote Repeated Review Findings into Governance

**Principle**

當同一類問題在多輪 Review 中反覆出現時，應提升為 Governance Rule，而非只修正當前文件。

**Why**

可將一次性修補轉化為長期可重用的工程知識。

**Trade-offs**

優點：

* 防止相同問題重複發生。
* 累積 Engineering Playbook。

代價：

* Governance 文件可能持續成長，需要控制範圍。

**When NOT to use**

* 僅出現一次且缺乏證據支持的問題。

**Related Concepts**

* Continuous Improvement
* Governance
* Lessons Learned
* Institutional Knowledge

> **Metadata (Audit Only)**
>
> * Source: Current Stage
> * Evidence: Format ≠ Authority、Evidence vs Authority 等均由 Review 提升為 Principle。
> * Observation Count: 4
> * Confidence: High

---

# Rejected Decisions

### Introduce a Runtime Ingestion Component

**Why rejected**

Evidence 僅支持需要定義邊界（Contract），不足以支持新增 Runtime Component。

**When it becomes valid**

若未來確實需要獨立執行流程或協調邏輯，且有足夠證據支持。

---

### Reference Conversation Content Directly

**Why rejected**

Conversation 並非正式 Artifact，不符合 Single Source of Truth。

**When it becomes valid**

當內容已轉化為正式、已批准的 Repository Artifact。

---

# Anti-patterns

### Leting Documentation Implicitly Decide Pending Architecture

**Why harmful**

文件措辭可能在無意中將 Pending Decision 變成既定政策，削弱 Governance。

---

### Treating Observational Evidence as Normative Policy

**Why harmful**

觀察到現象存在，不代表應採取特定解法，容易造成錯誤的架構推導。

---

# Decision Heuristics

### Governance-first Architecture Evolution

```text
Evidence
        ↓
Architecture Discussion
        ↓
Governance Rule
        ↓
Architecture Document
        ↓
Specification
        ↓
Implementation
        ↓
Independent Review
        ↓
Approval
        ↓
Repository Artifact
```

### Architecture Decision Escalation

```text
Repeated Review Finding
        ↓
Generalizable Principle
        ↓
Governance Candidate
        ↓
Human Approval
        ↓
Permanent Governance Rule
```
