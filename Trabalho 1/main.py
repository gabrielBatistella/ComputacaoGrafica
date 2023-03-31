from random import random
import glfw
from OpenGL.GL import *
import numpy as np
from classesCG import *
from constructsCG import *
import time



################################## Criando os objetos ##################################
objects = []

mill = createMill()
mill.translate(0.85, -1)
objects.append(mill)

axis = createAxis()
translateAxis = mill.getCurrentPositionOfPointInModel(mill.circle) 
axis.translate(translateAxis.x, translateAxis.y)
objects.append(axis)

socket = createSocket()
socket.translate(0.2, -0.2)
objects.append(socket)

pluggedSocket = createPluggedSocket()
pluggedSocket.translate(0.2, -0.2)
pluggedSocket.isVisible = False
objects.append(pluggedSocket)

ground = createGround()
objects.append(ground)

qtdGrass = 160
distanciaGrass = 1.8
grasses = []
while qtdGrass > 0:
    xPosition = 1 - distanciaGrass*random()
    grass = createGrass()
    grass.translate(xPosition, -1+ground.height+grass.height/2)
    grasses.append(grass)
    objects.append(grass)
    qtdGrass -= 1

hero = createHero()
hero.translate(-0.5, 0.5)
objects.append(hero)

wire = createWire()
objects.append(wire)

plug = createPlug()
plug.translate(-0.5, -0.5)
plug.rotate(-90)
objects.append(plug)

mower = createMower()
mower.translate(-0.8, -0.65)
objects.append(mower)
########################################################################################



##################### Preparando janela, shaders e buffer ##############################
glfw.init()
glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
window = glfw.create_window(800, 800, "Trabalho 1", None, None)
glfw.make_context_current(window)

vertex_code = """
        attribute vec2 position;
        uniform mat4 mat;
        void main(){
            gl_Position = mat * vec4(position,0.0,1.0);
        }
        """
fragment_code = """
        uniform vec4 color;
        void main(){
            gl_FragColor = color;
        }
        """

program = glCreateProgram()
vertex = glCreateShader(GL_VERTEX_SHADER)
fragment = glCreateShader(GL_FRAGMENT_SHADER)
glShaderSource(vertex, vertex_code)
glShaderSource(fragment, fragment_code)
glCompileShader(vertex)
if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(vertex).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Vertex Shader")
glCompileShader(fragment)
if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
    error = glGetShaderInfoLog(fragment).decode()
    print(error)
    raise RuntimeError("Erro de compilacao do Fragment Shader")
glAttachShader(program, vertex)
glAttachShader(program, fragment)
glLinkProgram(program)
if not glGetProgramiv(program, GL_LINK_STATUS):
    print(glGetProgramInfoLog(program))
    raise RuntimeError('Linking error')
glUseProgram(program)
########################################################################################



########################### Passando vértices para o buffer ############################
size = 0
for object in objects:
    size += object.getNumVertices()

vertices = np.zeros(size, [("position", np.float32, 2)])
i = 0
for object in objects:
    verticesInObject = object.getAllVertices()
    for vertexInObject in verticesInObject:
        vertices['position'][i] = (vertexInObject.x, vertexInObject.y)
        i = i + 1

index = 0
for object in objects:
    index = object.defineIndexOfVerticesOnBuffer(index)


buffer = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, buffer)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, buffer)
stride = vertices.strides[0]
offset = ctypes.c_void_p(0)
loc = glGetAttribLocation(program, "position")
glEnableVertexAttribArray(loc)
glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)   
########################################################################################



############################# Captando entrada do teclado ##############################
global KEY_W, KEY_S, KEY_A, KEY_D, KEY_ARROWUP, KEY_ARROWDOWN, KEY_ARROWLEFT, KEY_ARROWRIGHT
KEY_W = False
KEY_S = False
KEY_A = False
KEY_D = False
KEY_ARROWUP = False
KEY_ARROWDOWN = False
KEY_ARROWLEFT = False
KEY_ARROWRIGHT = False

def key_event(window, key, scancode, action, mods):
    global KEY_W, KEY_S, KEY_A, KEY_D, KEY_ARROWUP, KEY_ARROWDOWN, KEY_ARROWLEFT, KEY_ARROWRIGHT

    if action == 1:
        if key == 65:
            KEY_A = True
        elif key == 83:
            KEY_S = True
        elif key == 68:
            KEY_D = True
        elif key == 87:
            KEY_W = True
        elif key == 265:
            KEY_ARROWUP = True
        elif key == 264:
            KEY_ARROWDOWN = True
        elif key == 263:
            KEY_ARROWLEFT = True
        elif key == 262:
            KEY_ARROWRIGHT = True
    elif action == 0:
        if key == 65:
            KEY_A = False
        elif key == 83:
            KEY_S = False
        elif key == 68:
            KEY_D = False
        elif key == 87:
            KEY_W = False
        elif key == 265:
            KEY_ARROWUP = False
        elif key == 264:
            KEY_ARROWDOWN = False
        elif key == 263:
            KEY_ARROWLEFT = False
        elif key == 262:
            KEY_ARROWRIGHT = False
########################################################################################



###################### Checa colisões e movimentação por teclado #######################
global plugHoldingPointInModel, plugConnectingPointInModel, plugWiringPointInModel, hasPickedPlug, isPlugInSocket
plugHoldingPointInModel = Vertex2f(0.0, -0.075)
plugConnectingPointInModel = Vertex2f(0.0, 0.06)
plugWiringPointInModel = Vertex2f(0.0, -0.08)
hasPickedPlug = False
isPlugInSocket = False

