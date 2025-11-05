"""
UI Button System - Sistem button yang lebih baik dengan hover dan click effects
"""
import pygame
from typing import Callable, Optional, Tuple

class Button:
    """Button class dengan hover, click, dan visual feedback"""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 text: str = "", action: Optional[Callable] = None,
                 color: Tuple[int, int, int] = (100, 100, 100),
                 hover_color: Tuple[int, int, int] = (150, 150, 150),
                 text_color: Tuple[int, int, int] = (255, 255, 255),
                 border_color: Tuple[int, int, int] = (255, 255, 255),
                 border_width: int = 2,
                 font_size: int = 24):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.font = pygame.font.Font(None, font_size)
        self.is_hovered = False
        self.is_clicked = False
        self.click_timer = 0.0
        
    def update(self, dt: float, mouse_pos: Tuple[int, int], mouse_clicked: bool):
        """Update button state"""
        # Check hover
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Check click
        if mouse_clicked and self.is_hovered and not self.is_clicked:
            self.is_clicked = True
            self.click_timer = 0.15  # 150ms click animation
            if self.action:
                self.action()
        
        # Update click timer
        if self.is_clicked:
            self.click_timer -= dt
            if self.click_timer <= 0:
                self.is_clicked = False
    
    def render(self, screen: pygame.Surface):
        """Render button"""
        # Determine color based on state
        if self.is_clicked:
            current_color = tuple(max(0, c - 50) for c in self.color)
        elif self.is_hovered:
            current_color = self.hover_color
        else:
            current_color = self.color
        
        # Draw button background
        pygame.draw.rect(screen, current_color, self.rect)
        
        # Draw border
        if self.is_hovered:
            pygame.draw.rect(screen, (255, 255, 0), self.rect, self.border_width + 1)
        else:
            pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)
        
        # Draw text or icon
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
        elif self.rect.width == 25 and self.rect.height == 25:
            # Close button - draw X icon
            from utils.icons import IconRenderer
            IconRenderer.draw_close_icon(screen, self.rect.x + 5, self.rect.y + 5, 15)
    
    def is_pressed(self) -> bool:
        """Check jika button sedang ditekan"""
        return self.is_clicked

class ButtonManager:
    """Manager untuk multiple buttons"""
    
    def __init__(self):
        self.buttons: list[Button] = []
    
    def add_button(self, button: Button):
        """Tambahkan button ke manager"""
        self.buttons.append(button)
    
    def update(self, dt: float, mouse_pos: Tuple[int, int], mouse_clicked: bool):
        """Update semua buttons"""
        for button in self.buttons:
            button.update(dt, mouse_pos, mouse_clicked)
    
    def render(self, screen: pygame.Surface):
        """Render semua buttons"""
        for button in self.buttons:
            button.render(screen)
    
    def clear(self):
        """Clear semua buttons"""
        self.buttons.clear()

