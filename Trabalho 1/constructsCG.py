import math
from shutil import move
from OpenGL.GL import *
from classesCG import *



########################### Função que cria o objeto herói #############################
def createHero():
    deltaCape = 0.03
    deltaY = 0.025
    bodyWidth = 0.15
    bodyHeight = 0.15
    headRadius = 0.05
    xC = 0
    yC = headRadius
    numVertices = 20



    hero = Object()

    cape = Shape()
    cape.drawFunction = GL_TRIANGLE_STRIP
    cape.color = (0.9, 0.9, 0.9, 1.0)

    capeStroke = Shape()
    capeStroke.drawFunction = GL_LINE_LOOP
    capeStroke.color = (0.0, 0.0, 0.0, 0.0)

    body = Shape()
    body.drawFunction = GL_TRIANGLES
    body.color = (0.9, 0.9, 0.0, 1.0)

    bodyStroke = Shape()
    bodyStroke.drawFunction = GL_LINE_LOOP
    bodyStroke.color = (0.0, 0.0, 0.0, 1.0)

    head = Shape()
    head.drawFunction = GL_TRIANGLE_FAN
    head.color = (0.9882, 0.8333, 0.7118, 1.0)

    headStroke = Shape()
    headStroke.drawFunction = GL_LINE_LOOP
    headStroke.color = (0.0, 0.0, 0.0, 1.0)



    leftShoulder = Vertex2f(-bodyWidth/2,deltaY)
    rightShoulder = Vertex2f(bodyWidth/2,deltaY)
    capeLeftDownVertex = Vertex2f(-bodyWidth/2-deltaCape, -bodyHeight)
    capeRightDownVertex = Vertex2f(bodyWidth/2+deltaCape, -bodyHeight)
    foot = Vertex2f(0, deltaY-bodyHeight) 



    cape.addVertex(leftShoulder)
    cape.addVertex(rightShoulder)
    cape.addVertex(capeLeftDownVertex)
    cape.addVertex(capeRightDownVertex)
    
    capeStroke.addVertex(leftShoulder)
    capeStroke.addVertex(rightShoulder)
    capeStroke.addVertex(capeRightDownVertex)
    capeStroke.addVertex(capeLeftDownVertex)

    body.addVertex(foot)
    body.addVertex(leftShoulder)
    body.addVertex(rightShoulder)

    bodyStroke.addVertex(foot)
    bodyStroke.addVertex(leftShoulder)
    bodyStroke.addVertex(rightShoulder)



    theta = 0
    dTheta = 2*math.pi/numVertices
    while theta < 2*math.pi:
        x = xC+headRadius*math.cos(theta)
        y = yC+headRadius*math.sin(theta)
        vertex = Vertex2f(x, y)
        head.addVertex(vertex)
        headStroke.addVertex(vertex)
        theta += dTheta



    hero.addShape(cape)
    hero.addShape(capeStroke)
    hero.addShape(body)
    hero.addShape(bodyStroke)
    hero.addShape(head)
    hero.addShape(headStroke)    

    return hero
########################################################################################





