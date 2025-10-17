# Research Report: Logics of Formal Inconsistency (LFIs)

## 1. Introduction

This report summarizes the findings of a research investigation into Logics of Formal Inconsistency (LFIs). The goal of this research was to gain a foundational understanding of LFIs and their relationship to intuitionistic logic, in order to inform the development of a paraconsistent universal computing model based on an LFI variant of intuitionistic linear logic.

## 2. Key Concepts of LFIs

Logics of Formal Inconsistency (LFIs) are a family of paraconsistent logics that aim to control the explosive power of contradictions in classical logic. The key features of LFIs are:

*   **Rejection of the Principle of Explosion:** In classical logic, the principle of explosion (ex contradictione quodlibet) states that from a contradiction, anything follows. LFIs reject this principle, allowing for contradictions to exist in a system without leading to triviality (where every statement is provable).

*   **Consistency Operator:** LFIs introduce a "consistency operator" (often denoted by `∘`) into the object language. This operator allows the logic to express the consistency of a statement. For example, `∘A` means that the statement `A` is consistent.

*   **Gentle Explosion:** While LFIs reject the principle of explosion in general, they often include a "gentle explosion" principle, which states that from a contradiction *and* a statement of consistency, anything follows. For example, from `A`, `¬A`, and `∘A`, anything can be derived. This allows the logic to recover classical reasoning when it is safe to do so.

*   **Epistemological Interpretation:** LFIs can be interpreted as an epistemological tool for reasoning about inconsistent information. They do not necessarily require a commitment to "dialetheism" (the belief that contradictions can be true). Instead, they provide a framework for reasoning about systems that may contain contradictory information, such as databases or knowledge bases.

## 3. LFIs and Intuitionistic Logic

A key finding of this research is that LFIs can be built on top of intuitionistic logic. Specifically, the positive fragment of intuitionistic logic can be used as a foundation for LFIs. This is a significant result for this project, as it provides a clear path forward for creating an LFI variant of intuitionistic linear logic.

The combination of LFIs and intuitionistic logic is a powerful one. Intuitionistic logic is a constructive logic, which means that it is well-suited for reasoning about computation. By combining it with LFIs, we can create a logic that is both constructive and paraconsistent. This is exactly what is needed for a paraconsistent universal computing model.

## 4. Conclusion

This research has provided a solid foundation for the next steps of this project. I now have a clear understanding of the key concepts of LFIs and their relationship to intuitionistic logic. I will now proceed with the implementation of the LFI ILL language, with the goal of creating a paraconsistent universal computing model.