"""
Game Constants
"""
# Screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Colors
COLOR_OCEAN_BLUE = (30, 60, 90)
COLOR_SKY_BLUE = (135, 206, 235)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_GOLD = (255, 215, 0)

# Ship constants
SHIP_SPEED = 150
SHIP_WIDTH = 80
SHIP_HEIGHT = 60

# Enemy constants
ENEMY_SPEED = 100
ENEMY_SPAWN_RATE = 3.0  # seconds
ENEMY_HEALTH = 50

# Projectile constants
CANNONBALL_SPEED = 400
CANNONBALL_DAMAGE = 25
CANNONBALL_SIZE = 8

# Spices
SPICES = {
    'cengkeh': {'name': 'Cengkeh', 'price': 50, 'description': 'Rempah rempah dari Maluku'},
    'pala': {'name': 'Pala', 'price': 75, 'description': 'Rempah rempah dari Banda'},
    'lada': {'name': 'Lada', 'price': 30, 'description': 'Rempah rempah dari Lampung'},
    'kayu_manis': {'name': 'Kayu Manis', 'price': 40, 'description': 'Rempah rempah dari Sumatra'}
}

# Food (makanan khas daerah)
FOODS = {
    'rendang': {'name': 'Rendang', 'price': 25, 'region': 'Sumatra', 'description': 'Daging sapi dengan bumbu rempah'},
    'gudeg': {'name': 'Gudeg', 'price': 20, 'region': 'Yogyakarta', 'description': 'Nangka muda dengan santan'},
    'rawon': {'name': 'Rawon', 'price': 22, 'region': 'Jawa Timur', 'description': 'Sup daging dengan keluak'},
    'sate': {'name': 'Sate', 'price': 15, 'region': 'Jawa', 'description': 'Daging bakar dengan bumbu kacang'}
}

# Islands
ISLANDS = [
    {'name': 'Sumatra', 'harbor': 'Aceh', 'spices': ['lada', 'kayu_manis']},
    {'name': 'Jawa', 'harbor': 'Jakarta', 'spices': ['lada']},
    {'name': 'Kalimantan', 'harbor': 'Banjarmasin', 'spices': ['lada']},
    {'name': 'Sulawesi', 'harbor': 'Makassar', 'spices': ['lada']},
    {'name': 'Maluku', 'harbor': 'Ambon', 'spices': ['cengkeh', 'pala']},
    {'name': 'Banda', 'harbor': 'Banda Neira', 'spices': ['pala']}
]