############################ Função que cria o objeto plug #############################
def createPlug():
    boxWidth = 0.12
    boxHeight = 0.1
    deltaY = 0.02
    pinWidth = 0.02
    pinHeight = 0.07
    deltaPin = 0.02
    cordWidth = 0.03
    cordHeight = 0.05
    deltaCord = 0.005    



    plug = Object()
    
    box = Shape()
    box.drawFunction = GL_TRIANGLE_STRIP
    box.color = (0.0, 0.0, 0.0, 1.0)

    leftPin = Shape()
    leftPin.drawFunction = GL_TRIANGLE_STRIP
    leftPin.color = (0.5, 0.5, 0.5, 1.0)

    rightPin = Shape()
    rightPin.drawFunction = GL_TRIANGLE_STRIP
    rightPin.color = (0.5, 0.5, 0.5, 1.0)

    cord = Shape()
    cord.drawFunction = GL_TRIANGLE_STRIP
    cord.color = (0.0, 0.0, 0.0, 1.0)



    boxcableTopLeft = Vertex2f(-boxWidth/2, boxHeight/2+deltaY)
    boxcableTopRight = Vertex2f(boxWidth/2, boxHeight/2+deltaY)
    boxDownLeft = Vertex2f(-boxWidth/2, -boxHeight/2+deltaY)
    boxDownRight = Vertex2f(boxWidth/2, -boxHeight/2+deltaY)

    leftPincableTopLeft = Vertex2f(-deltaPin-pinWidth, boxHeight/2+deltaY+pinHeight)
    leftPincableTopRight = Vertex2f(-deltaPin, boxHeight/2+deltaY+pinHeight)
    leftPinDownLeft = Vertex2f(-deltaPin-pinWidth, boxHeight/2+deltaY)
    leftPinDownRight = Vertex2f(-deltaPin, boxHeight/2+deltaY)

    rightPincableTopLeft = Vertex2f(deltaPin, boxHeight/2+deltaY+pinHeight)
    rightPincableTopRight = Vertex2f(deltaPin+pinWidth, boxHeight/2+deltaY+pinHeight)
    rightPinDownLeft = Vertex2f(deltaPin, boxHeight/2+deltaY)
    rightPinDownRight = Vertex2f(deltaPin+pinWidth, boxHeight/2+deltaY)

    cordcableTopLeft = Vertex2f(-cordWidth/2, -boxHeight/2+deltaY)
    cordcableTopRight = Vertex2f(cordWidth/2, -boxHeight/2+deltaY)
    cordDownLeft = Vertex2f(-cordWidth/2+deltaCord, -boxHeight/2+deltaY-cordHeight)
    cordDownRight = Vertex2f(cordWidth/2-deltaCord, -boxHeight/2+deltaY-cordHeight)



    box.addVertex(boxcableTopLeft)
    box.addVertex(boxcableTopRight)
    box.addVertex(boxDownLeft)
    box.addVertex(boxDownRight)

    leftPin.addVertex(leftPincableTopLeft)
    leftPin.addVertex(leftPincableTopRight)
    leftPin.addVertex(leftPinDownLeft)
    leftPin.addVertex(leftPinDownRight)

    rightPin.addVertex(rightPincableTopLeft)
    rightPin.addVertex(rightPincableTopRight)
    rightPin.addVertex(rightPinDownLeft)
    rightPin.addVertex(rightPinDownRight)

    cord.addVertex(cordcableTopLeft)
    cord.addVertex(cordcableTopRight)
    cord.addVertex(cordDownLeft)
    cord.addVertex(cordDownRight)



    plug.addShape(box)
    plug.addShape(leftPin)
    plug.addShape(rightPin)
    plug.addShape(cord)

    return plug
########################################################################################





########################### Função que cria o objeto tomada ############################
def createSocket():
    wallWidth = 0.56
    wallHeight = 0.84
    holeWidth = 0.06
    holeHeight = 0.18
    deltaHole = 0.03
    circleRadius = 0.18
    numVertices = 20



    socket = Object()

    wall = Shape()
    wall.drawFunction = GL_TRIANGLE_STRIP
    wall.color = (0.95, 0.95, 0.85, 1.0)

    leftHole = Shape()
    leftHole.drawFunction = GL_TRIANGLE_STRIP
    leftHole.color = (0.0, 0.0, 0.0, 1.0)

    rightHole = Shape()
    rightHole.drawFunction = GL_TRIANGLE_STRIP
    rightHole.color = (0.0, 0.0, 0.0, 1.0)

    circle = Shape()
    circle.drawFunction = GL_TRIANGLE_FAN
    circle.color = (1.0, 1.0, 1.0, 1.0)

    circleStroke = Shape()
    circleStroke.drawFunction = GL_LINE_LOOP
    circleStroke.color = (0.0, 0.0, 0.0, 1.0) 



    wallcableTopLeft = Vertex2f(-wallWidth/2, wallHeight/2)
    wallcableTopRight = Vertex2f(wallWidth/2, wallHeight/2)
    wallDownLeft = Vertex2f(-wallWidth/2, -wallHeight/2)
    wallDownRight = Vertex2f(wallWidth/2, -wallHeight/2)

    leftHolecableTopLeft = Vertex2f(-deltaHole-holeWidth, holeHeight/2)
    leftHolecableTopRight = Vertex2f(-deltaHole, holeHeight/2)
    leftHoleDownLeft = Vertex2f(-deltaHole-holeWidth, -holeHeight/2)
    leftHoleDownRight = Vertex2f(-deltaHole, -holeHeight/2)

    rightHolecableTopLeft = Vertex2f(deltaHole, holeHeight/2)
    rightHolecableTopRight = Vertex2f(deltaHole+holeWidth, holeHeight/2)
    rightHoleDownLeft = Vertex2f(deltaHole, -holeHeight/2)
    rightHoleDownRight = Vertex2f(deltaHole+holeWidth, -holeHeight/2)



    wall.addVertex(wallcableTopLeft)
    wall.addVertex(wallcableTopRight)
    wall.addVertex(wallDownLeft)
    wall.addVertex(wallDownRight)

    leftHole.addVertex(leftHolecableTopLeft)
    leftHole.addVertex(leftHolecableTopRight)
    leftHole.addVertex(leftHoleDownLeft)
    leftHole.addVertex(leftHoleDownRight)

    rightHole.addVertex(rightHolecableTopLeft)
    rightHole.addVertex(rightHolecableTopRight)
    rightHole.addVertex(rightHoleDownLeft)
    rightHole.addVertex(rightHoleDownRight)



    theta = 0
    dTheta = 2*math.pi/numVertices
    while theta < 2*math.pi:
        x = circleRadius*math.cos(theta)
        y = circleRadius*math.sin(theta)
        vertex = Vertex2f(x, y)
        circle.addVertex(vertex)
        circleStroke.addVertex(vertex)
        theta += dTheta
    


    socket.addShape(wall)
    socket.addShape(circle)
    socket.addShape(circleStroke)
    socket.addShape(leftHole)
    socket.addShape(rightHole)

    return socket
