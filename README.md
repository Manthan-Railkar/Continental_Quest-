# Continental Quest - Interactive 3D Globe

A stunning 3D Earth visualization with interactive location marks for each continent, featuring realistic textures, atmospheric effects, and space background.

## Features

### 🌍 Interactive 3D Globe
- Realistic Earth texture with atmospheric effects
- Dynamic cloud system with rotation
- Stunning space background with stars, nebulas, and galaxy textures
- Smooth rotation and zoom controls
- Realistic lighting and materials

### 🎯 Location Marks (PokéStop Style)
- Interactive markers for all 7 continents
- Hover to reveal continent information
- Difficulty levels based on real land area:
  - **Easy**: Australia (7.7M km²)
  - **Medium**: Europe (10.2M km²)
  - **Hard**: Africa (30.4M km²), North America (24.7M km²), South America (17.8M km²)
  - **Extreme**: Asia (44.6M km²), Antarctica (14.0M km²)

### 🎮 Interactive Features
- **Hover Effects**: Location marks glow and pulse when hovered
- **Information Tooltips**: Display continent name, difficulty, and area
- **Play Buttons**: Ready for game integration
- **Smooth Animations**: Pulsing effects and smooth transitions

## Controls

- **Mouse Drag**: Rotate the globe
- **Mouse Wheel**: Zoom in/out
- **Arrow Keys**: Fine-tune rotation
- **L Key**: Toggle lighting effects
- **ESC**: Exit the application
- **Hover**: View continent information and play button

## Installation

1. Ensure you have Python 3.6+ installed
2. Install required dependencies:
   ```bash
   pip install pygame PyOpenGL numpy
   ```
3. Place `world.jpg` in the same directory for Earth texture
4. Run the application:
   ```bash
   python globe.py
   ```

## Technical Details

- **Engine**: Pygame with OpenGL
- **Graphics**: 3D rendering with texture mapping
- **Audio**: Background space ambient sound
- **UI**: Professional tooltip system with alpha blending
- **Performance**: Optimized for smooth 60 FPS rendering

## Continent Data

Each continent marker includes:
- **Geographic Position**: Accurately placed on the globe
- **Difficulty Rating**: Based on real land area
- **Color Coding**: Unique colors for easy identification
- **Area Information**: Real land area in square kilometers

## Future Enhancements

- Click functionality for play buttons
- Game integration for each continent
- Additional geographic features
- Multiplayer support
- Achievement system

---

*Developed with professional UI/UX design principles and 7+ years of game development experience.*
