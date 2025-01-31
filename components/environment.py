import random
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import sin, cos, radians

# Draw all environment
def draw_environment():
    """Draw the entire environment."""
    draw_ground()
    draw_heli_base()
    draw_road()
    draw_volcanoes()
    draw_trees()
    update_lava()
    draw_lava()
    draw_refugee_camp()

# Draw ground
def draw_ground():
    """Draw the ground with green as a base."""
    glColor3f(0.3, 0.7, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(-200, 0, -200)
    glVertex3f(200, 0, -200)
    glVertex3f(200, 0, 200)
    glVertex3f(-200, 0, 200)
    glEnd()

# Draw helicopter base
def draw_heli_base():
    """Drawing the helicopter base with runway and headquarters."""
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(-1.0, -1.0)

    # Helicopter base
    glColor3f(0.5, 0.5, 0.5)  # Grey color
    glBegin(GL_QUADS)
    glVertex3f(-5, 0.01, -5)
    glVertex3f(5, 0.01, -5)
    glVertex3f(5, 0.01, 5)
    glVertex3f(-5, 0.01, 5)
    glEnd()

    glDisable(GL_POLYGON_OFFSET_FILL)

    glColor3f(0.8, 0.8, 0.8)  # Light grey color
    glPushMatrix()
    glTranslatef(-7, 1, -7)
    glScalef(3, 9, 3)
    glutSolidCube(1)
    glPopMatrix()

# Draw road
def draw_road():
    """Drawing the main road from the base to the mountain with an intersection to refugee camp."""
    
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(-1.0, -1.0)

    glColor3f(0.1, 0.1, 0.1)  # Black color for the road
    glBegin(GL_QUADS)

    # Main road from base to mountain (north)
    glVertex3f(-2, 0.01, -5)   
    glVertex3f(2, 0.01, -5)    
    glVertex3f(2, 0.01, -200)  
    glVertex3f(-2, 0.01, -200)

    # Road to the right (east)
    glVertex3f(5, 0.01, -2)   
    glVertex3f(170, 0.01, -2)  
    glVertex3f(170, 0.01, 2)  
    glVertex3f(5, 0.01, 2)

    # Road to the left (west)
    glVertex3f(-200, 0.01, -2)  
    glVertex3f(-5, 0.01, -2)   
    glVertex3f(-5, 0.01, 2)  
    glVertex3f(-200, 0.01, 2)

    # Road to downward (south)
    glVertex3f(-2, 0.01, 200)  
    glVertex3f(2, 0.01, 200)   
    glVertex3f(2, 0.01, -5)   
    glVertex3f(-2, 0.01, -5)

    # First crossing road to refugee camp
    glVertex3f(-200, 0.01, -50)
    glVertex3f(150, 0.01, -50)
    glVertex3f(150, 0.01, -46)
    glVertex3f(-200, 0.01, -46)

    # Second crossing road to refugee camp
    glVertex3f(-200, 0.01, -85)
    glVertex3f(170, 0.01, -85)
    glVertex3f(170, 0.01, -81)
    glVertex3f(-200, 0.01, -81)

    # Road from refugee camp (north)
    glVertex3f(170, 0.01, -60)
    glVertex3f(166, 0.01, -60)
    glVertex3f(166, 0.01, -85)
    glVertex3f(170, 0.01, -85)

    # Road from refugee camp (south)
    glVertex3f(170, 0.01, 0)
    glVertex3f(166, 0.01, 0)
    glVertex3f(166, 0.01, -40)
    glVertex3f(170, 0.01, -40)

    glEnd()
    glDisable(GL_POLYGON_OFFSET_FILL)

    # Draw white line on the road
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_LINE_SMOOTH)
    glLineWidth(2)
    glColor3f(1.0, 1.0, 1.0)
    
    glBegin(GL_LINES)

    # Dotted lines on the main road
    for z in range(-5, -194, -7):
        glVertex3f(0, 0.05, z)    
        glVertex3f(0, 0.05, z - 3)

    # Dotted line on the road to the right (east)
    for x in range(5, 161, 7):  
        glVertex3f(x, 0.02, 0)  
        glVertex3f(x + 3, 0.02, 0)

    # Dotted line on the road to the left (west)
    for x in range(-5, -195, -7):  
        glVertex3f(x, 0.02, 0)  
        glVertex3f(x - 3, 0.02, 0)

    # Dotted line on the road to the downward (south)
    for z in range(5, 194, 7):  
        glVertex3f(0, 0.02, z)  
        glVertex3f(0, 0.02, z + 3)

    # Dotted line on first crossing road to refugee camp
    for x in range(-194, 147, 7):
        glVertex3f(x, 0.05, -48)  
        glVertex3f(x + 3, 0.05, -48)

    # Dotted line on first crossing road to refugee camp
    for x in range(-194, 147, 7):  
        glVertex3f(x, 0.05, -48)  
        glVertex3f(x + 3, 0.05, -48)

    # Dotted line on second crossing road to refugee camp
    for x in range(-194, 168, 7):
        glVertex3f(x, 0.02, -83)  
        glVertex3f(x + 3, 0.02, -83)

    # Dotted line on the road from refugee camp (north)
    for z in range(-60, -81, -5):
        glVertex3f(168, 0.02, z)  
        glVertex3f(168, 0.02, z - 3)

    # Dotted line on the road from refugee camp (south)
    for z in range(0, -40, -7): 
        glVertex3f(168, 0.02, z)
        glVertex3f(168, 0.02, z - 3)

    glEnd()

    glEnable(GL_DEPTH_TEST)

