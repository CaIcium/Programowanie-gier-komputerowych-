extends Area3D

var speed = 200.0

@export var explosion_scene : PackedScene

func _physics_process(delta):
	position += transform.basis.z * speed * delta

func _on_body_entered(body):
	if body.has_method("take_damage"):
		body.take_damage(1)  
	
	queue_free() 
