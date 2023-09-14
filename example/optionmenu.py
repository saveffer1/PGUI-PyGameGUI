import pygame
from pygame.locals import *
from pygame import mixer
import sys
import os

# add pgui from another folder
sys.path.insert(0, './src')

from pgui import *

mixer.init()
        
FONT = None

SOUND_BTNCLICK = mixer.Sound(os.path.join("src", "click.wav"))
SOUND_COLLIDE = mixer.Sound(os.path.join("src", "collide.mp3"))

lst = ["test0", "test1", "test2", "test3", "test4"]

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.surf_width = self.screen.get_width()
        self.surf_height = self.screen.get_height()
        
        self.option_rect = pygame.Rect(self.surf_width//4, self.surf_height//4, 
                                       self.surf_width//2, self.surf_height//2+100
        )            
        self.option_surf = pygame.Surface(self.option_rect.size, pygame.SRCALPHA)
    
        self.option_label = Label('Options', font=FONT, font_size=60, text_color="#000000", 
                                  x=self.surf_width//2-100, y=self.surf_height//2-300
        )
        self.music_label = Label('Music Volume', font=FONT, font_size=30, text_color="#FFFFFF", 
                                 x=self.surf_width//2-250, y=self.option_rect.top+20
        )
        self.sfx_label = Label('SFX Volume', font=FONT, font_size=30, text_color="#FFFFFF", 
                               x=self.surf_width//2-250, y=self.option_rect.top+80
        )
        self.fullscreen_label = Label('Full Screen', font=FONT, font_size=30, text_color="#FFFFFF", 
                                      x=self.surf_width//2-250, y=self.option_rect.top+140
        )
        self.del_save_label = Label('Clear Save', font=FONT, font_size=30, text_color="#FFFFFF", 
                                    x=self.surf_width//2-250, y=self.option_rect.top+210
        )
        self.music_menu_label = Label('Menu Music', font=FONT, font_size=30, text_color="#FFFFFF", 
                                      x=self.surf_width//2-250, y=self.option_rect.top+300
        )

        self.btn_back = Button("Exit", font=FONT, font_size=30, 
                               width=150, height=50, x=50, y=100,
        )
        self.btn_back.top_color = "#83502E"
        self.btn_back.bottom_color = "#342012"
        
        self.btn_delsave = Button('del', font=FONT, font_size=50, 
                                         x=self.surf_width//2+50, y=self.option_rect.top+220, 
                                         width=100, height=50
        )
        
        self.confirm_prompt = None

        self.music_slider = RangeSlider(min_value=0, max_value=100, start_value=0, 
                                        x=self.surf_width//2, y=self.option_rect.top+50, 
                                        button_color="#FFFFFF", range_width=200, 
                                        text_color="#FFFFFF", show_min_max=False, 
                                        callback=self.callback
        )
        
        self.sfx_slider = RangeSlider(min_value=0, max_value=100, start_value=0, 
                                      x=self.surf_width//2, y=self.option_rect.top+110, 
                                      button_color="#FFFFFF", range_width=200, 
                                      text_color="#FFFFFF", show_min_max=False, 
                                      callback=self.callback
        )
        self.sfx_slider.drag_sound = SOUND_COLLIDE
        self.sfx_slider.play_sound_after_drag = True
        
        self.toggle_fullscreen = ToggleSwitch(font=FONT, font_size=30, width=100, height=50, 
                                              x=self.surf_width//2+50, y=self.option_rect.top+150, 
                                              start_state=False, callback=self.fullscreen
        )
        self.toggle_fullscreen.on_color = "#1C945C"
        self.toggle_fullscreen.off_color = "#D74B4B"
        
        
        self.music_menu_selector = Selector(lst, start_index=0, font=FONT, uifont=FONT, 
                                            x=self.surf_width//2+50, y=self.option_rect.top+300, 
                                            callback=self.selector_callback
        )
        self.music_menu_selector.uileft = "<"
        self.music_menu_selector.uiright = ">"
         
        self.all_label = (self.option_label, self.music_label, 
                          self.fullscreen_label, self.del_save_label, 
                          self.music_menu_label, self.sfx_label
        )
        self.all_btn = (self.btn_back, self.btn_delsave)
    
    def fullscreen(self, val):
        pygame.display.set_mode((1280, 720), pygame.FULLSCREEN if val else 0)
    
    def callback(self, val):
        print(f"got some: {val}")
    
    def selector_callback(self, val):
        print(f"changed to: {val}")
        
    def handle_events(self, events):
        for event in events:
            if event.type == QUIT:
                pygame.quit()
                sys.exit()            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_clicked = True
                    if self.btn_delsave.clicked():
                        Button.clicked_sound(SOUND_BTNCLICK)
                        self.confirm_prompt = YesNoPopup("You sure?", FONT, width=500, height=300)
                        self.confirm_prompt.fill_color = "#83502E"
                        self.confirm_prompt.text_color = "#FFFFFF"

                    if self.btn_back.clicked():
                        pygame.quit()
                        sys.exit() 

            self.sfx_slider.handle_event(event)
            self.music_slider.handle_event(event)
            self.toggle_fullscreen.handle_event(event)
            self.music_menu_selector.handle_event(event)

            if isinstance(self.confirm_prompt, YesNoPopup):
                self.confirm_prompt.handle_event(event)
                if self.confirm_prompt.result is not None:
                    if self.confirm_prompt.result:
                        Button.clicked_sound(SOUND_BTNCLICK, addition_vol=0.3)
                        print("Wow you reset the game")
                    else:
                        Button.clicked_sound(SOUND_BTNCLICK)
                    self.confirm_prompt = None
    
    def update(self):
        self.surf_width = self.screen.get_width()
        self.surf_height = self.screen.get_height()
        
        for btn in self.all_btn:
            btn.collide_sound(SOUND_COLLIDE)
            btn.set_hover()
            btn.set_elevate()
        
        self.sfx_slider.update()
        self.music_slider.update()
    
    def render(self):
        self.screen.fill((217,189,165))

        pygame.draw.rect(self.option_surf, (0, 0, 0, 128), self.option_surf.get_rect())
        self.screen.blit(self.option_surf, self.option_rect)
        
        
        for label in self.all_label:
            label.draw()
            
        for btn in self.all_btn:
            btn.draw()
            
        self.toggle_fullscreen.draw()

        self.sfx_slider.draw()
        self.music_slider.draw()
        self.music_menu_selector.draw()
        
        if isinstance(self.confirm_prompt, YesNoPopup) and self.confirm_prompt.result is None:
            self.confirm_prompt.draw()
        
        pygame.display.update()

    def run(self):
        while True:
            self.handle_events(pygame.event.get())
            self.update()
            self.render()
            
if __name__ == "__main__":
    game = Game()
    game.run()