extends CharacterBody3D

@export var bullet_scene : PackedScene 

var kill_count = 0
var kills_to_win = 3

const SPEED = 5.0
const JUMP_VELOCITY = 4.5
var mouse_sensitivity = 0.003
var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")

@onready var camera = $Camera3D
@onready var weapon_pivot = $WeponPivot
@onready var gun = $WeponPivot/gun
@onready var muzzle = $WeponPivot/gun/Marker3D
@onready var ammo_label = $CanvasLayer/AmmoLabel
@onready var reload_bar = $CanvasLayer/ReloadBar
@onready var strzal_sound = $WeponPivot/StrzalSound  

var max_ammo = 6
var current_ammo = 6
var can_shoot = true
var fire_rate = 0
var is_reloading = false
var reload_time = 2

var default_fov = 75.0
var ads_fov = 50.0
var ads_speed = 10.0
var is_aiming = false

var gun_default_pos = Vector3(0.148, 1.47, -1.234)
var gun_default_rot = Vector3(0, 0, 0)
var gun_ads_pos = Vector3(7.55, 0.0, 0.0) 
var gun_ads_rot = Vector3(deg_to_rad(2.0), 0, 0)

func _ready():
	add_to_group("gracz")  
	
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
	default_fov = camera.fov
	update_ammo_display()
	reload_bar.visible = false
	
	if gun:
		gun.position = gun_default_pos
		gun.rotation = gun_default_rot

func _input(event):
	if Input.is_action_just_pressed("strzal"):
		shoot()
	
	if Input.is_action_just_pressed("reload"):
		if not is_reloading and current_ammo < max_ammo:
			start_reload()

func _unhandled_input(event):
	is_aiming = Input.is_mouse_button_pressed(MOUSE_BUTTON_RIGHT)

	if event is InputEventMouseMotion:
		rotate_y(-event.relative.x * mouse_sensitivity)
		camera.rotate_x(-event.relative.y * mouse_sensitivity)
		camera.rotation.x = clamp(camera.rotation.x, deg_to_rad(-85), deg_to_rad(85))

func _physics_process(delta):
	weapon_pivot.rotation.x = 0

	var target_fov = ads_fov if is_aiming else default_fov
	camera.fov = lerp(camera.fov, target_fov, ads_speed * delta)

	if gun:
		var target_pos = gun_ads_pos if is_aiming else gun_default_pos
		var target_rot = gun_ads_rot if is_aiming else gun_default_rot
		
		gun.position = gun.position.lerp(target_pos, ads_speed * delta)
		gun.rotation.x = lerp_angle(gun.rotation.x, target_rot.x, ads_speed * delta)
		gun.rotation.y = lerp_angle(gun.rotation.y, target_rot.y, ads_speed * delta)
		gun.rotation.z = lerp_angle(gun.rotation.z, target_rot.z, ads_speed * delta)

	if not is_on_floor():
		velocity.y -= gravity * delta

	if Input.is_action_just_pressed("ui_accept") and is_on_floor():
		velocity.y = JUMP_VELOCITY

	var input_dir = Input.get_vector("lewo", "prawo", "przod", "tyl")
	var direction = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

	if direction:
		velocity.x = direction.x * SPEED
		velocity.z = direction.z * SPEED
	else:
		velocity.x = move_toward(velocity.x, 0, SPEED)
		velocity.z = move_toward(velocity.z, 0, SPEED)

	move_and_slide()

func shoot():
	if is_reloading:
		is_reloading = false 
		return

	if can_shoot and current_ammo > 0:
		can_shoot = false
		current_ammo -= 1
		update_ammo_display()
		strzal_sound.play()
		
		await get_tree().create_timer(2.0).timeout  # czekaj sekundę
		var bullet = bullet_scene.instantiate()  # pocisk PO SEKUNDZIE
		get_tree().root.add_child(bullet)
		bullet.global_transform = muzzle.global_transform
		
		await get_tree().create_timer(fire_rate).timeout
		can_shoot = true

func start_reload():
	is_reloading = true
	reload_bar.visible = true 
	
	while is_reloading and current_ammo < max_ammo:
		reload_bar.value = 0 
		var time_passed = 0.0
		while time_passed < reload_time:
			if not is_reloading: break
			time_passed += get_process_delta_time()
			reload_bar.value = (time_passed / reload_time) * 100
			await get_tree().process_frame 
		
		if is_reloading:
			current_ammo += 1
			update_ammo_display()
	
	is_reloading = false
	reload_bar.visible = false

func die():
	print("Gracz zginął!")
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	get_tree().change_scene_to_file("res://end_screen.tscn")

func potwor_zabity():
	kill_count += 1
	print("Zabite potwory: ", kill_count, " / ", kills_to_win)
	
	if kill_count >= kills_to_win:
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
		get_tree().change_scene_to_file("res://win_screen.tscn")

func update_ammo_display():
	ammo_label.text = str(current_ammo) + " / " + str(max_ammo)
