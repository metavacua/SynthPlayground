;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;
;;;  Commutative Diagrams of Logical Languages
;;;
;;;  This file defines the core data structures for representing
;;;  and manipulating commutative diagrams of logical languages.
;;;  The goal is to create a framework that can automatically
;;;  construct missing vertices or morphisms in a given diagram,
;;;  effectively "solving" the diagram.
;;;
;;;  The key components are:
;;;
;;;  - `logical-language`: Represents a formal language with its
;;;    own syntax, axioms, and inference rules.
;;;
;;;  - `morphism`: Represents a mapping or transformation between
;;;    two logical languages.
;;;
;;;  - `diagram`: Represents the commutative diagram itself as a
;;;    graph of logical languages and morphisms.
;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defclass logical-language ()
  ((name :initarg :name :accessor name
         :documentation "The name of the logical language (e.g., 'Propositional Logic').")
   (syntax :initarg :syntax :accessor syntax
           :documentation "A list of valid connectives in the language (e.g., '(:and :or :not)).")
   (axioms :initarg :axioms :accessor axioms
           :documentation "A list of axioms, represented as formulas.")
   (inference-rules :initarg :rules :accessor rules
                    :documentation "A list of inference rules for the language.")))

(defclass morphism ()
  ((source :initarg :source :accessor source
           :documentation "The source logical language.")
   (target :initarg :target :accessor target
           :documentation "The target logical language.")
   (translation :initarg :translation :accessor translation
                :documentation "A function that translates a formula from the source to the target language.")))

(defclass diagram ()
  ((vertices :initarg :vertices :accessor vertices
             :documentation "A list of the logical languages in the diagram.")
   (edges :initarg :edges :accessor edges
          :documentation "A list of the morphisms between the logical languages.")))

(defun compute-pushout (morphism1 morphism2)
  "Computes the pushout of two morphisms sharing a common source.
   This constructs a new logical language by amalgamating the two target languages."
  (let* ((source-lang (source morphism1))
         (target-lang1 (target morphism1))
         (target-lang2 (target morphism2))
         (new-syntax (union (syntax target-lang1) (syntax target-lang2)))
         (new-axioms (union (axioms target-lang1) (axioms target-lang2) :test #'equal))
         (new-rules (union (rules target-lang1) (rules target-lang2) :test #'equal))
         (pushout-lang (make-instance 'logical-language
                                      :name (intern (format nil "PUSHOUT-~A-~A" (name target-lang1) (name target-lang2)))
                                      :syntax new-syntax
                                      :axioms new-axioms
                                      :rules new-rules)))
    (values pushout-lang
            (make-instance 'morphism :source target-lang1 :target pushout-lang :translation #'identity)
            (make-instance 'morphism :source target-lang2 :target pushout-lang :translation #'identity))))

(defun compute-pullback (morphism1 morphism2)
  "Computes the pullback of two morphisms sharing a common target.
   This constructs a new logical language representing the 'common ground'
   of the two source languages."
  (let* ((source-lang1 (source morphism1))
         (source-lang2 (source morphism2))
         (target-lang (target morphism1))
         (new-syntax (intersection (syntax source-lang1) (syntax source-lang2)))
         (new-axioms (intersection (axioms source-lang1) (axioms source-lang2) :test #'equal))
         (new-rules (intersection (rules source-lang1) (rules source-lang2) :test #'equal))
         (pullback-lang (make-instance 'logical-language
                                       :name (intern (format nil "PULLBACK-~A-~A" (name source-lang1) (name source-lang2)))
                                       :syntax new-syntax
                                       :axioms new-axioms
                                       :rules new-rules)))
    (values pullback-lang
            (make-instance 'morphism :source pullback-lang :target source-lang1 :translation #'identity)
            (make-instance 'morphism :source pullback-lang :target source-lang2 :translation #'identity))))

(defun solve-diagram (diagram)
  "Solves a commutative diagram with one missing component.
   The missing component should be represented by the symbol '?.
   This function will determine whether to compute a pushout or a pullback."
  (let ((unknown-vertex (find '? (vertices diagram) :key #'name)))
    (if unknown-vertex
        (let* ((known-edges (remove-if (lambda (edge)
                                         (or (eq (name (source edge)) '?)
                                             (eq (name (target edge)) '?)))
                                       (edges diagram))))
          (if (= (length known-edges) 2)
              (let ((morphism1 (first known-edges))
                    (morphism2 (second known-edges)))
                (cond
                  ((eq (source morphism1) (source morphism2))
                   (compute-pushout morphism1 morphism2))
                  ((eq (target morphism1) (target morphism2))
                   (compute-pullback morphism1 morphism2))
                  (t (error "The two known morphisms do not form a span or cospan."))))
              (error "Expected exactly two known edges to solve the diagram.")))
        (error "No unknown vertex found in the diagram."))))