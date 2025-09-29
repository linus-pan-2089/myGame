class Settings:
    def __init__(self):
        #static settings
        #settings for the screen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        #ship setting
        self.ship_limit = 3
        #settings for bullet
        self.bullet_width = 45
        self.bullet_height = 90
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5
        
        #settings for aliens
        self.fleet_drop_speed = 10
        
        #dynamic settings
        self.initialize_dynamic_settings()
        
        #speed up factor
        self.speedup_scale = 1.1
        
        #score setting
        self.alien_points = 50
        self.score_scale = 1.5
        
    def initialize_dynamic_settings(self):
        #the following settings will change when game continue
        self.ship_speed = 10.0
        self.bullet_speed = 20.0
        self.alien_speed = 5.0
        #integer 1 represents fleet moves to right, and -1 means the fleet moves to left
        self.fleet_direction = 1
        
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        