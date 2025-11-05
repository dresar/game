"""
Ship Scene - Scene untuk gameplay di kapal merchant
Style: Warship game
"""
import pygame
import random
import math
from typing import List, Dict, Any
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from game_engine.scene import Scene
from utils.constants import *
from utils.ocean_effects import OceanRenderer
from utils.particle_system import ParticleSystem
from utils.ship_icons import ShipIconRenderer
from utils.ui_button import Button, ButtonManager

class Ship:
    """Kelas untuk player ship"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.width = SHIP_WIDTH
        self.height = SHIP_HEIGHT
        self.speed = SHIP_SPEED
        self.health = 100
        self.max_health = 100
        self.angle = 0  # Angle in degrees
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def update(self, dt: float, keys: pygame.key.ScancodeWrapper):
        """Update ship position berdasarkan input"""
        dx, dy = 0, 0
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed * dt
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed * dt
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed * dt
        
        self.x += dx
        self.y += dy
        
        # Boundary check
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        
        # Update angle based on movement
        if dx != 0 or dy != 0:
            self.angle = math.degrees(math.atan2(dy, dx))
    
    def render(self, screen: pygame.Surface):
        """Render ship ke screen"""
        # Draw merchant ship dengan icon yang lebih baik
        ShipIconRenderer.draw_merchant_ship(
            screen, 
            int(self.rect.x), 
            int(self.rect.y),
            self.width, 
            self.height,
            self.angle
        )
        
        # Draw ship label dengan background
        center_x = self.rect.centerx
        center_y = self.rect.centery
        font = pygame.font.Font(None, 16)
        text = font.render("MERCHANT", True, (255, 255, 255))
        text_rect = text.get_rect(center=(center_x, self.rect.y - 15))
        # Background untuk text
        bg_rect = pygame.Rect(text_rect.x - 5, text_rect.y - 2, text_rect.width + 10, text_rect.height + 4)
        overlay = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, bg_rect)
        screen.blit(text, text_rect)

class EnemyShip:
    """Kelas untuk enemy ship"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 45
        self.speed = ENEMY_SPEED
        self.health = ENEMY_HEALTH
        self.max_health = ENEMY_HEALTH
        self.angle = 0
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.target = None  # Target player ship
        
    def set_target(self, target: Ship):
        """Set target untuk enemy"""
        self.target = target
    
    def update(self, dt: float):
        """Update enemy position dengan AI sederhana"""
        if self.target:
            # Move towards target
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                dx = (dx / distance) * self.speed * dt
                dy = (dy / distance) * self.speed * dt
                self.x += dx
                self.y += dy
                self.angle = math.degrees(math.atan2(dy, dx))
                
                self.rect.x = int(self.x)
                self.rect.y = int(self.y)
    
    def render(self, screen: pygame.Surface):
        """Render enemy ship"""
        # Draw enemy ship dengan icon yang lebih baik
        ShipIconRenderer.draw_enemy_ship(
            screen,
            int(self.rect.x),
            int(self.rect.y),
            self.width,
            self.height,
            self.angle
        )
        
        # Health bar above ship dengan style yang lebih baik
        bar_width = 50
        bar_height = 6
        bar_x = self.rect.x + (self.rect.width - bar_width) // 2
        bar_y = self.rect.y - 12
        
        # Background
        pygame.draw.rect(screen, (30, 30, 30), (bar_x - 1, bar_y - 1, bar_width + 2, bar_height + 2))
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # Health fill
        health_percent = self.health / self.max_health
        health_width = int(bar_width * health_percent)
        if health_percent > 0.6:
            health_color = (0, 255, 0)
        elif health_percent > 0.3:
            health_color = (255, 255, 0)
        else:
            health_color = (255, 0, 0)
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))

class Cannonball:
    """Kelas untuk cannonball projectile"""
    def __init__(self, x: float, y: float, angle: float):
        self.x = x
        self.y = y
        self.radius = CANNONBALL_SIZE
        self.speed = CANNONBALL_SPEED
        self.angle = angle  # in radians
        self.damage = CANNONBALL_DAMAGE
        self.active = True
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
        
    def update(self, dt: float):
        """Update cannonball position"""
        if not self.active:
            return
        
        dx = math.cos(self.angle) * self.speed * dt
        dy = math.sin(self.angle) * self.speed * dt
        
        self.x += dx
        self.y += dy
        
        self.rect.x = int(self.x - self.radius)
        self.rect.y = int(self.y - self.radius)
        
        # Check boundaries
        if (self.x < 0 or self.x > SCREEN_WIDTH or 
            self.y < 0 or self.y > SCREEN_HEIGHT):
            self.active = False
    
    def render(self, screen: pygame.Surface):
        """Render cannonball"""
        if self.active:
            ShipIconRenderer.draw_cannonball(
                screen,
                int(self.x),
                int(self.y),
                self.radius
            )

