"""
Main Game File - Jalankan game Spice Trader 1400
"""
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from game_engine.core import GameEngine
from scenes.ship.ship_scene import ShipScene
from scenes.harbor.harbor_scene import HarborScene
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    """Main function untuk menjalankan game"""
    print("=" * 50)
    print("Spice Trader 1400 - Prototype Demo")
    print("=" * 50)
    print("Story: Trader dari luar negeri yang datang ke Indonesia")
    print("untuk berdagang rempah dan mempelajari budaya.")
    print("=" * 50)
    print()
    
    # Initialize game engine
    engine = GameEngine(
        width=SCREEN_WIDTH,
        height=SCREEN_HEIGHT,
        title="Spice Trader 1400 - Prototype Demo"
    )
    
    # Register scenes
    ship_scene = ShipScene()
    harbor_scene = HarborScene()
    
    engine.register_scene("ship", ship_scene)
    engine.register_scene("harbor", harbor_scene)
    
    # Start dengan ship scene
    initial_scene = engine.game_state.get('current_scene', 'ship')
    engine.change_scene(initial_scene)
    
    print(f"Memulai game dengan scene: {initial_scene}")
    print("Kontrol:")
    print("  - Ship Scene: WASD untuk bergerak, Z untuk menembak cannonball")
    print("  - Harbor Scene: WASD untuk bergerak, E untuk berinteraksi")
    print("  - ESC untuk keluar")
    print()
    
    # Run game
    try:
        engine.run()
    except KeyboardInterrupt:
        print("\nGame dihentikan oleh user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