def update(deltaTime):
    global plugHoldingPointInModel, hasPickedPlug, isPlugInSocket

    rotateMill(deltaTime)
    stretchWire()
    checkInputForHeroMovement(deltaTime)
    if(not hasPickedPlug):
        checkIfHeroPickedPlug()
    if((hasPickedPlug) and (not isPlugInSocket)):
        plug.position = hero.getCurrentPositionOfPointInModel(plugHoldingPointInModel)
        checkInputForPlugTransformation(deltaTime)
        checkIfPlugEnteredSocket()
    if(isPlugInSocket):
        moveMower(deltaTime)
        checkGrassBeingCut()
        updateGrass(deltaTime)

def updateGrass(deltaTime):
    for grass in grassAnimation:
        if(grass.update(deltaTime) == False):
            grassAnimation.remove(grass)

def moveMower(deltaTime):
    speed = 0.7
    displacement = speed*deltaTime
    newX = mower.position.x + displacement
    if( newX <= 1.3):
        mower.translate(displacement, 0)

grassAnimation = []
def checkGrassBeingCut():
    mowerPosition = mower.position.x
    for grass in grasses:
        grassPositon = grass.position.x
        if(grassPositon <= mowerPosition):
            grasses.remove(grass)
            grass.cutGrass(mower.position)
            grassAnimation.append(grass)

def rotateMill(deltaTime):
    speedRotation = 30
    displacementAngle = speedRotation*deltaTime
    axis.rotate(displacementAngle)

def stretchWire():
    global plugWiringPointInModel

    wire.position = mower.position
    scaleX = plug.getCurrentPositionOfPointInModel(plugWiringPointInModel).x - wire.position.x
    scaleY = plug.getCurrentPositionOfPointInModel(plugWiringPointInModel).y - wire.position.y
    wire.size = Vector2f(scaleX, scaleY)

def distanceBetweenPoints(point1, point2):
    return np.sqrt(np.power(point1.x - point2.x, 2) + np.power(point1.y - point2.y, 2))

def checkIfHeroPickedPlug():
    global plugHoldingPointInModel, hasPickedPlug
    range = 0.1

    centerPosition = hero.getCurrentPositionOfPointInModel(plugHoldingPointInModel)
    plugPosition = plug.position
    if(distanceBetweenPoints(centerPosition, plugPosition) < range):
        hasPickedPlug = True

def doesPlugFitSocket():
    angleFits = (plug.angle < 5 and plug.angle > -5) or (plug.angle < 185 and plug.angle > 175)
    sizeFits = (plug.size.x < 2.5 and plug.size.x > 2.0)
    return angleFits and sizeFits

def checkIfPlugEnteredSocket():
    global plugConnectingPointInModel, isPlugInSocket
    range = 0.06*plug.size.x
    
    centerPosition = plug.getCurrentPositionOfPointInModel(plugConnectingPointInModel)
    socketPosition = socket.position
    if(distanceBetweenPoints(centerPosition, socketPosition) < range):
        if(doesPlugFitSocket()):
            isPlugInSocket = True
            plug.angle = 0
            plug.size = Vector2f(2.24, 2.24)
            plug.position = Vector2f(0.2, -0.265)
            plug.isVisible = False
            socket.isVisible = False
            pluggedSocket.isVisible = True
        
def checkInputForHeroMovement(deltaTime):
    global KEY_W, KEY_S, KEY_A, KEY_D

    speed = 1
    displacement = speed * deltaTime
    direction = Vector2f(0, 0)
    if KEY_W:
        direction.y = 1
    if KEY_S:
        direction.y = -1
    if KEY_A:
        direction.x = -1
    if KEY_D:
        direction.x = 1
    direction.normalize()

    dx = displacement*direction.x
    dy = displacement*direction.y

    newX = hero.position.x + dx
    newY = hero.position.y + dy

    if((newX >= -1 and newX <= 1) and (newY >= -1 and newY <= 1)):
        hero.translate(direction.x*displacement, direction.y*displacement)

def checkInputForPlugTransformation(deltaTime):
    global KEY_ARROWUP, KEY_ARROWDOWN, KEY_ARROWLEFT, KEY_ARROWRIGHT

    speedScale = 0.5
    speedRotation = 90
    displacementScale = speedScale*deltaTime
    displacementAngle = speedRotation*deltaTime
    if KEY_ARROWLEFT:
        plug.rotate(displacementAngle)
    if KEY_ARROWRIGHT:
        plug.rotate(-displacementAngle)
    if KEY_ARROWUP:
        newScale = plug.size.x + displacementScale
        if(newScale <= 3.5):
            plug.scale(displacementScale, displacementScale)
    if KEY_ARROWDOWN:
        newScale = plug.size.x - displacementScale
        if(newScale >= 0.5):
            plug.scale(-displacementScale, -displacementScale)
########################################################################################



################################## Loop principal ######################################
glfw.set_key_callback(window, key_event)
glfw.show_window(window)

glLineWidth(2.0)

global now, newNow, timer, frames
frames = 0
now = newNow = timer = time.time_ns()

def gameloop():
    global now, newNow, timer, frames
    now = time.time_ns()
    deltaTimeInSeconds = (now - newNow) / 1000000000.0
    if(deltaTimeInSeconds < 0):
        deltaTimeInSeconds = 0

    glfw.poll_events()
    update(deltaTimeInSeconds)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0.5, 0.8, 1.0, 1.0)

    for object in objects:
        object.drawObject(program)

    glfw.swap_buffers(window)

    frames += 1

    newNow = now
    timeAtual = time.time_ns()
    if(timeAtual - timer >= 1000000000): 
        timer += 1000000000
        FPS_ATUAL = frames
        print(FPS_ATUAL)
        frames = 0

while not glfw.window_should_close(window):
    gameloop()

glfw.terminate()
########################################################################################