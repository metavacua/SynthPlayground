

# **Gaps and Gluts Controlled: An Analysis of the Duality Between Logics of Formal Inconsistency and Undeterminedness**

## **The Foundational Duality: Paraconsistency and Paracompleteness**

Classical logic is built upon twin pillars: the Law of Non-Contradiction (LNC), which asserts that a proposition and its negation cannot both be true, and the Law of Excluded Middle (LEM), which asserts that for any proposition, either it or its negation must be true.1 Together, these principles enforce a bivalent worldview where every statement is unequivocally either true or false, with no middle ground and no overlap. However, the application of logic to real-world reasoning—spanning domains from database management and artificial intelligence to legal argumentation and formal semantics—frequently encounters scenarios of imperfect information that challenge this pristine classical edifice.3 Information can be overabundant and contradictory, or it can be sparse and incomplete. The formal study of these scenarios has given rise to two broad, and dual, families of non-classical logics: paraconsistent logics, which tolerate contradictions, and paracomplete logics, which tolerate informational gaps. The duality between these approaches is not merely a technical curiosity; it reflects a fundamental philosophical choice about how to manage imperfect information. It is a choice between prioritizing the preservation of all available data, even if contradictory (completeness), and prioritizing the structural integrity of the system, even if it means acknowledging gaps (coherence).

### **Philosophical Motivations: Reasoning with Inconsistency vs. Incompleteness**

The primary motivation for paraconsistent logic is the conviction that it should be possible to reason with inconsistent information in a controlled and discriminating manner.6 In classical logic, the presence of a single contradiction, such as $P \\land \\lnot P$, triggers the principle of explosion, or *Ex Contradictione Quodlibet* (ECQ), which renders the entire system trivial by allowing any arbitrary proposition to be proven true.6 This "explosive" nature of classical logic is ill-suited for contexts where contradictions are common, if not inevitable. Large databases may contain conflicting entries from different sources; scientific theories evolve through stages of inconsistency; legal frameworks contain contradictory statutes; and formal theories of truth, when sufficiently expressive, can generate semantic paradoxes like the Liar paradox.8 A paraconsistent logic abandons ECQ, making it possible to distinguish between inconsistent theories and to reason with them without lapsing into absurdity.6 It treats inconsistency not as a catastrophic failure, but as a potentially informative state of affairs that requires careful management.8

Dually, paracomplete logics are motivated by situations of informational incompleteness or indeterminacy, where there may be insufficient grounds to assert either a proposition or its negation.5 The most prominent example is intuitionistic logic, which rejects LEM on constructivist grounds; for instance, for an unsolved mathematical problem like Goldbach's Conjecture ($G$), an intuitionist would refuse to assert $G \\lor \\lnot G$ because no proof of either disjunct is known.10 This rejection of LEM is not limited to mathematical constructivism. It is also relevant to reasoning about future contingents, where the truth value of a statement about the future may not yet be determined, and to modeling vague predicates, where there may be borderline cases that are neither clearly true nor clearly false.1 Paracomplete logics formalize the idea of a "truth-value gap," allowing for a "third possibility" beyond the classical dichotomy of true and false, where a proposition and its negation can both be considered not true.2

### **Formalizing the Divide: The Principle of Explosion and the Law of Excluded Middle**

The formal distinction between these two families of logic is defined by their rejection of a core classical principle.

* **The Principle of Explosion (ECQ):** Formally, this principle states that from a set of premises containing a contradiction, any conclusion follows. In a standard single-conclusion consequence relation, this is written as $\\{A, \\lnot A\\} \\vdash B$ for any formulas $A$ and $B$.6 A logic is defined as **paraconsistent** if its consequence relation $\\vdash$ is not explosive; that is, there exist some $A$ and $B$ such that $\\{A, \\lnot A\\} \\not\\vdash B$.8 This is the minimal, negative definition of paraconsistency.8  
* **The Law of Excluded Middle (LEM):** This principle states that for any proposition $A$, the disjunction $A \\lor \\lnot A$ is a logical truth, written as $\\vdash A \\lor \\lnot A$.2 A logic is defined as **paracomplete** if LEM is not a universal theorem; that is, there exists some $A$ for which $\\not\\vdash A \\lor \\lnot A$.6

The duality between these principles is most perspicuously represented within a multiple-conclusion sequent calculus framework. In this setting, the comma on the left of the turnstile ($\\vdash$) is interpreted conjunctively, while the comma on the right is interpreted disjunctively.14 The principles can then be expressed as structural rules:

* **Explosion (Law of Non-Contradiction):** $A, \\lnot A \\vdash$  
* **Excluded Middle:** $\\vdash A, \\lnot A$

Viewed this way, paraconsistency arises from rejecting the first sequent, which states that $A$ and $\\lnot A$ cannot hold together as premises. Paracompleteness arises from rejecting the second, which states that $A$ and $\\lnot A$ must hold together as possible conclusions.12 The former concerns the simultaneous truth of $A$ and $\\lnot A$ (a "glut"), while the latter concerns their simultaneous falsity (a "gap").

### **Semantic Intuitions: Truth-Value Gaps, Gluts, and Many-Valued Logics**

Many-valued logics provide a natural semantic framework for modeling these non-classical behaviors by introducing truth values beyond the classical {True, False}.

