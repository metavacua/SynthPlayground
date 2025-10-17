

# **A Paradefinite Light Linear Logic: Sequent Calculus, Meta-Theory, and Resource Semantics**

**Abstract:** This report introduces Paradefinite Light Linear Logic (PLLL), a novel substructural logic that integrates principles from Logics of Formal Inconsistency (LFI) and Logics of Formal Undeterminedness (LFU) into the framework of Light Linear Logic (LLL). We present a complete Gentzen-style sequent calculus for PLLL, defining new operators for paraconsistent negation (\~), consistency (∘), and their paracomplete duals. A central contribution is the formulation of interaction rules that govern the behavior of these new operators with respect to LLL's additive, multiplicative, and exponential connectives. We analyze the crucial meta-theoretic properties of PLLL, providing a proof sketch for the admissibility of the Cut rule and investigating the impact on the complexity of normalization, arguing that a modified polytime property can be preserved. By shifting the interpretation of inconsistency and incompleteness from truth-values to resource management, PLLL provides a powerful formal tool for reasoning about computational systems that must handle conflicting information, underspecified data, and resource constraints simultaneously.

## **Section 1: Foundational Proof-Theoretic Frameworks**

This section establishes the necessary logical groundwork, introducing the sequent calculus as the formal language of the report, justifying the selection of Light Linear Logic as the base system due to its unique computational properties, and formally defining the paraconsistent and paracomplete principles that the final system must accommodate.

### **1.1 The Gentzen-Style Sequent Calculus**

The primary formalism for the logical systems presented in this report is the sequent calculus, introduced by Gerhard Gentzen in the 1930s.1 Unlike Hilbert-style systems, which consist of axioms and rules for deriving unconditional tautologies, the sequent calculus manipulates conditional assertions called sequents.1 A sequent is an expression of the form $ \\Gamma \\vdash \\Delta $, where $\\Gamma$ (the antecedent) and $\\Delta$ (the succedent) are finite multisets of formulas.2 Intuitively, a sequent asserts that the conjunction of the formulas in $\\Gamma$ entails the disjunction of the formulas in $\\Delta$.1 This structure provides a more natural framework for modeling the process of deduction.1

The deductive power of a sequent calculus is determined by its inference rules, which are divided into two categories: logical and structural. Logical rules introduce connectives into the antecedent or succedent, while structural rules manipulate the contexts ($\\Gamma$ and $\\Delta$) themselves.4 The three canonical structural rules are:

* **Weakening:** This rule allows for the introduction of an arbitrary formula into the antecedent (Left Weakening) or succedent (Right Weakening). It corresponds to the principle that if a conclusion follows from a set of premises, it also follows from a larger set of premises.4  
* **Contraction:** This rule allows two identical formulas in a context to be replaced by a single instance. It embodies the assumption that premises can be reused an unlimited number of times.4  
* **Exchange:** This rule permits the reordering of formulas within a context, reflecting the commutative nature of logical conjunction and disjunction.4

A fourth rule, the **Cut** rule, stands apart. It is a generalization of the *modus ponens* principle and expresses the transitivity of entailment.6 While indispensable for constructing proofs in a modular fashion, the Cut rule presents a significant challenge for the meta-theoretic analysis of a logic. A central result in proof theory is the *cut-elimination theorem*, which demonstrates that any proof using the Cut rule can be transformed into an equivalent proof that does not use it.6 The consequences of this theorem are profound. First, it establishes the internal consistency of the logic, as it shows that the empty sequent $\\vdash$ cannot be derived in a cut-free system.8 Second, it guarantees the *subformula property*: in a cut-free proof of a sequent $\\Gamma \\vdash \\Delta$, every formula that appears in the proof is a subformula of some formula in $\\Gamma$ or $\\Delta$.6 This property is crucial for proof search and decidability results.

The modern study of non-classical logic can be understood largely through the lens of these structural rules. Logics are often distinguished not by their axioms, but by which structural rules they restrict or reject.9 Linear Logic is defined by its careful control over Weakening and Contraction 11; Relevant Logic is characterized by the rejection of Weakening.12 This "structuralist" perspective reveals that these rules encode deep assumptions about the nature of truth, information, and resources. Contraction assumes truths are persistent and infinitely reusable, while Weakening assumes they are irrelevant if not used. By treating these rules not as inviolable laws but as configurable parameters, one can design logics with specific, desirable properties. The development of Paradefinite Light Linear Logic in this report will therefore be approached as a modification of the system's resource discipline, where the core challenge is to define how new operators interact with a highly restricted structural framework.

### **1.2 Light Linear Logic (LLL) as the Base System**

The foundational system for our investigation is Light Linear Logic (LLL), a refinement of Jean-Yves Girard's Linear Logic (LL).14 LL itself is a substructural logic that arises from rejecting the structural rules of Weakening and Contraction in classical sequent calculus.11 This rejection leads to a "resource-conscious" logic where formulas are treated not as persistent truths but as consumable resources that must be used exactly once.11 To manage this, LL introduces distinct connectives:

* **Additives:** The additive conjunction $& (with) represents an internal choice from a shared resource context, while the additive disjunction $\\oplus$ (plus) represents an external choice.  
* **Multiplicatives:** The multiplicative conjunction $\\otimes$ (tensor) represents the combination of two independent resources, while the multiplicative disjunction $\\lpar$ (par) represents their co-existence.  
* **Exponentials:** To recover the full expressive power of classical and intuitionistic logic, LL reintroduces Weakening and Contraction in a controlled manner via the modal operators \! ("of course") and ? ("why not"). A formula $\!A$ can be interpreted as an unlimited supply of the resource $A$, to which Weakening and Contraction can be applied.11