########################################################################################





###################### Função que cria o objeto tomada com plug ########################
def createPluggedSocket():
    correctPlugScale = 2.24
    wallWidth = 0.56
    wallHeight = 0.84
    circleRadius = 0.18
    numVertices = 20
    boxWidth = 0.12*correctPlugScale
    boxHeight = 0.1*correctPlugScale
    deltaY = -0.045
    cordWidth = 0.03*correctPlugScale
    cordHeight = 0.05*correctPlugScale
    deltaCord = 0.005*correctPlugScale



    pluggedSocket = Object()

    wall = Shape()
    wall.drawFunction = GL_TRIANGLE_STRIP
    wall.color = (0.95, 0.95, 0.85, 1.0)

    circle = Shape()
    circle.drawFunction = GL_TRIANGLE_FAN
    circle.color = (1.0, 1.0, 1.0, 1.0)

    circleStroke = Shape()
    circleStroke.drawFunction = GL_LINE_LOOP
    circleStroke.color = (0.0, 0.0, 0.0, 1.0) 

    box = Shape()
    box.drawFunction = GL_TRIANGLE_STRIP
    box.color = (0.0, 0.0, 0.0, 1.0)

    cord = Shape()
    cord.drawFunction = GL_TRIANGLE_STRIP
    cord.color = (0.0, 0.0, 0.0, 1.0)



    wallcableTopLeft = Vertex2f(-wallWidth/2, wallHeight/2)
    wallcableTopRight = Vertex2f(wallWidth/2, wallHeight/2)
    wallDownLeft = Vertex2f(-wallWidth/2, -wallHeight/2)
    wallDownRight = Vertex2f(wallWidth/2, -wallHeight/2)

    boxcableTopLeft = Vertex2f(-boxWidth/2, boxHeight/2+deltaY)
    boxcableTopRight = Vertex2f(boxWidth/2, boxHeight/2+deltaY)
    boxDownLeft = Vertex2f(-boxWidth/2, -boxHeight/2+deltaY)
    boxDownRight = Vertex2f(boxWidth/2, -boxHeight/2+deltaY)

    cordcableTopLeft = Vertex2f(-cordWidth/2, -boxHeight/2+deltaY)
    cordcableTopRight = Vertex2f(cordWidth/2, -boxHeight/2+deltaY)
    cordDownLeft = Vertex2f(-cordWidth/2+deltaCord, -boxHeight/2+deltaY-cordHeight)
    cordDownRight = Vertex2f(cordWidth/2-deltaCord, -boxHeight/2+deltaY-cordHeight)



    wall.addVertex(wallcableTopLeft)
    wall.addVertex(wallcableTopRight)
    wall.addVertex(wallDownLeft)
    wall.addVertex(wallDownRight)

    box.addVertex(boxcableTopLeft)
    box.addVertex(boxcableTopRight)
    box.addVertex(boxDownLeft)
    box.addVertex(boxDownRight)

    cord.addVertex(cordcableTopLeft)
    cord.addVertex(cordcableTopRight)
    cord.addVertex(cordDownLeft)
    cord.addVertex(cordDownRight)



    theta = 0
    dTheta = 2*math.pi/numVertices
    while theta < 2*math.pi:
        x = circleRadius*math.cos(theta)
        y = circleRadius*math.sin(theta)
        vertex = Vertex2f(x, y)
        circle.addVertex(vertex)
        circleStroke.addVertex(vertex)
        theta += dTheta
    


    pluggedSocket.addShape(wall)
    pluggedSocket.addShape(circle)
    pluggedSocket.addShape(circleStroke)
    pluggedSocket.addShape(box)
    pluggedSocket.addShape(cord)
    

    return pluggedSocket
