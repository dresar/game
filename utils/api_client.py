"""
API Client untuk komunikasi dengan Flask backend
"""
import requests
import json
from typing import Dict, Any, Optional

class APIClient:
    """Client untuk berkomunikasi dengan Flask API"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.player_id = 'default'
    
    def get_game_state(self) -> Optional[Dict[str, Any]]:
        """Mendapatkan game state dari server"""
        try:
            response = requests.get(f"{self.base_url}/api/game/state", params={'player_id': self.player_id})
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def save_game_state(self, state: Dict[str, Any]) -> bool:
        """Menyimpan game state ke server"""
        try:
            state['player_id'] = self.player_id
            response = requests.post(f"{self.base_url}/api/game/state", json=state)
            return response.status_code == 200
        except:
            return False
    
    def buy_spice(self, spice_name: str, quantity: int, price: int) -> Optional[Dict[str, Any]]:
        """Membeli spice dari harbor"""
        try:
            data = {
                'player_id': self.player_id,
                'spice_name': spice_name,
                'quantity': quantity,
                'price': price
            }
            response = requests.post(f"{self.base_url}/api/game/buy-spice", json=data)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def change_scene(self, scene: str) -> Optional[Dict[str, Any]]:
        """Mengubah scene"""
        try:
            data = {
                'player_id': self.player_id,
                'scene': scene
            }
            response = requests.post(f"{self.base_url}/api/game/change-scene", json=data)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None

