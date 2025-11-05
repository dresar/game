"""
Particle System - Particle effects untuk cannonball impact dan explosion
"""
import pygame
import math
import random
from typing import List, Tuple

class Particle:
    """Single particle"""
    def __init__(self, x: float, y: float, vx: float, vy: float, color: Tuple[int, int, int], lifetime: float):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.uniform(2, 5)
        
    def update(self, dt: float):
        """Update particle"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 200 * dt  # Gravity
        self.lifetime -= dt
        
    def is_alive(self) -> bool:
        """Check if particle is still alive"""
        return self.lifetime > 0
    
    def render(self, screen: pygame.Surface):
        """Render particle"""
        if self.is_alive():
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            color = (*self.color[:3], alpha)
            size = int(self.size * (self.lifetime / self.max_lifetime))
            if size > 0:
                pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

class ParticleSystem:
    """Particle system manager"""
    
    def __init__(self):
        self.particles: List[Particle] = []
    
    def create_explosion(self, x: float, y: float, color: Tuple[int, int, int] = (255, 200, 0), count: int = 15):
        """Create explosion effect"""
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(100, 300)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            lifetime = random.uniform(0.3, 0.8)
            particle = Particle(x, y, vx, vy, color, lifetime)
            self.particles.append(particle)
    
    def create_smoke(self, x: float, y: float, count: int = 8):
        """Create smoke effect"""
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(20, 80)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 50  # Upward
            lifetime = random.uniform(0.5, 1.2)
            color = (100, 100, 100, 200)
            particle = Particle(x, y, vx, vy, color, lifetime)
            self.particles.append(particle)
    
    def create_water_splash(self, x: float, y: float, count: int = 10):
        """Create water splash effect"""
        for _ in range(count):
            angle = random.uniform(-math.pi / 2, math.pi / 2)
            speed = random.uniform(50, 150)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            lifetime = random.uniform(0.2, 0.6)
            color = (100, 150, 255)
            particle = Particle(x, y, vx, vy, color, lifetime)
            self.particles.append(particle)
    
    def update(self, dt: float):
        """Update all particles"""
        for particle in self.particles[:]:
            particle.update(dt)
            if not particle.is_alive():
                self.particles.remove(particle)
    
    def render(self, screen: pygame.Surface):
        """Render all particles"""
        for particle in self.particles:
            particle.render(screen)

