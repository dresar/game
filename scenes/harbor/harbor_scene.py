"""
Harbor Scene - Scene untuk gameplay di pelabuhan
Style: Zenless Zone Zero semi-open world
"""
import pygame
import math
import sys
import os
from typing import List, Dict, Any, Optional

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from game_engine.scene import Scene
from utils.constants import *
from utils.ui_button import Button, ButtonManager
from utils.database import db
from utils.icons import IconRenderer
from utils.inventory_display import InventoryCart
from utils.ocean_effects import OceanRenderer
from utils.minimap import Minimap

class Player:
    """Player character untuk harbor exploration"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.speed = 200
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def update(self, dt: float, keys: pygame.key.ScancodeWrapper):
        """Update player position"""
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
        
        # Boundary check (allow movement in larger area)
        self.x = max(0, min(SCREEN_WIDTH * 2 - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT * 2 - self.height, self.y))
        
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    
    def render(self, screen: pygame.Surface, camera_x: int, camera_y: int):
        """Render player dengan camera offset"""
        screen_x = self.rect.x - camera_x
        screen_y = self.rect.y - camera_y
        
        # Draw player sebagai character dengan detail lebih baik
        # Body (circle)
        center_x = screen_x + self.width // 2
        center_y = screen_y + self.height // 2
        pygame.draw.circle(screen, (100, 200, 255), (center_x, center_y), self.width // 2)
        pygame.draw.circle(screen, (150, 220, 255), (center_x, center_y), self.width // 2 - 2)
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), self.width // 2, 2)
        
        # Head
        head_y = center_y - self.height // 3
        pygame.draw.circle(screen, (255, 220, 177), (center_x, head_y), 6)
        
        # Simple body indicator
        pygame.draw.rect(screen, (50, 150, 200), 
                        (center_x - 4, center_y - 2, 8, 10))
        
        # Draw player label dengan background
        font = pygame.font.Font(None, 14)
        text = font.render("PLAYER", True, (255, 255, 255))
        text_rect = text.get_rect(center=(center_x, screen_y - 12))
        bg_rect = pygame.Rect(text_rect.x - 4, text_rect.y - 2, text_rect.width + 8, text_rect.height + 4)
        overlay = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, bg_rect)
        screen.blit(text, text_rect)

class NPC:
    """NPC untuk interaction"""
    def __init__(self, x: float, y: float, name: str, npc_type: str = "merchant"):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.name = name
        self.npc_type = npc_type  # "merchant", "restaurant", "story"
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.interaction_range = 50
        self.dialog_active = False
        
    def can_interact(self, player: Player) -> bool:
        """Check apakah player dalam range interaction"""
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx*dx + dy*dy)
        return distance <= self.interaction_range
    
    def render(self, screen: pygame.Surface, camera_x: int, camera_y: int):
        """Render NPC dengan camera offset"""
        screen_x = self.rect.x - camera_x
        screen_y = self.rect.y - camera_y
        
        # Color berdasarkan type
        if self.npc_type == "merchant":
            color = (255, 200, 100)
            icon = "🛒"
        elif self.npc_type == "restaurant":
            color = (255, 100, 100)
            icon = "🍜"
        else:
            color = (150, 150, 255)
            icon = "📖"
        
        # NPC body (circle dengan detail)
        center_x = screen_x + self.width // 2
        center_y = screen_y + self.height // 2
        pygame.draw.circle(screen, color, (center_x, center_y), self.width // 2)
        pygame.draw.circle(screen, tuple(min(255, c + 30) for c in color), (center_x, center_y), self.width // 2 - 2)
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), self.width // 2, 2)
        
        # Icon indicator
        icon_font = pygame.font.Font(None, 20)
        icon_text = icon_font.render(icon, True, (255, 255, 255))
        icon_rect = icon_text.get_rect(center=(center_x, center_y))
        screen.blit(icon_text, icon_rect)
        
        # Draw name dengan background
        font = pygame.font.Font(None, 14)
        text = font.render(self.name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(center_x, screen_y - 15))
        bg_rect = pygame.Rect(text_rect.x - 4, text_rect.y - 2, text_rect.width + 8, text_rect.height + 4)
        overlay = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, bg_rect)
        screen.blit(text, text_rect)
        
        # Draw interaction indicator dengan animasi
        if self.dialog_active:
            indicator_bg = pygame.Rect(screen_x + self.width // 2 - 10, screen_y + self.height + 5, 20, 20)
            pygame.draw.ellipse(screen, (255, 255, 0, 200), indicator_bg)
            pygame.draw.ellipse(screen, (255, 255, 255), indicator_bg, 2)
            indicator = font.render("E", True, (0, 0, 0))
            indicator_rect = indicator.get_rect(center=(center_x, screen_y + self.height + 15))
            screen.blit(indicator, indicator_rect)

class Building:
    """Building di harbor"""
    def __init__(self, x: float, y: float, width: int, height: int, building_type: str):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.building_type = building_type
        self.rect = pygame.Rect(x, y, width, height)
        
    def render(self, screen: pygame.Surface, camera_x: int, camera_y: int):
        """Render building dengan camera offset"""
        screen_x = self.rect.x - camera_x
        screen_y = self.rect.y - camera_y
        
        # Color berdasarkan type dengan gradient
        if self.building_type == "shop":
            base_color = (100, 150, 200)
            roof_color = (80, 120, 160)
            window_color = (255, 255, 200)
        elif self.building_type == "restaurant":
            base_color = (200, 100, 100)
            roof_color = (160, 80, 80)
            window_color = (255, 200, 200)
        else:
            base_color = (150, 150, 150)
            roof_color = (120, 120, 120)
            window_color = (200, 200, 200)
        
        building_rect = pygame.Rect(screen_x, screen_y, self.width, self.height)
        
        # Building base
        pygame.draw.rect(screen, base_color, building_rect)
        pygame.draw.rect(screen, tuple(max(0, c - 20) for c in base_color), 
                        (screen_x, screen_y, self.width, self.height // 2))
        
        # Roof (triangle)
        roof_points = [
            (screen_x, screen_y),
            (screen_x + self.width // 2, screen_y - self.height // 4),
            (screen_x + self.width, screen_y)
        ]
        pygame.draw.polygon(screen, roof_color, roof_points)
        pygame.draw.polygon(screen, tuple(max(0, c - 30) for c in roof_color), roof_points, 2)
        
        # Windows
        window_size = 12
        window1_rect = pygame.Rect(screen_x + self.width // 4 - window_size // 2, 
                                  screen_y + self.height // 3, window_size, window_size)
        window2_rect = pygame.Rect(screen_x + 3 * self.width // 4 - window_size // 2,
                                  screen_y + self.height // 3, window_size, window_size)
        pygame.draw.rect(screen, window_color, window1_rect)
        pygame.draw.rect(screen, window_color, window2_rect)
        pygame.draw.rect(screen, (0, 0, 0), window1_rect, 2)
        pygame.draw.rect(screen, (0, 0, 0), window2_rect, 2)
        
        # Door
        door_rect = pygame.Rect(screen_x + self.width // 2 - 8, 
                               screen_y + self.height - 20, 16, 20)
        pygame.draw.rect(screen, (101, 67, 33), door_rect)
        pygame.draw.rect(screen, (0, 0, 0), door_rect, 2)
        
        # Border
        pygame.draw.rect(screen, (255, 255, 255), building_rect, 2)
        
        # Draw label dengan background
        font = pygame.font.Font(None, 14)
        text = font.render(self.building_type.upper(), True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_x + self.width // 2, screen_y + self.height + 15))
        bg_rect = pygame.Rect(text_rect.x - 4, text_rect.y - 2, text_rect.width + 8, text_rect.height + 4)
        overlay = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, bg_rect)
        screen.blit(text, text_rect)

class HarborScene(Scene):
    """Scene untuk gameplay di pelabuhan"""
    
    def __init__(self):
        super().__init__("harbor")
        self.player: Player = None
        self.npcs: List[NPC] = []
        self.buildings: List[Building] = []
        self.camera_x = 0
        self.camera_y = 0
        self.current_npc: Optional[NPC] = None
        self.show_dialog = False
        self.show_shop = False
        self.show_restaurant = False
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.button_manager = ButtonManager()
        self.mouse_pos = (0, 0)
        self.mouse_clicked = False
        self.player_id = 'default'
        self.close_button = None
        self.inventory_cart = InventoryCart(SCREEN_WIDTH - 320, 10, 300, 250)
        self.show_inventory = False
        self.harbor_effects = None  # Untuk efek visual harbor
        self.minimap = Minimap(SCREEN_WIDTH - 220, SCREEN_HEIGHT - 170, 200, 150)
        
    def setup(self, game_state: Dict[str, Any]):
        """Setup harbor scene"""
        super().setup(game_state)
        
        # Get player_id from state
        self.player_id = game_state.get('player_id', 'default')
        
        # Load inventory from database
        if self.state:
            db_inventory = db.get_inventory_spices(self.player_id)
            if db_inventory:
                if 'inventory' not in self.state:
                    self.state['inventory'] = {'spices': {}}
                self.state['inventory']['spices'].update(db_inventory)
            
            db_foods = db.get_tried_foods(self.player_id)
            if db_foods:
                self.state['tried_foods'] = db_foods
        
        # Initialize player
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Initialize harbor effects (optional ocean view in background)
        # self.harbor_effects = OceanRenderer(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Initialize NPCs
        self.npcs = [
            NPC(200, 200, "Pedagang Rempah", "merchant"),
            NPC(500, 300, "Warung Makan", "restaurant"),
            NPC(800, 400, "Elderman", "story"),
            NPC(300, 600, "Pedagang Rempah 2", "merchant"),
            NPC(600, 500, "Restoran Tradisional", "restaurant")
        ]
        
        # Initialize buildings
        self.buildings = [
            Building(150, 150, 80, 80, "shop"),
            Building(450, 250, 80, 80, "restaurant"),
            Building(750, 350, 80, 80, "shop"),
            Building(250, 550, 80, 80, "restaurant"),
            Building(550, 450, 80, 80, "shop")
        ]
        
        # Reset camera
        self.camera_x = 0
        self.camera_y = 0
        self.current_npc = None
        self.show_dialog = False
        self.show_shop = False
        self.show_restaurant = False
        
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
            if event.key == pygame.K_i:
                # Toggle inventory cart
                self.show_inventory = not self.show_inventory
                self.inventory_cart.visible = self.show_inventory
            elif event.key == pygame.K_e:
                # Interact with NPC
                if self.current_npc:
                    if self.current_npc.npc_type == "merchant":
                        self.show_shop = True
                        self.show_dialog = False
                        self._setup_shop_buttons()
                    elif self.current_npc.npc_type == "restaurant":
                        self.show_restaurant = True
                        self.show_dialog = False
                        self._setup_restaurant_buttons()
                    else:
                        self.show_dialog = True
                        self._setup_story_buttons()
    
    def update(self, dt: float):
        """Update scene logic"""
        # Update button manager
        self.button_manager.update(dt, self.mouse_pos, self.mouse_clicked)
        self.mouse_clicked = False  # Reset setelah update
        
        keys = pygame.key.get_pressed()
        
        # Update player
        if self.player:
            self.player.update(dt, keys)
            
            # Update camera to follow player
            self.camera_x = self.player.rect.centerx - SCREEN_WIDTH // 2
            self.camera_y = self.player.rect.centery - SCREEN_HEIGHT // 2
            
            # Clamp camera
            self.camera_x = max(0, min(SCREEN_WIDTH * 2 - SCREEN_WIDTH, self.camera_x))
            self.camera_y = max(0, min(SCREEN_HEIGHT * 2 - SCREEN_HEIGHT, self.camera_y))
            
            # Update state
            if self.state:
                self.state['harbor_position'] = {'x': self.player.x, 'y': self.player.y}
                # Save game state to database periodically
                db.save_game_state(self.player_id, self.state)
        
        # Check NPC interactions
        self.current_npc = None
        for npc in self.npcs:
            if npc.can_interact(self.player):
                self.current_npc = npc
                npc.dialog_active = True
            else:
                npc.dialog_active = False
    
    def render(self, screen: pygame.Surface):
        """Render scene"""
        # Draw harbor background dengan gradient yang lebih menarik
        # Sky gradient
        for y in range(SCREEN_HEIGHT // 2):
            ratio = y / (SCREEN_HEIGHT // 2)
            r = int(135 + (100 - 135) * ratio)
            g = int(206 + (150 - 206) * ratio)
            b = int(235 + (200 - 235) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Ground dengan texture
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT // 2, SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2)
        # Base color
        for y in range(SCREEN_HEIGHT // 2, SCREEN_HEIGHT * 2, 2):
            ratio = (y - SCREEN_HEIGHT // 2) / (SCREEN_HEIGHT * 1.5)
            r = int(139 + (100 - 139) * ratio)
            g = int(115 + (80 - 115) * ratio)
            b = int(85 + (60 - 85) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH * 2, y))
        
        # Draw grid pattern untuk semi-open world effect (subtle)
        for x in range(0, SCREEN_WIDTH * 2, 100):
            color = (110, 90, 65) if (x // 100) % 2 == 0 else (120, 100, 75)
            pygame.draw.line(screen, color, 
                           (x - self.camera_x, SCREEN_HEIGHT // 2), 
                           (x - self.camera_x, SCREEN_HEIGHT * 2), 1)
        for y in range(SCREEN_HEIGHT // 2, SCREEN_HEIGHT * 2, 100):
            color = (110, 90, 65) if ((y - SCREEN_HEIGHT // 2) // 100) % 2 == 0 else (120, 100, 75)
            pygame.draw.line(screen, color, 
                           (0, y - self.camera_y), 
                           (SCREEN_WIDTH * 2, y - self.camera_y), 1)
        
        # Decorative elements (clouds, sun)
        if self.harbor_effects:
            self.harbor_effects.render(screen)
        
        # Draw buildings
        for building in self.buildings:
            building.render(screen, self.camera_x, self.camera_y)
        
        # Draw NPCs
        for npc in self.npcs:
            npc.render(screen, self.camera_x, self.camera_y)
        
        # Draw player
        if self.player:
            self.player.render(screen, self.camera_x, self.camera_y)
        
        # HUD Panel
        hud_panel = pygame.Rect(10, 10, 250, 100)
        overlay = pygame.Surface((hud_panel.width, hud_panel.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, hud_panel)
        pygame.draw.rect(screen, (100, 150, 200), hud_panel, 2)
        
        # Coins display
        coins = self.state.get('coins', 0) if self.state else 0
        IconRenderer.draw_coin_icon(screen, 20, 20, 24)
        coins_text = self.font.render(f"Koin: {coins}", True, (255, 215, 0))
        screen.blit(coins_text, (50, 20))
        
        # Inventory button hint
        inv_hint = self.small_font.render("Tekan I untuk keranjang", True, (200, 200, 200))
        screen.blit(inv_hint, (20, 50))
        
        # Interaction hint
        if self.current_npc:
            hint_text = self.small_font.render(f"Tekan E: {self.current_npc.name}", True, (255, 255, 0))
            screen.blit(hint_text, (20, 75))
        
        # Draw inventory cart
        if self.show_inventory:
            self.inventory_cart.render(screen, self.state)
        
        # Draw minimap
        if self.player:
            npc_positions = [(npc.x, npc.y, npc.npc_type) for npc in self.npcs]
            self.minimap.render(
                screen,
                (self.player.x, self.player.y),
                npc_positions,
                self.camera_x, self.camera_y,
                SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2
            )
        
        # Draw dialogs
        if self.show_shop:
            self._render_shop_dialog(screen)
            self.button_manager.render(screen)
        elif self.show_restaurant:
            self._render_restaurant_dialog(screen)
            self.button_manager.render(screen)
        elif self.show_dialog:
            self._render_story_dialog(screen)
            self.button_manager.render(screen)
    
    def _close_dialog(self):
        """Close semua dialog"""
        self.show_dialog = False
        self.show_shop = False
        self.show_restaurant = False
        self.button_manager.clear()
    
    def _setup_shop_buttons(self):
        """Setup buttons untuk shop dialog"""
        self.button_manager.clear()
        dialog_width = 700
        dialog_height = 500
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        
        # Close button di pojok kanan atas
        close_button = Button(
            dialog_x + dialog_width - 35, dialog_y + 10,
            25, 25, "", self._close_dialog,
            color=(200, 50, 50), hover_color=(255, 0, 0),
            text_color=(255, 255, 255), border_width=2
        )
        self.button_manager.add_button(close_button)
        
        y_offset = 90
        
        for i, (spice_id, spice_info) in enumerate(SPICES.items()):
            spice_name = spice_info['name']
            spice_price = spice_info['price']
            
            # Check if already owned
            owned_qty = 0
            if self.state and 'inventory' in self.state and 'spices' in self.state['inventory']:
                owned_qty = self.state['inventory']['spices'].get(spice_name, 0)
            
            def make_buy_func(s_id=spice_id, s_name=spice_name, s_price=spice_price):
                def buy_func():
                    if self.state:
                        coins = self.state.get('coins', 0)
                        if coins >= s_price:
                            self.state['coins'] -= s_price
                            if 'inventory' not in self.state:
                                self.state['inventory'] = {'spices': {}}
                            if s_name not in self.state['inventory']['spices']:
                                self.state['inventory']['spices'][s_name] = 0
                            self.state['inventory']['spices'][s_name] += 1
                            
                            # Save to database
                            db.save_inventory_spice(self.player_id, s_name, self.state['inventory']['spices'][s_name])
                            db.add_purchase(self.player_id, 'spice', s_name, s_price, 1)
                            
                            # Add to inventory cart
                            self.inventory_cart.add_item('spice', s_name, 1)
                            
                            print(f"Beli {s_name} dengan {s_price} koin")
                return buy_func
            
            buy_button = Button(
                dialog_x + dialog_width - 130, dialog_y + y_offset + i * 50,
                100, 30, "Beli", make_buy_func(),
                color=(0, 120, 0), hover_color=(0, 180, 0),
                text_color=(255, 255, 255), font_size=18
            )
            self.button_manager.add_button(buy_button)
    
    def _render_shop_dialog(self, screen: pygame.Surface):
        """Render shop dialog untuk membeli rempah"""
        dialog_width = 700
        dialog_height = 500
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        
        # Dialog background dengan gradient effect
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(screen, (25, 25, 35), dialog_rect)
        pygame.draw.rect(screen, (80, 80, 100), dialog_rect, 4)
        
        # Title bar dengan background
        title_bg = pygame.Rect(dialog_x, dialog_y, dialog_width, 60)
        pygame.draw.rect(screen, (50, 50, 70), title_bg)
        pygame.draw.rect(screen, (100, 100, 120), title_bg, 2)
        
        # Title text
        title = pygame.font.Font(None, 28).render("🛒 Toko Rempah", True, (255, 255, 100))
        screen.blit(title, (dialog_x + 25, dialog_y + 18))
        
        # Spice list dengan spacing lebih baik
        y_offset = 90
        coins = self.state.get('coins', 0) if self.state else 0
        
        # Header
        header_y = dialog_y + 70
        header_bg = pygame.Rect(dialog_x + 15, header_y, dialog_width - 30, 25)
        pygame.draw.rect(screen, (40, 40, 60), header_bg)
        header_text = self.small_font.render("Rempah", True, (255, 255, 200))
        screen.blit(header_text, (dialog_x + 60, header_y + 4))
        price_text = self.small_font.render("Harga", True, (255, 255, 200))
        screen.blit(price_text, (dialog_x + 250, header_y + 4))
        owned_text = self.small_font.render("Dimiliki", True, (255, 255, 200))
        screen.blit(owned_text, (dialog_x + 400, header_y + 4))
        
        for i, (spice_id, spice_info) in enumerate(SPICES.items()):
            spice_name = spice_info['name']
            spice_price = spice_info['price']
            
            # Check owned quantity
            owned_qty = 0
            if self.state and 'inventory' in self.state and 'spices' in self.state['inventory']:
                owned_qty = self.state['inventory']['spices'].get(spice_name, 0)
            
            item_y = dialog_y + y_offset + i * 50
            
            # Item background dengan spacing lebih baik
            item_bg = pygame.Rect(dialog_x + 15, item_y - 5, dialog_width - 30, 45)
            bg_color = (35, 35, 45) if i % 2 == 0 else (30, 30, 40)
            pygame.draw.rect(screen, bg_color, item_bg)
            pygame.draw.rect(screen, (60, 60, 80), item_bg, 1)
            
            # Icon spice
            IconRenderer.draw_spice_icon(screen, dialog_x + 25, item_y + 8, 28)
            
            # Spice name
            name_text = self.font.render(spice_name, True, (255, 255, 255))
            screen.blit(name_text, (dialog_x + 60, item_y + 5))
            
            # Price dengan coin icon
            IconRenderer.draw_coin_icon(screen, dialog_x + 250, item_y + 8, 20)
            price_text = self.small_font.render(f"{spice_price}", True, (255, 215, 0))
            screen.blit(price_text, (dialog_x + 275, item_y + 8))
            
            # Owned quantity
            owned_text = self.small_font.render(f"x{owned_qty}", True, (100, 255, 100))
            screen.blit(owned_text, (dialog_x + 400, item_y + 8))
        
        # Inventory section
        inv_y = dialog_y + y_offset + len(SPICES) * 50 + 10
        inv_bg = pygame.Rect(dialog_x + 15, inv_y, dialog_width - 30, 80)
        pygame.draw.rect(screen, (40, 40, 60), inv_bg)
        pygame.draw.rect(screen, (80, 80, 100), inv_bg, 2)
        
        inv_title = self.small_font.render("📦 Inventory Anda:", True, (255, 255, 200))
        screen.blit(inv_title, (dialog_x + 25, inv_y + 5))
        
        # Display owned spices
        inv_items_y = inv_y + 25
        if self.state and 'inventory' in self.state and 'spices' in self.state['inventory']:
            owned_items = [(name, qty) for name, qty in self.state['inventory']['spices'].items() if qty > 0]
            if owned_items:
                for idx, (name, qty) in enumerate(owned_items[:4]):  # Max 4 items
                    item_text = self.small_font.render(f"{name} x{qty}", True, (200, 255, 200))
                    screen.blit(item_text, (dialog_x + 25 + idx * 150, inv_items_y))
            else:
                no_items = self.small_font.render("Belum ada rempah", True, (150, 150, 150))
                screen.blit(no_items, (dialog_x + 25, inv_items_y))
        
        # Coins display dengan background
        coins_bg = pygame.Rect(dialog_x, dialog_y + dialog_height - 50, dialog_width, 40)
        pygame.draw.rect(screen, (40, 40, 60), coins_bg)
        pygame.draw.rect(screen, (80, 80, 100), coins_bg, 2)
        
        IconRenderer.draw_coin_icon(screen, dialog_x + 20, dialog_y + dialog_height - 40, 24)
        coins_text = self.font.render(f"Koin: {coins}", True, (255, 215, 0))
        screen.blit(coins_text, (dialog_x + 50, dialog_y + dialog_height - 40))
    
    def _setup_restaurant_buttons(self):
        """Setup buttons untuk restaurant dialog"""
        self.button_manager.clear()
        dialog_width = 700
        dialog_height = 500
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        
        # Close button
        close_button = Button(
            dialog_x + dialog_width - 35, dialog_y + 10,
            25, 25, "", self._close_dialog,
            color=(200, 50, 50), hover_color=(255, 0, 0),
            text_color=(255, 255, 255), border_width=2
        )
        self.button_manager.add_button(close_button)
        
        y_offset = 90
        
        for i, (food_id, food_info) in enumerate(FOODS.items()):
            food_name = food_info['name']
            food_price = food_info['price']
            
            # Check if already tried
            tried = False
            if self.state and 'tried_foods' in self.state:
                tried = food_name in self.state['tried_foods']
            
            def make_buy_func(f_id=food_id, f_name=food_name, f_price=food_price, f_region=food_info['region']):
                def buy_func():
                    if self.state:
                        coins = self.state.get('coins', 0)
                        if coins >= f_price:
                            self.state['coins'] -= f_price
                            if 'tried_foods' not in self.state:
                                self.state['tried_foods'] = []
                            if f_name not in self.state['tried_foods']:
                                self.state['tried_foods'].append(f_name)
                            
                            # Save to database
                            db.add_tried_food(self.player_id, f_name, f_region)
                            db.add_purchase(self.player_id, 'food', f_name, f_price, 1)
                            
                            # Add to inventory cart
                            self.inventory_cart.add_item('food', f_name, 1)
                            
                            print(f"Mencoba {f_name} dengan {f_price} koin")
                return buy_func
            
            buy_button = Button(
                dialog_x + dialog_width - 130, dialog_y + y_offset + i * 55,
                100, 30, "✓ Coba" if tried else "Coba", make_buy_func(),
                color=(120, 0, 0) if not tried else (80, 80, 80),
                hover_color=(180, 0, 0) if not tried else (100, 100, 100),
                text_color=(255, 255, 255), font_size=18
            )
            self.button_manager.add_button(buy_button)
    
    def _render_restaurant_dialog(self, screen: pygame.Surface):
        """Render restaurant dialog untuk mencoba makanan khas"""
        dialog_width = 700
        dialog_height = 500
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        
        # Dialog background dengan gradient effect
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(screen, (35, 25, 25), dialog_rect)
        pygame.draw.rect(screen, (100, 80, 80), dialog_rect, 4)
        
        # Title bar
        title_bg = pygame.Rect(dialog_x, dialog_y, dialog_width, 60)
        pygame.draw.rect(screen, (70, 50, 50), title_bg)
        pygame.draw.rect(screen, (120, 90, 90), title_bg, 2)
        
        title = pygame.font.Font(None, 28).render("🍜 Restoran - Makanan Khas Daerah", True, (255, 255, 100))
        screen.blit(title, (dialog_x + 25, dialog_y + 18))
        
        # Header
        header_y = dialog_y + 70
        header_bg = pygame.Rect(dialog_x + 15, header_y, dialog_width - 30, 25)
        pygame.draw.rect(screen, (50, 40, 40), header_bg)
        header_text = self.small_font.render("Makanan", True, (255, 255, 200))
        screen.blit(header_text, (dialog_x + 60, header_y + 4))
        region_text = self.small_font.render("Daerah", True, (255, 255, 200))
        screen.blit(region_text, (dialog_x + 250, header_y + 4))
        price_text = self.small_font.render("Harga", True, (255, 255, 200))
        screen.blit(price_text, (dialog_x + 400, header_y + 4))
        
        # Food list dengan spacing lebih baik
        y_offset = 90
        coins = self.state.get('coins', 0) if self.state else 0
        
        for i, (food_id, food_info) in enumerate(FOODS.items()):
            food_name = food_info['name']
            food_price = food_info['price']
            food_region = food_info['region']
            food_desc = food_info['description']
            
            # Check if tried
            tried = False
            if self.state and 'tried_foods' in self.state:
                tried = food_name in self.state['tried_foods']
            
            item_y = dialog_y + y_offset + i * 55
            
            # Item background dengan spacing lebih baik
            item_bg = pygame.Rect(dialog_x + 15, item_y - 5, dialog_width - 30, 50)
            bg_color = (45, 35, 35) if i % 2 == 0 else (40, 30, 30)
            pygame.draw.rect(screen, bg_color, item_bg)
            pygame.draw.rect(screen, (80, 60, 60), item_bg, 1)
            
            # Food icon
            IconRenderer.draw_food_icon(screen, dialog_x + 25, item_y + 8, 32)
            
            # Food name dengan checkmark jika sudah dicoba
            name_prefix = "✓ " if tried else ""
            name_text = self.font.render(f"{name_prefix}{food_name}", True, (255, 255, 255) if not tried else (150, 255, 150))
            screen.blit(name_text, (dialog_x + 65, item_y + 5))
            
            # Region
            region_text = self.small_font.render(food_region, True, (200, 200, 255))
            screen.blit(region_text, (dialog_x + 250, item_y + 8))
            
            # Price dengan coin icon
            IconRenderer.draw_coin_icon(screen, dialog_x + 400, item_y + 10, 20)
            price_text = self.small_font.render(f"{food_price}", True, (255, 215, 0))
            screen.blit(price_text, (dialog_x + 425, item_y + 10))
            
            # Description
            desc_text = self.small_font.render(food_desc, True, (200, 200, 200))
            screen.blit(desc_text, (dialog_x + 65, item_y + 25))
        
        # Tried foods section
        tried_y = dialog_y + y_offset + len(FOODS) * 55 + 10
        tried_bg = pygame.Rect(dialog_x + 15, tried_y, dialog_width - 30, 80)
        pygame.draw.rect(screen, (50, 40, 40), tried_bg)
        pygame.draw.rect(screen, (100, 80, 80), tried_bg, 2)
        
        tried_title = self.small_font.render("✓ Makanan yang Sudah Dicoba:", True, (255, 255, 200))
        screen.blit(tried_title, (dialog_x + 25, tried_y + 5))
        
        tried_items_y = tried_y + 25
        if self.state and 'tried_foods' in self.state and self.state['tried_foods']:
            for idx, food_name in enumerate(self.state['tried_foods'][:4]):  # Max 4 items
                food_text = self.small_font.render(f"✓ {food_name}", True, (150, 255, 150))
                screen.blit(food_text, (dialog_x + 25 + idx * 150, tried_items_y))
        else:
            no_items = self.small_font.render("Belum ada makanan yang dicoba", True, (150, 150, 150))
            screen.blit(no_items, (dialog_x + 25, tried_items_y))
        
        # Coins display
        coins_bg = pygame.Rect(dialog_x, dialog_y + dialog_height - 50, dialog_width, 40)
        pygame.draw.rect(screen, (50, 40, 40), coins_bg)
        pygame.draw.rect(screen, (100, 80, 80), coins_bg, 2)
        
        IconRenderer.draw_coin_icon(screen, dialog_x + 20, dialog_y + dialog_height - 40, 24)
        coins_text = self.font.render(f"Koin: {coins}", True, (255, 215, 0))
        screen.blit(coins_text, (dialog_x + 50, dialog_y + dialog_height - 40))
    
    def _setup_story_buttons(self):
        """Setup buttons untuk story dialog"""
        self.button_manager.clear()
        dialog_width = 650
        dialog_height = 400
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        
        # Close button
        close_button = Button(
            dialog_x + dialog_width - 35, dialog_y + 10,
            25, 25, "", self._close_dialog,
            color=(200, 50, 50), hover_color=(255, 0, 0),
            text_color=(255, 255, 255), border_width=2
        )
        self.button_manager.add_button(close_button)
    
    def _render_story_dialog(self, screen: pygame.Surface):
        """Render story dialog"""
        dialog_width = 650
        dialog_height = 400
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        
        # Dialog background dengan gradient
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(screen, (25, 25, 45), dialog_rect)
        pygame.draw.rect(screen, (90, 90, 140), dialog_rect, 4)
        
        # Title bar
        title_bg = pygame.Rect(dialog_x, dialog_y, dialog_width, 60)
        pygame.draw.rect(screen, (55, 55, 75), title_bg)
        pygame.draw.rect(screen, (100, 100, 150), title_bg, 2)
        
        title = pygame.font.Font(None, 28).render("📖 Cerita - Pedagang Tahun 1400 M", True, (255, 255, 100))
        screen.blit(title, (dialog_x + 25, dialog_y + 18))
        
        # Story text dengan background
        story_bg = pygame.Rect(dialog_x + 15, dialog_y + 70, dialog_width - 30, dialog_height - 120)
        pygame.draw.rect(screen, (35, 35, 55), story_bg)
        pygame.draw.rect(screen, (70, 70, 100), story_bg, 2)
        
        story_lines = [
            "Selamat datang di Pelabuhan!",
            "",
            "Sebagai pedagang dari luar negeri tahun 1400 M,",
            "Anda datang ke Indonesia untuk berdagang rempah.",
            "Jelajahi pelabuhan, beli rempah, dan coba",
            "makanan khas daerah untuk mempelajari budaya.",
            "",
            "Setelah tinggal di Indonesia untuk waktu yang lama,",
            "Anda mulai tertarik dengan budaya di kepulauan ini.",
            "",
            "Selamat menjelajah!"
        ]
        
        y_offset = 90
        for i, line in enumerate(story_lines):
            if line:
                text = self.small_font.render(line, True, (255, 255, 255))
                screen.blit(text, (dialog_x + 35, dialog_y + y_offset + i * 22))
    
    def get_state(self) -> Dict[str, Any]:
        """Get current state"""
        return self.state