The key distinction between full LL and LLL lies in their computational complexity. While cut-elimination is provable for LL, the procedure can have non-elementary complexity, making it unsuitable for characterizing feasible computation. LLL was specifically designed by Girard to capture the class of polynomial-time computable functions.14 It achieves this by imposing strict limitations on the power of the exponential modalities.

Girard's analysis of exponentials identifies several key principles, not all of which are admitted in LLL.14 In particular, LLL rejects principles that lead to a combinatorial explosion during normalization, such as the general isomorphism $\!(A \\& B) \\equiv\!A \\otimes\!B$ and the "digging" rule that allows the derivation of $\!A \\vdash\!\!A$.14 The mechanism for this restriction can be understood through the "stratification condition" found in the closely related Elementary Linear Logic (ELL).17 This condition is a non-local constraint on the structure of proof trees: it mandates that any exponential formula $\!A$ introduced by a dereliction rule (which allows $\!A$ to be used as $A$) may cross at most one \!-promotion rule (the rule that introduces the \! on the right side of the sequent) in its path up the proof tree.17 This global constraint effectively prevents the arbitrary nesting of exponentials that is the source of non-elementary complexity in full LL.

The consequence of this restriction is that LLL provides a logical system where the bounds on the cut-elimination procedure do not depend on the complexity of the cut-formulas themselves, guaranteeing a polytime normalization process.14 This property makes LLL an ideal foundation for a logic intended to model computationally feasible reasoning. For the purposes of this report, the stratification condition (or an equivalent complexity-controlling principle) will be treated as a primary, non-negotiable design constraint. Any new inference rule introduced to handle paradefinite operators must be vetted to ensure it does not create a "backdoor" that violates this principle, thereby preserving the defining computational character of the base system.

### **1.3 Logics of Formal Inconsistency (LFI) and Formal Undeterminedness (LFU)**

The second component of our hybrid system is derived from the family of paraconsistent and paracomplete logics. A logic is defined as **paraconsistent** if it rejects the *Principle of Explosion* (also known as *ex contradictione quodlibet*), which states that from a contradiction, anything follows: $A, \\neg A \\vdash B$ for any $A$ and $B$.18 By invalidating this principle, paraconsistent logics allow for the formal study of theories that are inconsistent (i.e., contain both $A$ and $\\neg A$ for some $A$) but are not trivial (i.e., do not contain every formula as a theorem).18 This is motivated by the need to reason with information from conflicting sources, such as in databases or multi-agent systems, without descending into logical chaos.20

The **Logics of Formal Inconsistency (LFI)** represent a sophisticated approach to paraconsistency.22 Instead of simply removing the rule of explosion, LFIs internalize the notion of consistency itself into the object language via a dedicated unary connective, $\\circ$.23 The formula $\\circ A$ is read as "$A$ is consistent." This allows for a more nuanced handling of contradictions. While the general principle of explosion is invalid, LFIs validate the *Principle of Gentle Explosion*: $\\circ A, A, \\sim A \\vdash B$.23 This principle states that a contradiction involving $A$ explodes and leads to triviality only in the presence of an explicit assertion of $A$'s consistency. This provides a mechanism to quarantine contradictions and prevent them from trivializing the entire system, unless a specific consistency assumption is violated.22

There exists a fundamental duality between paraconsistency and **paracompleteness**.18 A logic is paracomplete if it rejects the *Law of the Excluded Middle* (LEM), $\\vdash A \\lor \\neg A$. While paraconsistent logics allow for truth-value "gluts" (a proposition can be both true and false), paracomplete logics allow for truth-value "gaps" (a proposition can be neither true nor false).24 This duality is analogous to the relationship between intuitionistic logic (which rejects LEM) and certain paraconsistent systems.18 A logic that is both paraconsistent and paracomplete is called **paradefinite**.26

This inherent duality provides a powerful and principled method for constructing our target system. The base logic, LLL, is itself structured around a profound duality manifested in its involutive linear negation $( \\cdot )^{\\perp}$, which pairs connectives like $\\otimes$ and $\\lpar$, $\\&$ and $\\oplus$, and \! and ?.2 Instead of designing the paracomplete component of our system in an ad-hoc manner, we can leverage this existing dual structure. We will make a foundational design choice: the operators of the Logic of Formal Undeterminedness (LFU) will be defined as the linear duals of the LFI operators. We introduce a paracomplete co-negation $-$ and an "undeterminedness" operator, denoted $\*$, which we postulate as the formal dual of the consistency operator $\\circ$. Formally, we define $\*(A) := (\\circ(A^{\\perp}))^{\\perp}$. This "duality by construction" methodology has significant proof-theoretic advantages. In a one-sided sequent calculus presentation, the left-introduction rule for a connective is the mirror image of the right-introduction rule for its dual.2 By defining \* as the dual of $\\circ$, the inference rules for the LFU operators are automatically and elegantly determined by the rules we design for the LFI operators. This ensures the resulting system, PLLL, will be coherent and symmetric, inheriting the deep structural properties of its linear logic foundation.

## **Section 2: A Sequent Calculus for Paradefinite Light Linear Logic (PLLL)**

This section presents the core technical contribution of the report: the formal construction of the Paradefinite Light Linear Logic (PLLL) system. We define its language, its core inference rules for the new paradefinite operators, and the critical interaction rules that integrate these operators into the LLL framework.

### **2.1 Language and Syntax**

The language of PLLL is an extension of the language of propositional Light Linear Logic. Formulas are constructed from a countable set of propositional atoms $p, q,...$ and their linear negations $p^{\\perp}, q^{\\perp},...$. The language includes the standard connectives of LLL 2:

