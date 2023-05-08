import sys
import pygame
from time import sleep
from settings import Settings
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """overall class to manage game assets and behaviour"""

    def __init__(self):
        """initialize the game , and create game resources"""

        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.play_button = Button(self, "Play")
        self._create_fleet()

        music = pygame.mixer.Sound("music/music.wav")
        music.set_volume(0.25)
        music.play(loops = -1)
        self.laser_sound = pygame.mixer.Sound("music/laser.wav")
        self.laser_sound.set_volume(0.15)
        self.explosion_sound = pygame.mixer.Sound("music/explosion.wav")
        self.explosion_sound.set_volume(0.25)

    def run_game(self):
        """start the main loop for the game"""

        while True:
            self.clock.tick(self.settings.fps)
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open("high_score.txt", 'w') as file_object:
                    file_object.write(str(self.stats.high_score))

                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            with open("high_score.txt", 'w') as file_object:
                file_object.write(str(self.stats.high_score))
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_bullets(self):
        """update position of bullets and get rid of old bullets"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """check for bullet and alien collision"""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True , True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            self.explosion_sound.play()

        if not self.aliens:
            # destroy existing bullets and create new fleet
            self.bullets.empty()
            self.settings.fleet_direction = 1
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
            self._alien_number_incrementer()
            self._create_fleet()

    def _fire_bullet(self):
        """create a new bullet and add it to the bullets groud"""
        if len(self.bullets) < self.settings.bullets_allowed and self.stats.game_active:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.laser_sound.play()

    def _create_fleet(self):
        """create the fleet of aliens"""
        for row_number in range(self.settings.alien_row_number):
            for alien_number in range(self.settings.alien_number):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """fix the position for a particular alien"""
        alien = Alien(self)

        alien.x = alien.rect.width + \
            (alien.rect.width + self.settings.alien_padding) * alien_number
        alien.rect.y = 120 + \
            (alien.rect.height + self.settings.alien_padding) * row_number
        alien.rect.x = alien.x
        self.aliens.add(alien)

    def _update_aliens(self):
        """update the positons of all aliens in fleet"""
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """drop the entire fleet and change the fleet direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(1)
        else:
            self.stats.game_active = False
            self.ship.center_ship()
            self.bullets.empty()
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """check if any aliens have reached the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        """start a new game when the player clicks play"""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            # reset the game stats
            self.settings.iniatialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True

            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
 
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _alien_number_incrementer(self):
        if self.stats.level == 3:
            self.settings.alien_number = 6
            self.settings.bullet_color = (255,255,0)
        if self.stats.level == 5:
            self.settings.bullet_color = (255,0,255)
            self.settings.alien_row_number = 4
        if self.stats.level == 7:
            self.settings.alien_number = 7
            self.settings.bullet_color = (0,255,255)
        if self.stats.level == 9:
            self.settings.bullet_color = (200,200,200)
      

    def _update_screen(self):
        """update images on the screen, and flip to new screen"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        if self.stats.game_active:
            self.aliens.draw(self.screen)
        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == "__main__":
    # make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
