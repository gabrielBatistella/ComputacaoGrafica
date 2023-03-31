from turtle import isvisible
from sqlalchemy import null
import time
import glm
import util
import math
import numpy as np
import glfw
from OpenGL.GL import *

class Camera:
    def __init__(self, events, width, height):
        self.cameraPos   = glm.vec3(0.0,  10.0,  0.0)
        self.cameraFront = glm.vec3(1.0,  0.0, 0.0)
        self.cameraUp    = glm.vec3(0.0,  1.0,  0.0)

        self.speed = 15

        self.firstMouse = True
        self.yaw = -90.0 
        self.pitch = 0.0
        self.lastX =  0
        self.lastY =  0

        self.events = events
        self.lastX =  width/2
        self.lastY =  height/2

    def update(self, deltaTimeInSeconds):
        if self.events == null:
            return
        
        speed = self.speed
        if self.events.KEY_SHIFT:
            speed *= 3

        if self.events.KEY_W: # tecla W
           self.moveToRelativeFront(deltaTimeInSeconds*speed)
        
        elif self.events.KEY_S: # tecla S
            self.moveToRelativeFront(-deltaTimeInSeconds*speed)
        
        elif self.events.KEY_A: # tecla A
            self.moveToRelativeRight(-deltaTimeInSeconds*speed)
            
        elif self.events.KEY_D: # tecla D
            self.moveToRelativeRight(deltaTimeInSeconds*speed)
    
    def mouse_event(self, xpos, ypos):
        if self.firstMouse:
            self.lastX = xpos
            self.lastY = ypos
            self.firstMouse = False

        xoffset = xpos - self.lastX
        yoffset = self.lastY - ypos
        self.lastX = xpos
        self.lastY = ypos

        sensitivity = 0.3
        xoffset *= sensitivity
        yoffset *= sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        limite = 88
        if self.pitch >= limite: self.pitch = limite
        if self.pitch <= -limite: self.pitch = -limite

        front = glm.vec3()
        front.x = math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        front.y = math.sin(glm.radians(self.pitch))
        front.z = math.sin(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        self.cameraFront = glm.normalize(front)

    def setPosition(self, vec3):
        self.cameraPos = vec3

    def movePosition(self, delta_vec3):
        self.cameraPos += delta_vec3
        limiteInferior = 1
        if self.cameraPos.y < limiteInferior:
            self.cameraPos.y = limiteInferior
        if glm.length(self.cameraPos) > 750/5 - 5:
            self.cameraPos -= delta_vec3

    def setCameraFront(self, vec3):
        self.cameraFront = vec3

    def setCameraUp(self, vec3):
        self.cameraUp(self, vec3)
    
    def moveTo(self, vec_dir, displacement):
        self.movePosition(glm.normalize(vec_dir)*displacement)

    def moveToRelativeFront(self, displacement):
        self.movePosition(displacement * glm.normalize(self.cameraFront))
    
    def moveToRelativeRight(self, displacement):
         self.movePosition(glm.normalize(glm.cross(self.cameraFront, self.cameraUp))*displacement)

    def moveToRelativeTop(self, displacement):
        self.movePosition(glm.normalize(self.cameraUp)*displacement)

    def setFront(self, front_vec):
        self.cameraFront = glm.normalize(front_vec)

    def getCamperaPos(self):
        return self.cameraPos
    
    def getCameraFront(self):
        return self.cameraFront

    def getCameraUp(self):
        return self.cameraUp

class Events:
    def __init__(self):
        self.KEY_W = False
        self.KEY_S = False
        self.KEY_A = False
        self.KEY_D = False
        self.KEY_ARROWUP = False
        self.KEY_ARROWDOWN = False
        self.KEY_ARROWLEFT = False
        self.KEY_ARROWRIGHT = False
        self.KEY_SHIFT = False
        self.KEY_STAR = False 
        self.KEY_ADD = False
        self.KEY_LESS = False

        self.polygonal_mode=False

    def changePoligonalMode(self):
        if self.polygonal_mode == False:
            self.polygonal_mode = True
        else:
            self.polygonal_mode = False

    def key_event(self, key, action):
        print('key:',key)
        if action == 1:
            if key == 65:
                self.KEY_A = True
            elif key == 83:
                self.KEY_S = True
            elif key == 68:
                self.KEY_D = True
            elif key == 87:
                self.KEY_W = True
            elif key == 265:
                self.KEY_ARROWUP = True
            elif key == 264:
                self.KEY_ARROWDOWN = True
            elif key == 263:
                self.KEY_ARROWLEFT = True
            elif key == 262:
                self.KEY_ARROWRIGHT = True
            elif key == 340:
                self.KEY_SHIFT = True
            elif key == 332:
                self.KEY_STAR = True 
                self.changePoligonalMode()
            elif key == 334:
                self.KEY_ADD = True
            elif key == 333:
                self.KEY_LESS = True
        elif action == 0:
            if key == 65:
                self.KEY_A = False
            elif key == 83:
                self.KEY_S = False
            elif key == 68:
                self.KEY_D = False
            elif key == 87:
                self.KEY_W = False
            elif key == 265:
                self.KEY_ARROWUP = False
            elif key == 264:
                self.KEY_ARROWDOWN = False
            elif key == 263:
                self.KEY_ARROWLEFT = False
            elif key == 262:
                self.KEY_ARROWRIGHT = False
            elif key == 340:
                self.KEY_SHIFT = False
            elif key == 332:
                self.KEY_STAR = False 
            elif key == 334:
                self.KEY_ADD = False
            elif key == 333:
                self.KEY_LESS = False

class Engine:
    def __init__(self):
        self.height = 1080
        self.width = 1920
        self.renderDistance = 500
        self.window = util.createWindow(self.width, self.height, 'Trabalho 2 - CG')
        self.program = util.createProgram()

        self.events = Events()
        self.camera = Camera(self.events, self.width, self.height)

        self.objects = []

    def initialize(self):
        self.loadModels()
        self.configInputs()
        self.startLoop()

    def addModel(self, model):
        self.objects.append(model)

    def configInputs(self):
        def key_event(window, key, scancode, action, mods):
            self.events.key_event(key,action)
        def mouse_event(window, xpos, ypos):
            self.camera.mouse_event(xpos, ypos)
        glfw.set_key_callback(self.window,key_event)
        glfw.set_cursor_pos_callback(self.window, mouse_event)

    def loadModels(self):
        glEnable(GL_TEXTURE_2D)
        qtd_texturas = len(self.objects)
        textures = glGenTextures(qtd_texturas)

        # Loading in models
        i = 0
        for object in self.objects:
            object.loadModel()
            object.loadTexture(i)
            i = i + 1

        buffer = glGenBuffers(3)

        # Creating and uploading Vetices Array
        size = 0
        for object in self.objects:
            size += len(object.vertices_list)
        vertices = np.zeros(size, [("position", np.float32, 3)])

        i = 0
        for object in self.objects:
            verticesInObject = object.getAllVertices()
            for vertexInObject in verticesInObject:
                vertices['position'][i] = vertexInObject
                i = i + 1

        index = 0
        for object in self.objects:
            index = object.defineIndexOfVerticesOnBuffer(index)

        glBindBuffer(GL_ARRAY_BUFFER, buffer[0])
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        stride = vertices.strides[0]
        offset = ctypes.c_void_p(0)
        loc_vertices = glGetAttribLocation(self.program, "position")
        glEnableVertexAttribArray(loc_vertices)
        glVertexAttribPointer(loc_vertices, 3, GL_FLOAT, False, stride, offset)

        # Creating and uploading textures coordinaties array
        sizeCoord = 0
        for object in self.objects:
            sizeCoord += len(object.textures_coord_list)
        textures = np.zeros(sizeCoord, [("position", np.float32, 2)])

        i = 0
        for object in self.objects:
            coordsInObject = object.textures_coord_list
            for coord in coordsInObject:
                textures['position'][i] = coord
                i = i + 1

        glBindBuffer(GL_ARRAY_BUFFER, buffer[1])
        glBufferData(GL_ARRAY_BUFFER, textures.nbytes, textures, GL_STATIC_DRAW)
        stride = textures.strides[0]
        offset = ctypes.c_void_p(0)
        loc_texture_coord = glGetAttribLocation(self.program, "texture_coord")
        glEnableVertexAttribArray(loc_texture_coord)
        glVertexAttribPointer(loc_texture_coord, 2, GL_FLOAT, False, stride, offset)

        # Creating and uploading Array of normals
        sizeNorm = 0
        for object in self.objects:
            sizeNorm += len(object.normals_list)
        normals = np.zeros(sizeNorm, [("position", np.float32, 3)])

        i = 0
        for object in self.objects:
            normsInObject = object.normals_list
            for norm in normsInObject:
                normals['position'][i] = norm
                i = i + 1

        glBindBuffer(GL_ARRAY_BUFFER, buffer[2])
        glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
        stride = normals.strides[0]
        offset = ctypes.c_void_p(0)
        loc_normals_coord = glGetAttribLocation(self.program, "normals")
        glEnableVertexAttribArray(loc_normals_coord)
        glVertexAttribPointer(loc_normals_coord, 3, GL_FLOAT, False, stride, offset)

    def startLoop(self):
        self.now = time.time_ns()
        self.newNow = self.now 
        self.timer = self.now
        self.frames = 0

        glEnable(GL_DEPTH_TEST)
        glfw.show_window(self.window)
        glfw.set_cursor_pos(self.window, self.width/2, self.height/2)
        while not glfw.window_should_close(self.window):
            self.gameloop()
        glfw.terminate()

    def updateRenderDistance(self, deltaTimeInSeconds):
        factor = 200
        limite = 10
        self.renderDistance += factor*deltaTimeInSeconds
        if(self.renderDistance < limite):
            self.renderDistance = limite

    def update(self, deltaTimeInSeconds):
        self.camera.update(deltaTimeInSeconds)
        
        if(self.events.KEY_ADD):
            self.updateRenderDistance(deltaTimeInSeconds)
        if(self.events.KEY_LESS):
            self.updateRenderDistance(-deltaTimeInSeconds)

        for object in self.objects:
            object.update(deltaTimeInSeconds)

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.2, 0.2, 0.2, 1.0)
        
        if self.events.polygonal_mode==True:
            glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        if self.events.polygonal_mode==False:
            glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
        
        for object in self.objects:
            object.drawObject(self.program)
        
    def gameloop(self):
        self.now = time.time_ns()
        deltaTimeInSeconds = (self.now - self.newNow) / 1000000000.0
        if(deltaTimeInSeconds < 0):
            deltaTimeInSeconds = 0

        glfw.poll_events()
        self.update(deltaTimeInSeconds)
        self.render()

        mat_view = util.view(self.camera.cameraPos, self.camera.cameraFront, self.camera.cameraUp)
        loc_view = glGetUniformLocation(self.program, "view")
        glUniformMatrix4fv(loc_view, 1, GL_TRUE, mat_view)

        mat_projection = util.projection(self.width, self.height, self.renderDistance)
        loc_projection = glGetUniformLocation(self.program, "projection")
        glUniformMatrix4fv(loc_projection, 1, GL_TRUE, mat_projection)    
        
        # atualizando a posicao da camera/observador na GPU para calculo da reflexao especular
        loc_view_pos = glGetUniformLocation(self.program, "viewPos") # recuperando localizacao da variavel viewPos na GPU
        glUniform3f(loc_view_pos, self.camera.cameraPos[0], self.camera.cameraPos[1], self.camera.cameraPos[2]) ### posicao da camera/observador (x,y,z)

        glfw.swap_buffers(self.window)

        self.frames += 1

        self.newNow = self.now
        timeAtual = time.time_ns()
        if(timeAtual - self.timer >= 1000000000): 
            self.timer += 1000000000
            FPS_ATUAL = self.frames
            print(FPS_ATUAL, ' FPS')
            self.frames = 0
        
