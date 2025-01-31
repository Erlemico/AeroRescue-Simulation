from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Color & Scale
COLOR_BODY = (0.4, 0.4, 0.4)  # Grey color for body
COLOR_WINGS = (0.0, 0.0, 0.0)  # Black color for propeller
COLOR_CONNECTOR = (0.5, 0.5, 0.5)  # Color for connector
SIZE_SCALE = 2  # Scale of helicopter size

def draw_helicopter(wingsAngle):
    glPushMatrix()
    glScalef(SIZE_SCALE, SIZE_SCALE, SIZE_SCALE)

    # Initial rotation of helicopter
    glRotatef(90, 1, 0, 0)

    # Initialization quadric
    quadric = gluNewQuadric()

    # Helicopter Body
    glPushMatrix()
    glColor3f(*COLOR_BODY)
    glScalef(1.5, 0.6, 0.6)
    glutSolidSphere(0.15, 30, 30)
    glPopMatrix()

    # Main Propeller Connector
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glRotatef(-180, 1, 0, 0)
    glColor3f(*COLOR_CONNECTOR)
    gluCylinder(quadric, 0.03, 0.03, 0.2, 30, 30)
    glPopMatrix()

    # Back Wings
    for angle in [45, -45]:
        glPushMatrix()
        glTranslatef(-0.65, 0.025 if angle == 45 else -0.025, 0)
        glRotatef(wingsAngle, 0, 1, 0)
        glRotatef(angle, 0, 1, 0)
        glScalef(0.25, 0.02, 0.05)
        glColor3f(*COLOR_CONNECTOR)
        glutSolidCube(1)
        glPopMatrix()

    # Main Propeller
    for angle in [45, -45]:
        glPushMatrix()
        glTranslatef(0, 0, -0.21)
        glRotatef(wingsAngle, 0, 0, -1)
        glRotatef(angle, 0, 0, -1)
        glScalef(1.0, 0.06, 0.02)
        glColor3f(*COLOR_WINGS)
        glutSolidCube(1)
        glPopMatrix()

    # Helicopter Backbone
    glPushMatrix()
    glTranslatef(-0.4, 0, 0)
    glScalef(0.6, 0.03, 0.07)
    glColor3f(*COLOR_BODY)
    glutSolidCube(1)
    glPopMatrix()

    # Helicopter Legs
    for pos in [(-0.25, -0.11, 0.1), (-0.25, 0.11, 0.1)]:
        glPushMatrix()
        glTranslatef(*pos)
        glRotatef(90, 0, 1, 0)
        gluCylinder(quadric, 0.03, 0.03, 0.5, 30, 30)
        glPopMatrix()

    # Connectors Between Body and Legs
    connector_positions = [
        (0.1, 0.1, 0.1, -210),
        (-0.1, 0.1, 0.1, -210),
        (-0.1, -0.1, 0.1, -150),
        (0.1, -0.1, 0.1, -150)
    ]
    for x, y, z, rotation in connector_positions:
        glPushMatrix()
        glTranslatef(x, y, z)
        glRotatef(rotation, 1, 0, 0)
        glColor3f(*COLOR_CONNECTOR)
        gluCylinder(quadric, 0.02, 0.02, 0.15, 30, 30)
        glPopMatrix()

    glPopMatrix()