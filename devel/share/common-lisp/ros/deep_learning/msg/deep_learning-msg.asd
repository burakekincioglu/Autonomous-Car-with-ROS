
(cl:in-package :asdf)

(defsystem "deep_learning-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "Burak" :depends-on ("_package_Burak"))
    (:file "_package_Burak" :depends-on ("_package"))
  ))