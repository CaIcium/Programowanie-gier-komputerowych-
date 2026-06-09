extends Control

@onready var label = $Label



func _on_menu_pressed():
	get_tree().change_scene_to_file("res://main_menu.tscn")