# Draw trees
def draw_trees():
    """Randomly draw trees in specific areas. Avoiding roads, bases and mountain areas."""
    random.seed(42)

    # List of road areas to avoid
    road_areas = [
        {"x_range": (-2, 2), "z_range": (-200, -5)},  # Main road (north)
        {"x_range": (5, 170), "z_range": (-2, 2)},  # Road to the right (east)
        {"x_range": (-200, -5), "z_range": (-2, 2)},  # Road to the left (west)
        {"x_range": (-2, 2), "z_range": (-5, 200)},  # Road to downward (south)
        {"x_range": (-200, 150), "z_range": (-50, -46)},  # First crossing road to refugee camp
        {"x_range": (-200, 170), "z_range": (-85, -81)},  # Second crossing road to refugee camp
        {"x_range": (166, 170), "z_range": (-85, -60)},  # Road from refugee camp (north)
        {"x_range": (166, 170), "z_range": (-40, 0)},  # Road from refugee camp (south)
    ]

    # List of base areas (helipads)
    heli_base_x_range = (-7, 7)  
    heli_base_z_range = (-7, 7)

    # List of mountains
    volcano_positions = [
        (50, -145), (70, -150), (30, -170), (60, -180), (20, -180)
    ]

    mountain_area = 40

    for _ in range(1000):
        x = random.uniform(-190, 190)
        z = random.uniform(-190, 190)

        # Avoid base area
        if heli_base_x_range[0] < x < heli_base_x_range[1] and heli_base_z_range[0] < z < heli_base_z_range[1]:
            continue

        # Avoid road area
        in_road = False
        for road in road_areas:
            if road["x_range"][0] < x < road["x_range"][1] and road["z_range"][0] < z < road["z_range"][1]:
                in_road = True
                break
        if in_road:
            continue

        # Avoid mountain area
        near_volcano = False
        for volcano_x, volcano_z in volcano_positions:
            if ((x - volcano_x) ** 2 + (z - volcano_z) ** 2) ** 0.5 < mountain_area:
                near_volcano = True
                break
        if near_volcano:
            continue

        # Tree trunk
        glColor3f(0.55, 0.27, 0.07)
        glPushMatrix()
        glTranslatef(x, 0, z)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 0.2, 0.2, 2, 10, 10)
        glPopMatrix()

        # Tree leaf
        glColor3f(0, 0.8, 0)
        glPushMatrix()
        glTranslatef(x, 2, z)
        glutSolidSphere(1, 10, 10)
        glPopMatrix()

