import pygame
from pygame.locals import *
from pygame import mixer
import sys
import os

# add pgui from another folder
sys.path.insert(0, './src')

from pgui import *

FONT = None

class TestButton:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.surf_width = self.screen.get_width()
        self.surf_height = self.screen.get_height()
        
        self.btn = Button("Hello?", font=FONT, font_size=30, 
                               width=150, height=50, x=50, y=100,
        )
        self.btn.top_color = "#83502E"
        self.btn.bottom_color = "#342012"
        
    def hello(self):
        print("hello world!")
        
    def handle_events(self, events):
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.btn.clicked():
                        self.hello()
    
    def update(self):
        # btn.collide_sound(SOUND_COLLIDE)
        self.btn.set_hover("#D74B4B")
        self.btn.set_elevate(5)
    
    def render(self):
        self.screen.fill("#FFFFFF")
        
        self.btn.draw()
        
        pygame.display.update()
        
    def run(self):
        while True:
            self.handle_events(pygame.event.get())
            self.update()
            self.render()
            
if __name__ == "__main__":
    game = TestButton()
    game.run()