class Settings:
    def __init__(self):
        #settings for the screen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        #ship setting
        self.ship_speed = 10.0
        self.ship_limit = 3
        #settings for bullet
        self.bullet_speed = 20.0
        self.bullet_width = 45
        self.bullet_height = 90
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5
        
        #settings for aliens
        self.alien_speed = 5.0
        self.fleet_drop_speed = 10
        #integer 1 represents fleet moves to right, and -1 means the fleet moves to left
        self.fleet_direction = 1
        