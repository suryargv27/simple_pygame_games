class Settings:
    """a class to store all settings"""

    def __init__(self):
        """initialize the game's settings"""
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (25, 25, 25)
        self.fps = 60

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 3
        self.bullet_height = 30
        self.bullet_color = (255,0,0)
        self.bullets_allowed = 3

        # alien settings
        self.fleet_drop_speed = 50
        self.alien_padding = 40
        self.alien_number = 5
        self.alien_row_number = 3

        # how quickly the game speeds up
        self.speedup_scale = 1.2
        self.score_scale = 1.5
        

    def iniatialize_dynamic_settings(self):
        """initialize settings that change throughout the game"""
        self.ship_speed = 5.0
        self.bullet_speed = 10.0
        self.alien_speed = 3.0
        self.fleet_direction = 1

        # scoring
        self.alien_points = 50

    def increase_speed(self):
        """increase speed settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        
        
