"""
Base Scene Class - Base class untuk semua scene
"""
import pygame
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class Scene(ABC):
    """Base class untuk semua scene dalam game"""
    
    def __init__(self, name: str):
        self.name = name
        self.state: Optional[Dict[str, Any]] = None
        
    @abstractmethod
    def setup(self, game_state: Dict[str, Any]):
        """Setup scene dengan game state"""
        self.state = game_state.copy()
        pass
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        """Handle event dari pygame"""
        pass
    
    @abstractmethod
    def update(self, dt: float):
        """Update scene logic"""
        pass
    
    @abstractmethod
    def render(self, screen: pygame.Surface):
        """Render scene ke screen"""
        pass
    
    def get_state(self) -> Optional[Dict[str, Any]]:
        """Mendapatkan state dari scene"""
        return self.state

