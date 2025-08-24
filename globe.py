import pygame
import math
import time
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random
import os
import subprocess
import sys

# ------------------ Texture helpers ------------------

def read_texture(path):
    """Load an image file as an OpenGL texture. Returns texture id or 0 on failure."""
    try:
        surface = pygame.image.load(path)
        surface = pygame.transform.flip(surface, False, True)  # OpenGL origin fix
        image = pygame.image.tostring(surface, "RGB", True)
        width, height = surface.get_rect().size

        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0,
                     GL_RGB, GL_UNSIGNED_BYTE, image)
        glBindTexture(GL_TEXTURE_2D, 0)
        return tex_id
    except Exception as e:
        print(f"[read_texture] Failed to load '{path}': {e}")
        return 0

def create_earth_texture():
    """Create a procedural Earth-like texture (used as fallback)."""
    size = 256
    texture_data = np.zeros((size, size, 3), dtype=np.uint8)
    for y in range(size):
        for x in range(size):
            u = x / size
            v = y / size
            noise1 = math.sin(u * math.pi * 8) * math.cos(v * math.pi * 6)
            noise2 = math.sin(u * math.pi * 12) * math.sin(v * math.pi * 4)
            noise3 = math.cos(u * math.pi * 16) * math.cos(v * math.pi * 8)
            land_value = (noise1 + noise2 * 0.5 + noise3 * 0.3) / 1.8
            if land_value > 0.1:
                texture_data[y, x] = [
                    34 + int(land_value * 50),
                    102 + int(land_value * 50),
                    34 + int(land_value * 30)
                ]
            else:
                ocean_depth = abs(land_value) * 100
                texture_data[y, x] = [0, 50 + int(ocean_depth), 150 + int(ocean_depth)]

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glBindTexture(GL_TEXTURE_2D, 0)
    return tex_id

