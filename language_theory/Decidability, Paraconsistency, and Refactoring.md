

# **A Formal Analysis of Bifurcations within Decidability: Diagonalization, Arithmetization, and Paraconsistent Incompatibility**

## **Introduction: Framing the Hypothesis**

The foundational limitative theorems of mathematical logic, particularly those of Gödel and Tarski, have established a profound bifurcation in the landscape of formal systems: the division between decidable and undecidable theories. This report undertakes a formal investigation of a novel and more granular hypothesis concerning a bifurcation *within* the class of decidable—or recursive—languages themselves. The central proposition is that the entire class of decidable languages can be partitioned based on the definability, or lack thereof, of two fundamental metamathematical constructs: the diagonalization function, which underpins self-reference, and the apparatus of arithmetization, which enables a theory to represent its own syntax.

This inquiry is situated within the domain of computationally weaker systems, specifically those that do not define all recursive functions, a class of systems referred to herein as "Class 2". The proposed bifurcation posits two mutually exclusive classes of decidable systems:

1. A class of decidable systems in which the functions necessary for diagonalization are not definable.  
2. A class of decidable systems in which the functions implicit in a comprehensive Gödel numbering scheme are not definable.

It is further hypothesized that the relationship between these two classes is one of "paraconsistent compatibility or mutual inconsistency," suggesting a non-explosive form of logical incompatibility. This concept is elucidated through an appeal to "constructive contradictions," drawing an analogy to the principle of complementarity in quantum mechanics, where the construction of an experiment to measure one property precludes the simultaneous measurement of a complementary one.

The central research question of this report is therefore threefold: First, can the class of decidable languages be meaningfully partitioned based on the definability of these two constructs? Second, what is the precise logical nature of this partition, and do the concepts of paraconsistency and constructive contradiction accurately model it? Third, how robust is the analogy to quantum complementarity?

This investigation will proceed by first establishing the precise technical machinery required for both diagonalization and arithmetization. It will then test the proposed bifurcation against well-understood decidable theories of arithmetic. Finally, it will analyze the logical and philosophical dimensions of the hypothesis, scrutinizing the applicability of paraconsistent logic and the quantum analogy. The scope is confined to recursive languages, a refinement that correctly identifies the appropriate domain for computability-theoretic analysis.1 The focus on systems with inherent computational limitations, as distinct from powerful but incomplete theories like Peano Arithmetic, is essential for exploring the fine structure of decidability itself.2

---

## **Part I: The Pillars of the Bifurcation**

This part deconstructs the two core concepts upon which the proposed bifurcation rests: the definability of the diagonal function and the capacity for full arithmetization. A rigorous examination of the formal prerequisites for each will establish the technical basis for the subsequent analysis.

### **Chapter 1: Definability of the Diagonal Function and Fixed-Point Theorems**

The notion of a "diagonalization function" is central to the limitative theorems. Its formalization requires a precise understanding of how functions are enumerated and how self-reference is constructed within a formal system. This construction is most powerfully generalized by the Diagonal Lemma, which is a form of fixed-point theorem.

#### **1.1 The Mechanics of Diagonalization**

The diagonal argument, in its essence, relies on the ability to systematically list all functions within a certain class and then construct a new function that differs from every function on that list. This requires a formal system of indexing or enumeration.

##### **Indexing and Enumeration**

For a class of computable functions, such as the primitive recursive (p.r.) functions, an indexing scheme is an effective procedure that assigns a unique natural number (an index) to each program that computes a function in that class.3 Since many programs can compute the same function, a given function will typically have many indices.4 The crucial properties of such a scheme are that every program has a number, every number decodes into some program, and this decoding is an effective process.3 A standard approach is to use separate enumerations for functions of different arities, denoted by $f^k\_x$, which represents the $k$-ary function computed by the program with index $x$.4

##### **The Diagonal Function diag(x)**

Given an enumeration of all unary primitive recursive functions, $f^1\_0, f^1\_1, f^1\_2, \\dots$, one can construct a new function, diag(x), defined as:

$$\\text{diag}(x) \= f^1\_x(x) \+ 1$$

This function is intuitively effective and total. For any input $x$, one can decode the index $x$ to get the program for the function $f^1\_x$, run that program on the input $x$, and add one to the result.4 By its very construction, diag(x) cannot be a primitive recursive function. If it were, it would have to appear somewhere in the enumeration, say at index $j$, such that $\\text{diag}(x) \= f^1\_j(x)$ for all $x$. But for the specific input $x=j$, we would have $\\text{diag}(j) \= f^1\_j(j)$. According to the definition of diag, however, $\\text{diag}(j) \= f^1\_j(j) \+ 1$. This leads to the contradiction $f^1\_j(j) \= f^1\_j(j) \+ 1$. Therefore, diag(x) is not in the enumeration and is not primitive recursive.4 This classic result demonstrates that the class of intuitively effective total functions is strictly larger than the class of primitive recursive functions.3

#### **1.2 The Diagonal Lemma as a Fixed-Point Theorem**

The core mechanism of the diagonal argument is generalized and formalized in the Diagonal Lemma, which is more accurately described as a fixed-point theorem. It establishes the existence of self-referential sentences in any sufficiently strong formal theory.5

##### **Formal Statement**

The syntactic version of the Diagonal Lemma states that for any formal theory $T$ that is sufficiently strong (e.g., containing Robinson Arithmetic, Q) and for any formula $\\Psi(x)$ with one free variable $x$, there exists a sentence $\\theta$ such that:

$$T \\vdash \\theta \\leftrightarrow \\Psi(\\ulcorner\\theta\\urcorner)$$

Here, $\\ulcorner\\theta\\urcorner$ is the numeral corresponding to the Gödel number of the sentence $\\theta$.5 The sentence $\\theta$ can be understood as asserting, "I have the property $\\Psi$." This lemma is the engine behind the proofs of the theorems of Gödel, Rosser, and Tarski.9

