"""
Icons Module - Simple icon rendering untuk game
"""
import pygame
from typing import Tuple

class IconRenderer:
    """Class untuk render icon sederhana"""
    
    @staticmethod
    def draw_spice_icon(surface: pygame.Surface, x: int, y: int, size: int = 24):
        """Draw spice icon (bentuk rempah)"""
        # Draw sebagai circle dengan detail
        center = (x + size // 2, y + size // 2)
        radius = size // 2 - 2
        
        # Background circle
        pygame.draw.circle(surface, (139, 69, 19), center, radius)  # Brown
        pygame.draw.circle(surface, (160, 82, 45), center, radius - 2)  # Saddle brown
        
        # Detail lines
        for i in range(4):
            angle = i * 90
            start_x = center[0] + int(radius * 0.5 * pygame.math.Vector2(1, 0).rotate(angle).x)
            start_y = center[1] + int(radius * 0.5 * pygame.math.Vector2(1, 0).rotate(angle).y)
            end_x = center[0] + int(radius * 0.8 * pygame.math.Vector2(1, 0).rotate(angle).x)
            end_y = center[1] + int(radius * 0.8 * pygame.math.Vector2(1, 0).rotate(angle).y)
            pygame.draw.line(surface, (101, 67, 33), (start_x, start_y), (end_x, end_y), 2)
    
    @staticmethod
    def draw_food_icon(surface: pygame.Surface, x: int, y: int, size: int = 24):
        """Draw food icon (bentuk piring)"""
        # Draw sebagai rounded rectangle (piring)
        rect = pygame.Rect(x, y, size, size)
        
        # Plate base
        pygame.draw.ellipse(surface, (200, 200, 200), rect)  # Gray plate
        pygame.draw.ellipse(surface, (255, 255, 255), pygame.Rect(x + 2, y + 2, size - 4, size - 4))
        
        # Food (rice/makanan)
        food_rect = pygame.Rect(x + 4, y + 4, size - 8, size - 8)
        pygame.draw.ellipse(surface, (255, 220, 177), food_rect)  # Light brown food
    
    @staticmethod
    def draw_coin_icon(surface: pygame.Surface, x: int, y: int, size: int = 20):
        """Draw coin icon"""
        center = (x + size // 2, y + size // 2)
        radius = size // 2 - 2
        
        # Coin circle
        pygame.draw.circle(surface, (255, 215, 0), center, radius)  # Gold
        pygame.draw.circle(surface, (255, 255, 0), center, radius - 2)  # Yellow
        
        # Coin symbol
        font = pygame.font.Font(None, size - 4)
        text = font.render("$", True, (139, 69, 19))
        text_rect = text.get_rect(center=center)
        surface.blit(text, text_rect)
    
    @staticmethod
    def draw_close_icon(surface: pygame.Surface, x: int, y: int, size: int = 20):
        """Draw close/X icon"""
        # Draw X symbol
        color = (255, 255, 255)
        thickness = 3
        
        # Top-left to bottom-right
        pygame.draw.line(surface, color, (x + 3, y + 3), (x + size - 3, y + size - 3), thickness)
        # Top-right to bottom-left
        pygame.draw.line(surface, color, (x + size - 3, y + 3), (x + 3, y + size - 3), thickness)

