import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from time import sleep
from button import Button
from config_manager import ConfigManager
from scoreboard import ScoreBoard

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        #settings for game screen
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        #game statistics 
        self.stats = GameStats(self)
        #game score board
        self.sb = ScoreBoard(self)
        #game status
        self.game_active = False
        #config manager
        self.cfg = ConfigManager()
        #create play button
        self.play_button = Button(self, "Play")
        #backgroud color
        self.bg_color = self.settings.bg_color
        #ship
        self.ship = Ship(self)
        #bullet group
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
        
        
    def run_game(self):
        while True:
            self._check_events()
            
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                
            self._update_screen()
            self.clock.tick(60)
            
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            
    
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = False
            
    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #reset 3 ships for restart game
            self.stats.reset_stats()
            self.sb.prep_score()
            
            self.game_active = True
            #empty bullets and aliens
            self.bullets.empty()
            self.aliens.empty()
            
            #recreate a fleet
            self._create_fleet()
            self.ship.center_ship()
            
            #hide mouse
            pygame.mouse.set_visible(False)
            
            #restore game speed settings
            self.settings.initialize_dynamic_settings()
            
    def _fire_bullet(self):
        #create a bullet and add it to bullets group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
    def _update_bullets(self):
        #update bullet locations
        self.bullets.update()
        
        #remove disappeared bullets    
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= self.screen.get_rect().top:
                self.bullets.remove(bullet)
        #print(len(self.bullets))
        #check collisions of bullets and aliens
        self._check_bullet_alien_collisions()
            
    def _check_bullet_alien_collisions(self):
        #if bullets hit the alien, they both disappear
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        #update score setting
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        #if aliens are all destroyed, system destroys the rest bullets and create a new fleet 
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            
            #if the whole fleet are down, level increase by 1
            self.stats.level += 1
            self.sb.prep_level()
        
    def _ship_hit(self):
        if self.stats.ship_left > 0:
            
            self.stats.ship_left -= 1
            
            self.bullets.empty()
            self.aliens.empty()
            
            self._create_fleet()
            self.ship.center_ship()
            
            sleep(1)
        else:
            self.game_active = False
            #restore mouse visible
            pygame.mouse.set_visible(True)
        
    def _check_aliens_bottom(self):
        #if an alien hits the screen bottom
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break
    
        
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        #check if the ship collide into an alien
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            #print("Ship hit!!!")
            self._ship_hit()
            
        #check if an alien gets to the bottom
        self._check_aliens_bottom()
        
    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 4 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
                
            #after creating a line of aliens, reset current_x and increase current_y
            current_x = alien_width
            current_y += 2 * alien_height
            
    def _create_alien(self, x_position, y_position):
        #create an alien and add it to fleet
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
        
    def _change_fleet_direction(self):
        #move the fleet downard by fleet_drop_speed
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        #change to reverse direction
        self.settings.fleet_direction *= -1
            
        
                
    
    
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)  
        #show score board
        self.sb.show_score()
        #if game in unactive status, show play button
        if not self.game_active:
            self.play_button.draw_button()
                
        pygame.display.flip()
    
    def _test_config(self):
        volume = float(self.cfg.get("Audio", "volume"))
        player_name = self.cfg.get("Player", "name")
        print(f"valume: {volume}, Player_name: {player_name}")
        
if __name__ == '__main__':
    ai = AlienInvasion()
    #test configuration
    #ai._test_config()
    ai.run_game()
    
    
#filled_char = "█"
#empty_char = "░"