##### **Required Machinery**

The proof of the Diagonal Lemma does not require the theory $T$ to define a single "diagonalization function" that maps $\\ulcorner\\Psi(x)\\urcorner$ to $\\ulcorner\\theta\\urcorner$. Instead, it requires a more fundamental capability: the theory must be able to **represent all primitive recursive functions**.10 Specifically, it must be able to represent the syntactic substitution function, $\\text{sub}(n, m)$, which takes the Gödel number $n$ of a formula $\\phi(x)$ and the Gödel number $m$ of a term $t$, and returns the Gödel number of the formula $\\phi(t)$.7 The ability to arithmetically represent this fundamental syntactic manipulation is the key prerequisite for constructing the fixed-point sentence $\\theta$.7

##### **Spectrum of Diagonal Lemmas**

The Diagonal Lemma is not a monolithic result. It exists in several forms with different logical strengths. There is a semantic version, which asserts the existence of a sentence $\\theta$ such that $\\theta \\leftrightarrow \\Psi(\\ulcorner\\theta\\urcorner)$ is true in the standard model of arithmetic ($\\mathbb{N}$), and a syntactic version, which asserts that this equivalence is provable in a given theory $T$.11 Furthermore, there are weak syntactic versions that only guarantee the consistency of adding such an equivalence to a theory.12 The semantic version of the Diagonal Lemma is logically equivalent to the semantic version of Tarski's Undefinability Theorem, highlighting the deep connection between self-reference and the limits of definability.12 This spectrum is crucial when analyzing weaker theories, as a theory might satisfy one version but not another.

#### **1.3 Broader Context: Recursion Theorems and Fixed Points**

The Diagonal Lemma is an instance of a more general principle of fixed points that appears in various forms across logic and computer science.

* **Kleene's Recursion Theorem:** In computability theory, the analogue of the Diagonal Lemma is Kleene's (second) recursion theorem. It states that for any total computable function $F$ that transforms program indices, there exists an index $e$ such that the program with index $e$ and the program with index $F(e)$ compute the same function.14 This can be interpreted as stating that it is impossible to write a program that modifies the extensional behavior of all other programs; there will always be a program that is a "fixed point" of the transformation.14 This theorem is fundamental for defining functions via recursive definitions in computability theory.  
* **Lawvere's Fixed-Point Theorem:** At a higher level of abstraction, Lawvere's fixed-point theorem captures the essence of all diagonalization arguments in a category-theoretic setting. It states that if there exists a surjective map $e: A \\to B^A$ (a map from a set $A$ onto the set of functions from $A$ to $B$), then every function $f: B \\to B$ must have a fixed point.15 The limitative theorems of Cantor, Gödel, and Tarski can all be seen as consequences of the contrapositive of Lawvere's theorem.15 This demonstrates that the capacity for self-reference leading to fixed points is a fundamental structural property not limited to arithmetic.

The crucial takeaway from this formal analysis is the distinction between the *definability of a specific diagonalization function* and a theory possessing the *property of the Diagonal Lemma*. The latter is the operative condition for the limitative theorems. This property does not hinge on defining a single, special-purpose function but on the broader capacity of the theory to represent all primitive recursive functions, which provides the necessary tools for manipulating syntax arithmetically. The proposed bifurcation, therefore, is more accurately framed as a division between theories that can represent all p.r. functions and those that cannot. The "Class 2" systems under consideration are precisely those that fall into the latter category.

### **Chapter 2: The Requisites of Arithmetization and Self-Reference**

Arithmetization, or Gödel numbering, is the second pillar of the proposed bifurcation. A common misconception is that this is merely a scheme for assigning unique numbers to symbols and formulas. In reality, it is a profound technique that allows a formal system to talk about its own structure, provided the system is sufficiently expressive.

#### **2.1 Gödel Numbering: More Than an Encoding**

A Gödel numbering scheme maps the syntactic elements of a formal language—symbols, terms, formulas, and proofs—to the natural numbers.16 However, for this mapping to be useful for self-reference, the theory itself must be able to arithmetically define or represent key syntactic properties and relations in terms of these numbers.

* **Syntactic Predicates:** A system capable of full arithmetization must be able to express, via formulas of arithmetic, predicates that capture syntactic notions. For example, there must be formulas Term(x), Formula(x), and Axiom(x) that are true if and only if the number $x$ is the Gödel number of a term, a formula, or an axiom, respectively.18  
* **Proof Predicate:** The most critical component is the proof predicate, often denoted Proof(x, y). This is a formula that holds if and only if $x$ is the Gödel number of a valid proof within the theory of the formula with Gödel number $y$.7 The ability to represent this relation is what allows a theory to formalize its own notion of provability, leading to the provability predicate Prov(y), which is defined as $\\exists x \\text{Proof}(x, y)$.

The existence of these representable predicates transforms a simple encoding into a powerful tool for metamathematical reasoning within the object theory itself.

#### **2.2 Tarski's Undefinability Theorem**

Tarski's theorem on the undefinability of truth is a direct and powerful consequence of a system possessing both the capacity for self-reference (via the Diagonal Lemma) and the expressive power to formalize its own semantics.20

* **The Liar Paradox Formalized:** The theorem's proof is a formalization of the classic liar paradox: "This sentence is false".21 Suppose a sufficiently strong theory of arithmetic $T$ could define its own truth predicate, i.e., there existed a formula True(x) such that for any sentence $\\phi$, $T \\vdash \\phi \\leftrightarrow \\text{True}(\\ulcorner\\phi\\urcorner)$. The Diagonal Lemma could then be applied to the formula $\\neg\\text{True}(x)$ to construct a sentence $L$ such that:  
  $$T \\vdash L \\leftrightarrow \\neg\\text{True}(\\ulcorner L \\urcorner)$$  
  This sentence $L$ asserts its own falsehood. From the definition of the True predicate, we must also have $T \\vdash L \\leftrightarrow \\text{True}(\\ulcorner L \\urcorner)$. Together, these two equivalences immediately yield a contradiction: $T \\vdash \\text{True}(\\ulcorner L \\urcorner) \\leftrightarrow \\neg\\text{True}(\\ulcorner L \\urcorner)$. Therefore, the initial assumption—that a truth predicate True(x) is definable within $T$—must be false.20  