# List of mountain position
volcano_positions = [
    (50, -145), (70, -150), (30, -170), (60, -180), (20, -180)
]

# Center of circle
center_x = 50
center_z = -160
radius = 30

# Circular mountain position
volcano_positions = [
    (center_x + radius * math.cos(math.radians(72 * i)),  # 360 derajat dibagi 5 gunung (72 derajat tiap gunung)
     center_z + radius * math.sin(math.radians(72 * i)))
    for i in range(5)
]

# List to store eruption particles per mountain
eruption_particles = {i: [] for i in range(len(volcano_positions))}

# Draw volcanoes
def draw_volcanoes():
    """Draw 5 volcanoes with eruption effects."""
    random.seed(42)

    for i, (x, z) in enumerate(volcano_positions):
        height = random.uniform(25, 45)
        base_size = random.uniform(20, 25)

        # Conical mountain
        glColor3f(0.4, 0.2, 0.1)  # Brown color
        glPushMatrix()
        glTranslatef(x, 0, z)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), base_size, 0, height, 30, 30)
        glPopMatrix()

        # Lava Eruption Effects
        glColor3f(1.0, 0.3, 0.0)  # Orange/red color
        for particle in eruption_particles[i]:
            px, py, pz = particle
            glPushMatrix()
            glTranslatef(px, py, pz)
            glutSolidSphere(1, 10, 10)  # Lava particles
            glPopMatrix()

        # Smoke Effect
        glColor3f(0.3, 0.3, 0.3)  # Grey color
        for _ in range(10):  
            glPushMatrix()
            glTranslatef(x + random.uniform(-2, 2), height + 10 + random.uniform(0, 5), z + random.uniform(-2, 2))
            glutSolidSphere(2, 10, 10)
            glPopMatrix()

        # Lava covering the mountain (Color gradation)
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1.0, 0.2, 0.0)
        glVertex3f(x, height, z)

        for angle in range(0, 360, 30):
            rad = radians(angle)
            lx = x + cos(rad) * (base_size * 0.6)
            lz = z + sin(rad) * (base_size * 0.6)
            glColor3f(0.6, 0.1, 0.0)
            glVertex3f(lx, height * 0.5, lz)  # Lava descends to slope
        glEnd()

        # Eruption of smoke & incandescent lava
        for _ in range(10):
            lava_x = x + random.uniform(-2, 2)
            lava_z = z + random.uniform(-2, 2)
            smoke_y = height + random.uniform(5, 15)

            # Smoke
            glColor3f(0.3, 0.3, 0.3)  # Grey color
            glPushMatrix()
            glTranslatef(lava_x + random.uniform(-1, 1), smoke_y + 3, lava_z)
            glutSolidSphere(random.uniform(2, 4), 10, 10)
            glPopMatrix()

# List of particles for lava and smoke
volcano_particles = []

# Position of lava & smoke
def update_volcanoes():
    """Update the position of lava & smoke particles for eruption simulation."""
    new_particles = []
    
    for particle in volcano_particles:
        x, y, z, vx, vy, vz, size, type_, lifetime = particle

        # Update position
        x += vx
        y += vy
        z += vz

        # Gravity effect for lava
        if type_ == "lava":
            vy -= 0.03
            size *= 0.98

        # Smoke effect lighter & rises higher
        elif type_ == "smoke":
            vy += 0.01
            vx *= 0.9
            vz *= 0.9
            size *= 1.02
            lifetime -= 1

        if lifetime > 0 and size > 0.1:
            new_particles.append((x, y, z, vx, vy, vz, size, type_, lifetime))

    for _ in range(5):
        angle = radians(random.randint(0, 360))
        speed = random.uniform(0.5, 2.5)
        vx = cos(angle) * speed
        vy = random.uniform(1.5, 3.5)
        vz = sin(angle) * speed
        x = random.choice([50, 70, 30, 60, 20])
        z = random.choice([-150, -160, -170, -190, -180])
        y = random.uniform(20, 40)

        new_particles.append((x, y, z, vx, vy, vz, random.uniform(0.5, 1.5), "lava", 60))
        new_particles.append((x, y, z, vx * 0.5, vy * 0.5, vz * 0.5, random.uniform(2, 4), "smoke", 80))

    volcano_particles[:] = new_particles

