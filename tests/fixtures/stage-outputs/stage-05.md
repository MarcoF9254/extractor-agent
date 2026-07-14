# Engineering Knowledge Extraction

## Engineering Principles

### Evidence-Driven Architecture Evolution

**Principle**

架構演化應由已證實的證據驅動，而非為推測中的未來需求提前抽象化。

**Why**

過早引入抽象層會增加系統複雜度與維護成本，而沒有足夠證據支持的設計往往難以驗證其價值。

**Trade-offs**

* Gains

  * 保持架構簡潔
  * 降低維護成本
  * 避免不必要 abstraction
* Sacrifices

  * 日後若需求擴大，可能需要再次重構

**When NOT to use**

當多個已驗證的使用案例已持續突破現有模型，且已有足夠證據證明抽象層能降低整體複雜度時。

**Related Concepts**

* YAGNI
* Evolutionary Architecture
* Evidence-based Design
* Incremental Refactoring

**Metadata (Audit Only)**

* Source: Current Stage
* Evidence: 討論是否 redesign 為 Canonical Content Model，最後因證據不足而維持現有 Pipeline。
* Observation Count: 4
* Confidence: High

---

### Separate Evidence Collection from Architectural Change

**Principle**

當發現新的系統現象時，可先定義研究邊界與分類方式，而不是立即修改核心架構。

**Why**

許多架構變更真正需要的是更好的問題定義，而不是更大的設計。

**Trade-offs**

* Gains

  * 降低錯誤設計風險
  * 保留未來演化空間
* Sacrifices

  * 短期內可能需要接受部分限制

**When NOT to use**

當現有架構已無法支撐現有需求，而非僅是未知需求時。

**Related Concepts**

* Domain Discovery
* Boundary Definition
* Architecture Governance
* Incremental Design

**Metadata (Audit Only)**

* Source: Current Stage
* Evidence: 將焦點由 Content Model redesign 轉為研究 Extraction Boundary。
* Observation Count: 2
* Confidence: High

---

## Architecture Patterns

### Preserve a Stable Processing Pipeline Until Boundaries Change

**Principle**

只要資料流仍符合既定責任分界，優先維持 Pipeline 穩定，而非重新設計整體流程。

**Why**

Pipeline 穩定性通常比理論上的模型完整性更重要。

**Trade-offs**

* Gains

  * 降低 Regression 風險
  * 保持模組責任清晰
* Sacrifices

  * 暫時接受部分模型限制

**When NOT to use**

當 Pipeline 已持續違反其原始責任或需要大量例外處理時。

**Related Concepts**

* Stable Interfaces
* Separation of Concerns
* Pipeline Architecture
* Architectural Stability

**Metadata (Audit Only)**

* Source: Current Stage
* Evidence: 最終決定保留既有 Extract → Validation → QA Pipeline。
* Observation Count: 3
* Confidence: High

---

## AI Collaboration Patterns

### Use Independent AI Review to Challenge Architectural Assumptions

**Principle**

重大架構決策應接受獨立 AI review，以驗證假設是否真正由證據支持。

**Why**

不同模型容易從不同角度發現推論跳躍、證據不足或過度設計。

**Trade-offs**

* Gains

  * 降低 confirmation bias
  * 提高決策可信度
* Sacrifices

  * 增加 review 時間
  * 可能延後實作

**When NOT to use**

小型、低風險或可快速回滾的變更。

**Related Concepts**

* Multi-model Review
* Design Review
* Evidence Validation
* Critical Evaluation

**Metadata (Audit Only)**

* Source: Current Stage
* Evidence: 重新檢視實際資料並結合 Claude review 後推翻原先 redesign 傾向。
* Observation Count: 2
* Confidence: Medium

---

## Decision Frameworks

### Validate Architecture Decisions Through an Evidence Escalation Process

**Problem**

出現可能需要改變架構的新案例。

↓

**Alternatives**

* 立即 redesign
* 保持現況
* 擴充研究邊界

↓

**Trade-offs**

評估證據是否足以支持新增抽象層。

↓

**Decision**

若證據不足，維持現有架構，同時定義新的研究邊界。

↓

**Evidence**

以實際資料與獨立 review 驗證，而非依直覺推論。

↓

**Implementation**

只有在累積足夠案例後才進行架構演化。

---

## Rejected Decisions

### Immediate Canonical Content Model Redesign

**Why rejected**

目前案例不足，無法證明全面 Content Model 能帶來長期收益，屬於過早抽象化。

**Would become valid when**

* 已出現多種類型內容持續突破現有模型。
* 新抽象層能明顯降低系統複雜度。
* 有足夠 evidence 支持長期維護效益。

---

## Anti-patterns

### Designing for Hypothetical Future Requirements

**Practice to avoid**

因單一或少量案例便重新設計整體架構。

**Why it is harmful**

容易增加系統複雜度，形成難以維護的抽象層，且缺乏足夠證據驗證其必要性。
