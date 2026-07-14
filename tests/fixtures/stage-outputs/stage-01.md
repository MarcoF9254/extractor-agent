# Engineering Knowledge Extraction — Stage 1

依據 Specification v1.0.1 執行：本輸出只抽取可跨專案重用的工程知識，不整理專案進度或一次性細節。規格要求每項知識必須可追溯至本 Stage 的實際決策、爭議或取捨，並排除 project progress、commit history、一次性 workaround 等內容。

---

## Engineering Principles

### Contract Before Implementation

**Principle** — 會被多個模組依賴的輸出格式、資料結構、狀態值與錯誤格式，應先被明確定義，再進入實作。

**Why** — 本 Stage 多次出現「先定 schema / output contract / rule definition，再寫 validator」的判斷。原因是 contract 一旦未定，後續 implementation、test、review 都會各自猜測，造成 drift。

**Trade-offs** —
獲得：一致性、可測試性、後續工具容易整合。
犧牲：早期進度較慢，需要先花時間討論格式與邊界。

**When NOT to use** — 快速丟棄型 prototype，或目標只是探索可行性而非長期維護。

**Related Concepts** — Contract-first development, schema design, interface stability, validation pipeline.

> **Metadata (Audit Only)**
>
> * Source: Stage 1
> * Evidence: 多次先定 output contract、schema、exit code，再調整 validator implementation。
> * Observation Count: 5
> * Confidence: High

---

### Separate Structural Validity from Business Correctness

**Principle** — 結構驗證與業務規則驗證應分層處理；前者檢查 shape / type / required fields，後者檢查 workflow、語意風險與 participant-facing correctness。

**Why** — Stage 中明確區分 schema validation 與 business validation，並指出 valid JSON 不代表內容可用。此分離令每層責任清晰，避免 schema 被塞入過多業務邏輯。

**Trade-offs** —
獲得：模組清晰、錯誤定位容易、測試可分層。
犧牲：需要多一層 validator 與 output aggregation。

**When NOT to use** — 極細型資料流程，且所有檢查都只是單純 type / required field。

**Related Concepts** — Separation of concerns, layered validation, business rule engine, data contracts.

> **Metadata (Audit Only)**
>
> * Source: Stage 1
> * Evidence: 針對 schema validator、business validator、QA agent 的責任分離討論。
> * Observation Count: 4
> * Confidence: High

---

### Unknown Information Should Stay Explicit

**Principle** — 抽取或轉換資料時，缺失、不清楚或需人工判斷的資訊應被明確標記，而不是由系統推測或自動補完。

**Why** — 本 Stage 多次強調不要 invent details、不要把 uncertainty 靜默修復，並將 uncertain fields 作為 workflow 的正式訊號。這對面向人使用的資料尤其重要。

**Trade-offs** —
獲得：降低錯誤資訊流入下游的風險，提高 QA 可追蹤性。
犧牲：輸出可能較不完整，需要 Human Review。

**When NOT to use** — 當業務場景允許 probabilistic approximation，且下游明確接受推測值。

**Related Concepts** — Source fidelity, uncertainty tracking, human review, QA workflow.

> **Metadata (Audit Only)**
>
> * Source: Stage 1
> * Evidence: 多次要求 missing / ambiguous fields 要進入 uncertainty，而非由 validator 或 agent 修復。
> * Observation Count: 5
> * Confidence: High

---

## Architecture Patterns

### Validation Pipeline with Human Review Gate

**Principle** — 對高風險資料流程，可採用「自動抽取 → 結構驗證 → 業務驗證 → QA → Human Review」的 staged pipeline。

**Why** — 本 Stage 中，Human Review 被定義為架構一部分，而不是例外處理。原因是現實文件常有 layout、footnote、table ambiguity，自動化不應假裝完全解決。

**Trade-offs** —
獲得：風險分層、責任清楚、人工只處理真正需要判斷的 case。
犧牲：流程較長，不適合追求即時輸出的低風險任務。

**When NOT to use** — 低風險、低影響、錯誤可容忍的 batch processing。

**Related Concepts** — Human-in-the-loop, staged validation, QA gate, publication workflow.

> **Metadata (Audit Only)**
>
> * Source: Stage 1
> * Evidence: 多次將 Human Review 放在 validation / QA 之後作為正式 handoff。
> * Observation Count: 4
> * Confidence: High

---

### Rule Engine as Engine + Rule Library

**Principle** — Rule engine 應分成「執行引擎」與「規則庫」；引擎負責載入與執行，規則庫負責定義可審核的判斷。

**Why** — 本 Stage 明確討論到 validator 不應硬寫所有規則，而應讓 rule definitions、rule modules、engine 分離。這使新增規則時不需重寫核心 engine。

**Trade-offs** —
獲得：可擴充、可 review、可逐條測試。
犧牲：初期結構較多，需要設計 registry / rule interface。