* **Strong Kleene Logic (K3):** This system introduces a third truth value, $n$ (for "neither" or "undetermined"), to the classical set {1, 0} (for True, False).17 The value $n$ represents a truth-value gap. In K3, if a proposition $A$ has the value $n$, its negation $\\lnot A$ also has the value $n$. Consequently, the disjunction $A \\lor \\lnot A$ evaluates to $n \\lor n \= n$. Since $n$ is not a designated (true) value, LEM fails, making K3 a archetypal paracomplete logic.9  
* **Logic of Paradox (LP):** Developed by Graham Priest, LP also uses three values, but its third value is $b$ (for "both").17 This value represents a truth-value glut, a proposition that is simultaneously true and false. In LP, if $v(A) \= b$, then $v(\\lnot A) \= b$. The designated values are {1, $b$}, meaning that anything that is at least true is designated. A contradiction $A \\land \\lnot A$ can be designated (if $v(A) \= b$), but it is possible for an arbitrary proposition $B$ to be false (if $v(B) \= 0$). Therefore, explosion fails, making LP a archetypal paraconsistent logic.6  
* **First Degree Entailment (FDE):** This logic, also known as Belnap-Dunn logic, combines the intuitions of K3 and LP by using a four-valued semantics with the set of values {1, $b$, $n$, 0}.5 These values can be understood as representing what a source of information might report about a proposition: {True}, {True, False}, {}, {False}. The designated values are {1, $b$}. Because $b$ is designated, contradictions can be true, so FDE is paraconsistent. Because $n$ is not designated, instances of LEM can fail to be true, so FDE is also paracomplete.5 FDE thus provides a foundational semantic space for logics that are sensitive to both inconsistency and incompleteness.

| Feature | Paraconsistency | Paracompleteness |
| :---- | :---- | :---- |
| **Core Idea** | Tolerating truth-value "gluts" | Tolerating truth-value "gaps" |
| **Rejected Principle** | Principle of Explosion (ECQ): $A, \\lnot A \\vdash B$ | Law of Excluded Middle (LEM): $\\vdash A \\lor \\lnot A$ |
| **Semantic Model** | $v(A) \= \\text{Both}$ is possible | $v(A) \= \\text{Neither}$ is possible |
| **Key Slogan** | A statement and its negation can both be true. | A statement and its negation can both be false. |
| **Prototypical Logic** | Priest's Logic of Paradox (LP) | Kleene's Logic K3 / Intuitionistic Logic |
| **Formal Dual** | Paracompleteness | Paraconsistency |

### **Genuine Paraconsistency and Paracompleteness: A Deeper Rejection of Classical Laws**

A more refined distinction, introduced by Jean-Yves Béziau, separates logics that merely fail to validate a classical principle from those that actively reject it in a stronger sense.18 This leads to the notions of "genuine" paraconsistency and paracompleteness.

* **Genuine Paraconsistency:** A logic is considered genuinely paraconsistent if it rejects both ECQ and the Law of Non-Contradiction as a theorem. Formally, it must satisfy two conditions for some formulas:  
  1. $A \\land \\lnot A \\not\\vdash B$ (Rejection of Explosion)  
  2. $\\not\\vdash \\lnot(A \\land \\lnot A)$ (Rejection of LNC as a tautology).16  
     This distinguishes logics that simply block the inference from a contradiction from those that also permit contradictions to be satisfiable within their semantics.  
* **Genuine Paracompleteness:** Dually, a logic is genuinely paracomplete if it rejects both LEM and its dual counterpart. Formally:  
  1. $\\not\\vdash A \\lor \\lnot A$ (Rejection of LEM)  
  2. $\\lnot(A \\lor \\lnot A) \\not\\vdash B$ (Rejection of the dual of LNC).12  
     This second condition ensures that the failure of LEM is not itself a trivializing event; it allows for the possibility that a proposition is undetermined to be a coherent, non-explosive state of affairs. For example, intuitionistic logic is paracomplete but not genuinely so, because the formula $\\lnot(A \\lor \\lnot A)$ is unsatisfiable and leads to triviality.12

This deeper distinction sets the stage for more expressive logical systems that do not merely tolerate deviations from classical logic but are designed to reason about them in a nuanced and controlled way.

## **Logics of Formal Inconsistency (LFIs): Internalizing Consistency**

While simple paraconsistent logics like LP successfully prevent inferential explosion, their global rejection of classical principles can be a significant drawback. In many reasoning contexts, it is known that certain propositions are, or ought to be, consistent and should therefore behave classically. Simple paraconsistency lacks the expressive resources to make such distinctions, treating all contradictions as equally benign. This limitation motivated the development of the **Logics of Formal Inconsistency (LFIs)**, a class of paraconsistent logics that internalize the notion of consistency, allowing for a fine-grained and conditional recovery of classical reasoning.10

### **Beyond Simple Paraconsistency: The Need for Controlled Explosion**

The universal invalidation of classically valid rules in simple paraconsistent systems can be overly restrictive. A key example is Disjunctive Syllogism: from $A \\lor B$ and $\\lnot A$, infer $B$. This rule is invalid in many paraconsistent logics because if $A$ were a dialetheia (both true and false), then $A \\lor B$ and $\\lnot A$ could both be true while $B$ is false.6 However, if one has an additional piece of information—namely, that $A$ is behaving consistently and is not a dialetheia—then the inference should be perfectly valid. Simple paraconsistent logics cannot accommodate this conditional validity because consistency is a meta-theoretic property of the logic itself, not a concept that can be expressed or reasoned about within the object language.13 They are unable to distinguish between a contradiction that signals a genuine dialetheia and one that indicates a serious error that should, in fact, lead to triviality. LFIs were created to solve precisely this problem.

### **The Consistency Operator (∘) and the Principle of Gentle Explosion**

The defining feature of an LFI is the introduction of a new unary connective, $\\circ$, into the object language.10 The formula $\\circ A$ is read as "$A$ is consistent." This operator allows the logic to talk about consistency directly. Its primary function is to replace the universally rejected Principle of Explosion with a controlled version known as the Principle of Gentle Explosion. This principle states that a contradiction leads to triviality only when the proposition involved is explicitly marked as consistent.13 Formally, this is expressed as:  
$\\{\\circ A, A, \\lnot A\\} \\vdash B$  
This principle allows the logic to remain paraconsistent by default (i.e., $\\{A, \\lnot A\\} \\not\\vdash B$ in general) while enabling explosive behavior in controlled contexts. A crucial feature of LFIs is that the notion of consistency expressed by $\\circ A$ is logically independent of the syntactic form $\\lnot(A \\land \\lnot A)$ (the Law of Non-Contradiction).10 This distinguishes LFIs from earlier systems like da Costa's C-systems and provides greater philosophical and formal flexibility.