# Mountain position that has lava
lava_mountains = []

# Position of flowing lava
lava_flows = {i: [] for i in lava_mountains}

# Update lava particle position
def update_lava():
    """Update the position of lava particles flowing down the mountain."""
    global lava_flows, volcano_positions

    for i in lava_mountains:
        new_lava = []
        for lava in lava_flows[i]:
            lx, ly, lz, speed = lava
            ly -= speed  # Lava flows down

            # If lava is too low, remove it
            if ly > 5:
                new_lava.append((lx, ly, lz, speed))

        lava_flows[i] = new_lava

        # Add new lava on the mountain peak
        if len(lava_flows[i]) < 40:
            base_x, base_z = volcano_positions[i]
            lava_flows[i].append((
                base_x + random.uniform(-3, 3),  # Spread on slopes
                random.uniform(25, 30),  # Appears from a certain height
                base_z + random.uniform(-3, 3),  # Spread on slopes
                random.uniform(0.1, 0.3)  # Flow speed down
            ))

# Draw lava
def draw_lava():
    """Draw lava particles flowing down the mountain."""
    glColor3f(1.0, 0.4, 0.0)  # Lava color red-orange
    glPointSize(5)

    glBegin(GL_POINTS)
    for i in lava_mountains:
        for lava in lava_flows[i]:
            glVertex3f(lava[0], lava[1], lava[2])
    glEnd()

# Draw refugee camp
def draw_refugee_camp():
    """Drawing an evacuation shelter in a safe area away from the volcano."""
    glEnable(GL_POLYGON_OFFSET_FILL)
    glPolygonOffset(-1.0, -1.0)

    glPushMatrix()
    glTranslatef(170, 0, -50)  # Refugee camp location
    
    # Refugee land
    glColor3f(0.5, 0.3, 0.1)  # Brown color for the ground
    glBegin(GL_QUADS)
    glVertex3f(-20, 0.01, -10)
    glVertex3f(20, 0.01, -10)
    glVertex3f(20, 0.01, 10)
    glVertex3f(-20, 0.01, 10)
    glEnd()

    glDisable(GL_POLYGON_OFFSET_FILL)
    
    # Refugee tents
    draw_tent(-10, 0, -5)
    draw_tent(10, 0, 5)
    draw_tent(-15, 0, 5)
    draw_tent(5, 0, -5)
    draw_tent(-5, 0, 5)
    draw_tent(15, 0, -5)
    
    glPopMatrix()

# Draw tents
def draw_tent(x, y, z):
    """Draw an evacuation tent."""
    glPushMatrix()
    glTranslatef(x, y, z)
    
    glColor3f(0.8, 0.0, 0.0)  # Red color for tent
    glBegin(GL_TRIANGLES)
    glVertex3f(-2, 0, -2)
    glVertex3f(2, 0, -2)
    glVertex3f(0, 3, 0)

    glVertex3f(-2, 0, 2)
    glVertex3f(2, 0, 2)
    glVertex3f(0, 3, 0)
    glEnd()

    glColor3f(0.6, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(-2, 0, -2)
    glVertex3f(-2, 0, 2)
    glVertex3f(0, 3, 0)
    glVertex3f(0, 3, 0)

    glVertex3f(2, 0, -2)
    glVertex3f(2, 0, 2)
    glVertex3f(0, 3, 0)
    glVertex3f(0, 3, 0)
    glEnd()

    glPopMatrix()