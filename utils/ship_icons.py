"""
Ship Icons - Icon rendering untuk ship, enemy, dan cannonball
"""
import pygame
import math

class ShipIconRenderer:
    """Renderer untuk ship icons"""
    
    @staticmethod
    def draw_merchant_ship(surface: pygame.Surface, x: int, y: int, width: int, height: int, angle: float = 0):
        """Draw merchant ship dengan detail"""
        # Ship body (hull)
        ship_points = [
            (x + width * 0.2, y + height),
            (x + width * 0.8, y + height),
            (x + width * 0.9, y + height * 0.7),
            (x + width * 0.7, y + height * 0.3),
            (x + width * 0.3, y + height * 0.3),
            (x + width * 0.1, y + height * 0.7)
        ]
        pygame.draw.polygon(surface, (100, 150, 200), ship_points)
        pygame.draw.polygon(surface, (255, 255, 255), ship_points, 2)
        
        # Deck
        deck_rect = pygame.Rect(x + width * 0.2, y + height * 0.3, width * 0.6, height * 0.15)
        pygame.draw.rect(surface, (139, 69, 19), deck_rect)
        
        # Mast
        mast_x = x + width * 0.5
        mast_y_start = y + height * 0.3
        mast_y_end = y + height * 0.1
        pygame.draw.line(surface, (101, 67, 33), (mast_x, mast_y_start), (mast_x, mast_y_end), 3)
        
        # Sail
        sail_points = [
            (mast_x, mast_y_start),
            (mast_x, mast_y_end),
            (mast_x + width * 0.2, mast_y_start * 0.7),
            (mast_x, mast_y_start)
        ]
        pygame.draw.polygon(surface, (240, 240, 240), sail_points)
        pygame.draw.polygon(surface, (200, 200, 200), sail_points, 2)
        
        # Flag
        flag_rect = pygame.Rect(mast_x, mast_y_end, width * 0.15, height * 0.1)
        pygame.draw.rect(surface, (200, 50, 50), flag_rect)
        pygame.draw.rect(surface, (255, 255, 255), flag_rect, 1)
    
    @staticmethod
    def draw_enemy_ship(surface: pygame.Surface, x: int, y: int, width: int, height: int, angle: float = 0):
        """Draw enemy ship (pirate ship)"""
        # Ship body - more aggressive shape
        ship_points = [
            (x + width * 0.15, y + height),
            (x + width * 0.85, y + height),
            (x + width * 0.95, y + height * 0.65),
            (x + width * 0.75, y + height * 0.25),
            (x + width * 0.25, y + height * 0.25),
            (x + width * 0.05, y + height * 0.65)
        ]
        pygame.draw.polygon(surface, (150, 50, 50), ship_points)
        pygame.draw.polygon(surface, (255, 255, 255), ship_points, 2)
        
        # Skull flag
        flag_rect = pygame.Rect(x + width * 0.5, y + height * 0.1, width * 0.2, height * 0.15)
        pygame.draw.rect(surface, (0, 0, 0), flag_rect)
        pygame.draw.rect(surface, (255, 255, 255), flag_rect, 2)
        
        # Skull symbol
        skull_center = (flag_rect.centerx, flag_rect.centery)
        pygame.draw.circle(surface, (255, 255, 255), skull_center, 5)
        # Eyes
        pygame.draw.circle(surface, (0, 0, 0), (skull_center[0] - 2, skull_center[1] - 1), 1)
        pygame.draw.circle(surface, (0, 0, 0), (skull_center[0] + 2, skull_center[1] - 1), 1)
        
        # Cannons on side
        for cannon_x in [x + width * 0.2, x + width * 0.8]:
            cannon_rect = pygame.Rect(cannon_x, y + height * 0.5, width * 0.15, height * 0.1)
            pygame.draw.rect(surface, (50, 50, 50), cannon_rect)
    
    @staticmethod
    def draw_cannonball(surface: pygame.Surface, x: int, y: int, radius: int):
        """Draw cannonball dengan detail"""
        # Main ball
        pygame.draw.circle(surface, (80, 80, 80), (x, y), radius)
        pygame.draw.circle(surface, (100, 100, 100), (x, y), radius - 1)
        
        # Highlight
        highlight_x = x - radius * 0.3
        highlight_y = y - radius * 0.3
        pygame.draw.circle(surface, (150, 150, 150), (int(highlight_x), int(highlight_y)), radius // 3)
        
        # Shadow
        shadow_x = x + radius * 0.3
        shadow_y = y + radius * 0.3
        pygame.draw.circle(surface, (50, 50, 50), (int(shadow_x), int(shadow_y)), radius // 3)
        
        # Trail effect (simple)
        pygame.draw.circle(surface, (120, 120, 120), (x - radius, y), radius // 2)

