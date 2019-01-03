; Auto-generated. Do not edit!


(cl:in-package deep_learning-msg)


;//! \htmlinclude Burak.msg.html

(cl:defclass <Burak> (roslisp-msg-protocol:ros-message)
  ((type
    :reader type
    :initarg :type
    :type cl:integer
    :initform 0)
   (steering
    :reader steering
    :initarg :steering
    :type cl:float
    :initform 0.0)
   (hasObstacle
    :reader hasObstacle
    :initarg :hasObstacle
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass Burak (<Burak>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Burak>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Burak)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name deep_learning-msg:<Burak> is deprecated: use deep_learning-msg:Burak instead.")))

(cl:ensure-generic-function 'type-val :lambda-list '(m))
(cl:defmethod type-val ((m <Burak>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader deep_learning-msg:type-val is deprecated.  Use deep_learning-msg:type instead.")
  (type m))

(cl:ensure-generic-function 'steering-val :lambda-list '(m))
(cl:defmethod steering-val ((m <Burak>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader deep_learning-msg:steering-val is deprecated.  Use deep_learning-msg:steering instead.")
  (steering m))

(cl:ensure-generic-function 'hasObstacle-val :lambda-list '(m))
(cl:defmethod hasObstacle-val ((m <Burak>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader deep_learning-msg:hasObstacle-val is deprecated.  Use deep_learning-msg:hasObstacle instead.")
  (hasObstacle m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Burak>) ostream)
  "Serializes a message object of type '<Burak>"
  (cl:let* ((signed (cl:slot-value msg 'type)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'steering))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'hasObstacle) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Burak>) istream)
  "Deserializes a message object of type '<Burak>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'type) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'steering) (roslisp-utils:decode-single-float-bits bits)))
    (cl:setf (cl:slot-value msg 'hasObstacle) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Burak>)))
  "Returns string type for a message object of type '<Burak>"
  "deep_learning/Burak")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Burak)))
  "Returns string type for a message object of type 'Burak"
  "deep_learning/Burak")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Burak>)))
  "Returns md5sum for a message object of type '<Burak>"
  "30cabddebe002ba107d2c72ae8a924cb")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Burak)))
  "Returns md5sum for a message object of type 'Burak"
  "30cabddebe002ba107d2c72ae8a924cb")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Burak>)))
  "Returns full string definition for message of type '<Burak>"
  (cl:format cl:nil "int32 type~%float32 steering~%bool hasObstacle~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Burak)))
  "Returns full string definition for message of type 'Burak"
  (cl:format cl:nil "int32 type~%float32 steering~%bool hasObstacle~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Burak>))
  (cl:+ 0
     4
     4
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Burak>))
  "Converts a ROS message object to a list"
  (cl:list 'Burak
    (cl:cons ':type (type msg))
    (cl:cons ':steering (steering msg))
    (cl:cons ':hasObstacle (hasObstacle msg))
))