### **A Prototypical LFI: The Axiomatic System mbC**

A foundational and straightforward example of an LFI is the system **mbC**. It is constructed by extending the positive fragment of classical propositional logic (CPL+) with axioms for negation and the consistency operator.19

The axiomatic system for mbC is defined as follows:

**Axiom Schemas:**

1. All axiom schemas of positive classical propositional logic (CPL+), such as:  
   * $A \\to (B \\to A)$  
   * $(A \\to (B \\to C)) \\to ((A \\to B) \\to (A \\to C))$  
   * ...and axioms for conjunction and disjunction.19  
2. **Excluded Middle:** $A \\lor \\lnot A$  
3. **Gentle Explosion (bc1):** $\\circ A \\to (A \\to (\\lnot A \\to B))$

**Inference Rule:**

* **Modus Ponens (MP):** From $A$ and $A \\to B$, infer $B$.19

In this system, $\\circ A$ is a primitive connective. The axiom bc1 is the formal heart of the LFI, stipulating that if $A$ is consistent ($\\circ A$), then from $A$ and $\\lnot A$, any $B$ can be derived. Since there is no axiom allowing the derivation of $\\circ A$ for all $A$, the system remains paraconsistent.

### **Recapturing Classicality: The Role of ∘ in Recovering Reasoning**

The consistency operator $\\circ$ functions as a recovery operator.20 By adding the assumption $\\circ A$ to a set of premises, one can restore or "recapture" classical inferences for the proposition $A$ that would otherwise be invalid. For instance, while Disjunctive Syllogism is not valid in mbC, a conditional version is:  
$\\{A \\lor B, \\lnot A, \\circ A\\} \\vdash B$  
This demonstrates the profound expressive power of LFIs. They are not merely "weaker" than classical logic; rather, they provide a framework for a form of logical pluralism within a single system. The logic behaves paraconsistently by default, accommodating inconsistency without triviality, but can "switch on" classical reasoning on a formula-by-formula basis whenever a consistency assumption is warranted.13 This shift from treating consistency as a global, immutable property of a logical system to treating it as a local, expressible property of a proposition is the central innovation of the LFI programme. It allows for a more nuanced and realistic modeling of reasoning processes where different pieces of information may come with different degrees of reliability.

## **Logics of Formal Undeterminedness (LFUs): The Dual Framework**

The philosophical and formal strategy employed by LFIs—internalizing a meta-theoretic property to gain finer-grained control over logical inferences—has a precise and elegant dual. Just as LFIs were developed to address the shortcomings of simple paraconsistency, the **Logics of Formal Undeterminedness (LFUs)** have been proposed to address the limitations of simple paracompleteness. Where LFIs manage truth-value gluts by introducing a consistency operator, LFUs manage truth-value gaps by introducing a dual **completeness** or **determinedness** operator. This creates a parallel family of logics that control the application of the Law of Excluded Middle in the same way LFIs control the Principle of Explosion.20

### **Formalizing Incompleteness: The Motivation for LFUs**

Standard paracomplete logics, such as intuitionistic logic or K3, invalidate the Law of Excluded Middle globally. For any proposition $A$, the formula $A \\lor \\lnot A$ is not a theorem. This uniform rejection, however, can be just as overly restrictive as the uniform rejection of explosion in simple paraconsistent logics. In many domains, we have good reason to believe that certain propositions, while perhaps currently unknown, are nonetheless determinate—that is, they must be either true or false. For example, while an intuitionist might reject LEM for Goldbach's Conjecture, a classical mathematician would argue that the conjecture is bivalent, even if its truth value is not yet known. A logic that globally rejects LEM cannot express this distinction between propositions that are fundamentally indeterminate and those that are merely epistemically unresolved.21 LFUs are designed to overcome this limitation by formalizing the notion of "determinedness" within the object language, allowing for a conditional recovery of LEM.5

### **The Completeness/Determinedness Operator (\~) and the Principle of Gentle Excluded Middle**

The defining feature of an LFU is the introduction of a unary connective, $\\sim$, into the language. The formula $\\sim A$ is read as "$A$ is complete," "$A$ is determined," or "$A$ is bivalent".20 This operator's role is to enable a controlled or "gentle" application of the Law of Excluded Middle. This is formalized in the Principle of Gentle Excluded Middle, which states that the disjunction $A \\lor \\lnot A$ holds, provided that the proposition $A$ is explicitly marked as complete. In an axiomatic system, this can be expressed as:  
$\\sim A \\to (A \\lor \\lnot A)$  
In a sequent calculus setting, this would correspond to the rule $\\sim A \\vdash A \\lor \\lnot A$. This principle is the exact dual of Gentle Explosion. While Gentle Explosion states $\\{\\circ A, A, \\lnot A\\} \\vdash B$, restricting a conjunctive principle (explosion), Gentle Excluded Middle states $\\sim A \\vdash A \\lor \\lnot A$, enabling a disjunctive principle (excluded middle). This allows the logic to be paracomplete by default but to enforce bivalence in controlled contexts.

### **The Dual System mbD: An Axiomatic Exposition**

The duality between LFIs and LFUs is perfectly captured by comparing the axiomatic system mbC with its dual, **mbD**. This system was designed to be a paracomplete logic that recovers LEM in a manner analogous to how mbC recovers explosion.20

The axiomatic system for mbD is defined as follows:

**Axiom Schemas:**

1. All axiom schemas of positive classical propositional logic (CPL+), identical to the common core of mbC.20  
2. **Principle of Explosion:** $A \\to (\\lnot A \\to B)$  
3. **Gentle Excluded Middle (GPEM):** $\\sim A \\to (A \\lor \\lnot A)$

**Inference Rule:**

* **Modus Ponens (MP)**.20

The structural symmetry with mbC is striking. Both systems share the CPL+ core. However, mbC retains LEM as an axiom and restricts explosion, while mbD retains explosion as an axiom and restricts LEM. The recovery axioms are perfect duals, each using a dedicated operator to conditionally reintroduce the principle that its counterpart restricts.

