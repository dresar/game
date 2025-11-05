# 🏴‍☠️ Spice Trader 1400 - Prototype Demo

<div align="center">

![Game Logo](https://img.shields.io/badge/Spice%20Trader%201400-Prototype%20Demo-orange?style=for-the-badge&logo=gamepad&logoColor=white)

**RPG Semi-Open World Game tentang Pedagang Rempah di Indonesia Tahun 1400 M**

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.5.2-green?style=flat-square&logo=pygame)](https://www.pygame.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-red?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

[🎮 Gameplay](#-gameplay) • [📋 Requirements](#-requirements) • [🚀 Installation](#-installation) • [▶️ Cara Menjalankan](#️-cara-menjalankan) • [🎯 Fitur](#-fitur) • [📖 Story](#-story)

</div>

---

## 📖 Story

**Spice Trader 1400** menceritakan tentang seorang pedagang dari luar negeri yang datang ke Indonesia pada tahun **1400 M** untuk berdagang rempah-rempah. Setelah tinggal di Indonesia untuk waktu yang lama, ia mulai tertarik dengan budaya di kepulauan ini. Kemudian ia mencoba berkeliling ke semua pulau di Indonesia sambil berdagang dan mengenal banyak budaya dan tradisi.

### 🎭 Setting

- **Era**: Tahun 1400 Masehi
- **Lokasi**: Kepulauan Indonesia
- **Genre**: RPG, Semi-Open World, Trading, Adventure
- **Style**: 2D Pixel Mix pada 3D World

---

## 🎮 Gameplay

Game ini terdiri dari **2 scene utama** dengan gameplay yang berbeda:

### 🚢 Scene 1: Ship Combat (Warship Style)

**Gameplay di atas kapal merchant yang sedang berlayar ke Indonesia**

- **Kontrol**:
  - `WASD` atau `Arrow Keys` - Gerakkan kapal merchant
  - `Z` - Tembakkan cannonball ke arah mouse
  - `ESC` - Keluar dari game

- **Tujuan**: 
  - Kalahkan **5 kapal musuh** untuk menang
  - Hindari collision dengan musuh
  - Tembak musuh dengan cannonball

- **Fitur**:
  - Menu screen dengan button Start dan Tutorial
  - Tutorial screen dengan instruksi lengkap
  - Visual ocean yang realistis dengan sky gradient, sun, clouds, dan waves
  - Icon kapal yang detail (merchant ship dan enemy ship)
  - Particle effects (explosion, smoke, water splash)
  - HUD dengan health bar, enemy count, dan instruksi
  - Win screen dengan animasi glow effect

### 🏝️ Scene 2: Harbor Exploration (Zenless Zone Zero Style)

**Gameplay di pelabuhan dengan semi-open world exploration**

- **Kontrol**:
  - `WASD` atau `Arrow Keys` - Gerakkan karakter
  - `E` - Berinteraksi dengan NPC
  - `I` - Buka/tutup keranjang pembelian
  - `ESC` - Keluar dari dialog

- **Fitur**:
  - Semi-open world dengan camera follow
  - NPCs dengan berbagai jenis (Merchant, Restaurant, Story)
  - Buildings dengan detail (roof, windows, doors)
  - Trading system untuk membeli rempah-rempah
  - Restaurant system untuk mencoba makanan khas daerah
  - Story dialog untuk mempelajari cerita
  - Inventory cart untuk melihat pembelian
  - Minimap untuk navigasi
  - Database integration untuk save/load

---

## 📋 Requirements

### System Requirements

- **OS**: Windows 10/11, Linux, atau macOS
- **Python**: 3.8 atau lebih tinggi
- **RAM**: Minimal 2GB
- **Storage**: ~100MB untuk game files

### Dependencies

Semua dependencies akan diinstall otomatis saat setup. Berikut daftarnya:

```
Flask==3.0.0           # Backend API server
Flask-CORS==4.0.0     # CORS support
pygame==2.5.2          # Game engine
pygame-gui==0.6.9      # UI components
pytmx==3.31           # Tile map support
pyscroll==2.31.0      # Scrolling map
numpy==1.24.3         # Mathematical operations
requests==2.31.0      # HTTP client
Pillow==10.0.0        # Image processing
```

---

## 🚀 Installation

### Langkah 1: Download atau Clone Repository

Jika menggunakan Git:
```bash
git clone <https://github.com/dresar/game.git>
cd game
```

Atau download dan extract ZIP file ke folder `game`.

### Langkah 2: Pastikan Python Terinstall

Cek versi Python:
```bash
python --version
# Harus Python 3.8 atau lebih tinggi
```

Jika belum terinstall, download dari [python.org](https://www.python.org/downloads/)

### Langkah 3: Buat Virtual Environment (venv)

**Windows:**
```powershell
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
source venv/bin/activate
```

**Catatan untuk Windows:**
- Jika mendapat error `ExecutionPolicy`, jalankan:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- Atau gunakan Command Prompt (cmd) dan jalankan:
  ```cmd
  venv\Scripts\activate.bat
  ```

### Langkah 4: Install Dependencies

Setelah venv aktif (anda akan melihat `(venv)` di terminal), install dependencies:

```bash
pip install -r requirements.txt
```

**Verifikasi Installation:**
```bash
# Test import
python -c "import pygame; import flask; print('All dependencies installed!')"
```

---

## ▶️ Cara Menjalankan

### Metode 1: Menggunakan Script (Recommended)

**Windows:**

1. **Setup pertama kali** (hanya sekali):
   ```powershell
   .\setup.bat
   ```

2. **Jalankan Flask Server** (Terminal 1):
   ```powershell
   .\run_server.bat
   ```
   Atau:
   ```powershell
   .\venv\Scripts\Activate.ps1
   python app.py
   ```

3. **Jalankan Game** (Terminal 2 - buka terminal baru):
   ```powershell
   .\run_game.bat
   ```
   Atau:
   ```powershell
   .\venv\Scripts\Activate.ps1
   python main.py
   ```

**Linux/Mac:**

1. **Setup pertama kali**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Jalankan Flask Server** (Terminal 1):
   ```bash
   source venv/bin/activate
   python app.py
   ```

3. **Jalankan Game** (Terminal 2):
   ```bash
   source venv/bin/activate
   python main.py
   ```

### Metode 2: Manual

**Setup (hanya sekali):**
```bash
# Buat venv
python -m venv venv

# Aktifkan venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Jalankan:**

1. **Terminal 1 - Flask Server:**
   ```bash
   # Aktifkan venv (jika belum)
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   
   # Jalankan server
   python app.py
   ```
   Server akan berjalan di `http://localhost:5000`

2. **Terminal 2 - Game Client:**
   ```bash
   # Aktifkan venv (jika belum)
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   
   # Jalankan game
   python main.py
   ```

### Metode 3: Web Interface (Optional)

Setelah Flask server berjalan, buka browser dan akses:
```
http://localhost:5000
```

---

## 🎯 Fitur Lengkap

### 🎨 Visual & Graphics

#### Ship Scene
- ✅ **Menu Screen** dengan button interaktif
  - Button "Mulai Game" dengan hover effect
  - Button "Cara Bermain" untuk tutorial
  - Title dengan glow effect
  
- ✅ **Tutorial Screen** dengan instruksi lengkap
  - Kontrol game
  - Tujuan permainan
  - Tips dan trik
  
- ✅ **Ocean Effects** yang realistis
  - Sky gradient (biru ke biru muda)
  - Sun dengan glow effect dan animasi
  - Clouds yang bergerak
  - Ocean gradient dengan depth
  - Animated waves (3 lapis dengan efek berbeda)
  
- ✅ **Ship Icons** yang detail
  - Merchant ship dengan mast, sail, dan flag
  - Enemy ship (pirate) dengan skull flag dan cannons
  - Cannonball dengan highlight dan shadow
  
- ✅ **Particle Effects**
  - Explosion saat musuh hancur
  - Smoke effect saat menembak dan musuh hancur
  - Water splash saat cannonball mengenai air
  - Impact effect saat cannonball mengenai musuh
  
- ✅ **HUD System**
  - Health bar dengan warna dinamis
  - Enemy count display
  - Instructions overlay
  - Win screen dengan animasi

#### Harbor Scene
- ✅ **Background dengan Gradient**
  - Sky gradient untuk atmosfer
  - Ground dengan texture gradient
  - Grid pattern untuk semi-open world effect
  
- ✅ **Character Design**
  - Player dengan detail (head, body, label)
  - NPCs dengan icon berdasarkan type
  - Buildings dengan detail (roof, windows, doors)
  
- ✅ **UI Components**
  - Dialog dengan gradient background
  - Title bar terpisah
  - Item list dengan alternating background
  - Button dengan hover dan click effects
  - Close button dengan icon X
  
- ✅ **Minimap**
  - Menampilkan posisi player
  - Menampilkan posisi NPCs dengan warna berbeda
  - Camera view indicator
  - Real-time update

### 🛒 Trading & Commerce System

#### Spice Trading
- ✅ **4 Jenis Rempah-Rempah**:
  - **Cengkeh** (50 koin) - Rempah dari Maluku
  - **Pala** (75 koin) - Rempah dari Banda
  - **Lada** (30 koin) - Rempah dari Lampung
  - **Kayu Manis** (40 koin) - Rempah dari Sumatra

- ✅ **Features**:
  - Beli rempah dengan klik button
  - Display harga dengan coin icon
  - Tampilkan jumlah yang sudah dimiliki
  - Inventory display di dialog
  - Auto-save ke database

#### Restaurant System
- ✅ **4 Makanan Khas Daerah**:
  - **Rendang** (25 koin) - Sumatra
  - **Gudeg** (20 koin) - Yogyakarta
  - **Rawon** (22 koin) - Jawa Timur
  - **Sate** (15 koin) - Jawa

- ✅ **Features**:
  - Coba makanan dengan klik button
  - Checkmark (✓) untuk makanan yang sudah dicoba
  - Display region dan description
  - Section "Makanan yang Sudah Dicoba"
  - Auto-save ke database

### 📦 Inventory & Cart System

- ✅ **Keranjang Pembelian** (Tekan `I`)
  - Menampilkan semua rempah yang dibeli
  - Menampilkan semua makanan yang sudah dicoba
  - Section terpisah untuk rempah dan makanan
  - Alternating background untuk readability
  - Empty state message
  
- ✅ **Inventory Display di Dialog**
  - Real-time update
  - Tampilkan quantity
  - Format yang rapi

### 💾 Database System

- ✅ **SQLite Database** (`game_data.db`)
  - **Table `inventory_spices`**: Menyimpan rempah yang dibeli
  - **Table `tried_foods`**: Menyimpan makanan yang sudah dicoba
  - **Table `purchase_history`**: Riwayat semua pembelian
  - **Table `game_state`**: Game state (coins, health, scene, dll)

- ✅ **Features**:
  - Auto-save saat membeli item
  - Auto-load saat masuk harbor scene
  - Persistent data (tidak hilang setelah game ditutup)
  - Purchase history tracking

### 🎮 Game Engine Features

- ✅ **Scene Management**
  - Automatic scene transition
  - State persistence
  - Scene setup dan cleanup
  
- ✅ **Event Handling**
  - Keyboard input
  - Mouse input
  - Button interactions
  
- ✅ **Rendering System**
  - Camera follow
  - Particle rendering
  - UI rendering dengan layering
  - HUD rendering

### 🎨 UI/UX Features

- ✅ **Button System**
  - Hover effect (warna berubah)
  - Click effect (animasi)
  - Icon support (close button dengan X icon)
  - Customizable colors dan fonts
  
- ✅ **Dialog System**
  - Gradient background
  - Title bar terpisah
  - Close button (bukan ESC)
  - Item list dengan spacing rapi
  - Responsive layout

- ✅ **Icons**
  - Spice icon (bentuk rempah)
  - Food icon (piring dengan makanan)
  - Coin icon (koin emas)
  - Close icon (X symbol)
  - Ship icons (merchant, enemy, cannonball)

### 🎯 Combat System (Ship Scene)

- ✅ **Player Ship**
  - Movement dengan WASD
  - Health system
  - Cannonball shooting (Z key)
  - Direction indicator
  
- ✅ **Enemy AI**
  - Chase behavior (mengikuti player)
  - Spawn dari edge of screen
  - Health bar dengan color coding
  - Collision detection
  
- ✅ **Projectile System**
  - Cannonball physics
  - Mouse direction targeting
  - Collision dengan enemies
  - Boundary detection

### 🗺️ Exploration System (Harbor Scene)

- ✅ **Semi-Open World**
  - Camera follow player
  - Grid-based movement
  - Larger world area (2x screen size)
  
- ✅ **NPC Interaction**
  - Interaction range detection
  - Visual indicator (E button)
  - Multiple NPC types
  - Dynamic dialog system
  
- ✅ **Building System**
  - Multiple buildings
  - Different types (shop, restaurant)
  - Visual detail (roof, windows, doors)
  - Labels dengan background

### 📊 Progress & Stats

- ✅ **Game State**
  - Health tracking
  - Coins tracking
  - Inventory tracking
  - Story progress
  - Visited islands (future feature)
  
- ✅ **Save/Load**
  - Auto-save ke database
  - Auto-load saat scene dimulai
  - State persistence
  - Purchase history

---

## 🎮 Kontrol Lengkap

### Ship Scene

| Tombol | Aksi |
|--------|------|
| `WASD` / `Arrow Keys` | Gerakkan kapal merchant |
| `Z` | Tembakkan cannonball ke arah mouse |
| `ESC` | Keluar dari game |
| `Mouse` | Arahkan untuk menentukan arah tembakan |

### Harbor Scene

| Tombol | Aksi |
|--------|------|
| `WASD` / `Arrow Keys` | Gerakkan karakter |
| `E` | Berinteraksi dengan NPC |
| `I` | Buka/tutup keranjang pembelian |
| `ESC` | Keluar dari game |
| `Mouse Click` | Klik button di dialog |

### Menu & Tutorial

| Tombol | Aksi |
|--------|------|
| `Mouse Click` | Klik button |
| `ENTER` / `SPACE` | Mulai game dari tutorial |

---

## 🗂️ Struktur Project

```
game/
├── 📄 main.py                    # Entry point game client
├── 📄 app.py                     # Flask backend server
├── 📄 requirements.txt           # Dependencies list
├── 📄 README.md                  # Dokumentasi ini
├── 📄 .gitignore                 # Git ignore file
│
├── 📁 game_engine/              # Core game engine
│   ├── __init__.py
│   ├── core.py                  # Game engine utama
│   └── scene.py                 # Base scene class
│
├── 📁 scenes/                   # Game scenes
│   ├── __init__.py
│   ├── 📁 ship/                # Ship combat scene
│   │   ├── __init__.py
│   │   └── ship_scene.py       # Ship scene implementation
│   └── 📁 harbor/              # Harbor exploration scene
│       ├── __init__.py
│       └── harbor_scene.py     # Harbor scene implementation
│
├── 📁 utils/                    # Utility modules
│   ├── __init__.py
│   ├── constants.py            # Game constants
│   ├── api_client.py           # Flask API client
│   ├── audio_manager.py        # Audio system (placeholder)
│   ├── database.py             # SQLite database
│   ├── icons.py                # Icon rendering
│   ├── inventory_display.py    # Inventory cart
│   ├── minimap.py              # Minimap system
│   ├── ocean_effects.py        # Ocean visual effects
│   ├── particle_system.py      # Particle effects
│   ├── ship_icons.py           # Ship icon rendering
│   └── ui_button.py            # Button system
│
├── 📁 templates/                # HTML templates
│   └── index.html              # Web interface
│
├── 📁 static/                   # Static assets
│   └── 📁 assets/
│       ├── 📁 images/          # Image assets
│       ├── 📁 sounds/          # Audio assets
│       └── 📁 fonts/           # Font assets
│
└── 📁 venv/                     # Virtual environment (dibuat saat setup)
```

---

## 📡 API Endpoints

Flask backend menyediakan REST API untuk game state management:

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/api/game/state` | Mendapatkan game state player |
| `POST` | `/api/game/state` | Menyimpan game state player |
| `POST` | `/api/game/buy-spice` | Membeli rempah di harbor |
| `POST` | `/api/game/buy-food` | Membeli makanan di restaurant |
| `POST` | `/api/game/change-scene` | Mengubah scene (ship/harbor) |
| `GET` | `/api/game/inventory` | Mendapatkan inventory player |
| `POST` | `/api/game/story-progress` | Update story progress |

**Base URL**: `http://localhost:5000`

---

## 🎨 Visual Features Detail

### 🌊 Ocean Effects

- **Sky Gradient**: Gradient dari biru terang ke biru muda untuk efek atmosfer
- **Sun**: Sun dengan multiple glow layers untuk efek realistis
- **Clouds**: 5 clouds yang bergerak dengan kecepatan berbeda
- **Ocean Waves**: 3 lapis waves dengan amplitude dan frequency berbeda
- **Ocean Gradient**: Gradient dari biru tua ke biru muda untuk efek depth

### 🚢 Ship Icons

- **Merchant Ship**:
  - Hull dengan detail
  - Deck dengan warna kayu
  - Mast dengan sail
  - Flag dengan warna merah
  
- **Enemy Ship**:
  - Hull dengan bentuk agresif
  - Skull flag dengan detail
  - Cannons di sisi kapal
  
- **Cannonball**:
  - Main ball dengan shadow
  - Highlight effect
  - Trail effect

### 💥 Particle Effects

- **Explosion**: 15-25 particles dengan warna orange/red
- **Smoke**: 8-20 particles dengan warna abu-abu, bergerak ke atas
- **Water Splash**: 8-10 particles dengan warna biru, bergerak menyebar
- **Impact**: 10 particles dengan warna kuning untuk impact effect

### 🏘️ Harbor Visual

- **Buildings**:
  - Roof dengan bentuk segitiga
  - Windows dengan frame
  - Door dengan detail
  - Gradient shading
  
- **Characters**:
  - Player dengan head dan body
  - NPCs dengan icon berdasarkan type
  - Labels dengan background untuk readability
  
- **Background**:
  - Sky gradient
  - Ground gradient dengan texture
  - Grid pattern untuk semi-open world

---

## 🔧 Troubleshooting

### ❌ Error: Module 'pygame' not found

**Solusi:**
```bash
# Pastikan venv aktif
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install ulang
pip install -r requirements.txt
```

### ❌ Error: Port 5000 already in use

**Solusi:**
- Tutup aplikasi lain yang menggunakan port 5000
- Atau ubah port di `app.py`:
  ```python
  app.run(debug=True, port=5001)  # Ganti ke port lain
  ```

### ❌ Error: ExecutionPolicy (Windows PowerShell)

**Solusi:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Atau gunakan Command Prompt (cmd) instead of PowerShell.

### ❌ Game tidak muncul / Black screen

**Solusi:**
1. Cek console untuk error messages
2. Pastikan Pygame terinstall:
   ```bash
   pip install pygame --upgrade
   ```
3. Pastikan resolusi layar mendukung 1280x720
4. Cek apakah ada error di terminal

### ❌ Game lag atau lambat

**Solusi:**
- Kurangi jumlah enemy (ubah `ENEMY_SPAWN_RATE` di `utils/constants.py`)
- Tutup aplikasi lain yang menggunakan resources
- Kurangi particle effects (edit di `utils/particle_system.py`)

### ❌ Database error

**Solusi:**
- Hapus file `game_data.db` jika corrupted
- Database akan dibuat ulang otomatis saat game dijalankan

---

## 📝 Tips & Tricks

### 🎮 Gameplay Tips

**Ship Scene:**
- ✅ Gerakkan mouse untuk mengarahkan tembakan
- ✅ Jaga jarak dengan musuh untuk menghindari collision
- ✅ Tembak musuh dari jarak jauh untuk safety
- ✅ Perhatikan health bar di kiri atas
- ✅ Fokus pada satu enemy pada satu waktu

**Harbor Scene:**
- ✅ Jelajahi semua area untuk menemukan NPC
- ✅ Kumpulkan koin dari trading untuk membeli makanan
- ✅ Coba semua makanan khas untuk mempelajari budaya
- ✅ Gunakan minimap untuk navigasi
- ✅ Tekan `I` untuk melihat keranjang pembelian

### 💰 Trading Tips

- ✅ Mulai dengan rempah murah (Lada) untuk build inventory
- ✅ Simpan koin untuk mencoba semua makanan
- ✅ Cek inventory sebelum membeli untuk menghindari duplikasi
- ✅ Makanan memberikan informasi budaya, jadi coba semua!

### 🎯 Achievement Goals

- ✅ Kalahkan semua 5 enemies
- ✅ Beli semua 4 jenis rempah
- ✅ Coba semua 4 makanan khas
- ✅ Berbicara dengan semua NPC
- ✅ Jelajahi seluruh harbor

---

## 🛠️ Development

### Menambah Fitur Baru

1. **Tambah Rempah Baru**:
   Edit `utils/constants.py`:
   ```python
   SPICES = {
       'nama_baru': {'name': 'Nama', 'price': 50, 'description': 'Deskripsi'}
   }
   ```

2. **Tambah Makanan Baru**:
   Edit `utils/constants.py`:
   ```python
   FOODS = {
       'nama_baru': {'name': 'Nama', 'price': 25, 'region': 'Daerah', 'description': 'Deskripsi'}
   }
   ```

3. **Ubah Gameplay**:
   - Edit `scenes/ship/ship_scene.py` untuk ship combat
   - Edit `scenes/harbor/harbor_scene.py` untuk harbor exploration

### Customization

- **Ubah Resolusi**: Edit `utils/constants.py` (`SCREEN_WIDTH`, `SCREEN_HEIGHT`)
- **Ubah Difficulty**: Edit `utils/constants.py` (`ENEMY_SPAWN_RATE`, `ENEMY_HEALTH`)
- **Ubah Colors**: Edit color constants di `utils/constants.py`
- **Tambah NPC**: Edit di `scenes/harbor/harbor_scene.py` setup method

---

## 📚 Technical Details

### Architecture

- **Game Engine**: Custom engine dengan Pygame
- **Scene System**: State-based scene management
- **Database**: SQLite untuk persistence
- **API**: Flask REST API untuk state management
- **Rendering**: 2D pixel mix pada 3D world style

### Performance

- **FPS**: 60 FPS target
- **Delta Time**: Frame-rate independent updates
- **Optimization**: Efficient collision detection, particle pooling

### Code Structure

- **Modular Design**: Setiap fitur di module terpisah
- **Clean Code**: Type hints, docstrings
- **Error Handling**: Try-catch untuk graceful failures

---

## 🎓 Learning Resources

### Python & Pygame
- [Pygame Documentation](https://www.pygame.org/docs/)
- [Python Tutorial](https://docs.python.org/3/tutorial/)

### Game Development
- [Game Design Patterns](https://gameprogrammingpatterns.com/)
- [2D Game Physics](https://www.iforce2d.net/b2dtut/)

---

## 🤝 Contributing

Kontribusi sangat diterima! Silakan:

1. Fork repository
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

Project ini adalah **prototype demo** untuk keperluan pembelajaran dan pengembangan.

---

## 🙏 Acknowledgments

- **Story Inspiration**: Sejarah perdagangan rempah di Indonesia
- **Visual Style**: Terinspirasi dari Warship games dan Zenless Zone Zero
- **Libraries**: Pygame, Flask, dan semua open-source libraries yang digunakan

---

## 📞 Support

Jika ada pertanyaan atau masalah:

1. Cek bagian [Troubleshooting](#-troubleshooting)
2. Baca dokumentasi di file-file source code
3. Buat issue di repository

---

## 🎉 Credits

**Spice Trader 1400** dibuat dengan ❤️ menggunakan:
- Python 3.10+
- Pygame 2.5.2
- Flask 3.0.0
- SQLite
- Dan banyak library lainnya!

---

<div align="center">

**Selamat Bermain! 🎮**

*Dibuat untuk mengenal budaya Indonesia melalui gameplay yang menyenangkan*

[⬆ Back to Top](#-spice-trader-1400---prototype-demo)

</div>

---

*Last Updated: 2025*