* **Hierarchy of Languages:** A key corollary of Tarski's theorem is that the concept of truth for an object language can only be defined within a semantically richer metalanguage.20 Any system that is sufficiently rich to express its own syntax cannot also express its own semantics. This establishes a fundamental limitation on the scope of self-representation for formal languages.

The analysis of these two pillars reveals a deep and symbiotic relationship between them, which stands in contrast to the mutual exclusivity posited by the bifurcation hypothesis. The limitative theorems of Gödel and Tarski do not present diagonalization and arithmetization as opposing forces. Rather, they demonstrate that these capabilities are intertwined prerequisites for undecidability. Tarski's proof, for example, requires *both* the Diagonal Lemma (a tool for self-reference) and the (hypothesized) definability of a truth predicate (a feat of semantic arithmetization). It is the potent combination of a system's ability to refer to its own sentences and its ability to describe its own properties that pushes it over the threshold into undecidability.

This indicates that the proposed bifurcation may mischaracterize the underlying logical structure. Instead of being mutually exclusive options available to decidable systems, the capacities for full diagonalization and arithmetization appear to be co-requisites for undecidability. Consequently, the two classes D1 (no definable diagonalization) and D2 (no definable arithmetization) are unlikely to be distinct within the realm of weak, decidable theories. It is more probable that such theories fail to meet *both* conditions simultaneously, a conjecture that will be tested in the following section.

---

## **Part II: Testing the Bifurcation Against Decidable Arithmetics**

This part forms the empirical core of the report, subjecting the proposed bifurcation to scrutiny by analyzing well-established decidable theories of arithmetic. By examining whether these systems fall into one of the two hypothesized classes, we can assess the formal coherence and applicability of the proposed framework.

### **Chapter 3: A Landscape of Decidable Theories**

Before conducting the case studies, it is essential to establish precise definitions for the key properties of logical theories and to introduce the systems that will serve as our test cases.

#### **3.1 Defining Decidability and Completeness**

In formal logic, the concepts of decidability and completeness are distinct and must not be confused.2

* **Decidability:** A theory $T$ is **decidable** if the set of its theorems (i.e., the set of all sentences provable in $T$) is a recursive set. This means there exists an effective method, or algorithm, that can determine for any arbitrary formula whether it is a theorem of $T$ or not.2  
* **Completeness:** A theory $T$ is **complete** if for every closed formula (sentence) $\\phi$ in its language, either $T \\vdash \\phi$ or $T \\vdash \\neg\\phi$. A complete theory provides a verdict on every sentence in its language.18

A critical result connects these two properties: any recursively axiomatizable theory that is complete is also decidable.2 However, the converse is not true, and the properties are otherwise independent. A theory can be decidable but incomplete (e.g., the theory of algebraically closed fields, which does not specify a characteristic).24 Conversely, a theory can be complete but undecidable (e.g., the set of all true sentences of standard arithmetic, Th(ℕ;+,×), which is complete by definition but not recursively axiomatizable).2

#### **3.2 Presburger Arithmetic: The Theory of Addition**

Presburger arithmetic is the first-order theory of the natural numbers with only the addition operation. It serves as a canonical example of a decidable, yet non-trivial, theory of arithmetic.

* **Axiomatization and Properties:** The language of Presburger arithmetic consists of a constant 0, a successor function S, and a binary function \+.25 Its axioms formalize the properties of addition and include a full schema of induction for all formulas in its language.25 The resulting theory is consistent, complete, and, most importantly, **decidable**.25 The decidability of Presburger arithmetic is typically established through the method of quantifier elimination, which allows any formula to be transformed into an equivalent quantifier-free formula whose truth can be checked algorithmically.26  
* **Expressive Limits:** The decidability of Presburger arithmetic is a direct consequence of its limited expressive power. The theory **cannot define multiplication**.17 This single limitation has profound consequences: it means that Presburger arithmetic cannot represent all primitive recursive functions, as many of these (like exponentiation) require multiplication in their definition. Because it cannot represent all p.r. functions, it is too weak for Gödel's incompleteness theorems to apply.17 The sets of numbers definable within Presburger arithmetic are known as semilinear sets, which have a simple, periodic structure.25

#### **3.3 Skolem Arithmetic: The Theory of Multiplication**

Skolem arithmetic provides a complementary case study: the first-order theory of the natural numbers with only the multiplication operation.

* **Axiomatization and Properties:** The language of Skolem arithmetic consists of the multiplication operation (·) and equality.28 Its axioms capture properties like commutativity and associativity, as well as axioms that leverage the unique prime factorization of natural numbers.28 Unlike Presburger arithmetic, Skolem arithmetic is **incomplete**.29 However, it is **decidable**.28 Its decidability proof is highly non-trivial and is often achieved by demonstrating an isomorphism between the structure $(\\mathbb{N}^{\>0}, \\cdot)$ and the structure of finite sequences of natural numbers under pointwise addition. The decidability of the latter structure can then be established via the Feferman-Vaught theorem, which effectively reduces the problem to the decidability of Presburger arithmetic applied to the exponents of the prime factors.28  
* **Expressive Limits:** Similar to Presburger arithmetic, the decidability of Skolem arithmetic stems from what it *cannot* express. The theory **cannot define addition**.28 Consequently, it cannot represent all primitive recursive functions. The sets definable in Skolem arithmetic are known as "semiskolemian" sets, whose definitions are characterized by applying Presburger formulas to the exponents in the prime factorizations of numbers.29 If the language of Skolem arithmetic is extended with an ordering predicate ($\<$) or a successor function, addition becomes definable, and the theory immediately becomes undecidable, equivalent in power to full Peano arithmetic.28

