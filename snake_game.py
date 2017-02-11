import game_object, game_state, pickle, pygame, random, sys
from pygame.locals import *

""" The Game class contains the presentation and view logic of the application """

class Game:

    def __init__(self):
        
        """ Sets the window size and starts the game """
        
        self.screen_width = 690;
        self.screen_height = 700;
        
        pygame.init()
        self.start_game()
        
    def start_game(self):
        
        """ Shows the main menu of the game and waits for performing an action from the player """

        color_index = 2
        number = 1
        self.create_new_screen()
        self.window_running = True
        
        while self.window_running:

            self.clock.tick(4)
            self.display_welcome(self.screen,color_index)
            
            number = - number
            color_index += number
            
            
            for event in pygame.event.get():
            
                if event.type ==  QUIT:
                    self.window_running = False
 
                    
                elif event.type == KEYDOWN:
                    if event.key == K_q:
                        self.window_running = False
                    if event.key == K_SPACE:
                        self.start_a_new_game()
                    elif event.key == K_F5:
                        self.load_saved_game()
                        
            pygame.display.update()
            
            
    def display_welcome(self,parent,index):
        
        r,g,b = 0,0,0
        
        if index % 2 == 0:
            r,g,b = 6,39,250
        else:
            r,g,b = 209,208,235
            
        font = pygame.font.SysFont('Arial',40)
        welcome_text = font.render('Welcome to Snake Game!', True, (250,31,6))
        instruction_one_text = font.render('Press Space for a New Game', True, (r, g, b ))
        instruction_two_text = font.render('Press F5 to Load previous Game',True,(r, g, b))
        
        parent.blit(welcome_text, (170,200))
        parent.blit(instruction_one_text, (140,300))
        parent.blit(instruction_two_text, (130,400))

        
    def load_saved_game(self):

        self.game_state = game_state.Game_State.load_saved_game_state()
        self.run_a_game()

    def start_a_new_game(self):
        """ Starts a new game from level 1 """
        
        self.game_state = game_state.Game_State(self.screen_width, self.screen_height)
        self.run_a_game()

    def run_a_game(self):
        """This function controls the main game loop , it handles the events from the player """
        
        self.create_new_screen()
        pygame.time.set_timer(pygame.NUMEVENTS - 1, 1000)
        self.load_music()
        
        self.game_running = True
       
        while self.game_running:

            self.clock.tick(self.game_state.speed)
            
            for event in pygame.event.get():

                if event.type == pygame.NUMEVENTS - 1:
                    self.game_state.time_left -= 1

                if event.type ==  QUIT:
                    self.exit_game()

                if event.type == KEYDOWN:
                    
                    if event.key == K_q:
                        self.exit_game()
                        return
                        
                    elif event.key == K_ESCAPE:
                        self.exit_game()
                        return
                    
                    elif event.key == K_F6:
                        self.game_state.save_game_state()
                        self.game_saved(self.screen)
                        
                    elif event.key == K_PAUSE:
                        self.pause_game()
                        
                    elif event.key == K_UP:
                        self.game_state.calculate_snake_last_move(1)
                    elif event.key == K_DOWN:
                        self.game_state.calculate_snake_last_move(2)
                    elif event.key == K_RIGHT:
                        self.game_state.calculate_snake_last_move(3)
                    elif event.key == K_LEFT:
                        self.game_state.calculate_snake_last_move(4)
                    else: pass

            self.process_game()

            if self.game_state.snake_crashed == True:
                self.game_running = False
            elif self.game_state.snake_won == True:
                self.game_running = False
           

    def process_game(self):
        """ Checks if certain caseses occur,and draws on the screen the effects caused by them """

        self.game_state.apple_catched()           
        self.game_state.set_new_snake_coordinates()

        if self.detect_crashes() == True or self.time_out() == True:
            self.game_end()
            return
        
        self.draw_objects()        
        pygame.display.update()

        self.process_next_level()
        
    def process_next_level(self):
        """ Controls the transition between levels,changes the game_state to the next level state,or declares the player a winner """
        
        if self.game_state.level_passed() == True:

            if self.game_state.level_number != 3:

                self.next_level(self.screen)
                pygame.display.update()
                pygame.time.wait(3000)
                self.game_state.set_next_level_game_state()
                self.create_new_screen()
                self.load_music()
            else:
                
                self.snake_a_winner(self.screen)
                self.game_state.snake_won = True

                self.game_end()

    def exit_game(self):
        """ Controls the game exit case """

        self.game_running = False
        #self.window_running = False
        self.stop_music()
        self.create_new_screen()
        
    def game_end(self):
        """ Draws on the screen the game end case """
        
        self.draw_status_bar(self.screen)
        pygame.display.update()
        pygame.time.wait(4000)
        self.create_new_screen()
        
    def detect_crashes(self):
        """ Checks if the snake head had crashed in a brick,or in it's body """
        
        if self.game_state.snake_crash() == True:
            self.snake_crashed(self.screen)
            return True
        
        return False
            
    def time_out(self):
        """ Draws on the screen the time out case """
        
        if self.game_state.time_out() == True:
            self.snake_time_out(self.screen)
            return True
        return False
        
    def restart_screen(self):
        self.screen.fill(1, 1, 1)
    
    def create_new_screen(self):
        """ Draw a new game screen,replacing the old """
        
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        
    def draw_objects(self):
            """ Draws the game objects on the screen - snake,apple,bricks,status bar """
            
            self.screen.fill((255, 255, 255))
            self.draw_bricks(self.screen)
            self.draw_apple(self.screen)
            self.draw_snake(self.screen)
            self.draw_status_bar(self.screen)
            
    def draw_snake(self, parent):

        for coordinates in self.game_state.snake:
            
            r_index = random.randint(0, 60)
            g_index = random.randint(0, 150)
            b_index = random.randint(0, 130)

            snake_segment = self.create_snake_segment(r_index, b_index, g_index)

            parent.blit(snake_segment, (coordinates[0],coordinates[1]))
            

    def create_snake_segment(self, i, j, s):
        """ Draws a portion of the snake's body """
        
        snake_w = self.game_state.snake.object_size[0]
        snake_h = self.game_state.snake.object_size[1]
        
        segment_image = self.create_an_image(snake_w, snake_h)
        segment_image.fill((66 + i, 245 - j, 6 + s))
        return segment_image

    def draw_bricks(self, parent):

        brick = self.create_brick()

        for coordinates in self.game_state.level:

            parent.blit(brick,(coordinates[0],coordinates[1]))

    def create_brick(self):
        """ Creates a brick size and color surface object to be drown """
        
        brick_w = self.game_state.level.object_size[0]
        brick_h = self.game_state.level.object_size[1]
        
        brick_image = self.create_an_image(brick_w, brick_h)
        brick_image.fill((6,5,5))
        
        return brick_image

    def draw_apple(self, parent):

        apple_image = self.create_apple()

        coordinates = self.game_state.apple[0]
        parent.blit(apple_image, (coordinates[0], coordinates[1]))
        

    def create_apple(self):

        g_index = random.randint(0,200)
        
        apple_w = self.game_state.apple.object_size[0]
        apple_h = self.game_state.apple.object_size[1]
        
        apple_image = self.create_an_image(apple_w, apple_h)
        apple_image.fill((209, 245 - g_index, 6))
        
        return apple_image

    def create_an_image(self, width, height):
        """ Creates a simple surface object """
        
        image = pygame.Surface((width,height))
        return image
        
    def snake_time_out(self, parent):
        """ Draws the time out label on the current screen """
        
        font = pygame.font.SysFont('Arial',50)
        end_text = font.render('Game Finished!Time Out!', True, (250,31,6))
        end_score = font.render('Your score was ' + str(self.game_state.score) + ' !', True, (250,31,6))

        parent.blit(end_text,(160, 200))
        parent.blit(end_score,(200, 400))

    def next_level(self, parent):
        """ Draws the next level label on the current screen """
        
        font = pygame.font.SysFont('Arial',50)
        next_level_text = font.render('Next Level!', True, (250,31,6))
        parent.blit(next_level_text, (300, 200))
         
    def snake_a_winner(self, parent):
        """ Draws the winner snake label on the current screen """
        
        r_index = random.randint(0,100)
        g_index = random.randint(0,20)
        
        font = pygame.font.SysFont('Arial',50)
        winner_text = font.render('Game Finished!You Won!', True, (250 - r_index,31 - g_index,6))
        end_score = font.render('Your score is ' + str(self.game_state.score) + 'pts.!', True, (250,31,6))
        
        parent.blit(winner_text,(160, 200))
        parent.blit(end_score, (190, 400))

    def snake_crashed(self, parent):
        """ Draws the snake crashed label on the current screen """
        
        font = pygame.font.SysFont('Arial',50)
        end_text = font.render('Game Finished!You Lost!', True, (250,31,6))
        end_score = font.render('Your score was ' + str(self.game_state.score) + ' !', True, (250,31,6))

        parent.blit(end_text,(160, 200))
        parent.blit(end_score,(200, 400))
        
    def game_saved(self, parent):
        """ Draws the game saved label on the current screen """
        
        font = pygame.font.SysFont('Arial',50)
        save_text = font.render('Game Saved!', True, (250, 31, 6))

        parent.blit(save_text, (250, 300))
        pygame.display.update()
        pygame.time.wait(2000)

        
    def draw_status_bar(self, parent):
        """Draws the status bar label on the current screen """
        
        r_index = random.randint(0,100)
        g_index = random.randint(0,80)
        
        bar = pygame.Surface((700,100))
        bar.fill((209 - r_index, 119 - g_index, 129))

        self.draw_score(bar)
        self.draw_time_left(bar)
        self.draw_goal_score(bar)
        self.draw_level_number(bar)
        
        parent.blit(bar, (0,600))
        
    def draw_score(self, parent):

        font = self.get_arial_font()
        score_text = font.render('SCORE: ' + str(self.game_state.score) +'pts.', True, (1, 1, 1))
        parent.blit(score_text,(30,30))
        
    def draw_time_left(self, parent):

        font = self.get_arial_font()
        time_text = font.render('Time Left: ' + str(self.game_state.time_left) +'s', True, (1, 1, 1))
        parent.blit(time_text, (220, 30))

    def draw_goal_score(self, parent):

        font = self.get_arial_font()
        goal_score_text = font.render('Goal: ' + str((self.game_state.level_number ** 2) * 20 + 120) +'pts.', True, (1, 1, 1))
        parent.blit(goal_score_text, (400, 30))

    def draw_level_number(self, parent):

        font = self.get_arial_font()
        level_number = font.render('Level: ' + str(self.game_state.level_number), True, (1, 1, 1))
        parent.blit(level_number, (570, 30))

    def get_arial_font(self):

        font = pygame.font.SysFont('Arial', 30)
        font.set_italic(True)

        return font

    def pause_game(self):
        """ ENTERS a paused game infinite loop """
        self.stop_music()
        paused = True
        
        while paused:            
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                  if event.key == K_PAUSE:
                        paused = False
                        
        self.load_music()
                    
    def load_music(self):
        """ Loads and plays the music file of the current game level """
        
        pygame.mixer.music.load('snakemusik' + str(self.game_state.level_number) + '.mid')
        pygame.mixer.music.play()

    def stop_music(self):

        pygame.mixer.music.stop()

    def pause_music(self):

        pygame.mixer.music.pause()
        
    def resume_music(self):

        pygame.mixer.music.unpause()
        
Game()

        

