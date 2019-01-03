;; Auto-generated. Do not edit!


(when (boundp 'deep_learning::Burak)
  (if (not (find-package "DEEP_LEARNING"))
    (make-package "DEEP_LEARNING"))
  (shadow 'Burak (find-package "DEEP_LEARNING")))
(unless (find-package "DEEP_LEARNING::BURAK")
  (make-package "DEEP_LEARNING::BURAK"))

(in-package "ROS")
;;//! \htmlinclude Burak.msg.html


(defclass deep_learning::Burak
  :super ros::object
  :slots (_type _steering _hasObstacle ))

(defmethod deep_learning::Burak
  (:init
   (&key
    ((:type __type) 0)
    ((:steering __steering) 0.0)
    ((:hasObstacle __hasObstacle) nil)
    )
   (send-super :init)
   (setq _type (round __type))
   (setq _steering (float __steering))
   (setq _hasObstacle __hasObstacle)
   self)
  (:type
   (&optional __type)
   (if __type (setq _type __type)) _type)
  (:steering
   (&optional __steering)
   (if __steering (setq _steering __steering)) _steering)
  (:hasObstacle
   (&optional __hasObstacle)
   (if __hasObstacle (setq _hasObstacle __hasObstacle)) _hasObstacle)
  (:serialization-length
   ()
   (+
    ;; int32 _type
    4
    ;; float32 _steering
    4
    ;; bool _hasObstacle
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _type
       (write-long _type s)
     ;; float32 _steering
       (sys::poke _steering (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; bool _hasObstacle
       (if _hasObstacle (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _type
     (setq _type (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; float32 _steering
     (setq _steering (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; bool _hasObstacle
     (setq _hasObstacle (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(setf (get deep_learning::Burak :md5sum-) "30cabddebe002ba107d2c72ae8a924cb")
(setf (get deep_learning::Burak :datatype-) "deep_learning/Burak")
(setf (get deep_learning::Burak :definition-)
      "int32 type
float32 steering
bool hasObstacle

")



(provide :deep_learning/Burak "30cabddebe002ba107d2c72ae8a924cb")