### **The Recovery of Bivalence for Determined Propositions**

The completeness operator $\\sim$ functions, dually to $\\circ$, as a **recovery operator**.20 Its purpose is to restore classical behavior for propositions that might otherwise inhabit a truth-value gap. By assuming $\\sim A$, one can recover classical principles that depend on bivalence, such as certain forms of proof by cases or the unrestricted validity of LEM for $A$. This provides LFUs with the same kind of fine-grained control seen in LFIs. The logic can behave paracompletely by default, allowing for indeterminacy, but can "switch on" classical bivalence for specific propositions that are known or assumed to be fully determined.

This capability transforms the LFU from a simple paracomplete logic into a more powerful epistemic framework. The operator $\\sim$ provides a formal tool to model concepts like epistemic closure, decidability, or observational completeness. For instance, $\\sim A$ could be interpreted as "the truth value of $A$ is knowable in principle," or "a decision procedure exists for $A$." This allows for a formal distinction between propositions that are contingently undetermined (due to a current lack of knowledge) and those that might be indeterminate in principle. LFUs are therefore not just formal duals to LFIs; they are expressive epistemic logics capable of representing nuanced positions about the determinacy of statements, a feature absent in simpler paracomplete systems.

## **A Proof-Theoretic Analysis of the Duality**

The duality between Logics of Formal Inconsistency and Logics of Formal Undeterminedness, while philosophically intuitive, finds its most rigorous and elegant expression in proof theory. By analyzing the axiomatic structures of mbC and mbD and, more revealingly, by situating them within the symmetrical framework of sequent calculus, the deep structural opposition between controlling inconsistency and controlling incompleteness becomes manifest. This proof-theoretic perspective reveals that the LFI/LFU duality is a specific, operator-driven instance of a more general symmetry in logic, famously exemplified by the relationship between intuitionistic and dual-intuitionistic systems.

### **Duality at the Axiomatic Level: A Comparative Study of mbC and mbD**

A side-by-side comparison of the axiomatic foundations of the prototypical LFI, mbC, and its dual LFU, mbD, lays bare their mirrored structure.

| Component | mbC (Paraconsistent LFI) | mbD (Paracomplete LFU) |
| :---- | :---- | :---- |
| **Common Core** | Axioms of Classical Positive Logic (CPL+) | Axioms of Classical Positive Logic (CPL+) |
| **Retained Classical Law** | Law of Excluded Middle: $A \\lor \\lnot A$ | Principle of Explosion: $A \\to (\\lnot A \\to B)$ |
| **Recovery Operator** | $\\circ A$ ("A is consistent") | $\\sim A$ ("A is complete/determined") |
| **Recovery Axiom** | Gentle Explosion (bc1): $\\circ A \\to (A \\to (\\lnot A \\to B))$ | Gentle Excluded Middle (GPEM): $\\sim A \\to (A \\lor \\lnot A)$ |
| **Primary Goal** | To control inconsistency and recover explosion conditionally. | To control incompleteness and recover excluded middle conditionally. |

As the table illustrates, both systems are built upon the stable foundation of positive classical logic.19 Their divergence is a perfect swap of classical negation principles: mbC holds onto LEM while restricting explosion, whereas mbD holds onto explosion while restricting LEM. The core of the duality resides in their respective recovery axioms. The axiom bc1 uses the consistency operator $\\circ$ to reintroduce a principle, explosion, that is fundamentally conjunctive in nature (it is triggered by the presence of both $A$ and $\\lnot A$). Dually, the axiom GPEM uses the completeness operator $\\sim$ to reintroduce a principle, excluded middle, that is fundamentally disjunctive (it asserts the availability of either $A$ or $\\lnot A$).

### **The Sequent Calculus as a Lens for Duality**

The sequent calculus, introduced by Gerhard Gentzen, is the ideal formal setting for analyzing such dualities.14 Its central object, the sequent $\\Gamma \\vdash \\Delta$, possesses an inherent left-right symmetry. The antecedent $\\Gamma$ (formulas to the left of the turnstile) is interpreted conjunctively, representing a set of assumptions that hold simultaneously. The succedent $\\Delta$ (formulas to the right) is interpreted disjunctively, representing a set of conclusions of which at least one must hold.15 This structure makes the duality between conjunction and disjunction, assumption and conclusion, and ultimately, paraconsistency and paracompleteness, formally explicit.14

### **Parallels with Intuitionistic (LJ) and Dual-Intuitionistic (LDJ) Calculi**

The LFI/LFU duality is deeply rooted in a historical and well-understood proof-theoretic relationship between intuitionistic and dual-intuitionistic logic.6

* **Intuitionistic Sequent Calculus (LJ):** Gentzen's calculus for intuitionistic logic, LJ, is obtained from the classical calculus LK by imposing a structural restriction: sequents may have at most one formula in the succedent ($|\\Delta| \\le 1$).26 This simple syntactic constraint has profound consequences. It directly blocks the derivation of sequents like $\\vdash A, \\lnot A$, which is a necessary step in proving the Law of Excluded Middle ($\\vdash A \\lor \\lnot A$).28 This structural feature is the proof-theoretic source of intuitionistic logic's paracompleteness.  
* **Dual-Intuitionistic Sequent Calculus (LDJ):** The perfect dual to LJ is a system, LDJ, obtained by imposing the symmetric restriction on LK: sequents may have at most one formula in the antecedent ($|\\Gamma| \\le 1$).26 This restriction blocks the formation of antecedents like $A, \\lnot A$, thereby preventing the application of any rule that would lead to explosion. The system LDJ is therefore inherently paraconsistent.29

This established duality provides a powerful conceptual model for understanding LFIs and LFUs. An LFU behaves, in essence, like a system that is globally paracomplete (like LJ) but contains a mechanism ($\\sim$) to locally suspend this restriction. Dually, an LFI behaves like a system that is globally paraconsistent (like LDJ) but contains a mechanism ($\\circ$) to locally override its non-explosive nature.

