class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.cfg = ai_game.cfg
        self.reset_stats()
        #high score won't reset
        self.high_score = self.cfg.get("Player", "high_score")
    
    def reset_stats(self):
        self.ship_left = self.settings.ship_limit - 1
        self.score = 0
        self.level = 1
        
        