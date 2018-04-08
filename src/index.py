# IF3260: Computer Graphics
# Texture Mapping - Immediate

# --Libraries and Packages--
import sys
import numpy
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image

# --Camera Settings--
# Camera Angle
angle = 0.0

# Camera Coordinate
x = 0.0
y = 0.0
z = 0.0

# Camera Direction
dx = 0.0
dy = 0.0
dz = 0.0

# --Mouse Settings--
xrot = 0.0
yrot = 0.0
 
xdiff = 0.0
ydiff = 0.0

mouseDown = False

# --CLASSES--
class Camera:
	def __init__(self):
		self.position = (0.0, 0.0, 0.0)
		self.rotation = (0.0, 0.0, 0.0)
		
	def translate(self, dx, dy, dz):
		x, y, z = self.position
		self.position = (x + dx, y + dy, z + dz)
		
	def rotate(self, dx, dy, dz):
		x, y, z = self.rotation
		self.rotation = (x + dx, y + dy, z + dz)
		
	def apply(self):
		glTranslate(*self.position)
		glRotated(self.rotation[0], -1, 0, 0)
		glRotated(self.rotation[1], 0, -1, 0)
		glRotated(self.rotation[2], 0, 0, -1)
		
camera = Camera()

# Key Processing Unit
def processNormalKeys(key, x, y):
	if (key == 27):
		exit(0)

def processSpecialKeys(key, xx, yy):
	global x, z, dX, dZ, angle
	fraction = 0.1
	movespeed = 1
	
	if (key == GLUT_KEY_LEFT):
		camera.translate(movespeed, 0, 0)
	elif (key == GLUT_KEY_RIGHT):
		camera.translate(-movespeed, 0, 0)
	elif (key == GLUT_KEY_UP):
		camera.translate(0, -movespeed, 0)
	elif (key == GLUT_KEY_DOWN):
		camera.translate(0, movespeed, 0)
	elif (key == GLUT_KEY_PAGE_UP):
		camera.translate(0, 0, movespeed)
	elif (key == GLUT_KEY_PAGE_DOWN):
		camera.translate(0, 0, -movespeed)

# Mouse Processing Unit
def mouseMotion(x, y):
	global yrot, xrot, mouseDown
	if (mouseDown):
		yrot = - x + xdiff
		xrot = - y - ydiff
		
