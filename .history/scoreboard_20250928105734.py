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
        self.prep_high_score()
        self.prep_level()
        
    def prep_score(self):
        #render score string into an image
        rounded_str = round(self.stats.score, -1)
        score_str = f"{rounded_str:,}"
        score_str = f"Current Score: {score_str}"
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        #place score string on topright corner
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        high_score_str = f"Max Score: {high_score_str}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)
        
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
        
    def prep_level(self):
        level = str(self.stats.level)
        level_str = f"Current Level: {level}"
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)
        
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
        
    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
    
    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
    
        
        
        