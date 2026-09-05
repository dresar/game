"""
Ocean Effects - Visual effects untuk suasana laut yang realistis
"""
import pygame
import math
import random
from typing import List, Tuple

class Wave:
    """Wave effect untuk ocean"""
    def __init__(self, x: float, y: float, amplitude: float, frequency: float, speed: float):
        self.x = x
        self.y = y
        self.amplitude = amplitude
        self.frequency = frequency
        self.speed = speed
        self.time = random.uniform(0, math.pi * 2)
        
    def update(self, dt: float):
        """Update wave animation"""
        self.time += self.speed * dt
        self.x += 30 * dt  # Wave moves
    
    def get_y_offset(self, x_pos: float) -> float:
        """Get Y offset untuk wave effect"""
        return math.sin((x_pos * self.frequency + self.time)) * self.amplitude
    
    def render(self, screen: pygame.Surface, screen_width: int, screen_height: int):
        """Render wave"""
        points = []
        for x in range(0, screen_width + 10, 5):
            y = self.y + self.get_y_offset(x)
            points.append((x, y))
        
        if len(points) > 1:
            pygame.draw.lines(screen, (70, 130, 180), False, points, 2)

class Cloud:
    """Cloud effect untuk sky"""
    def __init__(self, x: float, y: float, speed: float):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = random.uniform(40, 80)
        
    def update(self, dt: float, screen_width: int):
        """Update cloud position"""
        self.x += self.speed * dt
        if self.x > screen_width + 100:
            self.x = -100
    
    def render(self, screen: pygame.Surface):
        """Render cloud"""
        # Draw cloud as multiple circles
        pygame.draw.circle(screen, (220, 220, 220), (int(self.x), int(self.y)), int(self.size * 0.6))
        pygame.draw.circle(screen, (230, 230, 230), (int(self.x - self.size * 0.3), int(self.y)), int(self.size * 0.5))
        pygame.draw.circle(screen, (230, 230, 230), (int(self.x + self.size * 0.3), int(self.y)), int(self.size * 0.5))
        pygame.draw.circle(screen, (240, 240, 240), (int(self.x), int(self.y - self.size * 0.2)), int(self.size * 0.4))

class Sun:
    """Sun effect untuk sky"""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.radius = 60
        self.time = 0.0
        
    def update(self, dt: float):
        """Update sun animation"""
        self.time += dt
        
    def render(self, screen: pygame.Surface):
        """Render sun dengan glow effect"""
        # Glow layers
        for i in range(3, 0, -1):
            glow_radius = self.radius + i * 10
            alpha = 50 - i * 15
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            color = (255, 255, 200, alpha)
            pygame.draw.circle(glow_surface, color, (glow_radius, glow_radius), glow_radius)
            screen.blit(glow_surface, (self.x - glow_radius, self.y - glow_radius))
        
        # Main sun
        pygame.draw.circle(screen, (255, 255, 100), (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (255, 255, 200), (self.x, self.y), self.radius - 5)

class OceanRenderer:
    """Renderer untuk ocean dengan efek realistis"""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.waves: List[Wave] = []
        self.clouds: List[Cloud] = []
        self.sun = Sun(screen_width - 100, 80)
        
        # Initialize waves
        for i in range(3):
            wave = Wave(
                x=0,
                y=screen_height * 0.6 + i * 20,
                amplitude=8 + i * 3,
                frequency=0.02 + i * 0.01,
                speed=0.5 + i * 0.2
            )
            self.waves.append(wave)
        
        # Initialize clouds
        for i in range(5):
            cloud = Cloud(
                x=random.uniform(0, screen_width),
                y=random.uniform(50, 200),
                speed=random.uniform(10, 30)
            )
            self.clouds.append(cloud)
    
    def update(self, dt: float):
        """Update all effects"""
        for wave in self.waves:
            wave.update(dt)
        
        for cloud in self.clouds:
            cloud.update(dt, self.screen_width)
        
        self.sun.update(dt)
    
    def render(self, screen: pygame.Surface):
        """Render ocean scene"""
        # Sky gradient (blue to light blue)
        for y in range(self.screen_height // 2):
            ratio = y / (self.screen_height // 2)
            r = int(135 + (70 - 135) * ratio)
            g = int(206 + (130 - 206) * ratio)
            b = int(235 + (180 - 235) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (self.screen_width, y))
        
        # Sun
        self.sun.render(screen)
        
        # Clouds
        for cloud in self.clouds:
            cloud.render(screen)
        
        # Ocean base
        ocean_rect = pygame.Rect(0, self.screen_height // 2, self.screen_width, self.screen_height // 2)
        
        # Ocean gradient
        for y in range(self.screen_height // 2, self.screen_height):
            ratio = (y - self.screen_height // 2) / (self.screen_height // 2)
            r = int(30 + (60 - 30) * ratio)
            g = int(60 + (120 - 60) * ratio)
            b = int(90 + (180 - 90) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (self.screen_width, y))
        
        # Waves
        for wave in self.waves:
            wave.render(screen, self.screen_width, self.screen_height)

