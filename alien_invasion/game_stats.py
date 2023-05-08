class GameStats:
    """track statistics for alien invasion"""

    def __init__(self, ai_game):
        """initialize statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        try:
            with open("high_score.txt") as file_object:
                self.high_score = int(file_object.read())
        except ValueError:
            self.high_score=0
            with open("high_score.txt",'w') as file_object:
                file_object.write(str(self.high_score))
        except FileNotFoundError:
            self.high_score=0
            with open("high_score.txt",'w') as file_object:
                file_object.write(str(self.high_score))
       
        # start game in an inactive state
        self.game_active = False

    def reset_stats(self):
        """initialize statistics that can change during the game"""
        self.settings.bullet_color = (255,0,0)
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.settings.alien_number = 5
        self.settings.alien_row_number = 3
