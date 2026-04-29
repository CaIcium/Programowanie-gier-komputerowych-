extends MeshInstance3D

@export var maneuver_speed: float = 10.0
@export var LIMIT_X: float = 8.0
@export var LIMIT_Y: float = 4.0

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	var input_x = Input.get_axis("ui_left", "ui_right")
	var input_y = Input.get_axis("ui_down", "ui_up")
	
	position.x += input_x * maneuver_speed * delta
	position.y += input_y * maneuver_speed * delta
	
	position.x = clamp(position.x, -LIMIT_X, LIMIT_X)
	position.y = clamp(position.y, -LIMIT_Y, LIMIT_Y)
	pass
