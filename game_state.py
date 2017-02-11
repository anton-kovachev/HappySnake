import pickle,random,game_object
""" The Game State class contains the business logic of the application """
class Game_State:

    def __init__(self, screen_width, screen_height):

        self.init_a_start_game_state(screen_width, screen_height)

    def init_a_start_game_state(self, screen_width, screen_height):
        """ Initialize the game state of a start of a new game """

        self.frame = (screen_width, screen_height - 100)
        self.level_number = 1
        
        self.score = 0
        self.speed = 4
        
        self.total_time = 101
        self.time_left = self.total_time

        self.init_snake()
        self.last_move = 2
  
        self.snake_crashed = False
        self.snake_won = False

        self.load_current_level()
        self.calculate_new_apple_pos()

    def level_passed(self):
        """ Checks if the score for reaching the next level is achieved """
        
        if self.score == (self.level_number ** 2) * 20 + 120:
            self.snake_won = True
            return True
        return False
    
    def set_next_level_game_state(self):
        """ Set the next level game state properties """
        
        self.level_number += 1
        
        self.speed += (self.level_number - 1)
        self.total_time = self.total_time + self.level_number * 10
        self.time_left = self.total_time
        
        self.score = 0

        self.snake_crashed = False
        self.snake_won = False
        
        self.init_snake()     
        self.last_move = 2
        
        self.load_current_level()
        self.calculate_new_apple_pos()

    def init_snake(self):
        """ Creates the initial snake state on the start of every level """
        
        snake_segment_width = 30
        snake_segment_height = 30

        snake_x_pos = self.frame[0] // 2

        snake_init_position = [(360, 3 * snake_segment_height), (360, 2 * snake_segment_height), (360, snake_segment_height), (360, 0)]
        self.snake = game_object.Game_Object(snake_init_position,(snake_segment_width, snake_segment_height))

    def apple_catched(self):
        """Checks if the snake head current coordinates collide with the apple ones """ 
        if self.snake_head_apple_collide() == True:

            self.grow_snake()
            self.calculate_new_apple_pos()
            self.score += 10
            return True
        return False

    def calculate_new_apple_pos(self):
        """ Searches for a position of the apple on the screen which does not collide with the snake ,or rhe bricks """
        
        apple_w = self.snake.object_size[0]
        apple_h = self.snake.object_size[1]
        
        x = random.randint(0,self.frame[0] - apple_w)
        y = random.randint(0,self.frame[1] - apple_h)
        apple = game_object.Game_Object([(x,y)],(apple_w, apple_h))
        
        self.apple = apple
        
        while self.apple_snake_collide() == True or self.apple_brick_collide() == True:

            x = random.randint(0, self.frame[0] - apple_w)
            y = random.randint(0, self.frame[1] - apple_h)

            #if x > 670 or y > 570:
                #continue
            
            apple = game_object.Game_Object([(x,y)],(30,30))
            self.apple = apple

    def apple_brick_collide(self):

        apple_x = self.apple[0][0]
        apple_y = self.apple[0][1]

        apple_w = self.apple.object_size[0]
        apple_h = self.apple.object_size[1]

        brick_w = self.level.object_size[0]
        brick_h = self.level.object_size[1]
        
        for brick in self.level:

            brick_x = brick[0]
            brick_y = brick[1]

            if self.collide(apple_x, apple_y, brick_x, brick_y, apple_w, apple_h, brick_w, brick_h):
                return True

        return False

    def apple_snake_collide(self):

        apple_x = self.apple[0][0]
        apple_y = self.apple[0][1]

        apple_w = self.apple.object_size[0]
        apple_h = self.apple.object_size[1]

        for segment in self.snake:

            segment_x = segment[0]
            segment_y = segment[1]

            segment_w = self.snake.object_size[0]
            segment_h = self.snake.object_size[1]

            if self.collide(apple_x, apple_y, segment_x, segment_y, apple_w, apple_h, segment_w, segment_h):
                return True

        return False

    def calculate_snake_last_move(self, requested_move):
        """ Checks if the requested move from the player is possible """
        """ 1 - up move,2 - dow move,3 - right move,4 - left move """
        
        if requested_move == 1 and self.last_move != 2:
            self.last_move = 1
        elif requested_move == 2 and self.last_move != 1:
            self.last_move = 2
        elif requested_move == 3 and self.last_move != 4:
            self.last_move = 3
        elif requested_move == 4 and self.last_move != 3:
            self.last_move = 4
            
    def set_new_snake_coordinates(self):
        """ Checks the new snake coordinates according to the last possible move """
        
        self.set_new_snake_body_coordinates()

        snake_w = self.snake.object_size[0]
        snake_h = self.snake.object_size[1]

        snake_head_x = self.snake[0][0]
        snake_head_y = self.snake[0][1]
        
        if self.last_move == 1:
            self.snake[0] = (snake_head_x, snake_head_y - self.snake.object_size[1])
        elif self.last_move == 2:
            self.snake[0] = (snake_head_x, snake_head_y + self.snake.object_size[1])
        elif self.last_move == 3:
            self.snake[0] = (snake_head_x + self.snake.object_size[0], snake_head_y)
        elif self.last_move == 4:
            self.snake[0] = (snake_head_x - self.snake.object_size[0], snake_head_y)


        self.set_new_edge_coordinates()

    def set_new_snake_body_coordinates(self):
        """ Moves the snake one snake segment further """
        
        i = len(self.snake.objects_coordinates) - 1

        while i >= 1:
            self.snake[i] = self.snake[i - 1]
            i -= 1


    def set_new_edge_coordinates(self):
        """ Checks if the apple has reached the screen's borders and places the snake ot he other screen end """
        
        snake_w = self.snake.object_size[0]
        snake_h = self.snake.object_size[1]
        
        if self.snake[0][0] > self.frame[0] or self.snake[0][0] + snake_w > self.frame[0]: 
            self.snake[0] = (0, self.snake[0][1])
        elif self.snake[0][0] < 0:
            self.snake[0] = (self.frame[0] - self.snake.object_size[0], self.snake[0][1])
        elif self.snake[0][1] > self.frame[1] or self.snake[0][1] + snake_h > self.frame[1]:
            self.snake[0] = (self.snake[0][0],0)
        elif self.snake[0][1] < 0:
            self.snake[0] = (self.snake[0][0], self.frame[1] - self.snake.object_size[1])

    def snake_head_apple_collide(self):
        """ Checks for collision between the snake head coordinates and the apple coordinates """
        
        snake_x = self.snake[0][0]
        snake_y = self.snake[0][1]

        snake_w = self.snake.object_size[0]
        snake_h = self.snake.object_size[1]

        apple_x = self.apple[0][0]
        apple_y = self.apple[0][1]

        apple_w = self.apple.object_size[0]
        apple_h = self.apple.object_size[1]

        
        if self.collide(snake_x, snake_y, apple_x, apple_y, snake_w, snake_h, apple_w, apple_h):
            return True

        return False

    def grow_snake(self):
        """ Adds an addition segement to the snake """
        
        new_segment = self.snake[0]
        self.snake.append(new_segment)
        
    def snake_crash(self):
        """ Checks if the snake has crashed in a brick """
        
        if self.snake_head_brick_collide() == True:
            self.snake_crashed = True
            return True
        elif self.snake_head_snake_collide() == True:
            self.snake_crashed = True
            return True

        return False

    def snake_head_brick_collide(self):

        snake_x = self.snake[0][0]
        snake_y = self.snake[0][1]

        snake_w = self.snake.object_size[0]
        snake_h = self.snake.object_size[1]

        brick_w = self.level.object_size[0]
        brick_h = self.level.object_size[1]
        
        for brick in self.level:

            brick_x = brick[0]
            brick_y = brick[1]

            if self.collide(brick_x, brick_y, snake_x, snake_y, brick_w, brick_h, snake_w, snake_h):
                return True

        return False

   
    def snake_head_snake_collide(self):
        """ Checks whether the snake has crashed in itself """

        snake_head_x = self.snake[0][0]
        snake_head_y = self.snake[0][1]

        for i in range (2,len(self.snake.objects_coordinates)):

            coords = self.snake[i]
            size = self.snake.object_size

            if self.collide(snake_head_x,snake_head_y,coords[0],coords[1],size[0],size[1],size[0],size[1]):
                return True

        return False
    
    def collide(self, x_1, y_1, x_2, y_2, w_1, h_1, w_2, h_2):
        """ Checks for intersection between the given objecs coordinates and sizes """

        if x_1 + w_1 > x_2 and x_2 + w_2 > x_1 and y_1 + h_1 > y_2 and y_2 + h_2 > y_1:
            return True
        return False
    
    def time_out(self):
        if self.time_left == 0:
            self.snake_crashed = True
            return True
        return False

    def load_current_level(self):
        """ Loads the next level whichs is serialized in a .lv file """
        
        level_name = 'snake_level_' + str(self.level_number) + '.lv'

        level_object = game_object.Game_Object.load_game_object(level_name)
        self.level = level_object

    def save_game_state(self):
        """ Serializes the game state in a .sv file """
        
        with open('snake_save.sv','wb') as save:

            pickle.dump(self,save)

    def load_saved_game_state():
        """ Loads the serialized game state """
        
        self = None
        with open('snake_save.sv','rb') as save:

            self = pickle.load(save)
            
        return self

        