def create_galaxy_texture():
    """Create a procedural galaxy background texture."""
    size = 512
    texture_data = np.zeros((size, size, 3), dtype=np.uint8)
    center_x, center_y = size // 2, size // 2
    for y in range(size):
        for x in range(size):
            dx = x - center_x
            dy = y - center_y
            distance = math.sqrt(dx*dx + dy*dy) / (size/2)
            angle = math.atan2(dy, dx)
            spiral = math.sin(angle * 3 + distance * 10) * math.exp(-distance * 1.5)

            random.seed(x * 1000 + y)
            star_chance = random.random()

            if star_chance > 0.998:
                intensity = random.randint(200, 255)
                texture_data[y, x] = [intensity, intensity, intensity]
            elif star_chance > 0.995:
                r = random.randint(150, 255)
                g = random.randint(100, 200)
                b = random.randint(100, 255)
                texture_data[y, x] = [r, g, b]
            else:
                if spiral > 0.1:
                    intensity = int(spiral * 100)
                    texture_data[y, x] = [intensity + 20, intensity//2, intensity + 30]
                else:
                    base = int(distance * 15)
                    texture_data[y, x] = [base, base//2, base + 5]

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glBindTexture(GL_TEXTURE_2D, 0)
    return tex_id

# ------------------ Continent markers ------------------

class ContinentMarker:
    def __init__(self, lat, lon, color, size=0.15, game_file=None, name=None):
        self.lat = lat  # Latitude in degrees
        self.lon = lon  # Longitude in degrees
        self.color = color
        self.size = size
        self.game_file = game_file
        self.name = name
        self.hover = False
        self.selected = False
        
    def get_3d_position(self, radius):
        # Convert latitude and longitude to 3D coordinates
        # Note: In the Earth coordinate system:
        # - Latitude: -90 (South Pole) to 90 (North Pole)
        # - Longitude: -180 to 180, with 0 at Prime Meridian
        phi = math.radians(90 - self.lat)  # Convert to polar angle (0 at North Pole)
        theta = math.radians(self.lon)
        
        x = radius * math.sin(phi) * math.cos(theta)
        y = radius * math.sin(phi) * math.sin(theta)
        z = radius * math.cos(phi)
        
        return (x, y, z)
    
    def draw(self, radius):
        x, y, z = self.get_3d_position(radius)
        
        glPushMatrix()
        glTranslatef(x, y, z)
        
        # Calculate normal vector for proper orientation
        normal = [x/radius, y/radius, z/radius]
        glNormal3f(normal[0], normal[1], normal[2])
        
        # Draw the marker as a small pyramid
        if self.selected:
            glColor3f(1.0, 1.0, 0.0)  # Yellow when selected
            marker_size = self.size * 1.5
        elif self.hover:
            glColor3f(1.0, 0.5, 0.0)  # Orange when hovered
            marker_size = self.size * 1.3
        else:
            glColor3f(*self.color)
            marker_size = self.size
            
        glDisable(GL_LIGHTING)
        
        # Draw a pyramid pointing outward from the Earth's surface
        glBegin(GL_TRIANGLES)
        # Base
        glVertex3f(-marker_size, -marker_size, 0)
        glVertex3f(marker_size, -marker_size, 0)
        glVertex3f(marker_size, marker_size, 0)
        
        glVertex3f(-marker_size, -marker_size, 0)
        glVertex3f(marker_size, marker_size, 0)
        glVertex3f(-marker_size, marker_size, 0)
        
        # Sides
        glVertex3f(-marker_size, -marker_size, 0)
        glVertex3f(marker_size, -marker_size, 0)
        glVertex3f(0, 0, marker_size * 2)
        
        glVertex3f(marker_size, -marker_size, 0)
        glVertex3f(marker_size, marker_size, 0)
        glVertex3f(0, 0, marker_size * 2)
        
        glVertex3f(marker_size, marker_size, 0)
        glVertex3f(-marker_size, marker_size, 0)
        glVertex3f(0, 0, marker_size * 2)
        
        glVertex3f(-marker_size, marker_size, 0)
        glVertex3f(-marker_size, -marker_size, 0)
        glVertex3f(0, 0, marker_size * 2)
        glEnd()
        
        # Add a highlight
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINE_LOOP)
        glVertex3f(-marker_size, -marker_size, 0)
        glVertex3f(marker_size, -marker_size, 0)
        glVertex3f(marker_size, marker_size, 0)
        glVertex3f(-marker_size, marker_size, 0)
        glEnd()
        
        glEnable(GL_LIGHTING)
        glPopMatrix()
    
    def check_click(self, radius, mouse_pos, viewport, modelview, projection):
        # Get the 3D position of the marker
        x, y, z = self.get_3d_position(radius)
        
        # Project the 3D point to 2D screen coordinates
        win_x, win_y, win_z = gluProject(x, y, z, modelview, projection, viewport)
        
        # Calculate distance between mouse and marker in screen space
        dx = mouse_pos[0] - win_x
        dy = (viewport[3] - mouse_pos[1]) - win_y  # Flip y coordinate
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Check if the click is within the marker's radius (converted to screen space)
        return distance < 20  # 20 pixels threshold

# ------------------ Scene helpers ------------------

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glLightfv(GL_LIGHT0, GL_AMBIENT,  (0.1, 0.1, 0.15, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  (1.0, 0.95, 0.8, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.8, 0.8, 0.8, 1.0))
    glLightfv(GL_LIGHT0, GL_POSITION, (10.0, 5.0, 5.0, 1.0))

def draw_atmosphere(radius):
    glPushMatrix()
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthMask(GL_FALSE)
    glColor4f(0.2, 0.4, 0.8, 0.3)
    quad = gluNewQuadric()
    gluSphere(quad, radius * 1.05, 50, 50)
    gluDeleteQuadric(quad)
    glDepthMask(GL_TRUE)
    glDisable(GL_BLEND)
    glColor4f(1, 1, 1, 1)
    glPopMatrix()

def draw_stars(count=1000):
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_LIGHTING)

    random.seed(42)
    normal_stars, red_giants, blue_giants, bright_stars = [], [], [], []

    for _ in range(count):
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, math.pi)
        r = 45
        x = r * math.sin(phi) * math.cos(theta)
        y = r * math.sin(phi) * math.sin(theta)
        z = r * math.cos(phi)
        brightness = random.uniform(0.3, 1.0)
        t = random.random()
        if t > 0.95:
            blue_giants.append((x, y, z, brightness * 0.8, brightness * 0.9, brightness))
        elif t > 0.9:
            red_giants.append((x, y, z, brightness, brightness * 0.6, brightness * 0.4))
        else:
            normal_stars.append((x, y, z, brightness, brightness * 0.95, brightness * 0.8))

    random.seed(123)
    for _ in range(50):
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, math.pi)
        r = 48
        x = r * math.sin(phi) * math.cos(theta)
        y = r * math.sin(phi) * math.sin(theta)
        z = r * math.cos(phi)
        bright_stars.append((x, y, z, 1.0, 1.0, 0.9))

    glPointSize(1.0)
    glBegin(GL_POINTS)
    for x, y, z, r, g, b in normal_stars:
        glColor3f(r, g, b); glVertex3f(x, y, z)
    glEnd()

    glPointSize(1.5)
    glBegin(GL_POINTS)
    for x, y, z, r, g, b in red_giants:
        glColor3f(r, g, b); glVertex3f(x, y, z)
    glEnd()

    glPointSize(2.0)
    glBegin(GL_POINTS)
    for x, y, z, r, g, b in blue_giants:
        glColor3f(r, g, b); glVertex3f(x, y, z)
    glEnd()

    glPointSize(3.0)
    glBegin(GL_POINTS)
    for x, y, z, r, g, b in bright_stars:
        glColor3f(r, g, b); glVertex3f(x, y, z)
    glEnd()

    glPointSize(1.0)
    glEnable(GL_LIGHTING)