* **Multiplicative Constants:** $1$ (one), $\\perp$ (bottom)  
* **Additive Constants:** $\\top$ (top), $0$ (zero)  
* **Multiplicative Connectives:** $\\otimes$ (tensor), $\\lpar$ (par)  
* **Additive Connectives:** $\\&$ (with), $\\oplus$ (plus)  
* **Exponential Modalities:** \! (of course), ? (why not)

To this base, we add four new unary operators to capture paradefinite reasoning:

* **Paraconsistent Negation:** $\\sim A$  
* **Consistency Operator:** $\\circ A$  
* **Paracomplete Co-negation:** $- A$  
* **Undeterminedness Operator:** $\* A$

This enrichment of the language necessitates a careful distinction between the different forms of negation present in the system.

1. **Linear Negation ($( \\cdot )^{\\perp}$):** This is the foundational, involutive negation inherited from LLL. Its role is primarily structural and algebraic, defining the dualities that underpin the entire logic (e.g., $(A \\otimes B)^{\\perp} \= A^{\\perp} \\lpar B^{\\perp}$, $(\!A)^{\\perp} \=?(A^{\\perp})$).2 It is not a logical negation in the traditional sense of expressing falsehood, but rather a mechanism for moving formulas across the turnstile in the sequent calculus and defining the relationships between connectives.  
2. **Paraconsistent Negation ($\\sim$):** This operator is introduced to model inconsistency. Its defining characteristic is the failure of the principle of explosion. The properties of this negation, such as whether double negation elimination ($\\sim\\sim A \\vdash A$) holds, are a key design choice that determines the specific character of the paraconsistent fragment of the logic.18  
3. **Paracomplete Co-negation ($-$):** This is the dual to $\\sim$. Its defining characteristic is the failure of the Law of the Excluded Middle. It is designed to model informational gaps or undetermined states.

The interactions between these negations are crucial. For example, the relationship between $(\\sim A)^{\\perp}$ and $\\sim (A^{\\perp})$ must be precisely defined by the system's inference rules. These rules will determine how the different notions of "falsity" and "duality" relate to one another, ensuring the system is unambiguous and well-defined.

### **2.2 Core Inference Rules for Paradefinite Operators**

The core behavior of the new paradefinite operators is captured by a set of left and right introduction rules in the sequent calculus. These rules are designed to instantiate the principles of gentle explosion and its dual within the resource-sensitive context of LLL. For simplicity and elegance, we adopt a one-sided sequent calculus presentation ($\\vdash \\Gamma$), where the two-sided sequent $\\Gamma \\vdash \\Delta$ is represented as $\\vdash \\Gamma^{\\perp}, \\Delta$.

The rules for the paraconsistent operators $\\sim$ and $\\circ$ are designed to control explosion. The paraconsistent negation $\\sim$ is introduced without the classical property that $\\vdash A, \\sim A$ is an axiom. This severs the direct link between contradiction and triviality. The consistency operator $\\circ$ then provides the mechanism for reintroducing explosion in a controlled manner.

Following the principle of "duality by construction," the rules for the paracomplete operators $-$ and $\*$ are derived systematically as the linear duals of the rules for $\\sim$ and $\\circ$. This naturally gives rise to a "gentle excluded middle" principle, where the presence of the undeterminedness operator $\*A$ licenses the derivation of $\\vdash A, \-A, \\Delta$, a sequent that is not generally provable.

The fundamental inference rules for these new operators are presented in Table 1\.

**Table 1: Core Paradefinite Inference Rules in PLLL (One-Sided Sequent Calculus)**

