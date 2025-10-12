;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Duality Meta-System
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;
;;; WARNING: This implementation represents a SPECIALIZED case of duality
;;; and does not represent the general, more complex relationship between
;;; the prover and refuter systems. The dual operation is more general
;;; than negation, and this implementation makes simplifying assumptions
;;; (e.g., that dual is invertible) which may not hold in the broader
;;; logical framework.
;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(load "ProverV0.lisp")
(load "RefuterV0.lisp")

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Duality Transformation
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun dual-transform (formula)
  "Recursively transforms a formula into its dual.
   NOTE: This implementation is a SPECIALIZATION. The direct transformation
   of 'con' to 'incon' and vice-versa assumes properties like non-contradiction
   and excluded middle, which do not exist in the general form of this logic."
  (let ((op (formula-type formula)))
    (case op
      (con '(incon))
      (incon '(con))
      (dep `(ind ,(dual-transform (second formula)) ,(dual-transform (third formula))))
      (ind `(dep ,(dual-transform (second formula)) ,(dual-transform (third formula))))
      (t (error "Unknown operator in dual-transform: ~A" op)))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Meta-System Functions
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun meta-prove (formula)
  "Proves a formula using the ProverV0 system."
  (run-prover formula))

(defun meta-refute (formula)
  "Refutes a formula by proving its dual. refute(F) <=> prove(dual(F))"
  (let ((dual-formula (dual-transform formula)))
    (run-prover dual-formula)))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Main Entry Point - Test Meta-System
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(defun main ()
  (format t "Starting Duality Meta-System Tests.~%")

  (let* ((f1 '(dep (con) (con)))
         (f2 '(ind (con) (con)))
         (f3 '(dep (ind (con) (con)) (con))))

    (format t "~%--- Testing meta-prove ---~%")
    (format t "meta-prove(~A) => ~A~%" f1 (meta-prove f1))
    (format t "meta-prove(~A) => ~A~%" f2 (meta-prove f2))
    (format t "meta-prove(~A) => ~A~%" f3 (meta-prove f3))

    (format t "~%--- Testing meta-refute ---~%")
    (format t "meta-refute(~A) => ~A~%" f1 (meta-refute f1))
    (format t "meta-refute(~A) => ~A~%" f2 (meta-refute f2))
    (format t "meta-refute(~A) => ~A~%" f3 (meta-refute f3)))

  (format t "~%Duality Meta-System Tests Finished.~%"))

(main)