These two theories provide ideal test cases. Both are decidable theories of arithmetic, falling squarely within the domain of the user's hypothesis. Yet they achieve decidability by excluding complementary arithmetic operations, resulting in fundamentally different expressive limitations.

### **Chapter 4: Locating the Bifurcation: Case Studies**

This chapter applies the formal criteria established in Part I to the decidable theories of Presburger and Skolem arithmetic to determine if they conform to the proposed bifurcation.

#### **4.1 Analysis of Presburger Arithmetic**

* **Diagonalization:** As established in Chapter 1, the property of the Diagonal Lemma holding for a theory $T$ depends on $T$'s ability to represent all primitive recursive functions, particularly the substitution function sub(x, y). Presburger arithmetic cannot define multiplication, which is a prerequisite for defining the Gödel numbering schemes and syntactic manipulation functions like sub.17 Without the ability to represent these functions, the proof of the Diagonal Lemma cannot be carried out within the theory. Therefore, the Diagonal Lemma does not hold for Presburger Arithmetic.12 According to the proposed framework, this places Presburger arithmetic in **Class D1**, the class of decidable systems where the diagonalization function is not definable.  
* **Arithmetization:** The same expressive limitation prevents Presburger arithmetic from supporting a complete arithmetization of its syntax. The inability to represent all p.r. functions means that crucial syntactic predicates, most notably the Proof(x, y) predicate, cannot be defined within the theory. The system lacks the power to reason about its own provability in any meaningful way. Consequently, Presburger arithmetic also falls into **Class D2**, the class of decidable systems where the functions for a complete arithmetization are not definable.

#### **4.2 Analysis of Skolem Arithmetic**

* **Diagonalization:** The analysis for Skolem arithmetic is analogous. It cannot define addition, which is also a necessary component for representing the full class of primitive recursive functions.28 The functions required for Gödel's intricate coding of syntax rely on both addition and multiplication. Without addition, the theory cannot represent the substitution function, and the Diagonal Lemma does not hold. Skolem arithmetic therefore belongs to **Class D1**.  
* **Arithmetization:** For the same reason, Skolem arithmetic cannot achieve a full arithmetization of its syntax and proof theory. It lacks the expressive power to define the Proof(x, y) predicate and thus cannot engage in the kind of self-reference that characterizes undecidable theories. This places Skolem arithmetic firmly in **Class D2**.

#### **4.3 Comparative Analysis and the Proposed Table**

The case studies of Presburger and Skolem arithmetic yield a clear and decisive result that directly challenges the central premise of the bifurcation hypothesis. The hypothesis posits that the two conditions—the absence of definable diagonalization and the absence of definable arithmetization—are mutually exclusive, partitioning the space of decidable languages. The analysis demonstrates the opposite: for these canonical decidable theories of arithmetic, both conditions are met simultaneously. They are not in Class D1 *xor* Class D2; they are in Class D1 *and* Class D2.

This finding suggests that the proposed bifurcation is not a feature of decidable systems but rather a mischaracterization of the threshold for undecidability. The capacities for diagonalization (via the Diagonal Lemma) and full arithmetization are not opposing properties between which a system can choose. Instead, they are co-arising capabilities that emerge together once a theory crosses a certain threshold of expressive power—namely, the ability to represent all primitive recursive functions. Theories that remain below this threshold, like Presburger and Skolem arithmetic, lack both capabilities and can therefore be decidable. Theories that cross this threshold, like Robinson Arithmetic (Q) and Peano Arithmetic (PA), possess both capabilities and are consequently undecidable and incomplete.

The true bifurcation is not *within* decidability, but is the classical one *between* decidable and undecidable systems, now reframed in terms of these specific technical capacities. The following table synthesizes these findings, providing a clear comparative overview.

| Theory | Language | Decidable? | Complete? | Represents all PR Functions? | Diagonal Lemma Holds? | Falls into D1? | Falls into D2? |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Presburger Arithmetic | $(\\mathbb{N}; \+)$ | Yes | Yes | No | No | Yes | Yes |
| Skolem Arithmetic | $(\\mathbb{N}; \\times)$ | Yes | No | No | No | Yes | Yes |
| Robinson Arithmetic (Q) | $(\\mathbb{N}; S, \+, \\times)$ | No | No | Yes | Yes | No | No |
| Peano Arithmetic (PA) | $(\\mathbb{N}; S, \+, \\times, \\text{Ind})$ | No | No | Yes | Yes | No | No |

This table visually confirms the central conclusion of this section. The decidable theories (Presburger, Skolem) are characterized by the absence of both key properties, placing them in D1 and D2. The undecidable theories (Q, PA) are characterized by the presence of both, placing them in neither. This demonstrates that the proposed bifurcation based on mutual exclusivity is not supported by these foundational systems.

---

## **Part III: Logical and Philosophical Dimensions**

While the formal analysis in Part II challenges the proposed bifurcation, the user's query contains deeper philosophical and analogical claims about the nature of this incompatibility. This part addresses these more abstract dimensions, evaluating the applicability of paraconsistent logic and the analogy to quantum mechanics.

### **Chapter 5: Paraconsistency and the Nature of Incompatibility**

The suggestion that the relationship between the two definability conditions is "paraconsistently compatible" is a sophisticated one. It implies that their incompatibility is not of the explosive kind found in classical logic, where a contradiction entails triviality.

#### **5.1 Introduction to Paraconsistent Logic**

A paraconsistent logic is, by definition, any logical system that rejects the *principle of explosion*, also known as *ex contradictione quodlibet* ($A, \\neg A \\vdash B$).34 By invalidating this principle, paraconsistent logics allow for the existence of theories that are inconsistent (i.e., contain a contradiction) but are not trivial (i.e., do not prove every sentence).37 This is a crucial feature for reasoning with conflicting information, such as in large databases, legal systems, or scientific theory change.36

