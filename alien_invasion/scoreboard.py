import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """a class to report scoring info"""

    def __init__(self, ai_game):
        """initialize scorekeeping attributes"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # font settings for scoring info
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.high_score_font = pygame.font.SysFont(None, 32)

        # prep the score
        self.prep_score()
        self.prep_level()
        self.prep_ships()
        self.prep_high_score()

    def prep_score(self):
        """turn the score into a rendered image"""
        rounded_score = round(self.stats.score, -1)
        score_str = "Score : " + "{:,}".format(rounded_score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)

        # display the score at top of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """turn the high score into a rendered image"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "High Score : " + "{:,}".format(high_score)
        self.high_score_image = self.high_score_font.render(
            high_score_str, True, self.text_color, self.settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.screen_rect.right - 20
        self.high_score_rect.top = self.score_rect.bottom + 10

    def check_high_score(self):
        """check for new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """turn the level into a rendered image"""
        level_str = "Level : " + str(self.stats.level)
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color)

        # position the level at top center
        self.level_rect = self.level_image.get_rect()
        self.level_rect.center = self.screen_rect.center
        self.level_rect.top = 20

    def prep_ships(self):
        """show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 20 + ship_number * (ship.rect.width + 20)
            ship.rect.y = 20
            self.ships.add(ship)

    def show_score(self):
        """draw score and level and ships to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.ships.draw(self.screen)
