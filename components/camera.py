import math
from OpenGL.GL import *
from OpenGL.GLU import *

def setup_camera(helicopter_pos, helicopter_rot, camera_mode="third_person",
                  camera_angle_x=0, camera_angle_y=0, camera_distance=5):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800/600, 0.1, 100)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Limit vertical rotation to avoid upside down
    camera_angle_y = max(-60, min(60, camera_angle_y))

    adjusted_yaw = math.radians(helicopter_rot[1] - 90)  # camera rotation is on the back

    # Determine the camera position based on the selected mode
    if camera_mode == "third_person":
        camera_offset = [
            camera_distance * math.cos(adjusted_yaw),
            3,                                       
            camera_distance * math.sin(adjusted_yaw)
        ]
    elif camera_mode == "top_view":
        camera_offset = [0, camera_distance + 5, 0]  # Top view camera
    elif camera_mode == "side_view":
        camera_offset = [camera_distance, 3, 0]  # Side view camera
    else:
        camera_offset = [-5, 3, 5]  # Default to third person

    # Calculate the position of camera to be behind the helicopter
    camera_x = helicopter_pos[0] - camera_offset[0]
    camera_y = helicopter_pos[1] + camera_offset[1]
    camera_z = helicopter_pos[2] - camera_offset[2]

    # Use rotation based on mouse drag only if `third_person` mode
    if camera_mode == "third_person":
        glRotatef(camera_angle_y, 1, 0, 0)  # Vertical rotation (up-down)
        glRotatef(camera_angle_x, 0, 1, 0)  # Horizontal rotation (left-right)

    # Point the camera to helicopter
    gluLookAt(camera_x, camera_y, camera_z, 
              helicopter_pos[0], helicopter_pos[1], helicopter_pos[2], 
              0, 1, 0)