It is important to distinguish paraconsistency from **dialetheism**. Dialetheism is the metaphysical thesis that there are true contradictions.37 Paraconsistency is a logical property of an inference system. One can adopt a paraconsistent logic for purely pragmatic or epistemological reasons—as a tool for managing conflicting evidence or beliefs—without committing to the existence of true contradictions in reality.35

#### **5.2 Logics of Formal Inconsistency (LFIs)**

Among the many families of paraconsistent logics, the Logics of Formal Inconsistency (LFIs) are particularly relevant to this discussion. LFIs are a class of paraconsistent logics that internalize the notion of consistency at the object-language level through a dedicated consistency operator, typically denoted o.38

* **Gentle Explosion:** Instead of rejecting explosion outright, LFIs replace it with a controlled version called the **principle of gentle explosion**. This principle states that a contradiction A, ¬A leads to triviality only in a context that is explicitly marked as consistent, oA. Formally:  
  $$\\circ A, A, \\neg A \\vdash B$$  
  while $A, \\neg A \\not\\vdash B$ in general.39 This allows an LFI to reason paraconsistently by default but to restore classical, explosive reasoning in domains known or assumed to be consistent. This feature is sometimes called "recapturing classical logic".34

#### **5.3 Modeling the Bifurcation Paraconsistently**

The LFI framework provides a powerful tool for formally modeling the user's intuition about a "constructive contradiction." While the analysis in Part II showed that for decidable systems, the properties of definable diagonalization (Def\_Diag) and definable arithmetization (Def\_Arith) are both absent rather than mutually exclusive, we can use an LFI to model the logical structure at the *boundary* of decidability.

The limitative theorems establish that any recursively axiomatizable, consistent theory $T$ that possesses both Def\_Diag (in the sense of having the Diagonal Lemma) and Def\_Arith (in the sense of representing its own proof predicate) is undecidable. Let us denote the conjunction of these two properties as U\_prop (for "undecidability property"). The core result is thus:

$$U\_{\\text{prop}}(T) \\rightarrow \\text{Undecidable}(T)$$

The systems under consideration are, by hypothesis, decidable. Therefore, for any such system $T$:

$$\\text{Decidable}(T) \\rightarrow \\neg U\_{\\text{prop}}(T)$$

The "constructive contradiction" arises when one considers a hypothetical system that is both decidable and possesses U\_prop. In classical metatheory, the statement "There exists a theory $T$ such that $\\text{Decidable}(T) \\land U\_{\\text{prop}}(T)$" is a contradiction that implies anything.  
An LFI provides a more nuanced way to handle this. We can interpret the user's claim within a metatheory governed by an LFI. Let o(T) represent the proposition "T is a consistent, decidable theory." The limitative results can be framed as a metatheoretic axiom: o(T) \-\> ¬U\_prop(T). In this framework, if we were to encounter a theory $T^\*$ for which we had evidence for both Def\_Diag(T\*) and Def\_Arith(T\*) (i.e., for U\_prop(T\*)), we would not conclude that our metatheory is trivial. Instead, from the premises U\_prop(T\*) and o(T\*) \-\> ¬U\_prop(T\*), we would infer ¬o(T\*). This conclusion—that $T^\*$ cannot be a consistent, decidable theory—is precisely what Gödel's theorem shows. The LFI framework thus prevents the contradiction from being explosive and instead channels the reasoning toward a specific, constructive refutation of the system's assumed properties.

This demonstrates that the paraconsistent framing is not a literal description of the internal logic of Presburger arithmetic, but a sophisticated and coherent metatheoretic stance for reasoning about the boundaries of decidability and the nature of limitative results. It provides a formal language for the user's notion of "constructive contradiction," where two individually constructible properties (decidability and full expressiveness) are shown to be mutually incompatible in any single system.

### **Chapter 6: The Quantum Analogy: Complementarity and Definability**

The final component of the hypothesis is the analogy between the proposed logical bifurcation and the principle of complementarity in quantum mechanics. This analogy posits that the choice to define one construct (e.g., diagonalization) precludes the ability to define the other (e.g., arithmetization), much as measuring a particle's position precludes a simultaneous measurement of its momentum.

#### **6.1 Bohr's Principle of Complementarity**

Niels Bohr's principle of complementarity is a cornerstone of the Copenhagen interpretation of quantum mechanics. It asserts that quantum objects possess pairs of complementary properties that cannot be simultaneously observed or measured with arbitrary precision.42 The classic example is wave-particle duality: an experimental setup designed to measure the particle-like properties of a photon (e.g., its path through a slit) will necessarily obscure its wave-like properties (e.g., its interference pattern), and vice versa.45

This is not a statement about technological limitation but a fundamental feature of nature, mathematically formalized in the non-commutation of operators corresponding to incompatible observables, such as position and momentum.43 The choice of the measurement apparatus is not passive; it actively participates in the constitution of the phenomenon being observed.

#### **6.2 Evaluating the Analogy**

The proposed analogy maps the choice of measurement apparatus to the choice of axioms for a formal system. The claim is that choosing axioms that enable the definability of diagonalization (Def\_Diag) is a "measurement" that precludes the definability of arithmetization (Def\_Arith), and vice versa.

As demonstrated conclusively in Parts I and II, this specific formulation of the analogy is formally unsound. Def\_Diag (via the Diagonal Lemma) and Def\_Arith are not complementary, mutually exclusive properties that a system designer can choose between. They are co-arising properties that emerge in tandem when a system achieves a sufficient level of expressive power—namely, the ability to represent all primitive recursive functions. A system is either too weak to have either (and can be decidable) or strong enough to have both (and is undecidable). There is no trade-off between them.

#### **6.3 A Refined Analogy: Decidability as a Complementary Property**