### **Deriving Rules for the ∘ and \~ Operators in a Sequent Framework**

Translating the axiomatic definitions of $\\circ$ and $\\sim$ into the language of sequent calculus provides a computational perspective on their function. While the literature on this specific topic is sparse, the rules can be derived directly from the recovery axioms.

* **Rule for $\\circ$ (Consistency):** The gentle explosion axiom $\\circ A \\to (A \\to (\\lnot A \\to B))$ is most naturally expressed as a left rule, as it describes how to *use* an assumption of consistency. A direct translation would be complex, but its inferential power is captured by a rule that reintroduces explosion when licensed by $\\circ A$. A simple, powerful rule would be an axiom stating that an inconsistent context licensed by $\\circ A$ is trivial:  
  * Axiom of Controlled Explosion: $\\Gamma, \\circ A, A, \\lnot A \\vdash \\Delta$  
    This rule states that any sequent with $\\circ A, A, \\lnot A$ in its antecedent is provable.  
* **Rule for $\\sim$ (Completeness):** The gentle excluded middle axiom $\\sim A \\to (A \\lor \\lnot A)$ is also best captured as a left rule. It allows the assumption of $\\sim A$ to introduce the disjunction $A \\lor \\lnot A$. Given the disjunctive nature of the succedent, the most direct rule is one that adds both $A$ and $\\lnot A$ to the right-hand side of the sequent:  
  * Left Rule for Completeness ($\\sim$ L): $\\frac{}{\\Gamma, \\sim A \\vdash A, \\lnot A, \\Delta}$  
    This rule states that if $A$ is assumed to be complete, then one of $A$ or $\\lnot A$ must hold (in the context of other possibilities $\\Delta$).

The proposed rules, summarized in the table below, reveal the operators' function as meta-theoretic controls embedded in the object language. The operator $\\sim$ effectively licenses a temporary suspension of the "single-succedent" character of a paracomplete logic for the proposition $A$. Dually, $\\circ$ licenses the formation of an explosive "multi-antecedent" context for $A$ in a paraconsistent logic. They are not merely connectives that form new propositions; they are switches that alter the inferential landscape of the proof system itself.

| Operator | Left Rule (Introduction in Antecedent) | Right Rule (Introduction in Succedent) |
| :---- | :---- | :---- |
| **$\\circ$ (Consistency)** | $\\Gamma, \\circ A, A, \\lnot A \\vdash \\Delta$ (Axiom) | $\\Gamma, \\lnot(A \\land \\lnot A) \\vdash \\circ A, \\Delta$ (Example based on ci axiom) |
| **$\\sim$ (Completeness)** | $\\Gamma, \\sim A \\vdash A, \\lnot A, \\Delta$ (Axiom) | $\\Gamma, A \\lor \\lnot A \\vdash \\sim A, \\Delta$ (Hypothetical dual rule) |

## **Semantic Frameworks for LFIs and LFUs**

While proof theory reveals the syntactic and structural nature of the LFI-LFU duality, formal semantics provides the corresponding model-theoretic interpretation, grounding the systems in notions of truth and valuation. The choice of semantic framework—from three-valued matrices to more complex four-valued and algebraic structures—is not merely a technical decision; it reflects a deeper philosophical commitment regarding the relationship between inconsistency and incompleteness.

### **Many-Valued Matrix Semantics for mbC and mbD**

The most straightforward way to provide semantics for mbC and mbD is through three-valued logical matrices, which extend the classical truth values {1, 0} with a single non-classical value.

* **Semantics for mbC:** The system mbC can be given a semantics based on a matrix similar to that of Priest's LP, using the truth values {1, $b$, 0}, where $b$ represents a truth-value glut (both true and false) and the designated values are {1, $b$}.6 The key is the interpretation of the consistency operator $\\circ$. To ensure that $\\circ A$ captures the notion of consistency, its truth function must identify the non-classical, inconsistent value. Thus, the operator $\\circ$ is defined such that $v(\\circ A) \= 1$ if $v(A) \\in \\{1, 0\\}$, and $v(\\circ A) \= 0$ if $v(A) \= b$.19 This valuation ensures that the gentle explosion axiom $\\circ A \\to (A \\to (\\lnot A \\to B))$ is valid: if $v(\\circ A) \= 1$, then $A$ behaves classically, and if $v(A) \= b$, then $v(\\circ A) \= 0$, making the antecedent of the implication false and the whole formula true.  
* **Semantics for mbD:** Dually, mbD can be interpreted using a matrix similar to Kleene's K3, with truth values {1, $n$, 0}, where $n$ represents a truth-value gap (neither true nor false) and the sole designated value is {1}.17 Here, the completeness operator $\\sim$ must identify the non-classical, incomplete value. Its truth function is defined as $v(\\sim A) \= 1$ if $v(A) \\in \\{1, 0\\}$, and $v(\\sim A) \= 0$ if $v(A) \= n$. This ensures the validity of the gentle excluded middle axiom $\\sim A \\to (A \\lor \\lnot A)$. If $v(\\sim A) \= 1$, then $v(A)$ is classical, and $v(A \\lor \\lnot A) \= 1$. If $v(A) \= n$, then $v(\\sim A) \= 0$, making the axiom true by falsity of the antecedent.

### **Combined Systems: The Semantics of Paradefinite Logics**

The separate three-valued semantics for mbC and mbD are illuminating, but they each implicitly exclude the phenomenon modeled by the other; the LP-based semantics has no room for gaps, and the K3-based semantics has no room for gluts. A more general approach uses four-valued semantics, which can model logics that are simultaneously paraconsistent and paracomplete (often called paradefinite logics).

