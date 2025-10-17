(load "QHJ.lisp")
(setup-dependencies)
(load "STT.lisp")
(load "commutative-diagram.lisp")

(in-package #:refuter-api)
(setf *frontend-directory* #P"/home/madsci/Documents/Weaver/")
(start-refuter-api :port 8080)

(strace-test:restart-strace-test-server)


(load "SFT.lisp")
(static-file-tests:start-test-server :static-dir #P"/home/madsci/Documents/Weaver/")