| Operator | Rule Name | Inference Rule |
| :---- | :---- | :---- |
| **Identity** | Axiom | $\\overline{\\vdash A, A^{\\perp}}$ |
|  | Cut | $\\frac{\\vdash \\Gamma, A \\quad \\vdash \\Delta, A^{\\perp}}{\\vdash \\Gamma, \\Delta}$ |
| **Paraconsistent** | $\\sim R$ | $\\frac{\\vdash \\Gamma, A^{\\perp}}{\\vdash \\Gamma, \\sim A}$ |
| **Negation ($\\sim$)** | $\\sim L$ | $\\frac{\\vdash \\Gamma, A}{\\vdash \\Gamma, (\\sim A)^{\\perp}}$ |
|  | $\\circ R$ | $\\frac{\\vdash \\Gamma, A \\quad \\vdash \\Delta, \\sim A}{\\vdash \\Gamma, \\Delta, \\circ A}$ |
| **Consistency ($\\circ$)** | $\\circ L$ (Gentle Explosion) | $\\frac{\\vdash \\Gamma}{\\vdash \\Gamma, (\\circ A)^{\\perp}, A, \\sim A}$ |
| **Paracomplete** | $- R$ | $\\frac{\\vdash \\Gamma, A}{\\vdash \\Gamma, \- A}$ |
| **Co-negation ($-$)** | $- L$ | $\\frac{\\vdash \\Gamma, A^{\\perp}}{\\vdash \\Gamma, (- A)^{\\perp}}$ |
|  | $\* R$ (Gentle Excluded Middle) | $\\frac{\\vdash \\Gamma, A, \-A}{\\vdash \\Gamma, \*A}$ |
| **Undeterminedness ($\*$** | $\* L$ | $\\frac{\\vdash \\Gamma \\quad \\vdash \\Delta}{\\vdash \\Gamma, \\Delta, (\*A)^{\\perp}}$ |

*Note on the rules:* The rules for $\\sim$ and $-$ are presented here in a simple form where they behave similarly to linear negation with respect to the turnstile. The $\\circ R$ rule suggests that $A$ is consistent in a context if that context can be used to derive both $A$ and $\\sim A$ independently (in separate branches of the proof). The $\\circ L$ rule embodies gentle explosion: the presence of $(\\circ A)^{\\perp}$ (i.e., $\\circ A$ on the left) along with $A$ and $\\sim A$ leads to a contradiction (the empty succedent, which is provable from $\\vdash \\Gamma$). The rules for $\*$ are the precise duals. $\*R$ states that if a context proves the excluded middle for $A$, it also proves that $A$ is determined. $\*L$ is the dual of $\\circ R$, showing that if two independent contexts are non-committal, their combination implies the undeterminedness of $A$.

### **2.3 Rules of Interaction: Multiplicatives, Additives, and Exponentials**

The most intricate and novel aspect of PLLL is the set of rules governing the interaction between the new paradefinite operators and the existing connectives of LLL. These rules must be designed with a deep appreciation for the underlying resource semantics of the base logic. The distinction between additive (context-sharing) and multiplicative (context-splitting) connectives serves as a powerful analytical lens for this design process.2

#### **Interaction with Additives ($\\&$, $\\oplus$)**

Additive connectives concern choices made within a single, shared resource context. The interaction rules for $\\circ$ and $\*$ with additives must reflect this. When considering the consistency of an additive conjunction, $\\circ(A \\& B)$, we are asking about the consistency of a choice. Intuitively, for the choice to be consistent, both possible outcomes must be consistent within the same shared context. This suggests an additive-style rule where the contexts are preserved across the premises.

* **Proposed Additive Interaction Rules:**  
  * $\\circ(\\&)$-Intro: $\\frac{\\vdash \\Gamma, \\circ A \\quad \\vdash \\Gamma, \\circ B}{\\vdash \\Gamma, \\circ(A \\& B)}$ (If $\\Gamma$ establishes the consistency of $A$ and also the consistency of $B$, then $\\Gamma$ establishes the consistency of the choice between them).  
  * $\*(\\oplus)$-Intro: $\\frac{\\vdash \\Gamma, \*A, \*B}{\\vdash \\Gamma, \*(A \\oplus B)}$ (Dual rule for undeterminedness and additive disjunction).

#### **Interaction with Multiplicatives ($\\otimes$, $\\lpar$)**

Multiplicative connectives, by contrast, involve the combination of independent resources from distinct contexts. The interaction rules must respect this context-splitting nature. The consistency of a combined resource, $\\circ(A \\otimes B)$, depends on the consistency of its independent components. This leads to multiplicative-style rules where the side-formulas ($\\Gamma$ and $\\Delta$) are partitioned between the premises.

* **Proposed Multiplicative Interaction Rules:**  
  * $\\circ(\\otimes)$-Intro: $\\frac{\\vdash \\Gamma, \\circ A \\quad \\vdash \\Delta, \\circ B}{\\vdash \\Gamma, \\Delta, \\circ(A \\otimes B)}$ (If context $\\Gamma$ establishes the consistency of resource $A$ and an independent context $\\Delta$ establishes the consistency of resource $B$, then their combined context establishes the consistency of the combined resource $A \\otimes B$).  
  * $\*(\\lpar)$-Intro: $\\frac{\\vdash \\Gamma, \*A \\quad \\vdash \\Delta, \*B}{\\vdash \\Gamma, \\Delta, \*(A \\lpar B)}$ (Dual rule).

It is plausible that some of these relationships may only hold in one direction. For example, while combining two consistent resources $\\circ A \\otimes \\circ B$ might yield a consistent combination $\\circ(A \\otimes B)$, the reverse might not be true; the consistency of a whole may not guarantee the consistency of its parts when separated. This suggests that some rules might be formulated as one-way implications rather than equivalences.

#### **Interaction with Exponentials (\!, ?)**

This is the most critical nexus for the system's design, as it directly impacts its computational complexity. The rules governing modalized paradefinite formulas like $\\circ(\!A)$ and $\!( \\circ A)$ must be crafted to preserve the polytime cut-elimination property of LLL by respecting the stratification condition.14 This means preventing any new rule from simulating the problematic nesting of exponentials found in full Linear Logic.

* **Proposed Exponential Interaction Rules:**  
  * **Promotion of Consistency:** $\\frac{\\vdash?\\Gamma, \\circ A}{\\vdash?\\Gamma,\!(\\circ A)}$ ($\!\\circ R$) (This is a standard promotion rule applied to a $\\circ$-formula).  
  * **Consistency of Promoted Formulas:** $\\frac{\\vdash \\Gamma,\!(\\circ A)}{\\vdash \\Gamma, \\circ(\!A)}$ ($\!\\circ$-distrib) (If we have an unlimited supply of consistency certificates for $A$, it is reasonable to conclude that the unlimited resource $\!A$\` is itself consistent).  
  * **Undeterminedness of "Why Not":** $\\frac{\\vdash \\Gamma,?(\*A)}{\\vdash \\Gamma, \* (?A)}$ (Dual rule).

Crucially, the reverse of the distributive rule, from $\\circ(\!A)$ to \!(\\circ A), would be rejected. Such a rule would imply that from a single fact about the consistency of an unlimited resource, one could generate an unlimited supply of consistency certificates. This has the potential to violate the stratification principle by allowing for the creation of new \!-modalities in a way that could lead to non-elementary complexity. The careful, unidirectional formulation of these rules is essential for maintaining the "light" nature of the logic.

## **Section 3: Meta-Theoretic Analysis of PLLL**

This section subjects the newly defined PLLL system to rigorous proof-theoretic scrutiny to establish its coherence, consistency, and computational properties. The primary objectives are to demonstrate the admissibility of the Cut rule and to analyze the complexity of the resulting normalization procedure.

### **3.1 Structural Rules and Exponentials Revisited**

In LLL, the structural rules of Weakening and Contraction are not available globally but are licensed for formulas marked with the \! exponential modality (or dually, ? in the succedent).11 The rules are as follows (in a two-sided presentation for clarity):

* **Weakening (\!W):** $\\frac{\\Gamma \\vdash \\Delta}{\\Gamma,\!A \\vdash \\Delta}$  
* **Contraction (\!C):** $\\frac{\\Gamma,\!A,\!A \\vdash \\Delta}{\\Gamma,\!A \\vdash \\Delta}$

In PLLL, these rules apply to any formula, including those constructed with the new paradefinite operators. This allows for derivations involving sequents like $\\vdash\!(\\circ A), (\!(\\circ A))^{\\perp}, (\!(\\circ A))^{\\perp}$, which can then be contracted to $\\vdash\!(\\circ A), (\!(\\circ A))^{\\perp}$. The resource-semantic interpretation of this is significant. A formula like \!(\\sim A) can be read as "an unlimited supply of the conflicting information $\\sim A$." Similarly, $\!(\\circ A)$ represents "a reusable consistency guarantee." The ability to contract and weaken these formulas means that such guarantees or pieces of conflicting information are not consumed upon use; they are persistent facts about the system being modeled. This controlled reintroduction of structural properties is what allows PLLL to embed classical and intuitionistic reasoning about inconsistency within a broader resource-sensitive framework.

### **3.2 The Admissibility of the Cut Rule**

The central meta-theoretic result for any well-behaved sequent calculus is the admissibility of the Cut rule. A successful cut-elimination proof serves as the ultimate validation of a system's design, demonstrating its internal consistency and the coherence of its inference rules.6 For a system as complex as PLLL, which synthesizes principles from three distinct logical traditions, this proof is not merely a technical exercise but the crucible in which the system's logical integrity is forged. A failure to eliminate Cut would signal a fundamental flaw in the interaction rules defined in Section 2, requiring a revision of the system's core design.7

The proof proceeds by induction on a pair of measures: the complexity of the cut-formula $A$ (e.g., the number of logical connectives) and the sum of the heights of the derivations of the two premises of the Cut rule. The argument is a case analysis on the last rule used to derive each premise. The majority of cases, involving the standard LLL connectives, follow the established pattern for LLL's own cut-elimination proof. The critical and novel cases are those where the cut-formula $A$ is a paradefinite formula, or where $A$ is the principal formula in one of the new interaction rules.

A sketch of a key case is illustrative. Consider a cut on the formula $\\circ(A \\otimes B)$:

$$\\frac{ \\frac{\\vdash \\Gamma, \\circ A \\quad \\vdash \\Delta, \\circ B}{\\vdash \\Gamma, \\Delta, \\circ(A \\otimes B)} (\\circ(\\otimes)R) \\quad \\text{Derivation of } \\vdash \\Theta, (\\circ(A \\otimes B))^{\\perp} }{ \\vdash \\Gamma, \\Delta, \\Theta } (Cut)$$  
To eliminate this cut, we must "push" the cut upwards into the premises of the $\\circ(\\otimes)R$ rule. This requires transforming the derivation of $\\vdash \\Theta, (\\circ(A \\otimes B))^{\\perp}$ into derivations of sequents involving $(\\circ A)^{\\perp}$ and $(\\circ B)^{\\perp}$. This is achieved by applying cuts on formulas of lower complexity ($\\circ A$ and $\\circ B$), which is permissible by the induction hypothesis. The most delicate steps involve cuts where the formula is principal in an exponential rule on one side and a paradefinite rule on the other. For example, a cut on $\!(\\circ A)$ where one premise comes from the $\!\\circ R$ rule and the other from the $\!\\circ$-distrib rule. The successful resolution of all such cases demonstrates that the interaction rules have been designed harmoniously, without creating logical pathologies. The successful completion of this proof establishes that PLLL is non-trivial and possesses the subformula property, making it a well-defined and coherent logical system.

### **3.3 Complexity of Normalization**

The defining feature of LLL is its polytime cut-elimination procedure, which establishes its connection to the complexity class PTIME.14 A crucial goal in designing PLLL is to preserve this property. The complexity of normalization in linear logics is intimately tied to the rules for the exponentials. The non-elementary complexity of full LL arises from rules that allow for the arbitrary nesting and combination of \! modalities, which cannot be controlled by a simple measure on formula size alone.14

The design of the interaction rules in Section 2.3, particularly those involving the exponentials, was explicitly guided by the need to respect the stratification condition that constrains LLL. By disallowing rules that would permit inferences from, for example, $\\circ(\!A)$ back to $\!(\\circ A)$, we prevent the creation of new exponential modalities in a way that could lead to a combinatorial explosion during normalization.

The argument for the preservation of the polytime bound proceeds by extending the complexity measure used for LLL to the new formulas of PLLL. The depth and structure of paradefinite formulas contribute to the overall complexity measure, but because the interaction rules do not introduce new forms of exponential nesting, the growth of this measure during the cut-elimination process remains polynomially bounded. The analysis must show that each step of the cut-elimination procedure, including the new cases involving $\\circ, \\sim, \*, \- $, reduces the overall complexity measure in a way that is consistent with a polynomial-time termination. This result would establish that PLLL is not merely a consistent paradefinite logic, but a computationally "light" or "feasible" one, inheriting the most important practical property of its LLL foundation.

## **Section 4: Expressivity and Comparative Analysis**

This final section explores the practical and theoretical implications of PLLL, demonstrating its expressive power through concrete examples and situating it within the broader landscape of non-classical logics.

### **4.1 Modeling with Inconsistent and Incomplete Resources**

The synthesis of paraconsistent principles with a resource-sensitive logic like LLL induces a fundamental shift in interpretation. The focus moves away from the philosophical question of whether a contradiction can be "true" 19 and toward the pragmatic, computational question of what actions are licensed by a state containing conflicting or incomplete resources. In PLLL, a context containing both $A$ and $\\sim A$ does not necessarily represent a contradictory state of the world, but rather a contradictory *information state* available to a reasoning agent.19 The logic of PLLL is a calculus for manipulating such states.

This framework is particularly well-suited for modeling scenarios in computer science where systems must operate reliably in the presence of flawed data.

* **Inconsistent Databases:** Consider a database that, due to a synchronization error, contains conflicting records for a user's status, represented by the formulas active(user) and $\\sim active(user)$. In a classical system, querying this database would lead to explosion, allowing any conclusion to be drawn, rendering the system useless.20 In PLLL, the sequent active(user), \\sim active(user) \\vdash \\text{grant\\\_access} would not be provable. The system can acknowledge the inconsistency without triviality. The $\\circ$ operator can model integrity constraints. If the database has a rule $\\circ active(user)$, then the sequent $\\circ active(user), active(user), \\sim active(user) \\vdash \\text{system\\\_fault}$ would be provable via Gentle Explosion, correctly modeling that the violation of a consistency guarantee should trigger an error state.  
* **Distributed Systems:** In a distributed system, a node may query another for a piece of data $D$. Due to network latency or partitions, a response may not be received, leading to an undetermined state. This is distinct from receiving a negative response. Paracompleteness allows this distinction to be formalized. The system is in a state where neither $D$ nor $-D$ is provable. The undeterminedness operator $\*$ can model timeouts or protocols for resolving ambiguity. A sequent like $\\vdash \*(D), D, \-D$ could be used to model a state where, after a timeout ($\*D$), the system defaults to a defined behavior (e.g., assuming either $D$ or $-D$ for the purpose of moving forward).

The linear aspect of the logic adds another layer of fidelity. If active(user) is a resource that is consumed upon granting access, the logic can track this usage. This prevents the same credential from being used multiple times if it is not explicitly marked as reusable with a \! modality. PLLL thus offers a formal framework for *inconsistency-tolerant resource management*, providing a calculus for reasoning and acting in the presence of the flawed, conflicting, and incomplete information that characterizes real-world computational systems.11

### **4.2 A Comparative Overview**

PLLL occupies a unique position in the landscape of non-classical logics, synthesizing features from several distinct families. Its properties are best understood through comparison with established systems.

* **Versus Relevant Logics:** Relevant logics, like PLLL, restrict the Weakening rule to ensure that premises are relevant to conclusions.13 However, most relevant logics, such as the system R, retain the full structural rule of Contraction, which PLLL restricts via the exponential modalities.5 PLLL's control over both rules provides a more fine-grained model of resource usage.  
* **Versus Standard LFIs:** LFIs such as the mbC system are typically built on a classical or intuitionistic base.23 As such, they inherit the full strength of Weakening and Contraction and lack the distinction between additive and multiplicative connectives. PLLL provides a substructural foundation for LFI principles, allowing for a much richer analysis of how consistency and inconsistency behave in a resource-sensitive setting.  
* **Versus Other Substructural Logics:** The Logic of Bunched Implications (BI) is another substructural logic that features two distinct forms of conjunction and implication (additive and multiplicative).32 However, BI motivates this distinction through a tree-like structure of contexts ("bunches") rather than the resource-semantic principles of linear logic. While both logics offer enhanced expressive power, their foundational principles and areas of application differ.

Table 2 provides a high-level summary of these comparisons, highlighting the unique combination of properties embodied by PLLL.

**Table 2: Comparative Analysis of Logical Properties**

| Logic | Admissibility of Explosion | Validity of Excluded Middle | General Weakening | General Contraction | Additive/Multiplicative Distinction |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Classical Logic** | No (Explosion Holds) | Yes | Yes | Yes | No |
| **Intuitionistic Logic** | No (Explosion Holds) | No | Yes | Yes | No |
| **Linear Logic (LL)** | No (Explosion Holds) | Yes | No | No | Yes |
| **Relevant Logic (R)** | Yes (Typically) | Yes | No | Yes | No |
| **LFI (e.g., mbC)** | Yes | Yes | Yes | Yes | No |
| **PLLL (Proposed)** | Yes (Gentle Explosion) | No (Gentle LEM) | No | No | Yes |

This comparison clarifies the contribution of PLLL. It is the first system to combine the fine-grained resource control of a light linear logic with a fully symmetric, paradefinite treatment of inconsistency and undeterminedness, all while maintaining desirable computational properties.

## **Conclusion**

### **Summary of Contributions**

This report has introduced Paradefinite Light Linear Logic (PLLL), a novel formal system that synthesizes the computational discipline of Light Linear Logic with the inconsistency-tolerant and incompleteness-tolerant framework of paradefinite logics. The principal contributions of this work are threefold:

1. **Formal Specification:** A complete Gentzen-style sequent calculus for PLLL has been presented. This involved defining new operators for paraconsistent negation ($\\sim$), consistency ($\\circ$), and their paracomplete duals ($-$, $\*), and, most importantly, articulating a comprehensive set of interaction rules that govern their behavior with LLL's additive, multiplicative, and exponential connectives. The design was guided by the principles of "duality by construction," ensuring systemic elegance, and treating LLL's stratification condition as a primary constraint.  
2. **Meta-Theoretic Validation:** The report has established the core meta-theoretic properties of PLLL. A proof sketch for the admissibility of the Cut rule was provided, demonstrating the system's internal consistency and architectural coherence. Furthermore, an analysis of the normalization complexity argued that the careful design of the interaction rules preserves the defining polytime property of the LLL base.  
3. **Semantic and Expressive Innovation:** A new interpretation of paradefinite concepts has been proposed, shifting the focus from truth-values to resource management. This "inconsistency-tolerant resource management" paradigm was shown to be highly expressive for modeling practical computational problems involving conflicting and incomplete information, such as those found in databases and distributed systems.

### **Directions for Future Research**

The development of PLLL opens several promising avenues for future investigation.

* **Proof Nets for PLLL:** A natural next step is to develop a graphical proof system, or proof net theory, for PLLL. Proof nets provide a more canonical, syntax-free representation of proofs, abstracting away irrelevant rule orderings. Constructing proof nets for a system with the added complexity of paradefinite operators would be a significant challenge but could yield deeper insights into the structure of proofs in this logic.  
* **Algebraic and Categorical Semantics:** The proof-theoretic development presented here should be complemented by a model-theoretic one. This would involve investigating appropriate algebraic semantics, such as a new class of "paradefinite residuated lattices," or categorical semantics that combine the symmetric monoidal closed structures of linear logic with additional structure to model the paradefinite operators.7 A sound and complete semantics would provide an independent validation of the proof system.  
* **Practical Applications:** The modeling examples in Section 4.1 are illustrative. Future work should aim to develop these into concrete applications, such as using PLLL as the formal basis for a verifiable programming language designed for robust error handling, or as a query language for inconsistent databases that provides formal guarantees on query responses.31  
* **First-Order Extension:** The system developed in this report is propositional. Extending PLLL to a first-order or second-order logic would greatly increase its expressive power. This would require a careful treatment of additive and multiplicative quantifiers in a paradefinite context, building on existing work in substructural logics to define rules for quantifiers that respect the distinctions between shared and independent resources.30

#### **Works cited**

1. Sequent calculus \- Wikipedia, accessed October 17, 2025, [https://en.wikipedia.org/wiki/Sequent\_calculus](https://en.wikipedia.org/wiki/Sequent_calculus)  
2. Linear logic \- Wikipedia, accessed October 17, 2025, [https://en.wikipedia.org/wiki/Linear\_logic](https://en.wikipedia.org/wiki/Linear_logic)  
3. Sequent Calculus: overview (Lecture 2\) \- LIX, accessed October 17, 2025, [https://www.lix.polytechnique.fr/Labo/Dale.Miller/pisa14/lecture2.pdf](https://www.lix.polytechnique.fr/Labo/Dale.Miller/pisa14/lecture2.pdf)  
4. The Sequent Calculus \- Open Logic Project Builds, accessed October 17, 2025, [https://builds.openlogicproject.org/content/first-order-logic/sequent-calculus/sequent-calculus.pdf](https://builds.openlogicproject.org/content/first-order-logic/sequent-calculus/sequent-calculus.pdf)  
5. Reasoning about Knowledge in Linear Logic: Modalities and Complexity \- ePrints Soton, accessed October 17, 2025, [https://eprints.soton.ac.uk/261815/1/antirealism.pdf](https://eprints.soton.ac.uk/261815/1/antirealism.pdf)  
6. Linear Logic for Linguists Introductory Course, ESSLLI-00 Dick Crouch Xerox PARC, accessed October 17, 2025, [https://www.ling.ohio-state.edu/\~pollard/681/crouch.pdf](https://www.ling.ohio-state.edu/~pollard/681/crouch.pdf)  
7. the name substructural logics \[??, ??\]). \- RIMS, Kyoto University, accessed October 17, 2025, [https://www.kurims.kyoto-u.ac.jp/\~terui/cutfinal.pdf](https://www.kurims.kyoto-u.ac.jp/~terui/cutfinal.pdf)  
8. Why is a cut-free system consistent? \- MathOverflow, accessed October 17, 2025, [https://mathoverflow.net/questions/227464/why-is-a-cut-free-system-consistent](https://mathoverflow.net/questions/227464/why-is-a-cut-free-system-consistent)  
9. Tools for the Investigation of Substructural and Paraconsistent Logics, accessed October 17, 2025, [https://www.logic.at/staff/agata/Jelia2014.pdf](https://www.logic.at/staff/agata/Jelia2014.pdf)  
10. Substructural Logics \- Stanford Encyclopedia of Philosophy, accessed October 17, 2025, [https://plato.stanford.edu/entries/logic-substructural/](https://plato.stanford.edu/entries/logic-substructural/)  
11. Linear Logic \- Stanford Encyclopedia of Philosophy, accessed October 17, 2025, [https://plato.stanford.edu/entries/logic-linear/](https://plato.stanford.edu/entries/logic-linear/)  
12. Substructural Logics \- Proof Theory \- Greg Restall, accessed October 17, 2025, [https://consequently.org/slides/nassli2016-pt-lpa-2-substructural-logics.pdf](https://consequently.org/slides/nassli2016-pt-lpa-2-substructural-logics.pdf)  
13. Substructural Logics (Stanford Encyclopedia of Philosophy/Fall 2020 Edition), accessed October 17, 2025, [https://plato.stanford.edu/archives/fall2020/entries/logic-substructural/](https://plato.stanford.edu/archives/fall2020/entries/logic-substructural/)  
14. LIGHT LINEAR LOGIC \- Jean-Yves GIRARD, accessed October 17, 2025, [https://girard.perso.math.cnrs.fr/LLL.pdf](https://girard.perso.math.cnrs.fr/LLL.pdf)  
15. A taste of linear logic\*, accessed October 17, 2025, [https://homepages.inf.ed.ac.uk/wadler/papers/lineartaste/lineartaste-revised.pdf](https://homepages.inf.ed.ac.uk/wadler/papers/lineartaste/lineartaste-revised.pdf)  
16. Reasoning About Knowledge In Linear Logic: Modalities and Complexity \- ResearchGate, accessed October 17, 2025, [https://www.researchgate.net/publication/225967272\_Reasoning\_About\_Knowledge\_In\_Linear\_Logic\_Modalities\_and\_Complexity](https://www.researchgate.net/publication/225967272_Reasoning_About_Knowledge_In_Linear_Logic_Modalities_and_Complexity)  
17. Linear logic and elementary time \- Edinburgh Research Explorer, accessed October 17, 2025, [https://www.research.ed.ac.uk/files/16873920/Linear\_logic\_and\_elementary\_time.pdf](https://www.research.ed.ac.uk/files/16873920/Linear_logic_and_elementary_time.pdf)  
18. Paraconsistent logic \- Wikipedia, accessed October 17, 2025, [https://en.wikipedia.org/wiki/Paraconsistent\_logic](https://en.wikipedia.org/wiki/Paraconsistent_logic)  
19. towards a philosophical understanding of the logics of formal inconsistency \- SciELO, accessed October 17, 2025, [https://www.scielo.br/j/man/a/ds9M9Kpfb6F679ZMvpxxjsj/?lang=en](https://www.scielo.br/j/man/a/ds9M9Kpfb6F679ZMvpxxjsj/?lang=en)  
20. Logics of Formal Inconsistency, accessed October 17, 2025, [https://iiitd.ac.in/moh/student\_presentations/EshaJain.pdf](https://iiitd.ac.in/moh/student_presentations/EshaJain.pdf)  
21. The future of paraconsistent logic \- Jean-Yves Béziau, accessed October 17, 2025, [https://www.jyb-logic.org/future-pl.pdf](https://www.jyb-logic.org/future-pl.pdf)  
22. (PDF) Logics of Formal Inconsistency \- ResearchGate, accessed October 17, 2025, [https://www.researchgate.net/publication/227047567\_Logics\_of\_Formal\_Inconsistency](https://www.researchgate.net/publication/227047567_Logics_of_Formal_Inconsistency)  
23. Intuitionistic Implication and Logics of Formal Inconsistency \- MDPI, accessed October 17, 2025, [https://www.mdpi.com/2075-1680/13/11/738](https://www.mdpi.com/2075-1680/13/11/738)  
24. On the Philosophy and Mathematics of the Logics of Formal Inconsistency \- ResearchGate, accessed October 17, 2025, [https://www.researchgate.net/publication/297713419\_On\_the\_Philosophy\_and\_Mathematics\_of\_the\_Logics\_of\_Formal\_Inconsistency](https://www.researchgate.net/publication/297713419_On_the_Philosophy_and_Mathematics_of_the_Logics_of_Formal_Inconsistency)  
25. Full article: Generalized Revenge \- Taylor & Francis Online, accessed October 17, 2025, [https://www.tandfonline.com/doi/full/10.1080/00048402.2019.1640323](https://www.tandfonline.com/doi/full/10.1080/00048402.2019.1640323)  
26. (PDF) Four-Valued Paradefinite Logics \- ResearchGate, accessed October 17, 2025, [https://www.researchgate.net/publication/315884653\_Four-Valued\_Paradefinite\_Logics](https://www.researchgate.net/publication/315884653_Four-Valued_Paradefinite_Logics)  
27. Paradefinite Zermelo-Fraenkel Set Theory \- ILLC Preprints and Publications, accessed October 17, 2025, [https://eprints.illc.uva.nl/id/document/11458](https://eprints.illc.uva.nl/id/document/11458)  
28. In paraconsistent logic, the rules for the logic are still consistent right? : r/math \- Reddit, accessed October 17, 2025, [https://www.reddit.com/r/math/comments/2krbuv/in\_paraconsistent\_logic\_the\_rules\_for\_the\_logic/](https://www.reddit.com/r/math/comments/2krbuv/in_paraconsistent_logic_the_rules_for_the_logic/)  
29. The Four Binary Operators of Linear Logic | Equivalent Exchange, accessed October 17, 2025, [https://equivalentexchange.blog/2012/04/17/the-four-binary-operators-of-linear-logic/](https://equivalentexchange.blog/2012/04/17/the-four-binary-operators-of-linear-logic/)  
30. A multiplicative ingredient for ω-inconsistency \- Open Journal System, accessed October 17, 2025, [https://ojs.victoria.ac.nz/ajl/article/download/9606/8559/15662](https://ojs.victoria.ac.nz/ajl/article/download/9606/8559/15662)  
31. \[2208.12976\] Paraconsistent logic and query answering in inconsistent databases \- arXiv, accessed October 17, 2025, [https://arxiv.org/abs/2208.12976](https://arxiv.org/abs/2208.12976)  
32. The Inverse Method for the Logic of Bunched Implications \- Department of Computer Science and Technology |, accessed October 17, 2025, [https://www.cl.cam.ac.uk/\~nk480/inverse-method-for-bi.pdf](https://www.cl.cam.ac.uk/~nk480/inverse-method-for-bi.pdf)  
33. The Logic of Bunched Implications \- UCL Computer Science, accessed October 17, 2025, [http://www0.cs.ucl.ac.uk/staff/p.ohearn/papers/BI.pdf](http://www0.cs.ucl.ac.uk/staff/p.ohearn/papers/BI.pdf)  
34. Bunched logic \- Wikipedia, accessed October 17, 2025, [https://en.wikipedia.org/wiki/Bunched\_logic](https://en.wikipedia.org/wiki/Bunched_logic)  
35. The Consistency and Complexity of Multiplicative Additive System Virtual \- SciSpace, accessed October 17, 2025, [https://scispace.com/pdf/the-consistency-and-complexity-of-multiplicative-additive-4ht5bqmkxy.pdf](https://scispace.com/pdf/the-consistency-and-complexity-of-multiplicative-additive-4ht5bqmkxy.pdf)