class Model:
    def __init__(self, objFileName, textureFileName):
        self.objFileName = objFileName
        self.textureFileName = textureFileName    

        self.position = glm.vec3(0.0, 0.0, 0.0)
        self.rotationAngle = 0.0
        self.rotationAxis = glm.vec3(0.0, 0.0, 1.0)
        self.scale = glm.vec3(1.0, 1.0, 1.0)

        self.ka = 0.03 # coeficiente de reflexao ambiente do modelo
        self.kd = 0.15 # coeficiente de reflexao difusa do modelo
        self.ks = 0 # coeficiente de reflexao especular do modelo
        self.ns = 64 # expoente de reflexao especular

        self.vertices_list = []    
        self.normals_list = []    
        self.textures_coord_list = []

        self.startIndex = -1
        self.textureId = -1

        self.isVisible = True
        self.animation = null
        
    def setTextureId(self, id):
        self.textureId = id

    def getNumVertices(self):
        return len(self.vertices_list)

    def defineIndexOfVerticesOnBuffer(self, startIndex):
        self.startIndex = startIndex
        self.numVertices = len(self.vertices_list)
        return self.startIndex+self.numVertices

    def setLight(self, ka, kd, ks, ns):
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.ns = ns
    
    def setPosition(self, vec_position):
        self.position = vec_position
    
    def setScale(self, vec_scale):
        self.scale = vec_scale

    def setRotation(self, rotationAngle, vec_rotationAxis):
        self.rotationAngle = rotationAngle
        self.rotationAxis = vec_rotationAxis

    def getModelTransformation(self):
        if(self.animation == null):
            return util.model(self.rotationAngle, self.rotationAxis, self.position, self.scale)
        else:
            angle = math.radians(self.rotationAngle)
            
            matrix_transform = glm.mat4(1.0)

            matrix_transform = glm.translate(matrix_transform, glm.vec3(0, self.position.y, 0))    
            matrix_transform = self.animation.makeTranslate(matrix_transform)

            matrix_transform = glm.rotate(matrix_transform, angle,  self.rotationAxis)
            matrix_transform = self.animation.makeRotation(matrix_transform)

            matrix_transform = glm.scale(matrix_transform, self.scale)
            
            matrix_transform = np.array(matrix_transform)
            
            return matrix_transform

    def loadModel(self):
        modelo = util.load_model_from_file(self.objFileName)
        print('Processando modelo Vertice inicial:',len(self.vertices_list))
        for face in modelo['faces']:
            for vertice_id in face[0]:
                self.vertices_list.append( modelo['vertices'][vertice_id-1] )
            for texture_id in face[1]:
                self.textures_coord_list.append( modelo['texture'][texture_id-1] )
            for normal_id in face[2]:
                self.normals_list.append( modelo['normals'][normal_id-1] )
        self.numVertices = len(self.vertices_list)
        print('Processando modelo Vertice Final:',len(self.vertices_list))
    
    def loadTexture(self, bufferId):
        self.textureId = bufferId
        util.load_texture_from_file(bufferId, self.textureFileName)
        
    def getAllVertices(self):
        return self.vertices_list

    def getAllTextureCoord(self):
        return self.textures_coord_list

    def loadMatrixTransformation(self, program):
        mat_transform = self.getModelTransformation()
        loc = glGetUniformLocation(program, "model")
        glUniformMatrix4fv(loc, 1, GL_TRUE, mat_transform)

    def drawObject(self, program):
        if not self.isVisible:
            return

        self.loadMatrixTransformation(program)
        loc_ka = glGetUniformLocation(program, "ka") # recuperando localizacao da variavel ka na GPU
        glUniform1f(loc_ka, self.ka) ### envia ka pra gpu
    
        loc_kd = glGetUniformLocation(program, "kd") # recuperando localizacao da variavel kd na GPU
        glUniform1f(loc_kd, self.kd) ### envia kd pra gpu    
    
        loc_ks = glGetUniformLocation(program, "ks") # recuperando localizacao da variavel ks na GPU
        glUniform1f(loc_ks, self.ks) ### envia ks pra gpu        
    
        loc_ns = glGetUniformLocation(program, "ns") # recuperando localizacao da variavel ns na GPU
        glUniform1f(loc_ns, self.ns) ### envia ns pra gpu 

        glBindTexture(GL_TEXTURE_2D, self.textureId)   
        # desenha o modelo
        glDrawArrays(GL_TRIANGLES, self.startIndex, self.getNumVertices()) ## renderizando

    def setAnimation(self, animation):
        self.animation = animation

    def update(self, deltaTimeInSeconds):
        if self.animation != null:
            self.animation.update(deltaTimeInSeconds)
            if(self.animation.isFinished):
                self.animation = null
        

