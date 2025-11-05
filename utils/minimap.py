"""
Minimap - Mini map untuk navigasi di harbor
"""
import pygame
from typing import List, Tuple, Optional
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Minimap:
    """Mini map untuk menampilkan posisi player dan NPCs"""
    
    def __init__(self, x: int, y: int, width: int = 200, height: int = 150):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = True
        
    def render(self, screen: pygame.Surface, 
               player_pos: Tuple[float, float],
               npc_positions: List[Tuple[float, float, str]],
               camera_x: int, camera_y: int,
               world_width: int, world_height: int):
        """Render minimap"""
        if not self.visible:
            return
        
        # Minimap background
        map_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((20, 20, 40, 200))
        screen.blit(overlay, map_rect)
        pygame.draw.rect(screen, (100, 150, 200), map_rect, 2)
        
        # Title
        font = pygame.font.Font(None, 18)
        title = font.render("Peta", True, (255, 255, 255))
        screen.blit(title, (self.x + 5, self.y + 5))
        
        # Calculate scale
        scale_x = self.width / world_width
        scale_y = self.height / world_height
        
        # Draw NPCs
        for npc_x, npc_y, npc_type in npc_positions:
            map_x = int(self.x + 10 + npc_x * scale_x)
            map_y = int(self.y + 25 + npc_y * scale_y)
            
            # Color berdasarkan type
            if npc_type == "merchant":
                color = (255, 200, 100)
            elif npc_type == "restaurant":
                color = (255, 100, 100)
            else:
                color = (150, 150, 255)
            
            pygame.draw.circle(screen, color, (map_x, map_y), 3)
        
        # Draw player
        player_map_x = int(self.x + 10 + player_pos[0] * scale_x)
        player_map_y = int(self.y + 25 + player_pos[1] * scale_y)
        pygame.draw.circle(screen, (100, 200, 255), (player_map_x, player_map_y), 4)
        pygame.draw.circle(screen, (255, 255, 255), (player_map_x, player_map_y), 4, 2)
        
        # Camera view indicator
        view_x = int(self.x + 10 + camera_x * scale_x)
        view_y = int(self.y + 25 + camera_y * scale_y)
        view_w = int(SCREEN_WIDTH * scale_x)
        view_h = int(SCREEN_HEIGHT * scale_y)
        view_rect = pygame.Rect(view_x, view_y, view_w, view_h)
        pygame.draw.rect(screen, (255, 255, 0), view_rect, 1)