**When NOT to use** — 規則數量極少且不會成長的簡單 script。

**Related Concepts** — Rule registry, plugin architecture, modular validators, business rules.

> **Metadata (Audit Only)**
>
> * Source: Stage 1
> * Evidence: 討論 rule library、validator scaffold、rule module 分離。
> * Observation Count: 3
> * Confidence: High

---

## Development Workflow

### Review Before Commit

**Principle** — Commit 應代表經過 review、測試、可回到的工程 checkpoint，而不是暫存未審核工作的容器。

**Why** — 本 Stage 多次選擇「先不 commit」，等待 architecture review、Claude review 或 pytest 完成後才 commit。這令 Git history 成為可信紀錄。

**Trade-offs** —
獲得：乾淨 history、容易 rollback、review burden 低。
犧牲：需要管理 uncommitted work，工作節奏較慢。

**When NOT to use** — 個人快速 spike，且明確會 squash 或丟棄。

**Related Concepts** — Atomic commits, code review, checkpointing, Git hygiene.

> **Metadata (Audit Only)**
>
> * Source: Stage 1
> * Evidence: 多次要求指定 files staging、review 後才 commit、未 review scaffold 不 commit。
> * Observation Count: 6
> * Confidence: High

---

### Role-Based AI Collaboration

**Principle** — 多個 AI assistant 應按能力分工，而不是做相同 review：一個管架構與整合，一個負責實作，一個負責 edge cases / code review。

**Why** — Stage 中多次比較 ChatGPT、Codex、Claude 的分工，並發現不同模型抓到不同類型問題，例如 architecture risk、execution risk、implementation gaps。

**Trade-offs** —
獲得：review coverage 更廣，缺陷更早暴露。
犧牲：協作成本較高，需要 handoff 與 context 管理。

**When NOT to use** — 極小修改、低風險文件改動，或 review 成本高於錯誤成本。

**Related Concepts** — Multi-agent workflow, AI pair programming, code review, architecture review.

> **Metadata (Audit Only)**
>
> * Source: Stage 1
> * Evidence: 多次確立 ChatGPT / Codex / Claude 分工與何時需要 Claude review。
> * Observation Count: 5
> * Confidence: High

---

## Testing Strategy

### Test PASS, FAIL, and ERROR Paths Separately

**Principle** — CLI validator 或 automation tool 不應只測成功路徑，應分別測 validation pass、validation fail、tool execution error。

**Why** — 本 Stage 中，review 指出只測 PASS 不能證明 fail output、exit code、error handling 正確，於是補測 fail path 與 missing-file error path。

**Trade-offs** —
獲得：更可靠的 automation contract，更少 hidden failure。
犧牲：需要額外 fixtures 與 subprocess tests。

**When NOT to use** — 一次性手動工具，且不會被 runner、CI 或其他 automation 調用。

**Related Concepts** — Negative testing, CLI testing, exit codes, regression tests.

> **Metadata (Audit Only)**
>
> * Source: Stage 1
> * Evidence: 由 PASS-only 測試改為 PASS / FAIL / ERROR 三路徑驗證。
> * Observation Count: 3
> * Confidence: High

---

### Test Infrastructure Before Rule Complexity

**Principle** — 在實作多條互相影響的規則前，先建立測試基礎與 smoke tests。

**Why** — Stage 中明確決定在 business rules 前先建立 pytest，因為 rule engine 容易在後續修改時互相影響。

**Trade-offs** —
獲得：後續規則可逐條加入並回歸測試。
犧牲：初期功能進展較慢。

**When NOT to use** — 規則極少、無需長期維護、沒有 regression 風險。

**Related Concepts** — Test scaffolding, regression baseline, smoke tests, rule testing.

> **Metadata (Audit Only)**
>
> * Source: Stage 1
> * Evidence: 決定先建立 pytest，再逐條實作 business rules。
> * Observation Count: 3
> * Confidence: High

---

## Repository & Git Practices

### Treat Line Ending Policy as Repository Infrastructure

**Principle** — 跨平台專案應早定 line ending policy，避免 CRLF / LF 噪音污染 diff。

**Why** — 本 Stage 真實出現 line-ending noise，並導致多個文件顯示 modified。最終透過 repository-level policy 清理。

**Trade-offs** —
獲得：diff 乾淨、review 準確、跨機器一致。
犧牲：需要一次 housekeeping commit，並可能影響既有檔案顯示。

**When NOT to use** — 單機、短期、完全不使用 Git review 的 disposable project。

**Related Concepts** — `.gitattributes`, cross-platform development, diff hygiene, Git normalization.

> **Metadata (Audit Only)**
>
> * Source: Stage 1
> * Evidence: CRLF noise 被確認後，先清理再進下一 milestone。
> * Observation Count: 2
> * Confidence: High