########################################################################################





########################## Função que cria o objeto moinho #############################
def createMill():

    color = (0.6, 0.0, 0.0, 1.0)

    distBase = 0.7
    distMid = 0.35
    distTop = 0.2
    alturaMid = 0.6
    alturaMidTop = 0.9

    mill = Object()

    baseleft = Vertex2f(-distBase/2, 0)
    baseright = Vertex2f(distBase/2, 0)
    midLeft = Vertex2f(-distMid/2, alturaMid)
    midRight = Vertex2f(distMid/2, alturaMid)
    cableTopLeft = Vertex2f(-distTop/2, alturaMid+alturaMidTop)
    cableTopRight = Vertex2f(distTop/2, alturaMid+alturaMidTop)

    bodyDown = Shape()
    bodyDown.drawFunction = GL_TRIANGLE_STRIP
    bodyDown.color = color

    bodyDown.addVertex(baseright)
    bodyDown.addVertex(baseleft)
    bodyDown.addVertex(midRight)
    bodyDown.addVertex(midLeft)
    bodyDown.addVertex(cableTopRight)
    bodyDown.addVertex(cableTopLeft)

    mill.addShape(bodyDown)

    cicle = Shape()
    cicle.color = color
    cicle.drawFunction = GL_TRIANGLE_FAN

    numVertices = 20
    radius = distTop/2
    xC = 0
    yC = alturaMid+alturaMidTop

    theta = 0
    dTheta = 2*math.pi/numVertices
    while theta < 2*math.pi:
        x = xC+radius*math.cos(theta)
        y = yC+radius*math.sin(theta)
        vertex = Vertex2f(x, y)
        cicle.addVertex(vertex)
        theta += dTheta

    mill.addShape(cicle)
    mill.circle = Vertex2f(xC, yC)
    return mill
########################################################################################



def rotate(vector, theta):
    x = vector.x*math.cos(theta)-vector.y*math.sin(theta)
    y = vector.x*math.sin(theta)+vector.y*math.cos(theta)
    return Vector2f(x, y)




####################### Função que cria o objeto pás do moinho #########################
def createAxis():

    color = (0.6, 0.4, 0.8, 1.0)

    axis = Object()
    distX = 0.5
    altura1 = 0.8
    altura2 = 0.1

    center = Vertex2f(0,0)
    vertex1 = Vertex2f(distX/2, altura1)
    vertex2 = Vertex2f(-distX/2, altura1+altura2)

    shape = Shape()
    shape.color = color
    shape.drawFunction = GL_TRIANGLES

    shape.addVertex(center)
    shape.addVertex(vertex1)
    shape.addVertex(vertex2) 

    shape2 = Shape()
    shape2.color = color
    shape2.drawFunction = GL_TRIANGLES

    vertex1 = rotate(vertex1,math.pi/2)
    vertex2 = rotate(vertex2,math.pi/2)

    shape2.addVertex(center)
    shape2.addVertex(vertex1)
    shape2.addVertex(vertex2) 

    shape3 = Shape()
    shape3.color = color
    shape3.drawFunction = GL_TRIANGLES

    vertex1 = rotate(vertex1,math.pi/2)
    vertex2 = rotate(vertex2,math.pi/2)

    shape3.addVertex(center)
    shape3.addVertex(vertex1)
    shape3.addVertex(vertex2) 

    shape4 = Shape()
    shape4.color = color
    shape4.drawFunction = GL_TRIANGLES

    vertex1 = rotate(vertex1,math.pi/2)
    vertex2 = rotate(vertex2,math.pi/2)

    shape4.addVertex(center)
    shape4.addVertex(vertex1)
    shape4.addVertex(vertex2) 

    axis.addShape(shape)
    axis.addShape(shape2)
    axis.addShape(shape3)
    axis.addShape(shape4)
    
    return axis