class Light(Model):
    def __init__(self, nameLight, nomeLightColor):
        self.nameLightColor = nomeLightColor
        self.objFileName = './obj/light.obj'
        self.textureFileName = './texture/light_texture.png'    

        self.position = glm.vec3(0.0, 0.0, 0.0)
        self.rotationAngle = 0.0
        self.rotationAxis = glm.vec3(0.0, 0.0, 1.0)
        self.scale = glm.vec3(0.1, 0.1, 0.1)

        self.ka = 1 # coeficiente de reflexao ambiente do modelo
        self.kd = 1 # coeficiente de reflexao difusa do modelo
        self.ks = 1 # coeficiente de reflexao especular do modelo
        self.ns = 1000 # expoente de reflexao especular

        self.vertices_list = []    
        self.normals_list = []    
        self.textures_coord_list = []

        self.startIndex = -1
        self.textureId = -1

        self.isVisible = False
        self.setLightColor(glm.vec3(1,1,1))
        self.animation = null
        self.nameLight = nameLight
    
    def setLightColor(self, vec3_color):
        self.lightColor = vec3_color

    def drawObject(self, program):
        
        loc_light_color = glGetUniformLocation(program, self.nameLightColor) # recuperando localizacao da variavel lightPos na GPU
        glUniform3f(loc_light_color, self.lightColor.x, self.lightColor.y, self.lightColor.z) ### posicao da fonte de light

        pos = glm.vec3(0,0,0)
        pos += self.position
        if self.animation != null:
            mat_transform = self.getModelTransformation()
            pos_v4 = glm.vec4(0, 0, 0,1)
            pos_v4 = np.dot(mat_transform, pos_v4)
            pos = glm.vec3(pos_v4[0], pos_v4[1], pos_v4[2])
           
            
        loc_light_pos = glGetUniformLocation(program, self.nameLight) # recuperando localizacao da variavel lightPos na GPU
        glUniform3f(loc_light_pos, pos.x, pos.y, pos.z) ### posicao da fonte de light

        if not self.isVisible:
            return

        self.loadMatrixTransformation(program)
        loc_ka = glGetUniformLocation(program, "ka") # recuperando localizacao da variavel ka na GPU
        glUniform1f(loc_ka, self.ka) ### envia ka pra gpu
    
        loc_kd = glGetUniformLocation(program, "kd") # recuperando localizacao da variavel kd na GPU
        glUniform1f(loc_kd, self.kd) ### envia kd pra gpu    
    
        loc_ks = glGetUniformLocation(program, "ks") # recuperando localizacao da variavel ks na GPU
        glUniform1f(loc_ks, self.ks) ### envia ks pra gpu        
    
        loc_ns = glGetUniformLocation(program, "ns") # recuperando localizacao da variavel ns na GPU
        glUniform1f(loc_ns, self.ns) ### envia ns pra gpu 

        glBindTexture(GL_TEXTURE_2D, self.textureId)   
        # desenha o modelo
        glDrawArrays(GL_TRIANGLES, self.startIndex, self.getNumVertices()) ## renderizando

class AnimationInCircles:
    def __init__(self, xCenter, zCenter, position, t0):
        self.xCenter = xCenter
        self.zCenter = zCenter
        
        self.raio = math.sqrt(math.pow(xCenter-position.x,2) + math.pow(zCenter-position.z,2))
        self.isFinished = False
        self.speed = 0.1
        self.t = 0
        self.t0 = t0

    def update(self, deltaTimeInSeconds):
        self.t += deltaTimeInSeconds

    def makeRotation(self, matrix_tranform):
        angle = self.speed*self.t+self.t0
        matrix_tranform = glm.rotate(matrix_tranform, angle, glm.vec3(0,1,0))
        return matrix_tranform

    def makeTranslate(self, matrix_tranform):
        angle = self.speed*self.t+self.t0
        translation_vec = glm.vec3(self.xCenter+self.raio*math.sin(angle), 0, self.zCenter+self.raio*math.cos(angle))
        matrix_tranform = glm.translate(matrix_tranform, translation_vec)
        return matrix_tranform

    def getDeltaTranslate(self):
        angle = self.speed*self.t+self.t0
        return glm.vec3(self.xCenter+self.raio*math.sin(angle), 0, self.zCenter+self.raio*math.cos(angle))

