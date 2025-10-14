;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;
;;;  Example and Test for the Automated Logic Construction System
;;;
;;;  This file demonstrates how to use the `solve-diagram` function
;;;  to automatically construct a new logical language from a
;;;  commutative diagram with a missing component.
;;;
;;;  The example constructs a simple diagram with three languages
;;;  and two morphisms, leaving the fourth language as an unknown
;;;  to be solved by the system.
;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(load "commutative-diagram.lisp")

(defun run-pushout-test ()
  "Tests the pushout construction."
  (let* ((lang1 (make-instance 'logical-language :name 'L1 :syntax '(:not) :axioms '((p (not p))) :rules '()))
         (lang2 (make-instance 'logical-language :name 'L2 :syntax '(:and) :axioms '((p (and p p))) :rules '()))
         (lang3 (make-instance 'logical-language :name 'L3 :syntax '(:or) :axioms '((p (or p p))) :rules '()))
         (unknown-lang (make-instance 'logical-language :name '? :rules '()))
         (morph1 (make-instance 'morphism :source lang1 :target lang2 :translation #'identity))
         (morph2 (make-instance 'morphism :source lang1 :target lang3 :translation #'identity))
         (morph3 (make-instance 'morphism :source lang2 :target unknown-lang :translation #'identity))
         (morph4 (make-instance 'morphism :source lang3 :target unknown-lang :translation #'identity))
         (test-diagram (make-instance 'diagram
                                      :vertices (list lang1 lang2 lang3 unknown-lang)
                                      :edges (list morph1 morph2 morph3 morph4))))
    (multiple-value-bind (constructed-lang new-morph1 new-morph2)
        (solve-diagram test-diagram)
      (assert (equal (name constructed-lang) 'PUSHOUT-L2-L3))
      (assert (not (set-difference (syntax constructed-lang) '(:OR :AND))))
      (assert (not (set-difference (axioms constructed-lang) '((P (OR P P)) (P (AND P P))) :test #'equal)))
      (format t "Pushout Test Passed!~%"))))

(defun run-pullback-test ()
  "Tests the pullback construction."
  (let* ((lang1 (make-instance 'logical-language :name 'L1 :syntax '(:and :not) :axioms '((p (and p p))) :rules '()))
         (lang2 (make-instance 'logical-language :name 'L2 :syntax '(:or :not) :axioms '((p (or p p))) :rules '()))
         (lang3 (make-instance 'logical-language :name 'L3 :syntax '(:and :or :not) :axioms '((p (and p p)) (p (or p p))) :rules '()))
         (unknown-lang (make-instance 'logical-language :name '? :rules '()))
         (morph1 (make-instance 'morphism :source lang1 :target lang3 :translation #'identity))
         (morph2 (make-instance 'morphism :source lang2 :target lang3 :translation #'identity))
         (morph3 (make-instance 'morphism :source unknown-lang :target lang1 :translation #'identity))
         (morph4 (make-instance 'morphism :source unknown-lang :target lang2 :translation #'identity))
         (test-diagram (make-instance 'diagram
                                      :vertices (list lang1 lang2 lang3 unknown-lang)
                                      :edges (list morph1 morph2 morph3 morph4))))
    (multiple-value-bind (constructed-lang new-morph1 new-morph2)
        (solve-diagram test-diagram)
      (assert (equal (name constructed-lang) 'PULLBACK-L1-L2))
      (assert (equal (syntax constructed-lang) '(:NOT)))
      (assert (equal (axioms constructed-lang) '()))
      (format t "Pullback Test Passed!~%"))))

(defun run-all-tests ()
  (run-pushout-test)
  (run-pullback-test))

(run-all-tests)