########################################################################################





######################## Função que cria o objeto chão/grama ###########################
def createGround():

    height = 0.25
    deltaGrama = 0.05
    grassColor = (0.3, 0.6, 0.4, 1.0)

    ground = Object()
    baseLeft = Vertex2f(-1,-1)
    baseRight = Vertex2f(1,-1)
    cableTopLeft = Vertex2f(-1,-1+height)
    cableTopRight = Vertex2f(1,-1+height)
    grassleft = Vertex2f(-1, -1+height-deltaGrama)
    grassright = Vertex2f(1, -1+height-deltaGrama)

    groundFloor = Shape()
    groundFloor.color = (0.5882, 0.2941, 0.0, 1.0)
    groundFloor.drawFunction = GL_TRIANGLE_STRIP

    groundFloor.addVertex(baseLeft)
    groundFloor.addVertex(baseRight)
    groundFloor.addVertex(cableTopLeft)
    groundFloor.addVertex(cableTopRight)

    groundFloorStroke = Shape()
    groundFloorStroke.color = (0.0, 0.0, 0.0, 1.0)
    groundFloorStroke.drawFunction = GL_LINE_LOOP

    groundFloorStroke.addVertex(baseLeft)
    groundFloorStroke.addVertex(baseRight)
    groundFloorStroke.addVertex(cableTopRight)
    groundFloorStroke.addVertex(cableTopLeft)

    ground.addShape(groundFloor)
    ground.addShape(groundFloorStroke)

    groundGrassRect = Shape()
    groundGrassRect.drawFunction = GL_TRIANGLE_STRIP
    groundGrassRect.color = grassColor

    groundGrassRect.addVertex(grassleft)
    groundGrassRect.addVertex(grassright)
    groundGrassRect.addVertex(cableTopLeft)
    groundGrassRect.addVertex(cableTopRight)

    ground.addShape(groundGrassRect)    
    
    yC = -1+height-deltaGrama
    diametro = 2.0/15
    raio = diametro/2
    xC = raio-1

    while xC <= 1:
        aux = Shape()
        aux.color = grassColor
        aux.drawFunction = GL_TRIANGLE_FAN

        deltaTheta= math.pi/5
        theta = math.pi
        while theta <= 2*math.pi:
            x = xC + raio*math.cos(theta)
            y = yC + raio*math.sin(theta)
            v = Vertex2f(x, y)
            aux.addVertex(v)
            theta += deltaTheta
        xC += 2*raio
        ground.addShape(aux)

    ground.height = height

    return ground
########################################################################################





########################### Função que cria o objeto grama #############################
def createGrass():
    height = 0.05*random()+0.10
    distBase = 0.02
    color = (0.3, 0.6, 0.4, 1.0)

    baseLeft = Vertex2f(-distBase/2, -height/2)
    baseRight = Vertex2f(distBase/2, -height/2)
    top = Vertex2f(0, height/2)

    shape = Shape()
    shape.drawFunction = GL_TRIANGLE_STRIP
    shape.color = color

    shape.addVertex(baseLeft)
    shape.addVertex(baseRight)
    shape.addVertex(top)

    grass = grassCutted()
    grass.addShape(shape)

    grass.height = height
    return grass
########################################################################################





