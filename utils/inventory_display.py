"""
Inventory Display - Keranjang untuk menampilkan pembelian
"""
import pygame
from typing import Dict, List, Tuple

class InventoryCart:
    """Keranjang untuk menampilkan item yang dibeli"""
    
    def __init__(self, x: int, y: int, width: int = 300, height: int = 200):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = False
        self.items: List[Dict[str, any]] = []
        self.font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 16)
        
    def add_item(self, item_type: str, item_name: str, quantity: int = 1):
        """Tambahkan item ke keranjang"""
        # Check if item already exists
        for item in self.items:
            if item['name'] == item_name and item['type'] == item_type:
                item['quantity'] += quantity
                return
        
        # Add new item
        self.items.append({
            'type': item_type,
            'name': item_name,
            'quantity': quantity
        })
    
    def clear(self):
        """Clear semua items"""
        self.items.clear()
    
    def toggle(self):
        """Toggle visibility"""
        self.visible = not self.visible
    
    def render(self, screen: pygame.Surface, inventory_data: Dict = None):
        """Render inventory cart"""
        if not self.visible:
            return
        
        # Panel background
        panel_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((20, 20, 40, 240))
        screen.blit(overlay, panel_rect)
        pygame.draw.rect(screen, (100, 150, 200), panel_rect, 3)
        
        # Title
        title = self.font.render("🛒 Keranjang Pembelian", True, (255, 255, 100))
        screen.blit(title, (self.x + 10, self.y + 10))
        
        # Items list
        y_offset = 40
        if inventory_data:
            # Spices
            if 'inventory' in inventory_data and 'spices' in inventory_data['inventory']:
                spices = inventory_data['inventory']['spices']
                for idx, (name, qty) in enumerate(spices.items()):
                    if qty > 0:
                        item_text = self.small_font.render(f"• {name} x{qty}", True, (255, 255, 255))
                        screen.blit(item_text, (self.x + 15, self.y + y_offset + idx * 20))
            
            # Foods
            if 'tried_foods' in inventory_data:
                foods = inventory_data['tried_foods']
                start_y = y_offset + len([s for s in inventory_data.get('inventory', {}).get('spices', {}).values() if s > 0]) * 20
                for idx, food_name in enumerate(foods):
                    item_text = self.small_font.render(f"✓ {food_name}", True, (150, 255, 150))
                    screen.blit(item_text, (self.x + 15, self.y + start_y + idx * 20))
        
        # Close hint
        if len(self.items) == 0:
            hint_text = self.small_font.render("Keranjang kosong", True, (150, 150, 150))
            screen.blit(hint_text, (self.x + 15, self.y + y_offset))

