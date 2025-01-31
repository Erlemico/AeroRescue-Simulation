import pygame
import pygame.mixer
import threading
from OpenGL.GL import *
from OpenGL.GLU import *
from components.helicopter import draw_helicopter
from components.environment import draw_environment, update_volcanoes
from components.camera import setup_camera

# Pygame initialization 
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
pygame.display.set_caption("AeroRescue Military-Grade Emergency Response")
clock = pygame.time.Clock()

glEnable(GL_DEPTH_TEST)
glEnable(GL_TEXTURE_2D)  # Enable texture mode

# Load texture
def load_texture(file):
    texture_surface = pygame.image.load(file)
    texture_data = pygame.image.tostring(texture_surface, "RGB", True)
    width, height = texture_surface.get_size()

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return tex_id

# Helicopter texture
helicopter_texture = load_texture("assets/textures/army.jpg")

# Helicopter animation & position
wingsAngle = 0
wingsSpeed = 0  # Propeller initial speed
max_wingsSpeed = 40  # Propeller maximum speed

helicopter_pos = [0, 1, 0]  # Position (x, y, z) | Starting point: 1
helicopter_rot = [0, 0, 0]  # Rotation (yaw, pitch, roll)

# Camera control
camera_mode = "third_person"
camera_angle_x = 0  # Camera horizontal rotation
camera_angle_y = 0  # Camera vertical rotation
mouse_dragging = False
last_mouse_x, last_mouse_y = 0, 0

# Load sound helicopter
start_engine = pygame.mixer.Sound("assets/sounds/start-engine.mp3")
idle_engine = pygame.mixer.Sound("assets/sounds/idle-engine.mp3")
takeoff_engine = pygame.mixer.Sound("assets/sounds/takeoff-engine.mp3")
landing_engine = pygame.mixer.Sound("assets/sounds/landing-engine.mp3")
stop_engine = pygame.mixer.Sound("assets/sounds/stop-engine.mp3")

# Set sound volume
start_engine.set_volume(0.6)
idle_engine.set_volume(0.5)
takeoff_engine.set_volume(0.7)
landing_engine.set_volume(0.7)
stop_engine.set_volume(0.6)

# Dedicated mixer channel
engine_channel = pygame.mixer.Channel(0)  # Start, idle, stop
movement_channel = pygame.mixer.Channel(1)  # Takeoff & landing

# Helicopter engine status
engine_on = False
is_idle_playing = False 
is_takeoff = False
is_landing = False
is_engine_playing = False

# Play sound of start engine
def play_start_engine():
    """Play the engine start sound with a delay before idling."""
    engine_channel.play(start_engine)
    pygame.time.delay(24000)
    if engine_on:
        engine_channel.play(idle_engine, loops=-1)