* **Belnap-Dunn Logic (FDE/BD):** As introduced previously, the four-valued logic FDE, with values {1, $b$, $n$, 0}, provides a natural semantic foundation for combined systems.5 This framework can accommodate both a consistency operator $\\circ$ and a completeness operator $\\sim$. In this setting, $\\circ A$ would be true if and only if $v(A)$ is not $b$, while $\\sim A$ would be true if and only if $v(A)$ is not $n$.  
* \*\*The Logic BD$\\circ$: An example of such a combined system is BD$\\circ$, an expansion of Belnap-Dunn logic with a consistency operator $\\copyright$. This system is particularly interesting because it demonstrates that in a sufficiently rich four-valued setting, the concepts of consistency and undeterminedness become interdefinable. The operator $\\copyright$ is designed to satisfy certain axioms, and from it, an undeterminedness operator can be defined, showcasing the deep connection between the two concepts within a unified semantic space.5 Another such rich system is PŁ4, a four-valued logic that is both paraconsistent and paracomplete and possesses great expressive power.30

The move to a four-valued semantics suggests that inconsistency and incompleteness are not mutually exclusive deviations from classicism but are orthogonal phenomena. A proposition's status can be plotted on two axes: one related to truth/falsity (the T/F axis) and another related to consistency/inconsistency (the B/N axis). The $\\circ$ operator navigates the glut dimension, while the $\\sim$ operator navigates the gap dimension. This implies that the LFI/LFU duality can be viewed not just as a choice between two opposing types of logic, but as two independent dimensions of non-classicality that can be explored separately or together within a more general framework.

### **Towards Unification: An Exploration of Swap Structures Semantics**

A more abstract and powerful semantic framework is that of **swap structures semantics**. This approach, originally developed for LFIs, can be adapted to provide semantics for LFUs and for combined Logics of Formal Inconsistency and Undeterminedness (LFIUs).20 Swap structures semantics is a non-deterministic framework that can prove the decidability of these systems by means of finite non-deterministic matrices. It offers a uniform method for modeling the recovery of classical properties governed by operators like $\\circ$ and $\\sim$, providing a sophisticated and unifying semantic perspective on the entire family of logics.20

## **Frontiers and Speculative Applications: Bounded Completeness**

The theoretical framework of Logics of Formal Undeterminedness, with its completeness operator $\\sim$, provides a robust tool for reasoning about informational gaps. However, the standard formulation is static: a proposition $A$ is either determined ($\\sim A$) or it is not. A speculative but highly promising extension, prompted by the user query, is to dynamize this concept by introducing **bounded completeness**. This would involve parameterizing the completeness operator with respect to finite resources, such as time, evidence, or computational steps. Such a "bounded paracomplete logic" would bridge the gap between the philosophical logic of indeterminacy and the applied formal methods of resource-sensitive reasoning, with significant potential applications in artificial intelligence, database theory, and formal epistemology.

### **Interpreting the Completeness Operator (\~) in Resource-Sensitive Contexts**

The core idea is to move from a monolithic completeness operator $\\sim$ to a family of indexed operators $\\sim\_r$, where $r$ is an element of some structure R representing available resources. The formula $\\sim\_r A$ would be interpreted as "$A$ is determined given resource $r$." The nature of these resources could vary depending on the application domain:

* **Computational Resources:** $r$ could represent a number of computational steps, a memory bound, or the depth of a proof search. $\\sim\_n A$ would mean "$A$ is decidable within $n$ steps."  
* **Temporal Resources:** $r$ could be a point in time. $\\sim\_t A$ would mean "The truth value of $A$ is known or fixed at time \`$t$."  
* **Evidential Resources:** $r$ could represent a set of available evidence or data sources. $\\sim\_e A$ would mean "$A$ is determined on the basis of evidence \`$e$."

This interpretation transforms the LFU from a logic that describes static gaps into one that can model the dynamic process of resolving those gaps as resources are acquired or expended.

### **Theoretical Sketch: A Bounded Paracomplete Logic**

A formal system for bounded completeness would augment a base paracomplete logic (like mbD) with the necessary machinery to handle indexed operators and their interactions.

* **Language:** The language would be that of an LFU, extended with a set of indexed unary operators $\\{\\sim\_r\\}\_{r \\in R}$, where R is a partially ordered set or other algebraic structure representing resources.  
* **Axiomatics:** The axiomatic system would include:  
  1. The axioms of the underlying paracomplete logic (e.g., CPL+ and Explosion).  
  2. **Bounded Gentle Excluded Middle:** An axiom schema of the form $\\sim\_r A \\to (A \\lor \\lnot A)$. This is the core recovery axiom, now relativized to a specific resource bound.  
  3. **Axioms Governing Resource Interaction:** These axioms would define the behavior of the resource structure. Drawing inspiration from substructural and modal logics, they could include:  
     * **Resource Monotonicity:** If $r \\le r'$ in the resource ordering, then $\\sim\_r A \\to \\sim\_{r'} A$. This captures the intuition that having more resources cannot make a proposition less determined.  
     * **Resource Compositionality:** Rules for how the operators interact with logical connectives. For example, one might propose an axiom like $(\\sim\_r A \\land \\sim\_s B) \\to \\sim\_{f(r,s)} (A \\land B)$, where $f$ is a function for combining resources (e.g., $r+s$). This is analogous to resource accounting in linear logic.25

### **Potential Applications in AI, Database Theory, and Formal Epistemology**

The development of such a logic would open up numerous application areas:

* **Artificial Intelligence and Knowledge Representation:** A bounded LFU could model the reasoning of a resource-bounded agent. An agent might initially treat a proposition $P$ as undetermined ($\\lnot \\sim\_0 P$), but after performing computations or observations (expending resources), it might come to know that $P$ is decidable and assert $\\sim\_n P$, thereby unlocking classical reasoning about $P$.  
* **Database Theory:** In the context of large, evolving databases, $\\sim\_v A$ could signify that the proposition $A$ is consistently determined (i.e., has a stable, non-gappy truth value) across all data sources up to version $v$ of the database.5 This would allow for reasoning about data stability and convergence over time.  
* **Formal Epistemology:** The framework could model the process of scientific inquiry. $\\sim\_e A$ could mean that proposition $A$ is decidable given the available evidence $e$. As new evidence $e'$ is gathered, the system could transition to a state where $\\sim\_{e \\cup e'} A$ holds, formally capturing the notion that scientific questions become settled as more data becomes available.

