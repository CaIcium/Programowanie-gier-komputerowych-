extends Control

func _on_graj_pressed():
	
	get_tree().change_scene_to_file("res://mapa.tscn")

func _on_wyjscie_pressed():

	get_tree().quit()