# Play sound of stop engine
def stop_helicopter_engine():
    """Plays the engine stop sound with a delay before stopping the idle."""
    engine_channel.play(stop_engine)
    pygame.time.delay(15000)
    engine_channel.stop()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Camera control
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                camera_mode = "third_person"
            elif event.key == pygame.K_2:
                camera_mode = "top_view"
            elif event.key == pygame.K_3:
                camera_mode = "side_view"
            
            # Turn the engine on or off with the “O” button
            elif event.key == pygame.K_o:
                if not engine_on:
                    threading.Thread(target=play_start_engine).start()
                else:
                    threading.Thread(target=stop_helicopter_engine).start()
                engine_on = not engine_on

        # Capture the mouse event for camera drag
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_dragging = True
            last_mouse_x, last_mouse_y = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_dragging = False

        elif event.type == pygame.MOUSEMOTION and mouse_dragging:
            dx, dy = event.pos[0] - last_mouse_x, event.pos[1] - last_mouse_y
            camera_angle_x += dx * 0.2  # Horizontal rotation sensitivity
            camera_angle_y += dy * 0.2  # Vertical rotation sensitivity
            last_mouse_x, last_mouse_y = event.pos  # Update last mouse position

    # Change in propeller speed when engine is started/stopped
    if engine_on:
        if wingsSpeed < max_wingsSpeed:
            wingsSpeed += 0.1  # Accelerate the propeller slowly when the engine is on
    else:
        if wingsSpeed > 0:
            wingsSpeed -= 0.1  # Slow down the propeller when the engine is off

    # Can only fly when the propeller reaches full speed
    if wingsSpeed >= max_wingsSpeed:
        keys = pygame.key.get_pressed()

        # Button for takeoff (press Q button)
        if keys[pygame.K_q]:  
            if not is_takeoff:
                movement_channel.play(takeoff_engine, loops=-1)  # Play takeoff sound when button is pressed
                engine_channel.stop()  # Stop idle sound
                is_takeoff = True
            helicopter_pos[1] += 0.1  # Increase flight altitude

        # If the Q button is released, return to idle sound
        if not keys[pygame.K_q] and is_takeoff:
            movement_channel.stop()  # Stop takeoff sound
            engine_channel.play(idle_engine, loops=-1)  # Play idle sound
            is_takeoff = False
        else:  
            if not engine_channel.get_busy():
                idle_engine.set_volume(0.9)
                engine_channel.play(idle_engine, loops=-1)

            # When it's in the air, it can move everywhere
            if keys[pygame.K_w]: helicopter_pos[2] -= 0.1  # Forward movement
            if keys[pygame.K_s]: helicopter_pos[2] += 0.1  # Backward movement
            if keys[pygame.K_a]: helicopter_pos[0] -= 0.1  # Left movement 
            if keys[pygame.K_d]: helicopter_pos[0] += 0.1  # Right movement
            if keys[pygame.K_LEFT]: helicopter_rot[1] += 2  # Left rotation
            if keys[pygame.K_RIGHT]: helicopter_rot[1] -= 2  # Right rotation
            if keys[pygame.K_UP]: helicopter_rot[0] += 2  # Forward rotation
            if keys[pygame.K_DOWN]: helicopter_rot[0] -= 2  # Back rotation

            # Button for landing (press E button)
            elif keys[pygame.K_e] and helicopter_pos[1] > 1:
                if not is_landing:
                    movement_channel.play(landing_engine, loops=-1)  # Play landing sound when button is pressed
                    engine_channel.stop()  # Stop idle sound
                    is_landing = True
                helicopter_pos[1] -= 0.1  # Reduce flight altitude
            
            # If the E button is released, return to idle sound
            if not keys[pygame.K_e] and is_landing:
                movement_channel.stop()  # Stop landing sound
                engine_channel.play(idle_engine, loops=-1)  # Play idle sound
                is_landing = False

            if helicopter_pos[1] == 1:
                idle_engine.set_volume(0.9)

    elif helicopter_pos[1] > 1:
        helicopter_pos[1] -= 0.05  

    glClearColor(0.5, 0.7, 1.0, 1.0)

    update_volcanoes()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    setup_camera(helicopter_pos, helicopter_rot, camera_mode, camera_angle_x, camera_angle_y)

    # Draw environment
    glDisable(GL_TEXTURE_2D)
    draw_environment()
    glEnable(GL_TEXTURE_2D)

    # Draw helicopter
    glPushMatrix()
    glTranslatef(*helicopter_pos)
    glRotatef(90, 0, 1, 0)
    glRotatef(helicopter_rot[0], 1, 0, 0)
    glRotatef(helicopter_rot[1], 0, 1, 0)
    glRotatef(helicopter_rot[2], 0, 0, 1)
    glBindTexture(GL_TEXTURE_2D, helicopter_texture)
    draw_helicopter(wingsAngle)
    glBindTexture(GL_TEXTURE_2D, 0)
    glPopMatrix()

    wingsAngle += wingsSpeed

    pygame.display.flip()
    clock.tick(60)

pygame.quit()