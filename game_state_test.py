from game_state import *
import unittest

class Test_Game(unittest.TestCase):

    def setUp(self):
        self.game_state = Game_State(700,700)
        self.first_level = [(0, 0), (30, 0), (60, 0), (90, 0), (120, 0), (150, 0), (180, 0), (210, 0), (240, 0), (480, 0), (510, 0), (540, 0), (570, 0), (600, 0), (630, 0), (660, 0), (690, 0), (0, 90), (30, 90), (60, 90), (90, 90), (120, 90), (150, 90), (180, 90), (210, 90), (240, 90), (480, 90), (510, 90), (540, 90), (570, 90), (600, 90), (630, 90), (660, 90), (690, 90), (0, 180), (30, 180), (60, 180), (90, 180), (120, 180), (150, 180), (180, 180), (210, 180), (240, 180), (480, 180), (510, 180), (540, 180), (570, 180), (600, 180), (630, 180), (660, 180), (690, 180), (0, 270), (30, 270), (60, 270), (90, 270), (120, 270), (150, 270), (180, 270), (210, 270), (240, 270), (480, 270), (510, 270), (540, 270), (570, 270), (600, 270), (630, 270), (660, 270), (690, 270), (0, 360), (30, 360), (60, 360), (90, 360), (120, 360), (150, 360), (180, 360), (210, 360), (240, 360), (480, 360), (510, 360), (540, 360), (570, 360), (600, 360), (630, 360), (660, 360), (690, 360), (0, 450), (30, 450), (60, 450), (90, 450), (120, 450), (150, 450), (180, 450), (210, 450), (240, 450), (480, 450), (510, 450), (540, 450), (570, 450), (600, 450), (630, 450), (660, 450), (690, 450), (0, 540), (30, 540), (60, 540), (90, 540), (120, 540), (150, 540), (180, 540), (210, 540), (240, 540), (480, 540), (510, 540), (540, 540), (570, 540), (600, 540), (630, 540), (660, 540), (690, 540)]


    def test_init_gama_state(self):

        self.setUp()
        
        self.assertEqual(1, self.game_state.level_number)
        self.assertEqual(0, self.game_state.score)
        self.assertEqual(4, self.game_state.speed)
        self.assertEqual(101, self.game_state.total_time)
        self.assertEqual(101, self.game_state.time_left)
        self.assertEqual((700,600), self.game_state.frame)
        self.assertEqual(2, self.game_state.last_move)
        self.assertEqual(False, self.game_state.snake_crashed)
        self.assertEqual(False, self.game_state.snake_won)
        self.assertEqual(self.first_level, self.game_state.level.objects_coordinates)

    def test_calculate_new_apple_pos(self):

        self.setUp()
        
        self.game_state.calculate_new_apple_pos()
        
        apple = self.game_state.apple
        apple_x = apple.objects_coordinates[0][0]
        apple_y = apple.objects_coordinates[0][1]

        apple_w = apple.object_size[0]
        apple_h = apple.object_size[1]

        for brick in self.game_state.level:

            brick_x = brick[0]
            brick_y = brick[1]

            brick_w = self.game_state.level.object_size[0]
            brick_h = self.game_state.level.object_size[1]

            self.assertFalse(self.game_state.collide(apple_x, apple_y, brick_x, brick_y, apple_w, apple_h, brick_w, brick_h))

        for segment in self.game_state.snake:

            segment_x = segment[0]
            segment_y = segment[1]

            segment_w = self.game_state.snake.object_size[0]
            segment_h = self.game_state.snake.object_size[1]

            self.assertFalse(self.game_state.collide(apple_x, apple_y, segment_x, segment_y, apple_w, apple_h, segment_w, segment_h))

        self.assertTrue(apple_x <= self.game_state.frame[0] - apple_w)
        self.assertTrue(apple_y <= self.game_state.frame[1] - apple_h)

    def test_apple_catched(self):

        self.setUp()
        
        self.assertFalse(self.game_state.apple_catched())

        apple = self.game_state.apple
        snake = self.game_state.snake

        old_coords = snake.objects_coordinates[0]     
        old_len = len(snake.objects_coordinates)
        
        snake_w = snake.object_size[0]
        snake_h = snake.object_size[1]
        
        new_coords = (apple.objects_coordinates[0][0] + 1, apple.objects_coordinates[0][1] +1)
        self.game_state.snake.objects_coordinates[0] =  new_coords

        self.assertTrue(self.game_state.apple_catched())
        self.assertEqual(old_len + 1, len(self.game_state.snake.objects_coordinates))

        new_coords = (apple.objects_coordinates[0][0], apple.objects_coordinates[0][1])
        self.game_state.snake.objects_coordinates[0] =  new_coords

        self.assertFalse(self.game_state.apple_catched())

    def test_down_move_snake(self):
        
        self.setUp()
        
        self.game_state.calculate_snake_last_move(2)
        snake = self.game_state.snake
        snake_w = snake.object_size[0]
        snake_h = snake.object_size[1]
        
        snake_head = (snake.objects_coordinates[0][0], snake.objects_coordinates[0][1])

        self.game_state.set_new_snake_coordinates()
        self.assertEqual((snake_head[0], snake_head[1] + snake_h), snake.objects_coordinates[0])

        self.game_state.last_move = 1
        self.game_state.calculate_snake_last_move(2)
        
        snake_head = (snake.objects_coordinates[0][0], snake.objects_coordinates[0][1])
        self.game_state.set_new_snake_coordinates()
        
        self.assertEqual((snake_head[0], snake_head[1] - snake_h), snake.objects_coordinates[0])
        
    def test_up_move_snake(self):

        self.setUp()

        self.game_state.calculate_snake_last_move(1)
        snake = self.game_state.snake
        snake_w = snake.object_size[0]
        snake_h = snake.object_size[1]

        snake_head = (snake.objects_coordinates[0][0], snake.objects_coordinates[0][1])


        self.game_state.set_new_snake_coordinates()
        self.assertEqual((snake_head[0], snake_head[1] + snake_h), snake.objects_coordinates[0])

        self.game_state.last_move = 3
        self.game_state.calculate_snake_last_move(1)

        snake_head = (snake.objects_coordinates[0][0], snake.objects_coordinates[0][1])
        self.game_state.set_new_snake_coordinates()
        
        self.assertEqual((snake_head[0], snake_head[1] - snake_h), snake.objects_coordinates[0])

    def test_left_move_snake(self):

        self.setUp()

        self.game_state.calculate_snake_last_move(4)
        snake = self.game_state.snake
        snake_w = snake.object_size[0]
        snake_h = snake.object_size[1]

        snake_head = (snake.objects_coordinates[0][0], snake.objects_coordinates[0][1])
        self.game_state.set_new_snake_coordinates()

        self.assertEqual((snake_head[0] - snake_w, snake_head[1]), snake.objects_coordinates[0])        

        self.game_state.last_move = 3
        self.game_state.calculate_snake_last_move(4)
        
        snake_head = (snake.objects_coordinates[0][0], snake.objects_coordinates[0][1])
        self.game_state.set_new_snake_coordinates()

        self.assertEqual((snake_head[0] + snake_w, snake_head[1]), snake.objects_coordinates[0])        

    def test_right_move_snake(self):

        self.setUp()

        self.game_state.calculate_snake_last_move(3)
        snake = self.game_state.snake
        snake_w = snake.object_size[0]
        snake_h = snake.object_size[1]

        snake_head = (snake.objects_coordinates[0][0], snake.objects_coordinates[0][1])


        self.game_state.set_new_snake_coordinates()
        self.assertEqual((snake_head[0] + snake_w, snake_head[1]), snake.objects_coordinates[0])

        self.game_state.last_move = 4
        self.game_state.calculate_snake_last_move(3)

        snake_head = (snake.objects_coordinates[0][0], snake.objects_coordinates[0][1])
        self.game_state.set_new_snake_coordinates()
        
        self.assertEqual((snake_head[0] - snake_w, snake_head[1]), snake.objects_coordinates[0])

    def test_edge_move_snake(self):

        self.setUp()

        snake = self.game_state.snake
        snake_w = snake.object_size[0]
        snake_h = snake.object_size[1]
        frame = self.game_state.frame
        
        snake.objects_coordinates[0] = (frame[0] - snake_w,frame[1] // 2)
        self.game_state.set_new_snake_body_coordinates()

        self.game_state.calculate_snake_last_move(3)
        self.game_state.set_new_snake_coordinates()

        snake_head = (0, frame[1] // 2)
        self.assertEqual(snake_head, snake.objects_coordinates[0])

        snake.objects_coordinates[0] = (frame[0] // 2, frame[1] - snake_h)
        self.game_state.set_new_snake_body_coordinates()

        self.game_state.calculate_snake_last_move(2)
        self.game_state.set_new_snake_coordinates()

        snake_head = (frame[0] // 2, 0)
        self.assertEqual(snake_head, snake.objects_coordinates[0])

        snake.objects_coordinates[0] = (0, frame[1] // 3)
        self.game_state.set_new_snake_body_coordinates()

        self.game_state.calculate_snake_last_move(4)
        self.game_state.set_new_snake_coordinates()

        snake_head = (frame[0] - snake_w, frame[1] // 3)
        self.assertEqual(snake_head, snake.objects_coordinates[0])

        snake.objects_coordinates[0] = (frame[0] // 4,0)
        self.game_state.set_new_snake_body_coordinates()

        self.game_state.calculate_snake_last_move(1)
        self.game_state.set_new_snake_coordinates()

        snake_head = (frame[0] // 4, frame[1] - snake_h)
        self.assertEqual(snake_head, snake.objects_coordinates[0])

    def test_snake_crash(self):

        self.setUp()
        snake = self.game_state.snake
        level = self.game_state.level

        snake.objects_coordinates[0] = snake.objects_coordinates[2]

        self.assertTrue(self.game_state.snake_crash())

        snake.objects_coordinates[0] = level.objects_coordinates[len(level.objects_coordinates) - 1]
        
        self.assertTrue(self.game_state.snake_crash())
        
if __name__ == '__main__':
    unittest.main()