### **Open Questions and Directions for Future Research**

This proposal for bounded paracomplete logics is speculative and raises many important questions for future research:

1. **Proof Theory:** What is the appropriate proof-theoretic framework for such a logic? A resource-sensitive sequent calculus, perhaps drawing from labelled deductive systems or substructural logics, would be a natural candidate.  
2. **Semantics:** What is the corresponding model theory? This might involve a combination of possible-world semantics (to model epistemic states) and the algebraic semantics of resources.  
3. **Relationship to Other Formalisms:** What are the precise formal connections to existing logics, such as linear logic (for resource management), temporal logic (for time-based bounds), or justification logic (for evidence-based reasoning)?  
4. **Computational Complexity:** What are the decidability and complexity properties of these logics? The addition of indexed operators and resource axioms could significantly impact computational behavior.

By integrating the paracomplete framework of LFUs with the resource-consciousness of substructural logics, the concept of bounded completeness charts a course for a new class of dynamic epistemic logics. These logics would be capable not only of representing informational gaps but also of reasoning formally about the processes by which those gaps are filled.

## **Conclusion**

The duality between paraconsistency and paracompleteness represents one of the most fundamental bifurcations in non-classical logic, reflecting a deep philosophical choice between tolerating informational excess (gluts) and tolerating informational deficits (gaps). This report has demonstrated that the relationship between Logics of Formal Inconsistency (LFIs) and Logics of Formal Undeterminedness (LFUs) provides a sophisticated and powerful formalization of this duality.

The key innovation of these logical families is the internalization of meta-theoretic notions—consistency in the case of LFIs and completeness in the case of LFUs—into the object language via the dedicated operators $\\circ$ and $\\sim$. This allows for a conditional and fine-grained recovery of classical principles that are otherwise globally abandoned. The paraconsistent LFI mbC uses the consistency operator $\\circ$ to enable a "gentle" version of the Principle of Explosion, thereby recapturing classical reasoning for propositions known to be consistent. Dually, the paracomplete LFU mbD uses the completeness operator $\\sim$ to enable a "gentle" version of the Law of Excluded Middle, recapturing bivalence for propositions known to be determined.

The analysis of their axiomatic systems and, more pointedly, their expression within the symmetrical framework of sequent calculus, reveals this duality with striking clarity. The relationship between mbC and mbD mirrors the well-established proof-theoretic opposition between intuitionistic (LJ) and dual-intuitionistic (LDJ) logics, grounding the LFI/LFU duality in a broader and deeper logical tradition. The operators $\\circ$ and $\\sim$ function as powerful, language-immanent controls that locally modulate the structural rules governing inference, providing an unprecedented level of expressive control.

Finally, the speculative exploration of "bounded paracomplete logics" indicates a promising future direction for this research programme. By parameterizing the completeness operator with respect to resources like time, evidence, or computation, LFUs can be transformed from static systems for describing indeterminacy into dynamic logics capable of modeling the resolution of informational gaps. This extension would forge crucial links to resource-sensitive logics and open up significant applications in artificial intelligence, database theory, and formal epistemology. The study of the LFI-LFU duality is therefore not merely an exercise in formal symmetry; it is a gateway to developing more nuanced and powerful logical tools for reasoning in the complex, imperfect informational environments that characterize both human and artificial cognition.

#### **Works cited**