class ShipScene(Scene):
    """Scene untuk gameplay di kapal merchant"""
    
    def __init__(self):
        super().__init__("ship")
        self.player_ship: Ship = None
        self.enemies: List[EnemyShip] = []
        self.cannonballs: List[Cannonball] = []
        self.enemy_spawn_timer = 0.0
        self.enemy_spawn_rate = ENEMY_SPAWN_RATE
        self.enemies_defeated = 0
        self.enemies_to_defeat = 5  # Harus mengalahkan 5 enemy untuk menang
        self.won = False
        self.win_timer = 0.0
        self.win_delay = 2.0  # Delay 2 detik sebelum pindah scene
        
        # Menu and game states
        self.game_state = "menu"  # "menu", "tutorial", "playing", "won"
        self.ocean_renderer: OceanRenderer = None
        self.particle_system: ParticleSystem = None
        self.button_manager = ButtonManager()
        self.mouse_pos = (0, 0)
        self.mouse_clicked = False
        
        # Fonts
        self.font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 72)
        self.subtitle_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        
    def setup(self, game_state: Dict[str, Any]):
        """Setup ship scene"""
        super().setup(game_state)
        
        # Initialize ocean renderer
        self.ocean_renderer = OceanRenderer(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.particle_system = ParticleSystem()
        
        # Start with menu
        self.game_state = "menu"
        self._setup_menu_buttons()
        
        # Initialize player ship (will be used when game starts)
        self.player_ship = Ship(
            SCREEN_WIDTH // 2 - SHIP_WIDTH // 2,
            SCREEN_HEIGHT // 2 - SHIP_HEIGHT // 2
        )
        self.player_ship.health = game_state.get('health', 100)
        self.player_ship.max_health = game_state.get('max_health', 100)
        
        # Reset enemies dan cannonballs
        self.enemies.clear()
        self.cannonballs.clear()
        self.enemy_spawn_timer = 0.0
        self.enemies_defeated = 0
        self.won = False
        
    def handle_event(self, event: pygame.event.Event):
        """Handle events"""
        # Update mouse position
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
        
        # Update mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.mouse_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_clicked = False
        
        if event.type == pygame.KEYDOWN:
            if self.game_state == "playing":
                if event.key == pygame.K_z:
                    # Shoot cannonball
                    self._shoot_cannonball()
            elif self.game_state == "tutorial":
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Start game from tutorial
                    self._start_game()
    
    def _shoot_cannonball(self):
        """Menembakkan cannonball dari player ship"""
        if not self.player_ship:
            return
        
        # Calculate angle dari ship center ke mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        ship_center_x = self.player_ship.rect.centerx
        ship_center_y = self.player_ship.rect.centery
        
        dx = mouse_x - ship_center_x
        dy = mouse_y - ship_center_y
        angle = math.atan2(dy, dx)
        
        # Create cannonball
        cannonball = Cannonball(ship_center_x, ship_center_y, angle)
        self.cannonballs.append(cannonball)
        
        # Create smoke effect at ship
        if self.particle_system:
            self.particle_system.create_smoke(ship_center_x, ship_center_y, 5)
    
    def update(self, dt: float):
        """Update scene logic"""
        # Update button manager
        self.button_manager.update(dt, self.mouse_pos, self.mouse_clicked)
        self.mouse_clicked = False
        
        # Update ocean effects
        if self.ocean_renderer:
            self.ocean_renderer.update(dt)
        
        # Update particle system
        if self.particle_system:
            self.particle_system.update(dt)
        
        if self.game_state != "playing":
            return
        
        if self.won:
            # Delay sebelum pindah scene
            self.win_timer += dt
            if self.win_timer >= self.win_delay:
                if self.state:
                    # Force update scene
                    self.state['current_scene'] = 'harbor'
                    print("Switching to harbor scene...")
                    # Force immediate update
                    return  # State akan diupdate di get_state
            return
        
        keys = pygame.key.get_pressed()
        
        # Update player ship
        if self.player_ship:
            self.player_ship.update(dt, keys)
            
            # Update state
            if self.state:
                self.state['health'] = self.player_ship.health
                self.state['ship_position'] = {'x': self.player_ship.x, 'y': self.player_ship.y}
        
        # Spawn enemies
        self.enemy_spawn_timer += dt
        if self.enemy_spawn_timer >= self.enemy_spawn_rate and len(self.enemies) < 3:
            self._spawn_enemy()
            self.enemy_spawn_timer = 0.0
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.set_target(self.player_ship)
            enemy.update(dt)
            
            # Check collision dengan player
            if self.player_ship and enemy.rect.colliderect(self.player_ship.rect):
                # Damage player
                self.player_ship.health -= 5 * dt
                if self.player_ship.health <= 0:
                    self.player_ship.health = 0
                    # Game over logic bisa ditambahkan di sini
        
        # Update cannonballs
        for cannonball in self.cannonballs[:]:
            cannonball.update(dt)
            
            # Water splash when cannonball hits boundary
            if not cannonball.active and cannonball.rect.colliderect(pygame.Rect(0, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT // 2)):
                if self.particle_system:
                    self.particle_system.create_water_splash(cannonball.x, cannonball.y, 8)
            
            # Check collision dengan enemies
            for enemy in self.enemies[:]:
                if cannonball.active and cannonball.rect.colliderect(enemy.rect):
                    enemy.health -= cannonball.damage
                    cannonball.active = False
                    
                    # Create impact effect
                    if self.particle_system:
                        self.particle_system.create_explosion(enemy.rect.centerx, enemy.rect.centery, (255, 200, 0), 10)
                    
                    if enemy.health <= 0:
                        # Create explosion effect
                        if self.particle_system:
                            self.particle_system.create_explosion(enemy.rect.centerx, enemy.rect.centery, (255, 100, 0), 25)
                            self.particle_system.create_smoke(enemy.rect.centerx, enemy.rect.centery, 20)
                        
                        self.enemies.remove(enemy)
                        self.enemies_defeated += 1
                        
                        # Check win condition
                        if self.enemies_defeated >= self.enemies_to_defeat:
                            if not self.won:
                                self.won = True
                                self.win_timer = 0.0
                                print(f"Kemenangan! Mengalahkan {self.enemies_defeated} enemies")
                                # Immediately update state to trigger scene change
                                if self.state:
                                    self.state['current_scene'] = 'harbor'
        
        # Remove inactive cannonballs
        self.cannonballs = [cb for cb in self.cannonballs if cb.active]
    
    def _spawn_enemy(self):
        """Spawn enemy ship di edge of screen"""
        side = random.randint(0, 3)
        if side == 0:  # Top
            x = random.randint(0, SCREEN_WIDTH)
            y = -50
        elif side == 1:  # Right
            x = SCREEN_WIDTH + 50
            y = random.randint(0, SCREEN_HEIGHT)
        elif side == 2:  # Bottom
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + 50
        else:  # Left
            x = -50
            y = random.randint(0, SCREEN_HEIGHT)
        
        enemy = EnemyShip(x, y)
        self.enemies.append(enemy)
    
    def _setup_menu_buttons(self):
        """Setup menu buttons"""
        self.button_manager.clear()
        
        # Start button
        start_button = Button(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50,
            200, 50, "Mulai Game", self._start_game,
            color=(0, 150, 0), hover_color=(0, 200, 0),
            text_color=(255, 255, 255), font_size=32, border_width=3
        )
        self.button_manager.add_button(start_button)
        
        # Tutorial button
        tutorial_button = Button(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120,
            200, 50, "Cara Bermain", self._show_tutorial,
            color=(0, 100, 200), hover_color=(0, 150, 255),
            text_color=(255, 255, 255), font_size=32, border_width=3
        )
        self.button_manager.add_button(tutorial_button)
    
    def _start_game(self):
        """Start the game"""
        self.game_state = "playing"
        self.button_manager.clear()
        # Reset game state
        self.enemies.clear()
        self.cannonballs.clear()
        self.enemy_spawn_timer = 0.0
        self.enemies_defeated = 0
        self.won = False
    
    def _show_tutorial(self):
        """Show tutorial screen"""
        self.game_state = "tutorial"
        self.button_manager.clear()
    
    def _render_menu(self, screen: pygame.Surface):
        """Render menu screen"""
        # Render ocean background
        if self.ocean_renderer:
            self.ocean_renderer.render(screen)
        
        # Title
        title = self.title_font.render("SPICE TRADER 1400", True, (255, 255, 100))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150))
        
        # Glow effect
        for offset in [(3, 3), (-3, 3), (3, -3), (-3, -3)]:
            glow = self.title_font.render("SPICE TRADER 1400", True, (255, 200, 50))
            glow_rect = glow.get_rect(center=(title_rect.centerx + offset[0], title_rect.centery + offset[1]))
            screen.blit(glow, glow_rect)
        
        screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.subtitle_font.render("Battle at Sea", True, (200, 200, 255))
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        screen.blit(subtitle, subtitle_rect)
        
        # Render buttons
        self.button_manager.render(screen)
    
    def _render_tutorial(self, screen: pygame.Surface):
        """Render tutorial screen"""
        # Render ocean background
        if self.ocean_renderer:
            self.ocean_renderer.render(screen)
        
        # Tutorial panel
        panel_width = 700
        panel_height = 500
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2
        
        # Panel background
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        overlay = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        overlay.fill((20, 20, 40, 230))
        screen.blit(overlay, panel_rect)
        pygame.draw.rect(screen, (100, 150, 200), panel_rect, 4)
        
        # Title
        title = self.subtitle_font.render("Cara Bermain", True, (255, 255, 100))
        title_rect = title.get_rect(center=(panel_x + panel_width // 2, panel_y + 40))
        screen.blit(title, title_rect)
        
        # Instructions
        instructions = [
            "🎮 KONTROL:",
            "",
            "WASD / Arrow Keys - Gerakkan kapal merchant",
            "Z - Tembakkan cannonball ke arah mouse",
            "",
            "🎯 TUJUAN:",
            "",
            "Kalahkan 5 kapal musuh untuk menang!",
            "Hindari collision dengan musuh",
            "Tembak musuh dengan cannonball",
            "",
            "💡 TIPS:",
            "",
            "• Gerakkan mouse untuk mengarahkan tembakan",
            "• Jaga jarak dengan musuh",
            "• Perhatikan health bar di kiri atas",
            "",
            "Tekan ENTER atau SPACE untuk mulai!"
        ]
        
        y_offset = 100
        for i, line in enumerate(instructions):
            if line.startswith("🎮") or line.startswith("🎯") or line.startswith("💡"):
                text = self.font.render(line, True, (255, 255, 100))
            elif line == "":
                continue
            else:
                text = self.small_font.render(line, True, (255, 255, 255))
            screen.blit(text, (panel_x + 30, panel_y + y_offset + i * 25))
    
    def render(self, screen: pygame.Surface):
        """Render scene"""
        if self.game_state == "menu":
            self._render_menu(screen)
            return
        elif self.game_state == "tutorial":
            self._render_tutorial(screen)
            return
        
        # Render ocean dengan efek realistis
        if self.ocean_renderer:
            self.ocean_renderer.render(screen)
        
        # Draw player ship
        if self.player_ship:
            self.player_ship.render(screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.render(screen)
        
        # Draw cannonballs
        for cannonball in self.cannonballs:
            cannonball.render(screen)
        
        # Draw particles
        if self.particle_system:
            self.particle_system.render(screen)
        
        # HUD Panel
        hud_panel = pygame.Rect(10, 10, 350, 120)
        overlay = pygame.Surface((hud_panel.width, hud_panel.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, hud_panel)
        pygame.draw.rect(screen, (100, 150, 200), hud_panel, 2)
        
        # Instructions
        instruction_text = self.small_font.render("WASD: Gerak | Z: Tembak", True, (255, 255, 255))
        screen.blit(instruction_text, (20, 20))
        
        # Enemy count
        enemy_count_text = self.font.render(f"Enemy: {self.enemies_defeated}/{self.enemies_to_defeat}", True, (255, 255, 255))
        screen.blit(enemy_count_text, (20, 50))
        
        # Health info
        if self.player_ship:
            health_text = self.small_font.render(f"Health: {int(self.player_ship.health)}/{self.player_ship.max_health}", True, (255, 255, 255))
            screen.blit(health_text, (20, 85))
        
        # Win message dengan animasi
        if self.won:
            # Background overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            # Win text dengan glow effect
            win_text = self.title_font.render("KEMENANGAN!", True, (255, 255, 0))
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            
            # Draw glow effect
            for offset in [(3, 3), (-3, 3), (3, -3), (-3, -3)]:
                glow_text = self.title_font.render("KEMENANGAN!", True, (255, 200, 0))
                glow_rect = glow_text.get_rect(center=(text_rect.centerx + offset[0], text_rect.centery + offset[1]))
                screen.blit(glow_text, glow_rect)
            
            screen.blit(win_text, text_rect)
            
            # Subtitle dengan countdown
            remaining_time = max(0, self.win_delay - self.win_timer)
            if remaining_time > 0:
                subtitle = self.font.render(f"Menuju ke Harbor... ({int(remaining_time) + 1})", True, (255, 255, 255))
                subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
                screen.blit(subtitle, subtitle_rect)
    
    def get_state(self) -> Dict[str, Any]:
        """Get current state"""
        return self.state