##################### Função que cria o objeto cortador de grama #######################
def createMower():
    mower = Object()

    sizeBase = 0.4
    heightBase = 0.22
    raioWheel = 0.08

    deltaYWheel = -0.09
    xWheelBehind = -sizeBase/2+raioWheel/2
    yWheelBehind = deltaYWheel
    
    xWheel = sizeBase/2-raioWheel/2
    yWheel = yWheelBehind

    baseLeft = Vertex2f(-sizeBase/2, -heightBase/2)
    baseRight = Vertex2f(sizeBase/2, -heightBase/2)
    basecableTopLeft = Vertex2f(-sizeBase/2, heightBase/2)
    basecableTopRight = Vertex2f(sizeBase/2, heightBase/2)
        
    baseRect = Shape()
    baseRect.drawFunction = GL_TRIANGLE_STRIP
    baseRect.color = (1.0, 0.0, 0.0, 1.0)

    baseRect.addVertex(baseLeft)
    baseRect.addVertex(baseRight)
    baseRect.addVertex(basecableTopLeft)
    baseRect.addVertex(basecableTopRight)

    mower.addShape(baseRect)

    wheelBehind = Shape()
    wheelBehind.drawFunction = GL_TRIANGLE_FAN
    wheelBehind.color = (0.0, 0.0, 0.0, 1.0)
    
    dTheta = 2*math.pi/20
    theta = 0
    while theta < 2*math.pi:
        x = xWheelBehind + raioWheel*math.cos(theta)
        y = yWheelBehind + raioWheel*math.sin(theta)
        aux = Vertex2f(x, y)
        wheelBehind.addVertex(aux)
        theta += dTheta

    mower.addShape(wheelBehind)

    wheel = Shape()
    wheel.drawFunction = GL_TRIANGLE_FAN
    wheel.color = (0.0, 0.0, 0.0, 1.0)
    
    dTheta = 2*math.pi/20
    theta = 0
    while theta < 2*math.pi:
        x = xWheel + raioWheel*math.cos(theta)
        y = yWheel + raioWheel*math.sin(theta)
        aux = Vertex2f(x, y)
        wheel.addVertex(aux)
        theta += dTheta

    mower.addShape(wheel)
    
    engine = Shape()
    engine.color = (0.0,0.0,0.0,1.0)
    engine.drawFunction = GL_TRIANGLE_STRIP

    engineBaseLeft = Vertex2f(0, heightBase/4)
    engineBaseRight = Vertex2f(sizeBase/4, heightBase/4)
    enginecableTopLeft = Vertex2f(0, 3*heightBase/4)
    enginecableTopRight = Vertex2f(sizeBase/4, 3*heightBase/4)
    
    engine.addVertex(engineBaseLeft)
    engine.addVertex(engineBaseRight)
    engine.addVertex(enginecableTopLeft)
    engine.addVertex(enginecableTopRight)

    mower.addShape(engine)

    cable = Shape()
    cable.drawFunction = GL_TRIANGLE_STRIP
    cable.color = (0.0, 0.0, 0.0, 1.0)

    cableBase = 0.3
    cableHeight = 0.1
    cableDelta = sizeBase/5

    cableOrigin = Vertex2f(cableDelta,0)
    cableTopleft = Vertex2f(cableDelta, cableHeight)
    cableTopRight = Vertex2f(cableBase, cableHeight)
    cableRight = Vertex2f(cableBase, 0)

    angle = 3*math.pi/4
    cableOrigin = rotate(cableOrigin, angle)
    cableTopleft = rotate(cableTopleft, angle)
    cableTopRight = rotate(cableTopRight, angle)
    cableRight = rotate(cableRight, angle)

    cable.addVertex(cableOrigin)
    cable.addVertex(cableRight)
    cable.addVertex(cableTopleft)
    cable.addVertex(cableTopRight)

    mower.addShape(cable)

    return mower
########################################################################################





########################### Função que cria o objeto fio ###############################
def createWire():
    deltaY = 0.01
    numValues = 5
    
    xValues = np.linspace(0.0, 1.0, numValues)
    yValues = np.power(xValues, 2)

    wire = Object()
    
    curve = Shape()
    curve.drawFunction = GL_TRIANGLE_STRIP
    curve.color = (0.0, 0.0, 0.0, 1.0)

    for i in range(0, numValues):
        curve.addVertex(Vertex2f(xValues[i], yValues[i]-deltaY/2))
        curve.addVertex(Vertex2f(xValues[i], yValues[i]+deltaY/2))
        
    wire.addShape(curve)

    return wire
########################################################################################
    