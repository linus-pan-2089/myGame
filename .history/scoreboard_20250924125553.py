import pygame.font

class ScoreBoard:
    
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        #font settings
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        
        #prepare score image
        self.prep_score()
        
    def prep_score(self):
        #render score string into an image
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        #place score string on topright corner
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
        
        