---

### Review Packages Must Preserve Folder Structure

**Principle** — 給 reviewer 或 AI 的 zip / snapshot 應保留原始資料夾結構，不應 flatten。

**Why** — 本 Stage 發生 flatten zip 導致同名文件互相覆蓋，reviewer 需要靠 import path 反推結構。這是實際資料遺失風險。

**Trade-offs** —
獲得：避免同名 collision，保留 context 與 import path。
犧牲：打包指令稍微複雜。

**When NOT to use** — 只分享單一檔案或少量不重名文件。

**Related Concepts** — Review package, artifact hygiene, file structure, reproducibility.

> **Metadata (Audit Only)**
>
> * Source: Stage 1
> * Evidence: zip flatten 後根目錄文件與子資料夾文件撞名，需重新打包。
> * Observation Count: 2
> * Confidence: High

---

## Pitfalls & Lessons Learned

### Silent Defaults Can Hide Rule Authoring Errors

**Principle** — Rule engine 不應過度用 default values 補齊 finding object，否則 rule 實作漏欄位時可能不會 fail fast。

**Why** — Scaffold review 指出，如果 missing rule_id / severity 被自動補成 placeholder，bug 會靜默流入 output。

**Trade-offs** —
獲得：早期發現規則實作錯誤。
犧牲：rule author 需要更嚴格遵守 contract。

**When NOT to use** — 探索型工具，故意容忍 incomplete findings。

**Related Concepts** — Fail fast, output contract validation, rule authoring, defensive programming.

> **Metadata (Audit Only)**
>
> * Source: Stage 1
> * Evidence: Scaffold review 明確指出 normalize default 可能掩蓋 missing fields。
> * Observation Count: 1
> * Confidence: Medium

---

### Top-Level Input Shape Must Be Classified Explicitly

**Principle** — Valid JSON 但 top-level shape 錯誤時，應明確定義它是 validation failure 還是 tool execution error。

**Why** — Review 中指出 object-vs-array 這類 case 會影響 exit code contract；如果不定義，runner 無法可靠判斷是資料錯還是工具錯。

**Trade-offs** —
獲得：automation 行為可預測。
犧牲：需要更細緻的 error taxonomy。

**When NOT to use** — 沒有 CLI、runner、CI 或自動化整合的手動工具。

**Related Concepts** — Error taxonomy, exit code contract, CLI design, validation semantics.

> **Metadata (Audit Only)**
>
> * Source: Stage 1
> * Evidence: Claude review 提醒 valid JSON but not array 的 exit-code decision 需記錄。
> * Observation Count: 1
> * Confidence: Medium

---

# Rejected Decisions

## Commit Unreviewed Scaffold

**Rejected Because** — Scaffold 會成為後續規則的架構基礎，未經 review 便 commit 會把不穩定 interface 固化。

**Would Become Valid If** — 明確標記為 disposable spike，或將來會 squash / replace。

---

## Keep Two Validator Output Formats

**Rejected Because** — 會削弱 output contract 作為 shared interface 的價值，令 downstream runner 需要處理多套格式。

**Would Become Valid If** — 已有外部 consumer 依賴 legacy format，且不能立即破壞兼容。

---

## Delay Testing Until All Rules Are Written

**Rejected Because** — 多條規則容易互相影響，遲測會令 bug source 難定位。

**Would Become Valid If** — 規則只是短期 throwaway script，沒有長期維護目標。

---

# Anti-patterns

## Broad Git Staging by Habit

Practice to avoid — 未確認狀態下使用 broad staging。

Why harmful — 容易把 unrelated files、temporary artifacts、generated files 一併 commit，破壞 commit 粒度。

---

## Treating README as a Dumping Ground

Practice to avoid — 將所有 schema details、workflow details、implementation notes 塞入 README。

Why harmful — README 會失去 project homepage 功能，反而降低 onboarding 效率。

---

## Flattening Review Artifacts

Practice to avoid — 將整個 repo 壓成平面檔案集合。

Why harmful — 同名文件會 collision，資料夾語意與 import path 會消失。

---

# Decision Heuristics

## Contract Change Heuristic

```text
New shared behavior needed
↓
Define contract
↓
Compare against existing implementation
↓
If mismatch:
    retrofit implementation
    OR explicitly document compatibility
↓
Test all behavior paths
↓
Commit only after contract and implementation agree
```

## Rule Engine Heuristic

```text
Define rule behavior in human-readable spec
↓
Stabilize engine interface
↓
Add rule module
↓
Add direct unit tests for rule
↓
Run full regression
↓
Review
↓
Commit
```

## Milestone Closure Heuristic

```text
Feature complete
↓
Tests pass
↓
Working tree checked
↓
Housekeeping resolved
↓
Documentation / decisions updated
↓
Commit and push
↓
Start next milestone
```