def mouse(button, state, x, y):
	global xdiff, ydiff, mouseDown
	if (button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
		mouseDown = True
		xdiff = x + yrot
		ydiff = -y - xrot
	else:
		mouseDown = False

def idle():
	global mouseDown, xrot, yrot
	if (not mouseDown):
		
		if(xrot > 1):
			xrot -= 0.005 * xrot
		elif(xrot < -1):
			xrot += 0.005 * -xrot 
		else:
			xrot = 0

		if(yrot > 1):
			yrot -= 0.005 * yrot
		elif(yrot < -1):
			yrot += 0.005 * -yrot
		else:
			yrot = 0			

# Lighting
def renderLight():
	glEnable(GL_LIGHT0)
	glEnable(GL_LIGHTING)

	glEnable(GL_DEPTH_TEST)
	glDepthFunc(GL_LEQUAL)
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
	
	glShadeModel(GL_SMOOTH)
	
	glEnable(GL_COLOR_MATERIAL)
	glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
	glEnable(GL_TEXTURE_2D)
	
	specReflection = [1.0, 1.0, 1.0, 1.0]
	glMaterialfv(GL_FRONT, GL_SPECULAR, specReflection)
	glMateriali(GL_FRONT, GL_SHININESS, 30)
	glLightfv(GL_LIGHT0, GL_POSITION, [2.0, 2.0, 2.0, 1.0])

def drawCar():
	z = 1.5 
	#back
	glColor3f(206/255, 20/255, 55/255)
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, 1.5, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(-3.0, 1.5, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(-3.0, -1.0, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, -1.0, -z)
	glEnd()

	#top
	glColor3f(240/255, 20/255, 55/255)
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, 1.5, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(-3.0, 1.5, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(0.6, 1.5, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(0.6, 1.5, -z)
	glEnd()

	#bottom
	glColor3f(190/255, 20/255, 55/255)
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(-3.0, -1.0, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(-3.0, -1.0, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(3.0, -1.0, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(3.0, -1.0, -z)
	glEnd()

	#front
	glColor3f(206/255, 20/255, 55/255)
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(3.0, -1.0, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(3.0, 0.15, -z)
	glTexCoord2f(1.0, 1.0); glVertex3f(3.0, 0.15, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(3.0, -1.0, z)
	glEnd()

	#front cover
	glColor3f(230/255, 20/255, 55/255)
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(3.0, 0.15, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(1.2, 0.25, -z)
	glTexCoord2f(1.0, 1.0); glVertex3f(1.2, 0.25, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(3.0, 0.15, z)
	glEnd()

	#front window frame
	glColor3f(235/255, 20/255, 55/255)
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(0.6, 1.5, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(0.6, 1.5, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(0.65, 1.42, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(0.65, 1.42, -z)

	glTexCoord2f(0.0, 0.0); glVertex3f(1.15, 0.34, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(1.15, 0.34, -z+0.1)
	glTexCoord2f(1.0, 1.0); glVertex3f(0.65, 1.42, -z+0.1)
	glTexCoord2f(0.0, 1.0); glVertex3f(0.65, 1.42, -z)

	glTexCoord2f(0.0, 0.0); glVertex3f(1.15, 0.34, z)
	glTexCoord2f(1.0, 0.0); glVertex3f(1.15, 0.34, z-0.1)
	glTexCoord2f(1.0, 1.0); glVertex3f(0.65, 1.42, z-0.1)
	glTexCoord2f(0.0, 1.0); glVertex3f(0.65, 1.42, z)

	glTexCoord2f(0.0, 0.0); glVertex3f(1.15, 0.34, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(1.15, 0.34, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(1.2, 0.25, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(1.2, 0.25, -z)
	glEnd()

	#left back
	glColor3f(206/255, 20/255, 55/255)
	glBegin(GL_POLYGON)
	glTexCoord2f(0.0, 0.0); glVertex3f(0.6, 1.5, -z)
	glVertex3f(1.2, 0.25, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(1.2, -1.0, -z)
	glTexCoord2f(1.0, 1.0); glVertex3f(-3.0, -1.0, -z)
	glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, 1.5, -z)
	glEnd()

	#left front
	glBegin(GL_POLYGON)
	glTexCoord2f(0.0, 0.0); glVertex3f(1.2, 0.25, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(3.0, 0.15, -z)
	glTexCoord2f(1.0, 1.0); glVertex3f(3.0, -1.0, -z)
	glTexCoord2f(0.0, 1.0); glVertex3f(1.2, -1.0, -z)
	glEnd()

	#right back
	glBegin(GL_POLYGON)
	glTexCoord2f(0.0, 0.0); glVertex3f(0.6, 1.5, z)
	glVertex3f(1.2, 0.25, z)
	glTexCoord2f(1.0, 0.0); glVertex3f(1.2, -1.0, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(-3.0, -1.0, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(-3.0, 1.5, z)
	glEnd()

	#right front
	glBegin(GL_POLYGON)
	glTexCoord2f(0.0, 0.0); glVertex3f(1.2, 0.25, z)
	glTexCoord2f(1.0, 0.0); glVertex3f(3.0, 0.15, z)
	glTexCoord2f(1.0, 1.0); glVertex3f(3.0, -1.0, z)
	glTexCoord2f(0.0, 1.0); glVertex3f(1.2, -1.0, z)
	glEnd()

	#front window glass
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_BLEND)
	glColor4f(90/255, 90/255, 90/255, 0.3)
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 0.0); glVertex3f(0.65, 1.42, -z)
	glTexCoord2f(1.0, 0.0); glVertex3f(0.65, 1.42, -z)
	glTexCoord2f(1.0, 1.0); glVertex3f(1.15, 0.34, -z)
	glTexCoord2f(0.0, 1.0); glVertex3f(1.15, 0.34, -z)
	glEnd()
	glDisable(GL_BLEND)
	
# Initialization
def InitGL(Width, Height): 
 
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glClearDepth(1.0) 
	glDepthFunc(GL_LESS)
	glEnable(GL_DEPTH_TEST)
	glShadeModel(GL_SMOOTH)   
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)
 
	# initialize texture mapping
	glEnable(GL_TEXTURE_2D)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
 
def DrawGLScene():
	#global X_AXIS,Y_AXIS,Z_AXIS
	#global DIRECTION
	
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
 
	glLoadIdentity()

	renderLight()
	
	camera.apply()
	camera.rotate(xrot*0.001, 0.0, 0.0)
	camera.rotate(0, yrot*0.001, 0.0)
 
	# glBindTexture(GL_TEXTURE_2D, ID)
	# Draw Car
	drawCar()
	# Draw Cube (multiple quads)
	'''glBegin(GL_QUADS);
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
	glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
	glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0);
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0);
	glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0);
	glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
	glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
	glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0);
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0);
	glTexCoord2f(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0);
	glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
	glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0);
	glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0);
	glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
	glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
	glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0);
	glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0);
	glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0);
	glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0);
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0);
	glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0);
	glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0,  1.0);
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0);
	glEnd();
	idle()
	#X_AXIS = X_AXIS - 0.30
	#Z_AXIS = Z_AXIS - 0.30'''
	idle()
	glutSwapBuffers()
 
 
def loadImage():
	image = Image.open("../img/blue.jpg")
	ix = image.size[0]
	iy = image.size[1]
	data = numpy.array(list(image.getdata()),  dtype=numpy.int64)

	glPixelStorei(GL_UNPACK_ALIGNMENT,1)
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

      
def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
	glutInitWindowSize(640,480)
	glutInitWindowPosition(200,200)

	window = glutCreateWindow(b'OpenGL Python Textured Cube')
 
	glutDisplayFunc(DrawGLScene)
	glutIdleFunc(DrawGLScene)
	glutKeyboardFunc(processNormalKeys)
	glutSpecialFunc(processSpecialKeys)
	
	#Mouse Function
	glutMouseFunc(mouse)
	glutMotionFunc(mouseMotion)
	InitGL(640, 480)
	loadImage()
	glutMainLoop()
 
if __name__ == "__main__":
	main() 