Despite the flaw in the initial formulation, the intuition of a fundamental trade-off in formal systems that mirrors quantum complementarity is a powerful one. A more robust and formally sound analogy can be constructed not between two types of expressive power, but between **expressive power** and **decidability**.

Let us define "Expressive Power" ($EP$) as the capacity of a theory to represent all recursive functions. As shown, this capacity is the gateway to both the Diagonal Lemma and full arithmetization. Let us define "Decidability" ($D$) as the property that the set of theorems is recursive.

With these definitions, the limitative theorems of logic reveal a genuine complementarity:

1. **High Expressive Power $\\rightarrow$ No Decidability:** For any consistent, recursively axiomatizable theory $T$, if $EP(T)$ is true (the theory can represent all recursive functions), then Gödel's first incompleteness theorem applies. A direct consequence of this is Church's theorem, which states that such a theory is undecidable. Thus, $EP(T) \\rightarrow \\neg D(T)$.  
2. **Decidability $\\rightarrow$ Limited Expressive Power:** Conversely, the decidable theories we have examined, such as Presburger and Skolem arithmetic, achieve their decidability precisely because of their limited expressive power. Their inability to represent all recursive functions is not an incidental flaw but the very condition of their decidability. Thus, for these systems, $D(T) \\rightarrow \\neg EP(T)$.

This establishes a genuine, mutually exclusive relationship between these two properties for any given formal system. One can construct a system to have high expressive power (like Peano Arithmetic) or to be decidable (like Presburger Arithmetic), but not both. The "measurement" is the choice of axioms. Axiomatizing for full arithmetic expressiveness (including both addition and multiplication) constitutes a "measurement" of $EP$ that irrevocably "collapses" the system into a state of non-decidability. Axiomatizing for decidability requires deliberately restricting the language to prevent full expressiveness.

This refined analogy is formally sound and captures the spirit of the user's intuition about a "constructive contradiction." The two alternatives—a system with full arithmetic expressiveness or a decidable system—are individually constructible, but their composition in a single, consistent, axiomatizable system is impossible. This is a deep structural feature of formal systems that bears a striking resemblance to the complementary nature of physical reality at the quantum level.

---

## **Conclusion: Synthesis and Avenues for Future Research**

This report has conducted a rigorous formal analysis of the hypothesis that the class of decidable languages can be bifurcated based on the mutually exclusive definability of the diagonalization function and the apparatus of arithmetization. The investigation has yielded several key conclusions that both challenge and refine the initial proposition.

The central finding is that the proposed bifurcation, as originally formulated, is not supported by an analysis of canonical decidable theories of arithmetic. The capacities for diagonalization (as embodied by the Diagonal Lemma) and for full arithmetization are not mutually exclusive alternatives for decidable systems. Rather, they are deeply intertwined, co-arising properties that emerge together once a formal system crosses the expressive threshold of being able to represent all primitive recursive functions. Systems below this threshold, such as Presburger and Skolem arithmetic, lack *both* capabilities and can be decidable. Systems at or above this threshold, such as Robinson and Peano arithmetic, possess *both* capabilities and are consequently undecidable. The true bifurcation revealed by these constructs is the classical one between decidable and undecidable theories, albeit viewed through the lens of their specific representational power.

However, the more abstract and philosophical components of the hypothesis have proven to be highly insightful. The notion of a "paraconsistently compatible" or "constructive" contradiction, while not a literal description of the logic within Presburger arithmetic, serves as a powerful metatheoretic framework. Using a Logic of Formal Inconsistency (LFI), one can formally model the limitative results in a non-explosive manner. The "contradiction" of a system being simultaneously decidable and fully expressive does not lead to triviality but to the specific, constructive conclusion that such a system cannot be consistent and decidable, which is precisely the content of the incompleteness and undecidability theorems.

Similarly, the analogy to quantum complementarity, though flawed in its initial mapping, becomes remarkably robust when refined. The fundamental trade-off is not between two forms of expression but between **expressive power** and **decidability**. A formal system can be designed to possess one of these properties, but the choice to realize one precludes the realization of the other. This captures the essence of complementarity: two properties, individually coherent, that cannot be simultaneously actualized within a single system.

In summary, while the specific mechanism of the proposed bifurcation is not formally sustained, the underlying intuitions about non-classical incompatibility and fundamental trade-offs at the limits of formal systems are both valid and profound. This investigation validates these intuitions by re-framing them with greater formal precision.

Avenues for future research could proceed in several directions. One could investigate whether there exist non-standard or exotic decidable computational models that might conform more closely to the original bifurcation hypothesis. Another promising path is the further development of the LFI-based metatheory of formal systems, exploring how different paraconsistent logics can model the various limitative theorems. Finally, the formal connections between logical independence and physical complementarity, as suggested by the refined analogy, warrant deeper exploration, potentially bridging concepts from proof theory and theoretical physics.

#### **Works cited**

