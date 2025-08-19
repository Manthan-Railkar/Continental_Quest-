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
is_minimized = False

# Enhanced Star class with depth and perspective
class Star:
    def __init__(self):
        self.x = random.uniform(-SCREEN_WIDTH, SCREEN_WIDTH * 2)
        self.y = random.uniform(-SCREEN_HEIGHT, SCREEN_HEIGHT * 2)
        self.z = random.uniform(1, 100)  # Depth
        self.original_z = self.z
        self.speed = random.uniform(0.1, 0.5)
        self.brightness = random.randint(50, 255)
        self.color_variant = random.choice([WHITE, CYAN, (255, 255, 200), (200, 200, 255)])
        self.twinkle_speed = random.uniform(0.02, 0.1)
        self.twinkle_phase = random.uniform(0, math.pi * 2)
        
    def update(self, warp_factor=1.0):
        # Normal movement
        self.y += self.speed
        
        # Warp effect - stars move toward viewer
        if warp_factor > 1.0:
            self.z -= warp_factor * 2
            if self.z <= 0:
                self.z = 100
                self.x = random.uniform(-SCREEN_WIDTH, SCREEN_WIDTH * 2)
                self.y = random.uniform(-SCREEN_HEIGHT, SCREEN_HEIGHT * 2)
        
        # Reset star position
        if self.y > SCREEN_HEIGHT + 50:
            self.y = -50
            self.x = random.uniform(-SCREEN_WIDTH, SCREEN_WIDTH * 2)
        
        # Twinkle effect
        self.twinkle_phase += self.twinkle_speed
    
    def draw(self, surface, warp_factor=1.0):
        # Calculate screen position based on depth
        screen_x = int(self.x + (self.x - SCREEN_WIDTH/2) * (100 - self.z) / self.z)
        screen_y = int(self.y + (self.y - SCREEN_HEIGHT/2) * (100 - self.z) / self.z)
        
        # Skip if off screen
        if screen_x < -50 or screen_x > SCREEN_WIDTH + 50 or screen_y < -50 or screen_y > SCREEN_HEIGHT + 50:
            return
            
        # Size based on depth and warp
        size = max(1, int((100 - self.z) / 20))
        if warp_factor > 5:
            size = max(size, int(warp_factor / 3))
        
        # Brightness with twinkle
        twinkle = math.sin(self.twinkle_phase) * 0.3 + 0.7
        alpha = int(self.brightness * twinkle * (100 - self.z) / 100)
        
        # Color based on depth and warp
        if warp_factor > 3:
            # Warp colors - more energetic
            color = (
                min(255, int(self.color_variant[0] * twinkle + warp_factor * 10)),
                min(255, int(self.color_variant[1] * twinkle + warp_factor * 5)),
                min(255, int(self.color_variant[2] * twinkle))
            )
        else:
            color = (
                int(self.color_variant[0] * twinkle),
                int(self.color_variant[1] * twinkle),
                int(self.color_variant[2] * twinkle)
            )
        
        # Draw star with glow effect for larger stars
        if size > 2:
            # Glow
            for i in range(3, 0, -1):
                glow_color = (color[0] // (4-i), color[1] // (4-i), color[2] // (4-i))
                pygame.draw.circle(surface, glow_color, (screen_x, screen_y), size + i)
        
        pygame.draw.circle(surface, color, (screen_x, screen_y), size)

# Enhanced Particle class with realistic physics
class Particle:
    def __init__(self, x, y, particle_type="normal"):
        self.x = x
        self.y = y
        self.particle_type = particle_type
        
        if particle_type == "energy":
            self.speed = random.uniform(5, 20)
            angle = random.uniform(0, 2 * math.pi)
            self.dx = math.cos(angle) * self.speed
            self.dy = math.sin(angle) * self.speed
            self.life = random.uniform(60, 120)
            self.max_life = self.life
            self.color = random.choice([CYAN, BLUE, PURPLE, PINK])
        elif particle_type == "quantum":
            self.speed = random.uniform(15, 40)
            angle = random.uniform(0, 2 * math.pi)
            self.dx = math.cos(angle) * self.speed
            self.dy = math.sin(angle) * self.speed
            self.life = random.uniform(30, 80)
            self.max_life = self.life
            self.color = random.choice([GOLD, ORANGE, WHITE])
        else:  # normal
            self.speed = random.uniform(2, 10)
            angle = random.uniform(0, 2 * math.pi)
            self.dx = math.cos(angle) * self.speed
            self.dy = math.sin(angle) * self.speed
            self.life = random.uniform(40, 100)
            self.max_life = self.life
            self.color = WHITE
        
        self.decay = random.uniform(0.8, 2.0)
        self.size = random.uniform(1, 4)
        
    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= self.decay
        
        # Slight gravitational effect
        self.dy += 0.1
        
        # Friction
        self.dx *= 0.995
        self.dy *= 0.995
        
    def draw(self, surface):
        if self.life > 0:
            life_ratio = self.life / self.max_life
            alpha = int(255 * life_ratio)
            size = int(self.size * life_ratio)
            
            # Color fade
            color = (
                min(255, int(self.color[0] * life_ratio)),
                min(255, int(self.color[1] * life_ratio)),
                min(255, int(self.color[2] * life_ratio))
            )
            
            if size > 0:
                pygame.draw.circle(surface, color, (int(self.x), int(self.y)), size)

def create_realistic_warp_effect(surface, progress, particles):
    """Create realistic warp lines and energy fields"""
    current_width, current_height = surface.get_size()
    
    # Central warp core
    core_x, core_y = current_width // 2, current_height // 2
    
    # Spiral energy lines
    num_spirals = 8
    for spiral in range(num_spirals):
        points = []
        for i in range(50):
            angle = (spiral * math.pi * 2 / num_spirals) + (progress * 10) + (i * 0.3)
            radius = i * 8 * progress
            
            if radius > current_width:
                break
                
            x = core_x + math.cos(angle) * radius
            y = core_y + math.sin(angle) * radius
            
            if 0 <= x <= current_width and 0 <= y <= current_height:
                points.append((x, y))
        
        if len(points) > 1:
            # Color shift based on progress
            intensity = int(200 * progress * (1 + math.sin(progress * 5) * 0.3))
            color = (
                min(255, intensity),
                min(255, intensity // 2),
                min(255, intensity + int(50 * math.sin(progress * 3)))
            )
            
            # Draw spiral with varying thickness
            for i in range(len(points) - 1):
                thickness = max(1, int(5 * progress * (1 - i / len(points))))
                pygame.draw.line(surface, color, points[i], points[i + 1], thickness)

def create_energy_ripples(surface, progress, center_x, center_y):
    """Create expanding energy ripples"""
    current_width, current_height = surface.get_size()
    
    for i in range(5):
        radius = int(progress * 400 + i * 60)
        if radius > 0 and radius < 800:
            alpha = max(0, int(100 - i * 20 - progress * 50))
            color = (alpha, alpha // 2, alpha + 50) if alpha > 0 else (0, 0, 0)
            
            if color != (0, 0, 0):
                # Create ripple surface
                ripple_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(ripple_surface, (*color, alpha // 4), (radius, radius), radius, 3)
                
                surface.blit(ripple_surface, (center_x - radius, center_y - radius))

def draw_hacker_text(surface, text, font, x, y, color, glow_color, pulse_factor=1.0):
    """Hacker-style text aligned to bottom-left with glow effects"""
    current_width, current_height = surface.get_size()
    
    # Position from bottom-left (x from left, y from bottom)
    pos_x = x
    pos_y = current_height - y
    
    # Pulse effect
    pulse_size = int(font.get_height() * pulse_factor)
    
    if pulse_size > 0:
        # Create hacker-style monospace font
        try:
            # Try to use a monospace font for hacker aesthetic
            pulsed_font = pygame.font.SysFont('consolas', pulse_size)
            if not pulsed_font:
                pulsed_font = pygame.font.SysFont('courier', pulse_size)
            if not pulsed_font:
                pulsed_font = pygame.font.SysFont('monaco', pulse_size)
            if not pulsed_font:
                # Fallback to default monospace
                pulsed_font = pygame.font.Font(None, pulse_size)
        except:
            pulsed_font = pygame.font.Font(None, pulse_size)
        
        # Multi-layer glow
        glow_layers = 6
        for layer in range(glow_layers, 0, -1):
            layer_alpha = max(15, 90 - layer * 12)
            layer_color = (
                min(255, glow_color[0] + layer * 8),
                min(255, glow_color[1] + layer * 5),
                min(255, glow_color[2] + layer * 3)
            )
            
            glow_surf = pulsed_font.render(text, True, layer_color)
            offset = layer * 1
            
            for dx in range(-offset, offset + 1):
                for dy in range(-offset, offset + 1):
                    if dx != 0 or dy != 0:
                        surface.blit(glow_surf, (pos_x + dx, pos_y + dy))
        
        # Main text (bottom-left aligned)
        text_surf = pulsed_font.render(text, True, color)
        surface.blit(text_surf, (pos_x, pos_y))

def launch_globe_with_retry():
    """Launch globe.py with multiple attempts and keep it running"""
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        try:
            # Try different possible locations and names
            possible_files = ["globe.py", "global.py", "./globe.py", "./global.py"]
            
            for filename in possible_files:
                if os.path.exists(filename):
                    print(f"Launching {filename}...")
                    
                    # Launch process that stays open
                    if sys.platform == "win32":
                        # Windows - create new console window
                        process = subprocess.Popen(
                            [sys.executable, filename],
                            creationflags=subprocess.CREATE_NEW_CONSOLE,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                    else:
                        # Linux/Mac - detach from parent
                        process = subprocess.Popen(
                            [sys.executable, filename],
                            stdin=subprocess.DEVNULL,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            preexec_fn=os.setpgrp if hasattr(os, 'setpgrp') else None
                        )
                    
                    print(f"Successfully launched {filename} with PID: {process.pid}")
                    # Don't wait for the process - let it run independently
                    return True
            
            print(f"Attempt {attempts + 1}: Globe file not found")
            attempts += 1
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Attempt {attempts + 1} failed: {e}")
            attempts += 1
            time.sleep(0.5)
    
    print("Failed to launch globe after all attempts")
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
    global screen, is_fullscreen, is_minimized
    
    clock = pygame.time.Clock()
    
    # Create enhanced star field
    stars = [Star() for _ in range(300)]
    particles = []
    
    # Animation variables
    start_time = pygame.time.get_ticks()
    phase = "initialization"  # phases: "initialization", "calibration", "charging", "warp", "complete"
    
    # Enhanced font setup - hacker style monospace
    try:
        title_font = pygame.font.SysFont('consolas', 48)
        large_font = pygame.font.SysFont('consolas', 36)
        medium_font = pygame.font.SysFont('consolas', 28)
        small_font = pygame.font.SysFont('consolas', 20)
    except:
        try:
            title_font = pygame.font.SysFont('courier', 48)
            large_font = pygame.font.SysFont('courier', 36)
            medium_font = pygame.font.SysFont('courier', 28)
            small_font = pygame.font.SysFont('courier', 20)
        except:
            # Fallback fonts
            title_font = pygame.font.Font(None, 48)
            large_font = pygame.font.Font(None, 36)
            medium_font = pygame.font.Font(None, 28)
            small_font = pygame.font.Font(None, 20)
    
    phase_start_time = start_time
    warp_factor = 1.0
    transition_complete = False
    launch_attempted = False
    
    # Sound-like visual feedback variables
    audio_bars = [random.uniform(0.1, 0.8) for _ in range(20)]
    
    running = True
    while running:
        current_time = pygame.time.get_ticks()
        dt = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F11:
                    toggle_fullscreen()
                elif event.key == pygame.K_SPACE and phase in ["initialization", "calibration"]:
                    # Skip to next phase
                    if phase == "initialization":
                        phase = "calibration"
                        phase_start_time = current_time
                    elif phase == "calibration":
                        phase = "charging"
                        phase_start_time = current_time
            elif event.type == pygame.VIDEORESIZE and not is_fullscreen:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
        # Get current screen dimensions
        current_width, current_height = screen.get_size()
        
        # Fill screen with deep space
        screen.fill(BLACK)
        
        # Calculate phase progress
        phase_elapsed = current_time - phase_start_time
        
        # Phase management with realistic progression
        if phase == "initialization":
            # Initial system boot sequence
            duration = 4000
            progress = min(1.0, phase_elapsed / duration)
            
            # Update stars normally
            for star in stars:
                star.update(1.0)
                star.draw(screen, 1.0)
            
            # Initialization messages
            if progress < 0.3:
                pulse = 1.0 + math.sin(current_time * 0.01) * 0.1
                draw_hacker_text(screen, "> QUANTUM_DRIVE.init()", large_font, 
                                20, 200, GREEN, (0, 255, 0), pulse)
                
                # System check messages
                checks = [
                    "> spacetime_calibrators.check() ... [OK]",
                    "> quantum_flux_stabilizers.status() ... [OK]", 
                    "> navigation_systems.verify() ... [OK]",
                    "> reality_anchors.test() ... [OK]"
                ]
                for i, check in enumerate(checks):
                    if progress > i * 0.07:
                        draw_hacker_text(screen, check, small_font,
                                       20, 160 - i * 25,
                                       GREEN, (0, 150, 0), 0.8)
            
            elif progress < 0.7:
                draw_hacker_text(screen, "> COORDINATES_LOCKED", large_font,
                               20, 200, CYAN, (0, 255, 255), 1.2)
                draw_hacker_text(screen, "> target: earth.global_view", medium_font,
                               20, 160, GOLD, (255, 200, 0), 1.0)
            else:
                phase = "calibration"
                phase_start_time = current_time
                
        elif phase == "calibration":
            # Quantum field calibration
            duration = 3000
            progress = min(1.0, phase_elapsed / duration)
            
            # Add some energy particles
            if random.random() < 0.3:
                particles.append(Particle(random.randint(0, current_width), 
                                        random.randint(0, current_height), "energy"))
            
            # Update stars with slight acceleration
            for star in stars:
                star.update(1.0 + progress * 0.5)
                star.draw(screen, 1.0 + progress * 0.5)
            
            # Update particles
            particles = [p for p in particles if p.life > 0]
            for particle in particles:
                particle.update()
                particle.draw(screen)
            
            # Audio visualization effect
            for i in range(len(audio_bars)):
                audio_bars[i] += random.uniform(-0.1, 0.1)
                audio_bars[i] = max(0.1, min(0.9, audio_bars[i]))
            
            # Draw audio bars
            bar_width = current_width // len(audio_bars)
            for i, height in enumerate(audio_bars):
                bar_height = int(height * 100 * (1 + progress))
                color = (int(100 + height * 155), int(50 + height * 100), int(200))
                pygame.draw.rect(screen, color, 
                               (i * bar_width, current_height - bar_height, bar_width - 2, bar_height))
            
            if progress < 0.6:
                draw_hacker_text(screen, "> quantum_field.calibrate()", large_font,
                               20, 200, PURPLE, (255, 0, 255), 1.0 + progress * 0.3)
                draw_hacker_text(screen, f"> field_strength: {int(progress * 100)}%", medium_font,
                               20, 160, CYAN, (0, 255, 255), 1.0)
            else:
                phase = "charging"
                phase_start_time = current_time
                
        elif phase == "charging":
            # Energy charging phase
            duration = 4000
            progress = min(1.0, phase_elapsed / duration)
            
            # Intense particle generation
            for _ in range(int(10 + progress * 20)):
                particles.append(Particle(current_width//2 + random.randint(-100, 100),
                                        current_height//2 + random.randint(-100, 100),
                                        "quantum"))
            
            # Accelerating stars
            warp_factor = 1.0 + progress * 3
            for star in stars:
                star.update(warp_factor)
                star.draw(screen, warp_factor)
            
            # Update particles
            particles = [p for p in particles if p.life > 0]
            for particle in particles:
                particle.update()
                particle.draw(screen)
            
            # Energy ripples
            create_energy_ripples(screen, progress, current_width//2, current_height//2)
            
            if progress < 0.8:
                intensity = 1.0 + math.sin(progress * 20) * 0.3
                draw_hacker_text(screen, "> hyperdrive.charge_capacitors()", large_font,
                               20, 200, ORANGE, (255, 100, 0), intensity)
                
                # Energy percentage
                energy_pct = int(progress * 100)
                draw_hacker_text(screen, f"> energy_level: {energy_pct}%", medium_font,
                               20, 160, CYAN, (0, 255, 255), 1.0)
                draw_hacker_text(screen, "> status: CHARGING...", small_font,
                               20, 120, WHITE, (200, 200, 200), 1.0)
            else:
                phase = "warp"
                phase_start_time = current_time
                
        elif phase == "warp":
            # Full warp sequence
            duration = 6000
            progress = min(1.0, phase_elapsed / duration)
            
            # Extreme warp factor
            warp_factor = 1.0 + progress * 25
            
            # Update stars with extreme warp
            for star in stars:
                star.update(warp_factor)
                star.draw(screen, warp_factor)
            
            # Massive particle generation
            for _ in range(int(20 + progress * 50)):
                particles.append(Particle(
                    random.randint(-100, current_width + 100),
                    random.randint(-100, current_height + 100),
                    random.choice(["energy", "quantum", "normal"])
                ))
            
            # Update particles
            particles = [p for p in particles if p.life > 0]
            for particle in particles:
                particle.update()
                particle.draw(screen)
            
            # Advanced warp effects
            create_realistic_warp_effect(screen, progress, particles)
            create_energy_ripples(screen, progress, current_width//2, current_height//2)
            
            # Screen distortion effect
            if progress > 0.3:
                distortion_intensity = int((progress - 0.3) * 300)
                distort_surface = pygame.Surface((current_width, current_height))
                distort_surface.fill((distortion_intensity//3, distortion_intensity//4, distortion_intensity//2))
                distort_surface.set_alpha(distortion_intensity//2)
                screen.blit(distort_surface, (0, 0))
            
            # Warp messages
            if progress < 0.3:
                draw_hacker_text(screen, "> hyperdrive.engage()", title_font,
                               20, 240, WHITE, (255, 255, 255), 1.5)
                draw_hacker_text(screen, "> status: ENGAGED", medium_font,
                               20, 200, GREEN, (0, 255, 0), 1.2)
            elif progress < 0.6:
                draw_hacker_text(screen, "> spacetime.fold()", large_font,
                               20, 200, GOLD, (255, 215, 0), 1.3)
                draw_hacker_text(screen, "> reality.bend()", medium_font,
                               20, 160, ORANGE, (255, 165, 0), 1.1)
            elif progress < 0.9:
                flash_intensity = 1.0 + math.sin(progress * 30) * 0.5
                draw_hacker_text(screen, "> dimensional.breach_detected()", large_font,
                               20, 200, RED, (255, 0, 0), flash_intensity)
                draw_hacker_text(screen, "> WARNING: REALITY_UNSTABLE", medium_font,
                               20, 160, PINK, (255, 20, 147), flash_intensity)
            
            # Complete warp
            if progress >= 1.0 and not launch_attempted:
                phase = "complete"
                phase_start_time = current_time
                launch_attempted = True
                # Launch globe in separate thread
                threading.Thread(target=launch_globe_with_retry, daemon=True).start()
                
        elif phase == "complete":
            # Completion and transition to globe
            completion_elapsed = current_time - phase_start_time
            
            # Calm down effects
            warp_factor = max(1.0, 10 - completion_elapsed / 200)
            
            # Normalize stars
            for star in stars:
                star.update(warp_factor)
                star.draw(screen, warp_factor)
            
            # Final particles
            particles = [p for p in particles if p.life > 10]
            for particle in particles:
                particle.update()
                particle.draw(screen)
            
            # Success messages
            if completion_elapsed < 2000:
                draw_hacker_text(screen, "> jump.status: SUCCESS", title_font,
                               20, 240, GREEN, (0, 255, 0), 1.2)
                draw_hacker_text(screen, "> coordinates.reached: TRUE", medium_font,
                               20, 200, CYAN, (0, 255, 255), 1.1)
            elif completion_elapsed < 4000:
                draw_hacker_text(screen, "> global_view.launch()", large_font,
                               20, 200, CYAN, (0, 255, 255), 1.1)
                draw_hacker_text(screen, "> please_wait...", medium_font,
                               20, 160, WHITE, (200, 200, 200), 0.9)
                draw_hacker_text(screen, "> initializing_globe_interface", small_font,
                               20, 120, GREEN, (0, 200, 0), 0.8)
            
            # Auto-close after showing completion
            if completion_elapsed > 5000:
                running = False
        
        # Window controls hint
        if not is_fullscreen:
            controls_text = "F11: Fullscreen | SPACE: Skip Phase | ESC: Exit"
            control_surf = small_font.render(controls_text, True, (100, 100, 100))
            screen.blit(control_surf, (10, current_height - 30))
        else:
            controls_text = "F11: Window Mode | ESC: Exit"
            control_surf = small_font.render(controls_text, True, (100, 100, 100))
            screen.blit(control_surf, (10, current_height - 30))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()