def draw_clouds(radius, time_offset):
    glPushMatrix()
    glRotatef(time_offset * 5, 0, 1, 0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthMask(GL_FALSE)
    glColor4f(1, 1, 1, 0.6)

    glBegin(GL_TRIANGLES)
    random.seed(123)
    for _ in range(200):
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, math.pi)
        if random.random() > 0.7:
            cloud_radius = radius * 1.02
            for _ in range(3):
                offset_theta = theta + random.uniform(-0.1, 0.1)
                offset_phi = phi + random.uniform(-0.1, 0.1)
                x = cloud_radius * math.sin(offset_phi) * math.cos(offset_theta)
                y = cloud_radius * math.sin(offset_phi) * math.sin(offset_theta)
                z = cloud_radius * math.cos(offset_phi)
                glVertex3f(x, y, z)
    glEnd()

    glDepthMask(GL_TRUE)
    glDisable(GL_BLEND)
    glColor4f(1, 1, 1, 1)
    glPopMatrix()

def draw_nebula():
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    glDepthMask(GL_FALSE)

    random.seed(456)
    for _ in range(20):
        glPushMatrix()
        theta = random.uniform(0, 2 * math.pi)
        phi = random.uniform(0, math.pi)
        r = random.uniform(35, 40)
        x = r * math.sin(phi) * math.cos(theta)
        y = r * math.sin(phi) * math.sin(theta)
        z = r * math.cos(phi)
        glTranslatef(x, y, z)

        t = random.random()
        if t < 0.33:   glColor4f(0.8, 0.2, 0.8, 0.1)
        elif t < 0.66: glColor4f(0.2, 0.4, 0.9, 0.1)
        else:          glColor4f(0.9, 0.3, 0.5, 0.1)

        size_val = random.uniform(2, 5)
        glBegin(GL_QUADS)
        glVertex3f(-size_val, -size_val, 0)
        glVertex3f( size_val, -size_val, 0) 
        glVertex3f( size_val,  size_val, 0)
        glVertex3f(-size_val,  size_val, 0)
        glEnd()
        glPopMatrix()

    glDepthMask(GL_TRUE)
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)

def draw_background(texture):
    glPushMatrix()
    glColor4f(0.4, 0.4, 0.4, 1.0)
    glBindTexture(GL_TEXTURE_2D, texture)
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)
    gluQuadricOrientation(quad, GLU_INSIDE)
    gluSphere(quad, 40, 100, 100)
    gluDeleteQuadric(quad)
    glBindTexture(GL_TEXTURE_2D, 0)
    glColor4f(1, 1, 1, 1)
    glPopMatrix()

# ------------------ Main ------------------