1. Contradiction \- Stanford Encyclopedia of Philosophy, accessed October 16, 2025, [https://plato.stanford.edu/entries/contradiction/](https://plato.stanford.edu/entries/contradiction/)  
2. Law of excluded middle \- Wikipedia, accessed October 16, 2025, [https://en.wikipedia.org/wiki/Law\_of\_excluded\_middle](https://en.wikipedia.org/wiki/Law_of_excluded_middle)  
3. Paraconsistent Logic | Internet Encyclopedia of Philosophy, accessed October 16, 2025, [https://iep.utm.edu/para-log/](https://iep.utm.edu/para-log/)  
4. Tutorial on Inconsistency-Adaptive Logics, accessed October 16, 2025, [https://www.clps.ugent.be/sites/default/files/publications/kolkataALtutorial\_1.pdf](https://www.clps.ugent.be/sites/default/files/publications/kolkataALtutorial_1.pdf)  
5. (PDF) On a four-valued logic of formal inconsistency and formal undeterminedness \- ResearchGate, accessed October 16, 2025, [https://www.researchgate.net/publication/366027187\_On\_a\_four-valued\_logic\_of\_formal\_inconsistency\_and\_formal\_undeterminedness](https://www.researchgate.net/publication/366027187_On_a_four-valued_logic_of_formal_inconsistency_and_formal_undeterminedness)  
6. Paraconsistent logic \- Wikipedia, accessed October 16, 2025, [https://en.wikipedia.org/wiki/Paraconsistent\_logic](https://en.wikipedia.org/wiki/Paraconsistent_logic)  
7. What is paraconsistent logic ? \- Jean-Yves Béziau, accessed October 16, 2025, [https://www.jyb-logic.org/wplb.pdf](https://www.jyb-logic.org/wplb.pdf)  
8. Paraconsistent Logic \- Stanford Encyclopedia of Philosophy, accessed October 16, 2025, [https://plato.stanford.edu/entries/logic-paraconsistent/](https://plato.stanford.edu/entries/logic-paraconsistent/)  
9. Module 1 \- Instantiatins on Paraconsistent Logics, accessed October 16, 2025, [https://www2.mta.ac.il/\~oarieli/SPLogIC-2023-Slides/m1-paraconsistency.pdf](https://www2.mta.ac.il/~oarieli/SPLogIC-2023-Slides/m1-paraconsistency.pdf)  
10. towards a philosophical understanding of the logics of formal inconsistency \- SciELO, accessed October 16, 2025, [https://www.scielo.br/j/man/a/ds9M9Kpfb6F679ZMvpxxjsj/?lang=en](https://www.scielo.br/j/man/a/ds9M9Kpfb6F679ZMvpxxjsj/?lang=en)  
11. What logics/philosophies deny the law of excluded middle (LEM)?, accessed October 16, 2025, [https://philosophy.stackexchange.com/questions/99812/what-logics-philosophies-deny-the-law-of-excluded-middle-lem](https://philosophy.stackexchange.com/questions/99812/what-logics-philosophies-deny-the-law-of-excluded-middle-lem)  
12. Paracomplete Logics Dual to the Genuine Paraconsistent Logics: The Three-valued Case, accessed October 16, 2025, [https://www.researchgate.net/publication/347146117\_Paracomplete\_Logics\_Dual\_to\_the\_Genuine\_Paraconsistent\_Logics\_The\_Three-valued\_Case](https://www.researchgate.net/publication/347146117_Paracomplete_Logics_Dual_to_the_Genuine_Paraconsistent_Logics_The_Three-valued_Case)  
13. (PDF) Logics of Formal Inconsistency \- ResearchGate, accessed October 16, 2025, [https://www.researchgate.net/publication/227047567\_Logics\_of\_Formal\_Inconsistency](https://www.researchgate.net/publication/227047567_Logics_of_Formal_Inconsistency)  
14. Sequent calculus \- Wikipedia, accessed October 16, 2025, [https://en.wikipedia.org/wiki/Sequent\_calculus](https://en.wikipedia.org/wiki/Sequent_calculus)  
15. Interactive Tutorial of the Sequent Calculus \- Logitext, accessed October 16, 2025, [http://logitext.mit.edu/tutorial](http://logitext.mit.edu/tutorial)  
16. Paracomplete logics which are dual to the paraconsistent logics L3A and L3B \- cle.unicamp.br, accessed October 16, 2025, [https://www.cle.unicamp.br/prof/coniglio/paper4.pdf](https://www.cle.unicamp.br/prof/coniglio/paper4.pdf)  
17. Mini-Course : Paraconsistent and Paracomplete Logics \- University of St Andrews, accessed October 16, 2025, [https://www.st-andrews.ac.uk/\~ac117/teaching/minicourse4.pdf](https://www.st-andrews.ac.uk/~ac117/teaching/minicourse4.pdf)  
18. An axiomatization of the paracomplete logic L3AD \- CEUR-WS.org, accessed October 16, 2025, [https://ceur-ws.org/Vol-2818/paper05.pdf](https://ceur-ws.org/Vol-2818/paper05.pdf)  
19. Intuitionistic Implication and Logics of Formal Inconsistency \- MDPI, accessed October 16, 2025, [https://www.mdpi.com/2075-1680/13/11/738](https://www.mdpi.com/2075-1680/13/11/738)  
20. Recovery operators, paraconsistency and duality \- cle.unicamp.br, accessed October 16, 2025, [https://www.cle.unicamp.br/prof/coniglio/Recovery.pdf](https://www.cle.unicamp.br/prof/coniglio/Recovery.pdf)  
21. View of Hybridized Paracomplete and Paraconsistent Logics \- Open Journal System, accessed October 16, 2025, [https://ojs.victoria.ac.nz/ajl/article/view/4035/3588](https://ojs.victoria.ac.nz/ajl/article/view/4035/3588)  
22. Sequent Calculus, accessed October 16, 2025, [https://www.cs.cmu.edu/\~fp/courses/atp/handouts/ch3-seqcalc.pdf](https://www.cs.cmu.edu/~fp/courses/atp/handouts/ch3-seqcalc.pdf)  
23. The Sequent Calculus \- Open Logic Project Builds, accessed October 16, 2025, [https://builds.openlogicproject.org/content/first-order-logic/sequent-calculus/sequent-calculus.pdf](https://builds.openlogicproject.org/content/first-order-logic/sequent-calculus/sequent-calculus.pdf)  
24. A Tutorial on Computational Classical Logic and the Sequent Calculus \- Paul Downen, accessed October 16, 2025, [https://pauldownen.com/publications/sequent-intro.pdf](https://pauldownen.com/publications/sequent-intro.pdf)  
25. Is there a category whose internal logic is paraconsistent? \- Mathematics Stack Exchange, accessed October 16, 2025, [https://math.stackexchange.com/questions/476186/is-there-a-category-whose-internal-logic-is-paraconsistent](https://math.stackexchange.com/questions/476186/is-there-a-category-whose-internal-logic-is-paraconsistent)  
26. Intuitionistic Dual-intuitionistic Nets \- Pages Professionnelles Individuelles de l'ENS de Lyon, accessed October 16, 2025, [https://perso.ens-lyon.fr/olivier.laurent/idn.pdf](https://perso.ens-lyon.fr/olivier.laurent/idn.pdf)  
27. Chapter 12: Gentzen Sequent Calculus for Intuitionistic Logic \- Stony Brook CS, accessed October 16, 2025, [https://www3.cs.stonybrook.edu/\~pfodor/courses/CSE371/slides12/12slides.pdf](https://www3.cs.stonybrook.edu/~pfodor/courses/CSE371/slides12/12slides.pdf)  
28. Sequent Calculus Primer, accessed October 16, 2025, [http://sakharov.net/sequent.html](http://sakharov.net/sequent.html)  
29. Dual-Intuitionistic Logic \- Project Euclid, accessed October 16, 2025, [https://projecteuclid.org/journals/notre-dame-journal-of-formal-logic/volume-37/issue-3/Dual-Intuitionistic-Logic/10.1305/ndjfl/1039886520.pdf](https://projecteuclid.org/journals/notre-dame-journal-of-formal-logic/volume-37/issue-3/Dual-Intuitionistic-Logic/10.1305/ndjfl/1039886520.pdf)  
30. Relational Semantics for the Paraconsistent and Paracomplete 4-valued Logic PŁ4, accessed October 16, 2025, [https://apcz.umk.pl/LLP/article/download/37930/32048](https://apcz.umk.pl/LLP/article/download/37930/32048)