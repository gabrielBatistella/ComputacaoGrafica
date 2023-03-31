from random import random
from OpenGL.GL import *
import math
import numpy as np



##################### Função para realizar multiplicação matricial ##########################
def multiplica_matriz(a, b):
    m_a = a.reshape(4, 4)
    m_b = b.reshape(4, 4)
    m_c = np.dot(m_a, m_b)
    c = m_c.reshape(1, 16)
    return c
#############################################################################################



############################# Classe para representar um vetor ##############################
class Vector2f:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __str__(self):
        return "(" + str(self._x) + " ; " + str(self._y) + ")"

    def set_x(self, x):
        self._x = x

    def set_y(self, y):
        self._y = y

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    x = property(get_x, set_x)
    y = property(get_y, set_y)

    def modulo(self):
        return math.sqrt(math.pow(self._x, 2)+math.pow(self._y,2))

    def normalize(self):
        m = self.modulo()
        if m != 0: 
            self._x /= m
            self._y /= m

    def produto(self, a):
        result = Vector2f(0,0)
        result.x = self._x * a
        result.y = self._y * a
        return result

    def soma(self, vector):
        result = Vector2f(0,0)
        result.x = self._x + vector.x
        result.y = self._y + vector.y
        return result

        
#############################################################################################



############################ Classe para representar um vértice #############################
class Vertex2f(Vector2f):
    pass
#############################################################################################



############################ Classe para representar uma forma ##############################
class Shape:
    def __init__(self):
        self._vertices = []
        self._numVertices = 0
        self._startIndex = -1
        self._drawFunction = GL_TRIANGLES
        self._color = {'red': 0., "green": 0., 'blue': 1., 'alpha': 1.} 
    
    def set_startIndex(self, startIndex):
        self._startIndex = startIndex
    
    def set_drawFunction(self, drawFunction):
        self._drawFunction = drawFunction

    def set_color(self, color):
        self._color['red'] = color[0]
        self._color['green'] = color[1]
        self._color['blue'] = color[2]
        self._color['alpha'] = color[3]

    def get_vertices(self):
        return self._vertices

    def get_numVertices(self):
        return self._numVertices

    def get_color(self):
        return self._color

    vertices = property(get_vertices, None)
    startIndex = property(None, set_startIndex)
    numVertices = property(get_numVertices, None)
    drawFunction = property(None, set_drawFunction)
    color = property(get_color, set_color)

    def addVertex(self, vertex):
        self._vertices.append(vertex)
        self._numVertices += 1

    def drawShape(self):
        glDrawArrays(self._drawFunction, self._startIndex, self._numVertices)
#############################################################################################



