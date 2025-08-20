#!/usr/bin/env python3
"""
Continental Quest - Integrated Desktop Application
Combines the beautiful web landing page with your existing 3D OpenGL globe
"""

import os
import sys
import threading
import time
import subprocess
from pathlib import Path
import json

# Try to import webview for desktop integration
try:
    import webview
    WEBVIEW_AVAILABLE = True
except ImportError:
    WEBVIEW_AVAILABLE = False
    print("⚠️  pywebview not installed. Install with: pip install pywebview")

# Import your existing globe functionality
try:
    import globe
    GLOBE_AVAILABLE = True
except ImportError:
    GLOBE_AVAILABLE = False
    print("⚠️  globe.py not found or has import errors")

# Import the quantum space jump transition
try:
    # We'll define the transition code directly in this file
    pass
except ImportError:
    pass

# =============================================================================
# QUANTUM SPACE JUMP TRANSITION (COPIED FROM PREVIOUS CODE)
# =============================================================================
import pygame
import math
import random

# Initialize pygame (we'll do this when needed)
pygame_initialized = False

# Enhanced Star class for light-speed travel
class LightSpeedStar:
    def __init__(self, screen_width, screen_height):
        self.x = random.uniform(0, screen_width)
        self.y = random.uniform(0, screen_height)
        self.z = random.uniform(1, 1000)  # Far depth for 3D effect
        self.original_z = self.z
        self.speed = 0
        self.trail_length = 0
        self.brightness = random.uniform(0.3, 1.0)
        self.color_variant = random.choice([
            (255, 255, 255),
            (200, 220, 255),
            (255, 240, 200),
            (220, 255, 220),
            (255, 200, 255)
        ])
        
    def update(self, warp_speed=1.0, progress=0.0, screen_width=1200, screen_height=800):
        # Calculate speed based on warp factor - exponential increase
        base_speed = max(1, warp_speed ** 2.5)
        self.speed = base_speed * (1 + progress * 15)
        
        # Move star toward camera (z-axis movement)
        self.z -= self.speed
        
        # Trail length increases with speed
        self.trail_length = min(200, self.speed * 2)
        
        # Reset star when it passes the camera
        if self.z <= 1:
            self.z = random.uniform(800, 1000)
            self.x = random.uniform(0, screen_width)
            self.y = random.uniform(0, screen_height)
    
    def draw(self, surface, warp_speed=1.0, screen_width=1200, screen_height=800):
        current_width, current_height = surface.get_size()
        
        # Calculate screen position with perspective projection
        if self.z <= 0:
            return
            
        # Perspective calculation
        scale = 500.0 / self.z
        screen_x = int(current_width/2 + (self.x - screen_width/2) * scale)
        screen_y = int(current_height/2 + (self.y - screen_height/2) * scale)
        
        # Skip if off screen (with margin for trails)
        if (screen_x < -100 or screen_x > current_width + 100 or 
            screen_y < -100 or screen_y > current_height + 100):
            return
            
        # Calculate star size based on distance
        size = max(1, int(scale * 2))
        
        # Calculate brightness based on distance and base brightness
        distance_brightness = min(1.0, (1000 - self.z) / 1000)
        final_brightness = self.brightness * distance_brightness
        
        # Color with brightness
        color = (
            int(self.color_variant[0] * final_brightness),
            int(self.color_variant[1] * final_brightness),
            int(self.color_variant[2] * final_brightness)
        )
        
        # Draw light-speed trail
        if self.trail_length > 5 and warp_speed > 2:
            trail_points = []
            num_trail_points = max(5, int(self.trail_length / 10))
            
            for i in range(num_trail_points):
                # Calculate trail position
                trail_z = self.z + (i * self.speed / num_trail_points)
                if trail_z > 0:
                    trail_scale = 500.0 / trail_z
                    trail_x = int(current_width/2 + (self.x - screen_width/2) * trail_scale)
                    trail_y = int(current_height/2 + (self.y - screen_height/2) * trail_scale)
                    trail_points.append((trail_x, trail_y))
            
            # Draw trail as connected lines with fading alpha
            if len(trail_points) > 1:
                for i in range(len(trail_points) - 1):
                    alpha = int(255 * final_brightness * (1 - i / len(trail_points)) * 0.7)
                    trail_color = (
                        min(255, color[0] + 50),
                        min(255, color[1] + 30),
                        min(255, color[2])
                    )
                    
                    if alpha > 10:
                        try:
                            pygame.draw.line(surface, trail_color, 
                                           trail_points[i], trail_points[i + 1], 
                                           max(1, size))
                        except:
                            pass
        
        # Draw main star with glow effect
        if size >= 2:
            # Outer glow
            for glow_size in range(size + 4, size, -1):
                glow_alpha = max(10, int(final_brightness * 100 * (size + 4 - glow_size) / 4))
                glow_color = (
                    min(255, color[0] + glow_alpha // 3),
                    min(255, color[1] + glow_alpha // 4),
                    min(255, color[2] + glow_alpha // 5)
                )
                try:
                    pygame.draw.circle(surface, glow_color, (screen_x, screen_y), glow_size)
                except:
                    pass
        
        # Main star
        try:
            pygame.draw.circle(surface, color, (screen_x, screen_y), size)
            
            # Bright center for larger stars
            if size > 2:
                center_color = (
                    min(255, color[0] + 100),
                    min(255, color[1] + 100),
                    min(255, color[2] + 100)
                )
                pygame.draw.circle(surface, center_color, (screen_x, screen_y), max(1, size // 2))
        except:
            pass

# Enhanced Particle class for quantum effects
class QuantumParticle:
    def __init__(self, x, y, screen_width, screen_height, particle_type="energy"):
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.particle_type = particle_type
        
        if particle_type == "energy":
            self.speed = random.uniform(3, 12)
            angle = random.uniform(0, 2 * math.pi)
            self.dx = math.cos(angle) * self.speed
            self.dy = math.sin(angle) * self.speed
            self.life = random.uniform(60, 120)
            self.max_life = self.life
            self.color = random.choice([(0, 255, 255), (0, 100, 255), (128, 0, 128), (255, 255, 255)])
        elif particle_type == "quantum":
            self.speed = random.uniform(8, 25)
            angle = random.uniform(0, 2 * math.pi)
            self.dx = math.cos(angle) * self.speed
            self.dy = math.sin(angle) * self.speed
            self.life = random.uniform(40, 90)
            self.max_life = self.life
            self.color = random.choice([(255, 215, 0), (255, 165, 0), (255, 255, 255), (0, 255, 255)])
        else:
            self.speed = random.uniform(1, 8)
            angle = random.uniform(0, 2 * math.pi)
            self.dx = math.cos(angle) * self.speed
            self.dy = math.sin(angle) * self.speed
            self.life = random.uniform(30, 80)
            self.max_life = self.life
            self.color = (255, 255, 255)
        
        self.decay = random.uniform(0.5, 1.5)
        self.size = random.uniform(1, 3)
        self.pulse_phase = random.uniform(0, math.pi * 2)
        
    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= self.decay
        
        # Gentle acceleration toward center
        center_x = self.screen_width / 2
        center_y = self.screen_height / 2
        
        to_center_x = center_x - self.x
        to_center_y = center_y - self.y
        distance = math.sqrt(to_center_x**2 + to_center_y**2)
        
        if distance > 0:
            force = 0.1
            self.dx += (to_center_x / distance) * force
            self.dy += (to_center_y / distance) * force
        
        # Slight friction
        self.dx *= 0.998
        self.dy *= 0.998
        
        # Update pulse
        self.pulse_phase += 0.1
        
    def draw(self, surface):
        if self.life > 0:
            life_ratio = self.life / self.max_life
            pulse = math.sin(self.pulse_phase) * 0.3 + 0.7
            alpha = int(255 * life_ratio * pulse)
            size = int(self.size * life_ratio * pulse)
            
            # Color with life fade
            color = (
                min(255, int(self.color[0] * life_ratio)),
                min(255, int(self.color[1] * life_ratio)),
                min(255, int(self.color[2] * life_ratio))
            )
            
            if size > 0 and alpha > 10:
                try:
                    # Glow effect
                    if size > 1:
                        glow_color = (color[0] // 3, color[1] // 3, color[2] // 3)
                        pygame.draw.circle(surface, glow_color, 
                                         (int(self.x), int(self.y)), size + 2)
                    
                    pygame.draw.circle(surface, color, (int(self.x), int(self.y)), size)
                except:
                    pass

def create_warp_tunnel_effect(surface, progress, screen_width, screen_height):
    """Create tunnel effect for light speed travel"""
    current_width, current_height = surface.get_size()
    center_x, center_y = current_width // 2, current_height // 2
    
    # Create multiple concentric circles moving outward
    for ring in range(8):
        ring_progress = (progress + ring * 0.1) % 1.0
        radius = int(ring_progress * max(current_width, current_height) * 1.5)
        
        if radius > 10:
            alpha = int(100 * (1 - ring_progress) * progress)
            color = (alpha // 2, alpha // 3, alpha)
            
            if alpha > 5:
                try:
                    pygame.draw.circle(surface, color, (center_x, center_y), radius, 3)
                except:
                    pass

def create_hyperspace_grid(surface, progress, time_factor, screen_width, screen_height):
    """Create moving grid lines for hyperspace effect"""
    current_width, current_height = surface.get_size()
    
    # Vertical lines moving horizontally
    for i in range(-5, 15):
        x_offset = (time_factor * 200 + i * 100) % (current_width + 200) - 100
        alpha = int(50 * progress * math.sin(time_factor + i) * 0.5 + 25)
        
        if alpha > 5:
            color = (alpha, alpha // 2, alpha + 20)
            try:
                pygame.draw.line(surface, color, 
                               (x_offset, 0), (x_offset, current_height), 1)
            except:
                pass
    
    # Horizontal lines moving vertically
    for i in range(-3, 10):
        y_offset = (time_factor * 150 + i * 120) % (current_height + 240) - 120
        alpha = int(40 * progress * math.cos(time_factor + i) * 0.5 + 20)
        
        if alpha > 5:
            color = (alpha, alpha // 3, alpha + 15)
            try:
                pygame.draw.line(surface, color, 
                               (0, y_offset), (current_width, y_offset), 1)
            except:
                pass

def create_screen_flash(surface, intensity, screen_width, screen_height):
    """Create screen flash effect"""
    if intensity > 0:
        current_width, current_height = surface.get_size()
        flash_surface = pygame.Surface((current_width, current_height))
        
        # White flash with blue tint
        flash_color = (
            min(255, int(intensity * 255)),
            min(255, int(intensity * 255)),
            min(255, int(intensity * 255 * 1.2))
        )
        
        flash_surface.fill(flash_color)
        flash_surface.set_alpha(int(intensity * 200))
        surface.blit(flash_surface, (0, 0))

def run_quantum_transition(continent_name):
    """Run the quantum space jump transition animation"""
    global pygame_initialized
    
    # Initialize pygame if not already done
    if not pygame_initialized:
        pygame.init()
        pygame.mixer.init()
        pygame_initialized = True
    
    # Don't restart music here - it should already be playing from the launcher
    # Just check if music is already playing, if not, start it
    if not pygame.mixer.music.get_busy():
        music_path = Path("final.mp3")
        if music_path.exists():
            try:
                pygame.mixer.music.load(str(music_path))
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
                pygame.mixer.music.set_volume(0.7)  # Set volume to 70%
                print("🎵 Background music started in transition (final.mp3)")
            except Exception as e:
                print(f"⚠️ Could not load background music: {e}")
        else:
            print("⚠️ final.mp3 not found in current directory")
    else:
        print("🎵 Music already playing, continuing...")
    
    # Get screen dimensions
    info = pygame.display.Info()
    SCREEN_WIDTH = info.current_w
    SCREEN_HEIGHT = info.current_h
    
    # Set up display (start windowed for controls)
    screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
    pygame.display.set_caption(f"Quantum Jump to {continent_name}")
    
    # Colors
    BLACK = (0, 0, 0)
    
    # Create light-speed star field
    stars = [LightSpeedStar(SCREEN_WIDTH, SCREEN_HEIGHT) for _ in range(400)]
    particles = []
    
    # Animation variables
    start_time = pygame.time.get_ticks()
    total_duration = 8000  # 8 seconds total
    
    # Phase timings (in milliseconds)
    phase_timings = {
        "acceleration": 2000,      # 0-2s: Gradual acceleration
        "lightspeed": 4000,        # 2-6s: Full light speed travel
        "flash": 1000,             # 6-7s: Intense flash
        "arrival": 1000            # 7-8s: Arrival and completion
    }
    
    warp_speed = 1.0
    flash_intensity = 0.0
    time_factor = 0
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        current_time = pygame.time.get_ticks()
        elapsed = current_time - start_time
        dt = clock.tick(60) / 1000.0  # Delta time in seconds
        
        time_factor += dt
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Skip to flash phase
                    start_time = current_time - (phase_timings["acceleration"] + phase_timings["lightspeed"])
        
        # Calculate current phase and progress
        if elapsed < phase_timings["acceleration"]:
            # Phase 1: Gradual acceleration
            phase = "acceleration"
            progress = elapsed / phase_timings["acceleration"]
            warp_speed = 1 + progress * 4  # Speed up to 5x
            
        elif elapsed < phase_timings["acceleration"] + phase_timings["lightspeed"]:
            # Phase 2: Light speed travel
            phase = "lightspeed"
            phase_elapsed = elapsed - phase_timings["acceleration"]
            progress = phase_elapsed / phase_timings["lightspeed"]
            warp_speed = 5 + progress * 15  # Speed up to 20x
            
        elif elapsed < phase_timings["acceleration"] + phase_timings["lightspeed"] + phase_timings["flash"]:
            # Phase 3: Flash
            phase = "flash"
            phase_elapsed = elapsed - phase_timings["acceleration"] - phase_timings["lightspeed"]
            progress = phase_elapsed / phase_timings["flash"]
            warp_speed = 20 + progress * 30  # Max speed
            flash_intensity = math.sin(progress * math.pi) * 0.8
            
        else:
            # Phase 4: Arrival
            phase = "arrival"
            phase_elapsed = elapsed - phase_timings["acceleration"] - phase_timings["lightspeed"] - phase_timings["flash"]
            progress = phase_elapsed / phase_timings["arrival"]
            warp_speed = max(1, 50 - progress * 49)  # Slow down
            flash_intensity = max(0, 0.8 - progress * 0.8)
            
            # Exit after arrival phase
            if elapsed > total_duration:
                running = False
        
        # Get current screen dimensions
        current_width, current_height = screen.get_size()
        
        # Fill screen with deep space
        screen.fill(BLACK)
        
        # Add subtle quantum particles during acceleration and lightspeed
        if phase in ["acceleration", "lightspeed"] and random.random() < 0.1:
            particles.append(QuantumParticle(
                random.randint(0, current_width),
                random.randint(0, current_height),
                SCREEN_WIDTH, SCREEN_HEIGHT,
                "quantum" if random.random() < 0.7 else "energy"
            ))
        
        # Update and draw particles
        particles = [p for p in particles if p.life > 0]
        for particle in particles:
            particle.update()
            particle.draw(screen)
        
        # Create hyperspace grid effect during lightspeed
        if phase == "lightspeed":
            create_hyperspace_grid(screen, min(1.0, warp_speed / 10), time_factor, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Create warp tunnel during flash phase
        if phase == "flash":
            create_warp_tunnel_effect(screen, progress, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Update and draw stars
        for star in stars:
            star.update(warp_speed, progress if phase == "lightspeed" else 0, SCREEN_WIDTH, SCREEN_HEIGHT)
            star.draw(screen, warp_speed, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Screen flash effect
        if flash_intensity > 0:
            create_screen_flash(screen, flash_intensity, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        
        
        pygame.display.flip()
    
    # Don't stop the music when quantum transition ends - it should continue
    # pygame.mixer.music.stop()  # Commented out so music continues
    pygame.quit()
    return True

# =============================================================================
# MAIN APPLICATION CLASS
# =============================================================================

class ContinentalQuestApp:
    """Main application class that manages both the launcher and 3D globe"""
    
    def __init__(self):
        self.current_continent = None
        self.current_difficulty = 'medium'
        self.game_running = False
        self.web_window = None
        self.game_process = None
        self.music_started = False
        
        # Paths
        self.app_dir = Path(__file__).parent
        self.launcher_path = self.app_dir / 'continental_quest_landing.html'
        
        print("🌍 Continental Quest - Starting Application")
        print(f"📁 App Directory: {self.app_dir}")
        
    def start_background_music(self):
        """Start the background music if not already playing"""
        if not self.music_started:
            try:
                # Initialize pygame mixer if not already done
                import pygame
                if not pygame.get_init():
                    pygame.init()
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
                
                # Check if music is already playing (from another part of the app)
                if pygame.mixer.music.get_busy():
                    print("🎵 Music already playing from another source")
                    self.music_started = True
                    return
                
                music_path = Path("final.mp3")
                if music_path.exists():
                    pygame.mixer.music.load(str(music_path))
                    pygame.mixer.music.play(-1)  # Loop indefinitely
                    pygame.mixer.music.set_volume(0.7)
                    self.music_started = True
                    print("🎵 Background music started (final.mp3)")
                else:
                    print("⚠️ final.mp3 not found in current directory")
            except Exception as e:
                print(f"⚠️ Could not start background music: {e}")
        else:
            print("🎵 Background music already started, continuing...")
    
    def stop_background_music(self):
        """Stop the background music"""
        if self.music_started:
            try:
                import pygame
                if pygame.mixer.get_init():
                    pygame.mixer.music.stop()
                    self.music_started = False
                    print("🎵 Background music stopped")
            except Exception as e:
                print(f"⚠️ Could not stop background music: {e}")
        
    def setup_api_bridge(self):
        """Setup JavaScript-Python communication bridge"""
        
        class WebAPI:
            def __init__(self, app_instance):
                self.app = app_instance
            
            def launch_continent(self, continent_name):
                """Called when user selects a continent from the web interface"""
                print(f"🌍 Web: Launching {continent_name}")
                self.app.current_continent = continent_name
                
                # Start the 3D globe with the selected continent
                return self.app.start_3d_globe(continent_name)
            
            def start_game(self, options=None):
                """Start the main 3D globe game"""
                print("\n🚀 [DEBUG] start_game() called from JavaScript!")
                print(f"📊 [DEBUG] Options received: {options}")
                
                continent = 'earth'  # Default to full earth view
                difficulty = 'medium'
                
                if options:
                    continent = options.get('continent', 'earth')
                    difficulty = options.get('difficulty', 'medium')
                
                self.app.current_continent = continent
                self.app.current_difficulty = difficulty
                
                print(f"🎮 Starting 3D Globe: {continent} ({difficulty})")
                
                # Start background music only if not already playing
                if not self.app.music_started:
                    self.app.start_background_music()
                else:
                    print("🎵 Music already playing, continuing without restart")
                
                # Run the quantum transition first
                print("🚀 Starting quantum space jump transition...")
                run_quantum_transition(continent)
                
                # Then start the 3D globe
                result = self.app.start_3d_globe(continent)
                print(f"🔄 [DEBUG] Globe start result: {result}")
                return result
            
            def set_difficulty(self, difficulty):
                """Set game difficulty level"""
                self.app.current_difficulty = difficulty
                print(f"⚡ Difficulty set to: {difficulty}")
                return {'status': 'success', 'difficulty': difficulty}
            
            def get_progress(self, continent=None):
                """Get player progress (mock data for now)"""
                # You can integrate this with your actual game progress later
                progress_data = {
                    'north-america': 75,
                    'south-america': 60,
                    'europe': 85,
                    'africa': 45,
                    'asia': 55,
                    'australia': 90,
                    'antarctica': 25
                }
                
                if continent:
                    return progress_data.get(continent, 0)
                return progress_data
            
            def minimize_launcher(self):
                """Minimize the launcher window"""
                if self.app.web_window:
                    self.app.web_window.minimize()
                return {'status': 'success'}
            
            def close_application(self):
                """Close the entire application"""
                self.app.shutdown()
                return {'status': 'success'}
            
            def test_connection(self):
                """Test if the Python API bridge is working"""
                print("\n🔥 [TEST] Python API connection successful!")
                return {
                    'status': 'success',
                    'message': 'Python API bridge is working!',
                    'timestamp': time.time()
                }
        
        return WebAPI(self)
    
    def start_3d_globe(self, continent='earth'):
        """Start the 3D OpenGL globe"""
        try:
            if not GLOBE_AVAILABLE:
                return {
                    'status': 'error',
                    'message': 'globe.py not available'
                }
            
            # Minimize the web launcher
            if self.web_window:
                self.web_window.minimize()
            
            print(f"🌍 Starting 3D Globe for: {continent}")
            
            # Ensure music is playing before starting globe
            import pygame
            if self.music_started and pygame.mixer.get_init():
                if not pygame.mixer.music.get_busy():
                    print("🎵 Music not playing, restarting before globe...")
                    music_path = Path("final.mp3")
                    if music_path.exists():
                        try:
                            pygame.mixer.music.load(str(music_path))
                            pygame.mixer.music.play(-1)
                            pygame.mixer.music.set_volume(0.7)
                            print("🎵 Music restarted before globe")
                        except Exception as e:
                            print(f"⚠️ Could not restart music: {e}")
                else:
                    print("🎵 Music playing, continuing to globe...")
            
            # Start the 3D globe in a separate thread to avoid blocking
            globe_thread = threading.Thread(
                target=self.run_globe_with_continent,
                args=(continent,)
            )
            globe_thread.daemon = True
            globe_thread.start()
            
            return {
                'status': 'success',
                'continent': continent,
                'message': f'3D Globe started for {continent}'
            }
            
        except Exception as e:
            print(f"❌ Error starting 3D globe: {e}")
            return {
                'status': 'error',
                'message': f'Failed to start 3D globe: {str(e)}'
            }
    
    def run_globe_with_continent(self, continent):
        """Run the 3D globe with continent-specific settings"""
        try:
            self.game_running = True
            print(f"🎮 3D Globe running for: {continent}")
            
            # Ensure music continues playing by checking and restarting if needed
            import pygame
            if pygame.mixer.get_init() and not pygame.mixer.music.get_busy():
                print("🎵 Music stopped, restarting for globe...")
                music_path = Path("final.mp3")
                if music_path.exists():
                    try:
                        pygame.mixer.music.load(str(music_path))
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.7)
                        print("🎵 Music restarted for globe")
                    except Exception as e:
                        print(f"⚠️ Could not restart music for globe: {e}")
            else:
                print("🎵 Music continuing into globe...")
            
            # Store original pygame mixer state before running globe
            music_was_playing = False
            music_position = 0
            
            try:
                if pygame.mixer.get_init():
                    music_was_playing = pygame.mixer.music.get_busy()
                    # Save current music state
                    if music_was_playing:
                        print("🎵 Preserving music state for globe execution")
            except:
                pass
            
            # You can modify globe.py's main() function or create continent-specific versions
            # For now, we'll run the existing globe
            globe.main()
            
        except Exception as e:
            print(f"❌ Globe error: {e}")
        finally:
            self.game_running = False
            
            # Restore music after globe closes if it was interrupted
            try:
                import pygame
                if pygame.mixer.get_init() and not pygame.mixer.music.get_busy() and self.music_started:
                    print("🎵 Restoring music after globe closed...")
                    music_path = Path("final.mp3")
                    if music_path.exists():
                        pygame.mixer.music.load(str(music_path))
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.7)
                        print("🎵 Music restored after globe")
            except Exception as e:
                print(f"⚠️ Could not restore music after globe: {e}")
                
            # Restore the launcher window when globe closes
            if self.web_window:
                self.web_window.show()
    
    def create_launcher_files(self):
        """Copy the landing page files to the app directory if needed"""
        required_files = [
            'continental_quest_landing.html',
            'style.css',
            'script.js'
        ]
        
        source_dir = Path("C:\\Users\\Manthan Railkar")
        
        for filename in required_files:
            source_file = source_dir / filename
            target_file = self.app_dir / filename
            
            if source_file.exists() and not target_file.exists():
                try:
                    import shutil
                    shutil.copy2(source_file, target_file)
                    print(f"✅ Copied {filename} to app directory")
                except Exception as e:
                    print(f"⚠️  Could not copy {filename}: {e}")
    
    def run_webview_launcher(self):
        """Run the web launcher using pywebview"""
        if not WEBVIEW_AVAILABLE:
            print("❌ pywebview is not available")
            return False
        
        # Start background music when launcher starts
        self.start_background_music()
        
        # Ensure launcher files are available
        self.create_launcher_files()
        
        if not self.launcher_path.exists():
            print(f"❌ Launcher file not found: {self.launcher_path}")
            return False
        
        # Setup API bridge
        api = self.setup_api_bridge()
        
        # Create the webview window
        self.web_window = webview.create_window(
            title='Continental Quest - Choose Your Adventure',
            url=str(self.launcher_path),
            width=1400,
            height=900,
            resizable=True,
            fullscreen=False,
            js_api=api,
            on_top=False
        )
        
        # Add a callback to handle window events
        def on_window_loaded():
            print("\n🔥 [DEBUG] Window loaded - setting up Python integration")
            
            # Inject a direct call to our API
            script = f"""
            // Override the Python interface to force webview mode
            if (window.pythonInterface) {{
                window.pythonInterface.backend_type = 'webview';
                console.log('🔥 [FORCED] Backend type set to webview');
                
                // Override startGame to directly call the Python API
                const originalStartGame = window.pythonInterface.startGame.bind(window.pythonInterface);
                window.pythonInterface.startGame = async function(options) {{
                    console.log('🚀 [OVERRIDE] startGame called, triggering Python...');
                    try {{
                        // Call the Python API directly
                        const result = await pywebview.api.start_game(options);
                        console.log('✅ [PYTHON] Success:', result);
                        return result;
                    }} catch (error) {{
                        console.error('❌ [PYTHON] Error:', error);
                        // If that fails, try the original method
                        return await originalStartGame(options);
                    }}
                }};
            }}
            
            // Also inject a global direct function
            window.directStartGame = function() {{
                console.log('🚀 [DIRECT] Starting game directly!');
                return window.pythonInterface.startGame({{}});
            }};
            
            console.log('🔥 [INJECTED] Python integration enhanced');
            """
            
            try:
                # Wait a bit for the page to fully load
                import time
                time.sleep(1)
                self.web_window.evaluate_js(script)
                print("✅ [DEBUG] Successfully enhanced Python integration")
            except Exception as e:
                print(f"❌ [DEBUG] Failed to enhance integration: {e}")
        
        # Handle window closing to stop music
        def on_window_closing():
            print("🔄 Window closing - stopping background music")
            self.stop_background_music()
        
        # Set the callbacks
        webview.windows[0].events.loaded += on_window_loaded
        webview.windows[0].events.closing += on_window_closing
        
        print("🚀 Starting Continental Quest Launcher...")
        print("🌍 Use the web interface to select your continent!")
        
        # Start the webview (this blocks until window closes)
        try:
            webview.start(debug=False)  # Changed from debug=True to debug=False
        finally:
            # Ensure music is stopped when webview ends
            self.stop_background_music()
        
        return True
    
    def run_fallback_launcher(self):
        """Fallback method using system browser"""
        print("🔄 Using fallback browser launcher...")
        
        # Start background music for fallback mode too
        self.start_background_music()
        
        self.create_launcher_files()
        
        if self.launcher_path.exists():
            import webbrowser
            webbrowser.open(f'file://{self.launcher_path.absolute()}')
            print("🌐 Opened launcher in default browser")
            print("👉 The 3D globe integration works best with the desktop app")
            
            # Keep the app running
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("👋 Application closed")
                self.stop_background_music()
        else:
            print("❌ Launcher files not found")
    
    def shutdown(self):
        """Clean shutdown of the application"""
        print("🛑 Shutting down Continental Quest...")
        
        # Stop background music
        self.stop_background_music()
        
        if self.web_window:
            try:
                self.web_window.destroy()
            except:
                pass
        
        if self.game_process:
            try:
                self.game_process.terminate()
            except:
                pass
        
        # Force exit
        os._exit(0)
    
    def run(self):
        """Main application entry point"""
        print("🌍 Continental Quest - Desktop Application")
        print("=" * 50)
        
        # Check dependencies
        if not GLOBE_AVAILABLE:
            print("❌ Warning: globe.py not available - 3D features may not work")
        
        # Try to run with webview first (best experience)
        if WEBVIEW_AVAILABLE:
            print("🚀 Starting with WebView integration")
            success = self.run_webview_launcher()
        else:
            print("🔄 WebView not available, using browser fallback")
            self.run_fallback_launcher()

def main():
    """Main entry point"""
    try:
        app = ContinentalQuestApp()
        app.run()
    except KeyboardInterrupt:
        print("👋 Application interrupted by user")
    except Exception as e:
        print(f"❌ Application error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()