"""
Game Engine Core - Sistem utama untuk menjalankan game
"""
import pygame
import sys
from typing import Optional, Dict, Any

class GameEngine:
    """Engine utama untuk menjalankan game"""
    
    def __init__(self, width: int = 1280, height: int = 720, title: str = "Spice Trader 1400"):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        
        # Scene management
        self.current_scene: Optional[Any] = None
        self.scenes: Dict[str, Any] = {}
        
        # Game state
        self.game_state = {
            'player_id': 'default',
            'current_scene': 'ship',
            'health': 100,
            'max_health': 100,
            'coins': 500,
            'inventory': {'spices': {}},
            'ship_position': {'x': 0, 'y': 0},
            'harbor_position': {'x': 0, 'y': 0},
            'story_progress': 0,
            'visited_islands': []
        }
        
        # Fonts
        self.fonts = {}
        self._load_fonts()
        
    def _load_fonts(self):
        """Load fonts untuk game"""
        try:
            self.fonts['default'] = pygame.font.Font(None, 24)
            self.fonts['title'] = pygame.font.Font(None, 48)
            self.fonts['small'] = pygame.font.Font(None, 18)
        except:
            # Fallback ke system font
            self.fonts['default'] = pygame.font.SysFont('arial', 24)
            self.fonts['title'] = pygame.font.SysFont('arial', 48)
            self.fonts['small'] = pygame.font.SysFont('arial', 18)
    
    def register_scene(self, name: str, scene: Any):
        """Mendaftarkan scene ke engine"""
        self.scenes[name] = scene
        
    def change_scene(self, scene_name: str):
        """Mengubah scene yang aktif"""
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]
            self.current_scene.setup(self.game_state)
            self.game_state['current_scene'] = scene_name
            return True
        return False
    
    def handle_events(self):
        """Handle semua event dari pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif self.current_scene:
                    self.current_scene.handle_event(event)
            elif self.current_scene:
                self.current_scene.handle_event(event)
    
    def update(self, dt: float):
        """Update game logic"""
        # Simpan scene name sebelum update
        previous_scene = self.game_state.get('current_scene', 'ship')
        
        if self.current_scene:
            self.current_scene.update(dt)
            # Update game state dari scene
            updated_state = self.current_scene.get_state()
            if updated_state:
                self.game_state.update(updated_state)
        
        # Check jika scene berubah dan auto-switch
        current_scene_name = self.game_state.get('current_scene', 'ship')
        if previous_scene != current_scene_name and current_scene_name in self.scenes:
            print(f"Scene berubah dari '{previous_scene}' ke '{current_scene_name}'")
            self.change_scene(current_scene_name)
    
    def render(self):
        """Render semua objek ke screen"""
        # Clear screen dengan background
        self.screen.fill((30, 60, 90))  # Dark blue ocean color
        
        if self.current_scene:
            self.current_scene.render(self.screen)
        
        # Render HUD
        self._render_hud()
        
        pygame.display.flip()
    
    def _render_hud(self):
        """Render HUD (Health, Coins, dll)"""
        # Health bar
        bar_width = 200
        bar_height = 20
        bar_x = 10
        bar_y = 10
        
        # Background
        pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        # Health fill
        health_percent = self.game_state['health'] / self.game_state['max_health']
        health_width = int(bar_width * health_percent)
        health_color = (255, 0, 0) if health_percent < 0.3 else (0, 255, 0) if health_percent > 0.6 else (255, 255, 0)
        pygame.draw.rect(self.screen, health_color, (bar_x, bar_y, health_width, bar_height))
        # Border
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Health text
        health_text = self.fonts['small'].render(f"HP: {self.game_state['health']}/{self.game_state['max_health']}", True, (255, 255, 255))
        self.screen.blit(health_text, (bar_x + 5, bar_y + 2))
        
        # Coins display
        coins_text = self.fonts['default'].render(f"Koin: {self.game_state['coins']}", True, (255, 215, 0))
        self.screen.blit(coins_text, (bar_x, bar_y + 30))
        
        # Scene name
        scene_text = self.fonts['small'].render(f"Scene: {self.game_state['current_scene']}", True, (255, 255, 255))
        self.screen.blit(scene_text, (bar_x, bar_y + 60))
    
    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()
        sys.exit()
    
    def get_game_state(self) -> Dict[str, Any]:
        """Mendapatkan game state saat ini"""
        return self.game_state.copy()
    
    def set_game_state(self, state: Dict[str, Any]):
        """Mengatur game state"""
        self.game_state.update(state)