############################ Classe para representar um objeto ##############################
class Object:
    def __init__(self):
        self._shapes = []
        self._position = Vector2f(0, 0)
        self._size = Vector2f(1, 1)
        self._angle = 0
        self._isVisible = True

    def set_position(self, position):
        self._position = position

    def set_size(self, size):
        self._size = size

    def set_angle(self, angle):
        self._angle = angle

    def set_isVisible(self, isVisible):
        self._isVisible = isVisible

    def get_position(self):
        return self._position

    def get_size(self):
        return self._size

    def get_angle(self):
        return self._angle

    shapes = property()
    position = property(get_position, set_position)
    size = property(get_size, set_size)
    angle = property(get_angle, set_angle)
    isVisible = property(None, set_isVisible)

    def addShape(self, shape):
        self._shapes.append(shape)

    def getNumVertices(self):
        result = 0
        for shape in self._shapes:
            result += shape.numVertices
        return result

    def getAllVertices(self):
        allVertices = []
        for shape in self._shapes:
            for vertex in shape.vertices:
                allVertices.append(vertex)
        return allVertices

    def defineIndexOfVerticesOnBuffer(self, startIndex):
        index = startIndex
        for shape in self._shapes:
            shape.startIndex = index
            index += shape.numVertices
        return index

    def getCurrentPositionOfPointInModel(self, vertex):
        vertex4f = (vertex.x, vertex.y, 0.0, 1.0)
        matTransformation = self.getMatrixTransformation().reshape(4, 4)
        matrixProduct = np.dot(matTransformation, vertex4f)
        currentPosition = Vector2f(matrixProduct[0], matrixProduct[1])
        return currentPosition

    def rotate(self, dTheta):
        self._angle += dTheta

    def scale(self, dScaleX, dScaleY):
        self._size.x += dScaleX
        self._size.y += dScaleY

    def translate(self, dx, dy):
        self._position.x += dx
        self._position.y += dy

    def getMatrixRotation(self):
        c = math.cos(math.radians(self._angle))
        s = math.sin(math.radians(self._angle))
        mat_rotation = np.array([ c , -s , 0.0, 0.0,
                                  s ,  c , 0.0, 0.0,
                                 0.0, 0.0, 1.0, 0.0,
                                 0.0, 0.0, 0.0, 1.0], np.float32)
        return mat_rotation
    
    def getMatrixScale(self):
        mat_scale = np.array([self._size.x,     0.0    , 0.0, 0.0,
                                  0.0    , self._size.y, 0.0, 0.0,
                                  0.0    ,     0.0    , 1.0, 0.0,
                                  0.0    ,     0.0    , 0.0, 1.0], np.float32)
        return mat_scale

    def getMatrixTranslation(self):
        mat_translation = np.array([1.0, 0.0, 0.0, self._position.x,
                                    0.0, 1.0, 0.0, self._position.y,
                                    0.0, 0.0, 1.0,       0.0      ,
                                    0.0, 0.0, 0.0,       1.0      ], np.float32)
        return mat_translation

    def getMatrixTransformation(self):
        mat_rotation = self.getMatrixRotation()
        mat_scale = self.getMatrixScale()
        mat_translation = self.getMatrixTranslation()
        mat_transform = multiplica_matriz(mat_rotation, mat_scale)
        mat_transform = multiplica_matriz(mat_translation, mat_transform)
        return mat_transform

    def loadMatrixTransformation(self, program):
        mat_transform = self.getMatrixTransformation()
        loc = glGetUniformLocation(program, "mat")
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)
        
    def drawObject(self, program):
        loc_color = glGetUniformLocation(program, 'color')
        self.loadMatrixTransformation(program)
        if(self._isVisible):
            for shape in self._shapes:
                glUniform4f(loc_color, shape.color['red'], shape.color['green'], shape.color['blue'], shape.color['alpha'])
                shape.drawShape()
#############################################################################################



############################# Classe para representar a grama ###############################
class grassCutted(Object):
    
    time = 0
    posInicial = Vector2f(0, 0)
    direction = Vertex2f(0, 0)

    def setDirection(self, direction):
        direction.normalize()
        self.direction = direction

    def setPosInicial(self, posInicial):
        self.posInicial = Vector2f(posInicial._x, posInicial._y)

    def setTranslate(self, translate):
        self._position = translate

    def set_speed(self, speed):
        self._speed = speed
    
    def set_rotateSpeed(self, rotateSpeed):
        self._rotateSpeed = rotateSpeed

    speed = property(None, set_speed)
    speedRotate = property(None, set_rotateSpeed)

    def cutGrass(self, mowerPosition):
        self.time = 0
        self.setPosInicial(mowerPosition)

        angleGraus = (20)*random()+90
        angleRad = angleGraus*math.pi/180
        
        self.setDirection(Vector2f(math.cos(angleRad), math.sin(angleRad)))
        
        self._speed = 0.5*random()+0.8
        self._rotateSpeed = 90*random()+45

    def update(self, deltaTime):

        self.rotate(self._rotateSpeed*deltaTime)

        self.time += deltaTime

        posFinal = self.posInicial
        
        displacement = self.direction.produto(self._speed*self.time)
        posFinal = posFinal.soma(displacement)

        aceleration = Vector2f(0, -2)
        displacement2 = aceleration.produto(pow(self.time,2)/2)

        posFinal = posFinal.soma(displacement2)
        self._position = posFinal

        if(posFinal.y <= -3): 
            return False
        else:
            return True
#############################################################################################