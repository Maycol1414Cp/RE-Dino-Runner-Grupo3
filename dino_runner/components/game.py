from django.dispatch import receiver
import pygame
from dino_runner.utils.constants import BG,ICON,RUNNING,SCREEN_HEIGHT,SCREEN_WIDTH,TITLE,FPS
from dino_runner.components.dinosaur.dinosaur import dinosaur
from dino_runner.components.obstacles.obstaclemanager import ObstacleManager
from dino_runner.components.menu_score.text_utils import get_score_element, get_centered_message

class Game:
     def __init__ (self):
          pygame.init()

          pygame.display.set_caption(TITLE)
          pygame.display.set_icon(ICON)
          self.screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
          self.clock=pygame.time.Clock()
          self.color_bg=(33,33,33)

          self.playing=False
          self.game_speed=20
          self.x_pos_bg=0
          self.y_pos_bg=380
          self.player=dinosaur()
          self.obstacle_manager=ObstacleManager()

          self.points=0
          self.running=True
     
     def run(self):
          self.playing=True
          while self.playing:
               self.events()
               self.updates()
               self.draw()
          # pygame.quit()
     
     def events(self):
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    self.playing=False
     def updates(self):
          user_input=pygame.key.get_pressed()
          self.player.update(user_input)
          self.obstacle_manager.update(self)

     def draw(self):
          self.clock.tick(FPS)
          self.screen.fill(self.color_bg)
          self.draw_background()
          self.player.draw(self.screen)
          self.obstacle_manager.draw(self.screen)
          self.score()
          
          pygame.display.update()
          pygame.display.flip()

     def draw_background(self):
          image_with=BG.get_width()
          self.screen.blit(BG,(self.x_pos_bg,self.y_pos_bg))
          self.screen.blit(BG,(image_with+self.x_pos_bg,self.y_pos_bg))
          if self.x_pos_bg<=-image_with:
               self.screen.blit(BG,(image_with+self.x_pos_bg,150))
               self.x_pos_bg=0
          self.x_pos_bg-=self.game_speed

     def score(self):
          self.points+=1
          if self.points%100==0:
               self.game_speed+=1
          score,score_rect=get_score_element(self.points)

          self.screen.blit(score,score_rect)
     def show_menu(self,death_count=0):
          self.running=True
          self.screen.fill((33,33,33))
     
          self.print_menu_elements(death_count)

          pygame.display.update()

          self.handle_key_events_on_menu()

     def print_menu_elements(self,death_count=0):
          half_screen_height=SCREEN_HEIGHT//2
          half_screen_width=SCREEN_WIDTH//2

          if death_count==0:
               text,text_rect=get_centered_message("press any key to start")
               self.screen.blit(text,text_rect)
          elif death_count>0:
               text,text_rect=get_centered_message("Press any key to Restart")
               score,score_rect=get_centered_message("Your score is: "+str(self.points),height=half_screen_height+50)
               self.screen.blit(score,score_rect)
               self.screen.blit(text,text_rect)
          self.screen.blit(RUNNING[0],(half_screen_width-20 ,half_screen_height-140))


     
     def handle_key_events_on_menu(self):
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    print("Dino: Good Bye")
                    self.runing=False
                    self.playing=False
                    pygame.display.quit()
                    pygame.quit()
                    exit()
                    break
               if event.type == pygame.KEYDOWN:
                    self.__init__()
                    self.run()