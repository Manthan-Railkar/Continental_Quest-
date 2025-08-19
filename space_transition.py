import pygame
import sys
import math
import random
import subprocess
import os
import threading
import time

# Initialize pygame
pygame.init()

# Get screen dimensions
info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Set up display (start windowed for controls)
screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
pygame.display.set_caption("Quantum Space Jump - Loading Global View")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
PINK = (255, 20, 147)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)

# Global variables
is_fullscreen = False

# Enhanced Star class for light-speed travel
class LightSpeedStar:
    def __init__(self):
        self.x = random.uniform(0, SCREEN_WIDTH)
        self.y = random.uniform(0, SCREEN_HEIGHT)
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
        
    def update(self, warp_speed=1.0, progress=0.0):
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
            self.x = random.uniform(0, SCREEN_WIDTH)
            self.y = random.uniform(0, SCREEN_HEIGHT)
    
    def draw(self, surface, warp_speed=1.0):
        current_width, current_height = surface.get_size()
        
        # Calculate screen position with perspective projection
        if self.z <= 0:
            return
            
        # Perspective calculation
        scale = 500.0 / self.z
        screen_x = int(current_width/2 + (self.x - SCREEN_WIDTH/2) * scale)
        screen_y = int(current_height/2 + (self.y - SCREEN_HEIGHT/2) * scale)
        
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
                    trail_x = int(current_width/2 + (self.x - SCREEN_WIDTH/2) * trail_scale)
                    trail_y = int(current_height/2 + (self.y - SCREEN_HEIGHT/2) * trail_scale)
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
    def __init__(self, x, y, particle_type="energy"):
        self.x = x
        self.y = y
        self.particle_type = particle_type
        
        if particle_type == "energy":
            self.speed = random.uniform(3, 12)
            angle = random.uniform(0, 2 * math.pi)
            self.dx = math.cos(angle) * self.speed
            self.dy = math.sin(angle) * self.speed
            self.life = random.uniform(60, 120)
            self.max_life = self.life
            self.color = random.choice([CYAN, BLUE, PURPLE, WHITE])
        elif particle_type == "quantum":
            self.speed = random.uniform(8, 25)
            angle = random.uniform(0, 2 * math.pi)
            self.dx = math.cos(angle) * self.speed
            self.dy = math.sin(angle) * self.speed
            self.life = random.uniform(40, 90)
            self.max_life = self.life
            self.color = random.choice([GOLD, ORANGE, WHITE, CYAN])
        else:
            self.speed = random.uniform(1, 8)
            angle = random.uniform(0, 2 * math.pi)
            self.dx = math.cos(angle) * self.speed
            self.dy = math.sin(angle) * self.speed
            self.life = random.uniform(30, 80)
            self.max_life = self.life
            self.color = WHITE
        
        self.decay = random.uniform(0.5, 1.5)
        self.size = random.uniform(1, 3)
        self.pulse_phase = random.uniform(0, math.pi * 2)
        
    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= self.decay
        
        # Gentle acceleration toward center
        center_x = SCREEN_WIDTH / 2
        center_y = SCREEN_HEIGHT / 2
        
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

def create_warp_tunnel_effect(surface, progress):
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

def create_hyperspace_grid(surface, progress, time_factor):
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

def create_screen_flash(surface, intensity):
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

def launch_globe():
    """Launch globe.py and wait for it to complete"""
    try:
        # Find the globe file
        possible_files = ["globe.py", "global.py", "./globe.py", "./global.py"]
        
        for filename in possible_files:
            if os.path.exists(filename):
                print(f"Launching {filename}...")
                
                # Launch the globe script directly and wait for it to complete
                process = subprocess.Popen([sys.executable, filename])
                process.wait()  # Wait for the process to complete
                
                print(f"{filename} completed")
                return True
                
        print("Globe file not found")
        return False
        
    except Exception as e:
        print(f"Failed to launch globe: {e}")
        return False

def toggle_fullscreen():
    """Toggle between fullscreen and windowed mode"""
    global screen, is_fullscreen
    
    if is_fullscreen:
        screen = pygame.display.set_mode((1200, 800), pygame.RESIZABLE)
        is_fullscreen = False
    else:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        is_fullscreen = True

def main():
    global screen, is_fullscreen
    
    clock = pygame.time.Clock()
    
    # Create light-speed star field
    stars = [LightSpeedStar() for _ in range(400)]
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
    launch_attempted = False
    globe_process = None
    
    # Time tracking
    time_factor = 0
    
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
                elif event.key == pygame.K_F11:
                    toggle_fullscreen()
                elif event.key == pygame.K_SPACE:
                    # Skip to flash phase
                    start_time = current_time - (phase_timings["acceleration"] + phase_timings["lightspeed"])
            elif event.type == pygame.VIDEORESIZE and not is_fullscreen:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
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
            
            # Launch globe once during arrival phase
            if not launch_attempted and progress > 0.3:
                launch_attempted = True
                # Launch globe in a thread to not block the animation
                threading.Thread(target=launch_globe, daemon=True).start()
            
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
                "quantum" if random.random() < 0.7 else "energy"
            ))
        
        # Update and draw particles
        particles = [p for p in particles if p.life > 0]
        for particle in particles:
            particle.update()
            particle.draw(screen)
        
        # Create hyperspace grid effect during lightspeed
        if phase == "lightspeed":
            create_hyperspace_grid(screen, min(1.0, warp_speed / 10), time_factor)
        
        # Create warp tunnel during flash phase
        if phase == "flash":
            create_warp_tunnel_effect(screen, progress)
        
        # Update and draw stars
        for star in stars:
            star.update(warp_speed, progress if phase == "lightspeed" else 0)
            star.draw(screen, warp_speed)
        
        # Screen flash effect
        if flash_intensity > 0:
            create_screen_flash(screen, flash_intensity)
        
        # Subtle controls hint (bottom right, very discrete)
        if not is_fullscreen:
            font = pygame.font.Font(None, 24)
            controls_text = "F11: Fullscreen | SPACE: Skip | ESC: Exit"
            text_surf = font.render(controls_text, True, (60, 60, 60))
            text_rect = text_surf.get_rect()
            text_rect.bottomright = (current_width - 10, current_height - 10)
            screen.blit(text_surf, text_rect)
        
        pygame.display.flip()
    
    # After the transition, launch the globe and wait for it to complete
    pygame.quit()
    launch_globe()
    sys.exit()


if __name__ == "__main__":
    main()