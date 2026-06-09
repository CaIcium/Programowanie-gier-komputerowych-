extends Node3D

@export var monster_scene : PackedScene
@export var max_monsters = 2
@export var min_spawn_distance = 5.0
@export var max_spawn_distance = 10.0
@export var spawn_check_radius = 1.0  
@export var max_spawn_attempts = 10  

func spawn_monster():
	var current_monsters = get_tree().get_nodes_in_group("monster").size()
	
	if current_monsters >= max_monsters:
		print("Limit potworów osiągnięty (", current_monsters, "/", max_monsters, ")")
		return
	
	var gracz = get_tree().get_first_node_in_group("gracz")
	if not gracz:
		print("Nie ma gracza!")
		return
	
	var spawn_pos = find_valid_spawn_position(gracz.global_position)
	
	if spawn_pos == Vector3.ZERO:
		print("Nie znaleziono wolnego miejsca do spawnu!")
		return
	
	var nowy_potwor = monster_scene.instantiate()
	add_child(nowy_potwor)
	nowy_potwor.global_position = spawn_pos
	print("Zespawnowano potwora! (", current_monsters + 1, "/", max_monsters, ")")

func find_valid_spawn_position(player_pos: Vector3) -> Vector3:
	var space_state = get_world_3d().direct_space_state
	
	for attempt in range(max_spawn_attempts):
		var angle = randf() * PI * 2
		var distance = randf_range(min_spawn_distance, max_spawn_distance)
		var test_pos = player_pos + Vector3(cos(angle), 0, sin(angle)) * distance
		
		if is_position_clear(test_pos, space_state):
			print("Znaleziono wolne miejsce po ", attempt + 1, " próbach")
			return test_pos
	
	print("Wszystkie ", max_spawn_attempts, " próby się nie udały!")
	return Vector3.ZERO

func is_position_clear(pos: Vector3, space_state) -> bool:
	var shape = SphereShape3D.new()
	shape.radius = spawn_check_radius
	
	var query = PhysicsShapeQueryParameters3D.new()
	query.shape = shape
	query.transform = Transform3D(Basis(), pos)
	
	var result = space_state.intersect_shape(query, 1)  # 1 = wystarczy jedna kolizja
	
	return result.size() == 0  # true jeśli pusto

func _on_timer_timeout():
	spawn_monster()
