package main

import (
	rl "github.com/gen2brain/raylib-go/raylib"
)

const (
	WIDTH  int32 = 1920
	HEIGHT int32 = 1080
)

func main() {
	rl.InitWindow(WIDTH, HEIGHT, "Red Black Tree")
	rl.SetTargetFPS(60)

	camera := rl.NewCamera2D(rl.NewVector2(0, 0), rl.NewVector2(0, 0), 0.0, 1.0)
	for !rl.WindowShouldClose() {

		if rl.GetMouseWheelMove() != 0 {
			camera.Zoom += 0.1 * rl.GetMouseWheelMove()
			camera.Target = rl.GetScreenToWorld2D(rl.GetMousePosition(), camera)
			camera.Offset = rl.GetMousePosition()
		}

		if rl.IsMouseButtonDown(rl.MouseButtonLeft) {
			delta := rl.Vector2Scale(rl.GetMouseDelta(), -1.0/camera.Zoom)
			camera.Target = rl.Vector2Add(delta, camera.Target)
		}

		rl.BeginDrawing()
		rl.ClearBackground(rl.Gray)

		rl.BeginMode2D(camera)
		rl.DrawCircle(WIDTH/2, HEIGHT/2, 20, rl.Red)
		rl.EndMode2D()

		rl.EndDrawing()
	}
}