1. Computability theory \- Wikipedia, accessed October 25, 2025, [https://en.wikipedia.org/wiki/Computability\_theory](https://en.wikipedia.org/wiki/Computability_theory)  
2. Decidability (logic) \- Wikipedia, accessed October 25, 2025, [https://en.wikipedia.org/wiki/Decidability\_(logic)](https://en.wikipedia.org/wiki/Decidability_\(logic\))  
3. Indexing and Diagonalization over Prim \- andrew.cmu.ed, accessed October 25, 2025, [https://www.andrew.cmu.edu/user/kk3n/complearn/chapter3.pdf](https://www.andrew.cmu.edu/user/kk3n/complearn/chapter3.pdf)  
4. Indexing and Diagonalization \- andrew.cmu.ed, accessed October 25, 2025, [https://www.andrew.cmu.edu/user/kk3n/recursionclass/chap3.pdf](https://www.andrew.cmu.edu/user/kk3n/recursionclass/chap3.pdf)  
5. Diagonal lemma \- Wikipedia, accessed October 25, 2025, [https://en.wikipedia.org/wiki/Diagonal\_lemma](https://en.wikipedia.org/wiki/Diagonal_lemma)  
6. Fixed-point theorem \- Wikipedia, accessed October 25, 2025, [https://en.wikipedia.org/wiki/Fixed-point\_theorem](https://en.wikipedia.org/wiki/Fixed-point_theorem)  
7. A REVIEW OF SEVERAL FIXED-POINT THEOREMS, WITH APPLICATIONS 1\. Introduction Let us work in the usual language of arithmetic { \+,, accessed October 25, 2025, [https://users.ox.ac.uk/\~sfop0114/lehre/pdf/A%20review%20of%20several%20fixed-point%20theorems.pdf](https://users.ox.ac.uk/~sfop0114/lehre/pdf/A%20review%20of%20several%20fixed-point%20theorems.pdf)  
8. a review of the g¨odel fixed-point theorem with generalizations and applications \- Joel David Hamkins, accessed October 25, 2025, [https://jdh.hamkins.org/wp-content/uploads/A-review-of-several-fixed-point-theorems-1.pdf](https://jdh.hamkins.org/wp-content/uploads/A-review-of-several-fixed-point-theorems-1.pdf)  
9. (PDF) ON THE DIAGONAL LEMMA OF GÖDEL AND CARNAP \- ResearchGate, accessed October 25, 2025, [https://www.researchgate.net/publication/342116883\_ON\_THE\_DIAGONAL\_LEMMA\_OF\_GODEL\_AND\_CARNAP](https://www.researchgate.net/publication/342116883_ON_THE_DIAGONAL_LEMMA_OF_GODEL_AND_CARNAP)  
10. Diagonal Lemma justification \- Mathematics Stack Exchange, accessed October 25, 2025, [https://math.stackexchange.com/questions/160865/diagonal-lemma-justification](https://math.stackexchange.com/questions/160865/diagonal-lemma-justification)  
11. Carnap and the Diagonalization Lemma (Continued) \- \- Logic Matters, accessed October 25, 2025, [https://www.logicmatters.net/2012/01/09/carnap-and-the-diagonalization-lemma-continued/](https://www.logicmatters.net/2012/01/09/carnap-and-the-diagonalization-lemma-continued/)  
12. The Diagonalization Lemma Demystified Hopefully \- Saeed Salehi, accessed October 25, 2025, [https://saeedsalehi.ir/pdf/conf/Tubingen-2021.pdf](https://saeedsalehi.ir/pdf/conf/Tubingen-2021.pdf)  
13. Diagonal-Free Proofs of the Diagonal Lemma Saeed Salehi University of Tabriz & IPM \- Wormshop 2017, accessed October 25, 2025, [https://wrm17.mi-ras.ru/slides/Salehi.pdf](https://wrm17.mi-ras.ru/slides/Salehi.pdf)  
14. Kleene's recursion theorem \- Wikipedia, accessed October 25, 2025, [https://en.wikipedia.org/wiki/Kleene%27s\_recursion\_theorem](https://en.wikipedia.org/wiki/Kleene%27s_recursion_theorem)  
15. ON FIXED-POINT THEOREMS IN SYNTHETIC COMPUTABILITY A fixed point theorem of Lawvere's \[12, Theorem 1.1\] is the quintessential \- Mathematics and Computation, accessed October 25, 2025, [https://math.andrej.com/asset/data/recursion-theorem.pdf](https://math.andrej.com/asset/data/recursion-theorem.pdf)  
16. Diagonalization and the Diagonal Lemma \- M-Phi, accessed October 25, 2025, [http://m-phi.blogspot.com/2012/03/diagonalization-and-diagonal-lemma.html](http://m-phi.blogspot.com/2012/03/diagonalization-and-diagonal-lemma.html)  
17. Gödel's incompleteness theorems \- Wikipedia, accessed October 25, 2025, [https://en.wikipedia.org/wiki/G%C3%B6del%27s\_incompleteness\_theorems](https://en.wikipedia.org/wiki/G%C3%B6del%27s_incompleteness_theorems)  
18. Gödel's Incompleteness Theorems \- Stanford Encyclopedia of Philosophy, accessed October 25, 2025, [https://plato.stanford.edu/entries/goedel-incompleteness/](https://plato.stanford.edu/entries/goedel-incompleteness/)  
19. An Open Introduction to Gödel's Theorems \- Incompleteness and Computability, accessed October 25, 2025, [https://ic.openlogicproject.org/ic-screen.pdf](https://ic.openlogicproject.org/ic-screen.pdf)  
20. Tarski's undefinability theorem \- Wikipedia, accessed October 25, 2025, [https://en.wikipedia.org/wiki/Tarski%27s\_undefinability\_theorem](https://en.wikipedia.org/wiki/Tarski%27s_undefinability_theorem)  
21. Alfred Tarski \- Stanford Encyclopedia of Philosophy, accessed October 25, 2025, [https://plato.stanford.edu/entries/tarski/](https://plato.stanford.edu/entries/tarski/)  
22. Part II: Typed Truth and Tarski's Hierarchy \- Lavinia Picollo, accessed October 25, 2025, [http://fitelson.org/piksi/piksi\_18/picollo\_notes.pdf](http://fitelson.org/piksi/piksi_18/picollo_notes.pdf)  
23. Weak Theories and Essential Incompleteness, accessed October 25, 2025, [https://www1.cuni.cz/\~svejdar/papers/sv\_ybk07.pdf](https://www1.cuni.cz/~svejdar/papers/sv_ybk07.pdf)  
24. Example of incomplete, but decidable theory, and of complete and undecidable theory, question \- Mathematics Stack Exchange, accessed October 25, 2025, [https://math.stackexchange.com/questions/3017207/example-of-incomplete-but-decidable-theory-and-of-complete-and-undecidable-the](https://math.stackexchange.com/questions/3017207/example-of-incomplete-but-decidable-theory-and-of-complete-and-undecidable-the)  
25. Presburger arithmetic \- Wikipedia, accessed October 25, 2025, [https://en.wikipedia.org/wiki/Presburger\_arithmetic](https://en.wikipedia.org/wiki/Presburger_arithmetic)  
26. A Survival Guide to Presburger Arithmetic \- University of Oxford Department of Computer Science, accessed October 25, 2025, [https://www.cs.ox.ac.uk/people/christoph.haase/home/publication/haa-18/haa-18.pdf](https://www.cs.ox.ac.uk/people/christoph.haase/home/publication/haa-18/haa-18.pdf)  
27. Weak Systems of Arithmetic | The n-Category Café, accessed October 25, 2025, [https://golem.ph.utexas.edu/category/2011/10/weak\_systems\_of\_arithmetic.html](https://golem.ph.utexas.edu/category/2011/10/weak_systems_of_arithmetic.html)  
28. Skolem arithmetic \- Wikipedia, accessed October 25, 2025, [https://en.wikipedia.org/wiki/Skolem\_arithmetic](https://en.wikipedia.org/wiki/Skolem_arithmetic)  
29. lo.logic \- What are the definable sets in Skolem arithmetic ..., accessed October 25, 2025, [https://mathoverflow.net/questions/316546/what-are-the-definable-sets-in-skolem-arithmetic](https://mathoverflow.net/questions/316546/what-are-the-definable-sets-in-skolem-arithmetic)  
30. Definable sets in Skolem arithmetic \- arXiv, accessed October 25, 2025, [https://arxiv.org/html/2510.02062v1](https://arxiv.org/html/2510.02062v1)  
31. first order logic \- Decidability of Skolem arithmetic via the Feferman ..., accessed October 25, 2025, [https://math.stackexchange.com/questions/4989028/decidability-of-skolem-arithmetic-via-the-feferman-vaught-theorem](https://math.stackexchange.com/questions/4989028/decidability-of-skolem-arithmetic-via-the-feferman-vaught-theorem)  
32. Definability of arithmetic functions and relations \- MathOverflow, accessed October 25, 2025, [https://mathoverflow.net/questions/178864/definability-of-arithmetic-functions-and-relations](https://mathoverflow.net/questions/178864/definability-of-arithmetic-functions-and-relations)  
33. Undecidable extensions of Skolem arithmetic | The Journal of Symbolic Logic, accessed October 25, 2025, [https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/undecidable-extensions-of-skolem-arithmetic/652C70229877D78E1ABE445B4491D912](https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/undecidable-extensions-of-skolem-arithmetic/652C70229877D78E1ABE445B4491D912)  
34. (PDF) Logics of Formal Inconsistency \- ResearchGate, accessed October 25, 2025, [https://www.researchgate.net/publication/227047567\_Logics\_of\_Formal\_Inconsistency](https://www.researchgate.net/publication/227047567_Logics_of_Formal_Inconsistency)  
35. Paraconsistent Logic | Internet Encyclopedia of Philosophy, accessed October 25, 2025, [https://iep.utm.edu/para-log/](https://iep.utm.edu/para-log/)  
36. Paraconsistent logic \- Wikipedia, accessed October 25, 2025, [https://en.wikipedia.org/wiki/Paraconsistent\_logic](https://en.wikipedia.org/wiki/Paraconsistent_logic)  
37. Paraconsistent Logic \- Stanford Encyclopedia of Philosophy, accessed October 25, 2025, [https://plato.stanford.edu/entries/logic-paraconsistent/](https://plato.stanford.edu/entries/logic-paraconsistent/)  
38. TOWARDS A PHILOSOPHICAL UNDERSTANDING ... \- SciELO Brasil, accessed October 25, 2025, [https://www.scielo.br/j/man/a/ds9M9Kpfb6F679ZMvpxxjsj/?lang=en](https://www.scielo.br/j/man/a/ds9M9Kpfb6F679ZMvpxxjsj/?lang=en)  
39. Intuitionistic Implication and Logics of Formal Inconsistency \- MDPI, accessed October 25, 2025, [https://www.mdpi.com/2075-1680/13/11/738](https://www.mdpi.com/2075-1680/13/11/738)  
40. Logics of Formal Inconsistency, accessed October 25, 2025, [https://iiitd.ac.in/moh/student\_presentations/EshaJain.pdf](https://iiitd.ac.in/moh/student_presentations/EshaJain.pdf)  
41. A survey of inconsistency-adaptive logics \- UGent personal websites, accessed October 25, 2025, [https://users.ugent.be/\~dbatens/publ/A2000D\_surv-ial.pdf](https://users.ugent.be/~dbatens/publ/A2000D_surv-ial.pdf)  
42. Experimental analysis of the quantum complementarity principle | Phys. Rev. A, accessed October 25, 2025, [https://link.aps.org/doi/10.1103/PhysRevA.85.032121](https://link.aps.org/doi/10.1103/PhysRevA.85.032121)  
43. Complementarity (physics) \- Wikipedia, accessed October 25, 2025, [https://en.wikipedia.org/wiki/Complementarity\_(physics)](https://en.wikipedia.org/wiki/Complementarity_\(physics\))  
44. Complementarity principle | Quantum mechanics, Wave-particle duality, Uncertainty | Britannica, accessed October 25, 2025, [https://www.britannica.com/science/complementarity-principle](https://www.britannica.com/science/complementarity-principle)  
45. Complementarity principle \- (Principles of Physics III) \- Vocab, Definition, Explanations | Fiveable, accessed October 25, 2025, [https://fiveable.me/key-terms/principles-physics-iii-thermal-physics-waves/complementarity-principle](https://fiveable.me/key-terms/principles-physics-iii-thermal-physics-waves/complementarity-principle)