def main():
    try:
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL | RESIZABLE)
        pygame.display.set_caption('Continental Quest - Realistic Earth with Enhanced Space Background')
        pygame.key.set_repeat(1, 10)
        
        # Initialize pygame mixer and load the sound
        pygame.mixer.init()
        try:
            pygame.mixer.music.load('space_sound.mp3')
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            print("Playing space_sound.mp3 on loop")
        except Exception as e:
            print(f"Could not load or play space_sound.mp3: {e}")

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_NORMALIZE)
        glClearColor(0.0, 0.0, 0.02, 1.0)

        # Projection
        def set_projection(w, h):
            glViewport(0, 0, w, h)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            aspect = w / float(h if h else 1)
            gluPerspective(40, aspect, 0.1, 100.0)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glTranslatef(0.0, 0.0, -6)

        set_projection(*display)

        setup_lighting()

        # Load Earth texture, fallback if missing
        earth_tex = 0
        if os.path.exists('world.jpg'):
            print("Loading Earth texture from world.jpg")
            earth_tex = read_texture('world.jpg')
        if earth_tex == 0:
            print("Falling back to procedural Earth texture")
            earth_tex = create_earth_texture()

        galaxy_tex = create_galaxy_texture()

        qobj = gluNewQuadric()
        gluQuadricTexture(qobj, GL_TRUE)
        gluQuadricNormals(qobj, GLU_SMOOTH)

        earth_material_ambient = [0.2, 0.2, 0.2, 1.0]
        earth_material_diffuse = [0.8, 0.8, 0.8, 1.0]
        earth_material_specular = [0.1, 0.1, 0.1, 1.0]
        earth_material_shininess = [5.0]

        # Create continent markers with more accurate positions
        continent_markers = [
            ContinentMarker(34.0479, 100.6197, (1.0, 0.0, 0.0), 0.15, "asia_game.py", "Asia"),  # Asia (Central)
            ContinentMarker(1.0, 18.0, (0.0, 1.0, 0.0), 0.15, "africa_game.py", "Africa"),  # Africa (Central)
            ContinentMarker(50.0, 10.0, (0.0, 0.0, 1.0), 0.15, "europe_game.py", "Europe"),  # Europe (Central)
            ContinentMarker(45.0, -100.0, (1.0, 0.5, 0.0), 0.15, "northamerica_game.py", "North America"),  # North America (Central)
            ContinentMarker(-20.0, -60.0, (0.5, 0.0, 1.0), 0.15, "southamerica_game.py", "South America"),  # South America (Central)
            ContinentMarker(-25.0, 135.0, (1.0, 0.0, 1.0), 0.15, "australia_game.py", "Australia"),  # Australia (Central)
            ContinentMarker(-82.0, 0.0, (0.0, 1.0, 1.0), 0.15, "antarctica_game.py", "Antarctica")  # Antarctica
        ]

        start_time = time.time()
        lastPosX, lastPosY = 0, 0
        rotating = False

        print("Controls:")
        print("Arrow keys / Left-drag: rotate Earth")
        print("Mouse wheel: zoom")
        print("L: toggle lighting, ESC: quit")
        print("Click on continent markers to launch games")

        running = True
        while running:
            current_time = time.time() - start_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == VIDEORESIZE:
                    set_projection(event.w, event.h)
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_LEFT:
                        glRotatef(2, 0, 1, 0)
                    elif event.key == K_RIGHT:
                        glRotatef(2, 0, -1, 0)
                    elif event.key == K_UP:
                        glRotatef(2, -1, 0, 0)
                    elif event.key == K_DOWN:
                        glRotatef(2, 1, 0, 0)
                    elif event.key == K_l:
                        if glIsEnabled(GL_LIGHTING):
                            glDisable(GL_LIGHTING); print("Lighting disabled")
                        else:
                            glEnable(GL_LIGHTING); print("Lighting enabled")
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        rotating = True
                        
                        # Check if a marker was clicked
                        viewport = glGetIntegerv(GL_VIEWPORT)
                        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
                        projection = glGetDoublev(GL_PROJECTION_MATRIX)
                        
                        for marker in continent_markers:
                            if marker.check_click(2.5, event.pos, viewport, modelview, projection):
                                marker.selected = True
                                print(f"Launching {marker.game_file}...")
                                
                                # Launch the game in a new process
                                try:
                                    # Keep music playing by not terminating the mixer
                                    subprocess.Popen([sys.executable, marker.game_file])
                                except Exception as e:
                                    print(f"Failed to launch {marker.game_file}: {e}")
                            else:
                                marker.selected = False
                    elif event.button == 4:
                        glScaled(1.05, 1.05, 1.05)
                    elif event.button == 5:
                        glScaled(0.95, 0.95, 0.95)
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        rotating = False
                elif event.type == MOUSEMOTION and rotating:
                    x, y = event.pos
                    dx = x - lastPosX
                    dy = y - lastPosY
                    # Simple, stable world-axis rotation (avoids GLfloat usage)
                    glRotatef(dy * 0.3, 1, 0, 0)
                    glRotatef(dx * 0.3, 0, 1, 0)
                    lastPosX, lastPosY = x, y
                    
                    # Check for marker hover
                    viewport = glGetIntegerv(GL_VIEWPORT)
                    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
                    projection = glGetDoublev(GL_PROJECTION_MATRIX)
                    
                    for marker in continent_markers:
                        marker.hover = marker.check_click(2.5, (x, y), viewport, modelview, projection)
                if event.type == MOUSEMOTION and not rotating:
                    lastPosX, lastPosY = event.pos

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glPushMatrix()
            glDisable(GL_LIGHTING)
            glEnable(GL_TEXTURE_2D)
            draw_background(galaxy_tex)
            draw_nebula()
            draw_stars(1200)
            glPopMatrix()
            glEnable(GL_LIGHTING)
            glColor4f(1, 1, 1, 1)

            glMaterialfv(GL_FRONT, GL_AMBIENT,  earth_material_ambient)
            glMaterialfv(GL_FRONT, GL_DIFFUSE,  earth_material_diffuse)
            glMaterialfv(GL_FRONT, GL_SPECULAR, earth_material_specular)
            glMaterialfv(GL_FRONT, GL_SHININESS, earth_material_shininess)

            glDisable(GL_TEXTURE_2D)
            draw_atmosphere(2.5)

            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, earth_tex)
            gluSphere(qobj, 2.5, 100, 100)
            glBindTexture(GL_TEXTURE_2D, 0)

            glDisable(GL_TEXTURE_2D)
            draw_clouds(2.5, current_time)
            
            # Draw continent markers
            for marker in continent_markers:
                marker.draw(2.5)

            pygame.display.flip()
            pygame.time.wait(10)

        pygame.quit()

    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()

if __name__ == '__main__':
    main()