import pygame
from pygame.locals import *
import sys
import random

# add pgui from another folder
sys.path.insert(0, './src')

from pgui import *

FONT = None

class TestLabel:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.surf_width = self.screen.get_width()
        self.surf_height = self.screen.get_height()
        
        self.menutext = Label("Click Me!", font=FONT, font_size=60, text_color=(255, 255, 255), x=self.surf_width-420, y=80)
        
    def hello(self):
        print("hello world!")
    
    def handle_events(self, events):
        # reset the text and position
        self.menutext.text = "Click Me!"    
        self.menutext.pos_x = self.surf_width-420
        self.menutext.pos_y = 80
                        
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.menutext.clicked():
                        self.hello()
    
    def update(self):
        if self.menutext.clicked():
            self.menutext.text = "Let go!"
            self.menutext.pos_x = random.randint(20, 1200)
            self.menutext.pos_y = random.randint(20, 700)
        
    def render(self):
        self.screen.fill("#000000")
        
        self.menutext.draw()
        
        pygame.display.update()
        
    def run(self):
        while True:
            self.handle_events(pygame.event.get())
            self.update()
            self.render()
            
if __name__ == "__main__":
    game = TestLabel()
    game.run()