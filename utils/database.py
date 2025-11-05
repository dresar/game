"""
Database Module - SQLite database untuk menyimpan game data
"""
import sqlite3
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

class GameDatabase:
    """Database untuk menyimpan game state dan inventory"""
    
    def __init__(self, db_path: str = "game_data.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table untuk inventory (spices)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory_spices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id TEXT NOT NULL,
                spice_name TEXT NOT NULL,
                quantity INTEGER DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(player_id, spice_name)
            )
        ''')
        
        # Table untuk tried foods
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tried_foods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id TEXT NOT NULL,
                food_name TEXT NOT NULL,
                region TEXT,
                tried_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(player_id, food_name)
            )
        ''')
        
        # Table untuk purchase history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchase_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id TEXT NOT NULL,
                item_type TEXT NOT NULL,
                item_name TEXT NOT NULL,
                price INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table untuk game state
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_state (
                player_id TEXT PRIMARY KEY,
                coins INTEGER DEFAULT 500,
                health INTEGER DEFAULT 100,
                max_health INTEGER DEFAULT 100,
                current_scene TEXT DEFAULT 'ship',
                story_progress INTEGER DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_inventory_spice(self, player_id: str, spice_name: str, quantity: int):
        """Save spice inventory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO inventory_spices (player_id, spice_name, quantity, last_updated)
            VALUES (?, ?, ?, ?)
        ''', (player_id, spice_name, quantity, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_inventory_spices(self, player_id: str) -> Dict[str, int]:
        """Get all spices inventory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT spice_name, quantity FROM inventory_spices
            WHERE player_id = ?
        ''', (player_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return {name: qty for name, qty in results}
    
    def add_tried_food(self, player_id: str, food_name: str, region: str = ""):
        """Add tried food"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR IGNORE INTO tried_foods (player_id, food_name, region, tried_at)
            VALUES (?, ?, ?, ?)
        ''', (player_id, food_name, region, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_tried_foods(self, player_id: str) -> List[str]:
        """Get list of tried foods"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT food_name FROM tried_foods
            WHERE player_id = ?
            ORDER BY tried_at DESC
        ''', (player_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [row[0] for row in results]
    
    def add_purchase(self, player_id: str, item_type: str, item_name: str, price: int, quantity: int = 1):
        """Add purchase to history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO purchase_history (player_id, item_type, item_name, price, quantity, purchased_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (player_id, item_type, item_name, price, quantity, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_purchase_history(self, player_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get purchase history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT item_type, item_name, price, quantity, purchased_at
            FROM purchase_history
            WHERE player_id = ?
            ORDER BY purchased_at DESC
            LIMIT ?
        ''', (player_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'item_type': row[0],
                'item_name': row[1],
                'price': row[2],
                'quantity': row[3],
                'purchased_at': row[4]
            }
            for row in results
        ]
    
    def save_game_state(self, player_id: str, state: Dict[str, Any]):
        """Save game state"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO game_state 
            (player_id, coins, health, max_health, current_scene, story_progress, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            player_id,
            state.get('coins', 500),
            state.get('health', 100),
            state.get('max_health', 100),
            state.get('current_scene', 'ship'),
            state.get('story_progress', 0),
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
    
    def get_game_state(self, player_id: str) -> Optional[Dict[str, Any]]:
        """Get game state"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT coins, health, max_health, current_scene, story_progress
            FROM game_state
            WHERE player_id = ?
        ''', (player_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'coins': result[0],
                'health': result[1],
                'max_health': result[2],
                'current_scene': result[3],
                'story_progress': result[4]
            }
        return None

# Global database instance
db = GameDatabase()

