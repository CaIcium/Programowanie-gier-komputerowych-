extends CharacterBody3D

@export var speed = 2.0
@export var max_hp = 2
@export var animacja_chodzenia = "action"

var hp = 2
var player = null
var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")
var is_dead = false

var saved_position_offset = Vector3.ZERO
var animation_length = 0.0
var save_time_before_end = 0.05
var position_already_saved = false

# --- REFERENCJE ---
@onready var anim_player = $monster/AnimationPlayer
@onready var model = $monster

func _ready():
	scale = Vector3(2, 2, 2)
	add_to_group("monster")
	hp = max_hp
	player = get_tree().get_first_node_in_group("gracz")
	
	if anim_player:
		if anim_player.has_animation(animacja_chodzenia):
			var animation = anim_player.get_animation(animacja_chodzenia)
			animation.loop_mode = Animation.LOOP_NONE
			animation_length = animation.length
			
			if not anim_player.animation_finished.is_connected(_on_animation_loop):
				anim_player.animation_finished.connect(_on_animation_loop)
			
			anim_player.play(animacja_chodzenia)

func _physics_process(delta):
	if is_dead:
		return
	if global_position.y < -30.0:
		print("Potwór wypadł poza mapę - usuwam.")
		queue_free() 
		return 
	
	if anim_player and anim_player.is_playing():
		var current_time = anim_player.current_animation_position
		if current_time >= (animation_length - save_time_before_end) and not position_already_saved:
			saved_position_offset = model.position
			position_already_saved = true
	
	if not is_on_floor():
		velocity.y -= gravity * delta
	
	if player:
		var direction = (player.global_position - global_position)
		direction.y = 0
		direction = direction.normalized()
		
		velocity.x = direction.x * speed
		velocity.z = direction.z * speed
		
		
		obroc_w_strone_gracza()
		
		if global_position.distance_to(player.global_position) < 1.5:
			kill_player()
	
	move_and_slide()

func obroc_w_strone_gracza():
	if not player:
		return
	
	var look_pos = player.global_position
	look_pos.y = global_position.y  
	
	if global_position.distance_to(look_pos) < 0.1:
		return
	
	look_at(look_pos, Vector3.UP)
	rotation.y += deg_to_rad(80.0)
	

func _on_animation_loop(anim_name: String):
	if anim_name == animacja_chodzenia:
		model.position = saved_position_offset
		position_already_saved = false
		anim_player.play(animacja_chodzenia)

func take_damage(amount):
	if is_dead:
		return
	hp -= amount
	print("Potwór HP: ", hp)
	if hp <= 0:
		die()

func die():
	is_dead = true
	
	var gracz = get_tree().get_first_node_in_group("gracz")
	if gracz and gracz.has_method("potwor_zabity"):
		gracz.potwor_zabity()
	
	queue_free()

func kill_player():
	if player and player.has_method("die"):
		player.die()
	else:
		get_tree().reload_current_scene()
			
