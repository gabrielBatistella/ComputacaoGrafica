from OpenGL.GL import *
from PIL import Image
import glm
import math
import glfw
import numpy as np

def load_model_from_file(filename):
    """Loads a Wavefront OBJ file. """
    objects = {}
    vertices = []
    normals = []
    texture_coords = []
    faces = []

    material = None

    # abre o arquivo obj para leitura
    for line in open(filename, "r"): ## para cada linha do arquivo .obj
        if line.startswith('#'): continue ## ignora comentarios
        values = line.split() # quebra a linha por espaço
        if not values: continue

        ### recuperando vertices
        if values[0] == 'v':
            vertices.append(values[1:4])

        ### recuperando vertices
        if values[0] == 'vn':
            normals.append(values[1:4])

        ### recuperando coordenadas de textura
        elif values[0] == 'vt':
            texture_coords.append(values[1:3])

        ### recuperando faces 
        elif values[0] in ('usemtl', 'usemat'):
            material = values[1]
        elif values[0] == 'f':
            face = []
            face_texture = []
            face_normals = []
            for v in values[1:]:
                w = v.split('/')
                face.append(int(w[0]))
                face_normals.append(int(w[2]))
                if len(w) >= 2 and len(w[1]) > 0:
                    face_texture.append(int(w[1]))
                else:
                    face_texture.append(0)

            faces.append((face, face_texture, face_normals, material))

    model = {}
    model['vertices'] = vertices
    model['texture'] = texture_coords
    model['faces'] = faces
    model['normals'] = normals

    return model

def load_texture_from_file(texture_id, img_textura):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    img = Image.open(img_textura)
    img_width = img.size[0]
    img_height = img.size[1]
    image_data = img.tobytes("raw", "RGB", 0, -1)
    #image_data = np.array(list(img.getdata()), np.uint8)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img_width, img_height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

def model(angle, vec3_rotationAxis, vec3_translation, vec3_scale):
    
    angle = math.radians(angle)
    
    matrix_transform = glm.mat4(1.0) # instanciando uma matriz identidade
  
    # aplicando translacao
    matrix_transform = glm.translate(matrix_transform, vec3_translation)    
    
    # aplicando rotacao
    matrix_transform = glm.rotate(matrix_transform, angle, vec3_rotationAxis)

    # aplicando escala
    matrix_transform = glm.scale(matrix_transform, vec3_scale)
    
    matrix_transform = np.array(matrix_transform)
    
    return matrix_transform

def view(cameraPos, cameraFront, cameraUp):
    mat_view = glm.lookAt(cameraPos, cameraPos + cameraFront, cameraUp)
    mat_view = np.array(mat_view)
    return mat_view

def projection(largura, altura, renderDistance):
    # perspective parameters: fovy, aspect, near, far
    mat_projection = glm.perspective(glm.radians(45.0), largura/altura, 0.1, renderDistance)
    mat_projection = np.array(mat_projection)    
    return mat_projection

def createWindow(largura, altura, name):
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(largura, altura, name, None, None)
    glfw.make_context_current(window)
    return window

def createProgram():
    vertex_code = """
            attribute vec3 position;
            attribute vec2 texture_coord;
            attribute vec3 normals;
            
            varying vec2 out_texture;
            varying vec3 out_fragPos;
            varying vec3 out_normal;
                    
            uniform mat4 model;
            uniform mat4 view;
            uniform mat4 projection;        
            
            void main(){
                gl_Position = projection * view * model * vec4(position,1.0);
                out_texture = vec2(texture_coord);
                out_fragPos = vec3(model * vec4(position, 1.0));
                out_normal = normals;            
            }
            """

    fragment_code = """

            // parametros da iluminacao ambiente e difusa
            uniform vec3 lightPos1; // define coordenadas de posicao da luz #1
            uniform vec3 lightColor1 = vec3(1.0, 1.0, 1.0); //define cor da luz #1
            uniform vec3 lightPos2; // define coordenadas de posicao da luz #2
            uniform vec3 lightColor2 = vec3(1.0, 1.0, 1.0); //define cor da luz #2
            uniform vec3 lightPos3; // define coordenadas de posicao da luz #3
            uniform vec3 lightColor3 = vec3(1.0, 1.0, 1.0); //define cor da luz #3
            uniform float ka; // coeficiente de reflexao ambiente
            uniform float kd; // coeficiente de reflexao difusa
            
            // parametros da iluminacao especular
            uniform vec3 viewPos; // define coordenadas com a posicao da camera/observador
            uniform float ks; // coeficiente de reflexao especular
            uniform float ns; // expoente de reflexao especular
            
            // parametro com a cor da(s) fonte(s) de iluminacao
            vec3 lightColor = vec3(1.0, 1.0, 1.0);

            // parametros recebidos do vertex shader
            varying vec2 out_texture; // recebido do vertex shader
            varying vec3 out_normal; // recebido do vertex shader
            varying vec3 out_fragPos; // recebido do vertex shader
            uniform sampler2D samplerTexture;
            
            
            
            void main(){
            
                // calculando reflexao ambiente
                vec3 ambient = ka * lightColor;             
            
                ////////////////////////
                // Luz #1
                ////////////////////////
                
                // calculando reflexao difusa
                vec3 norm1 = normalize(out_normal); // normaliza vetores perpendiculares
                vec3 lightDir1 = normalize(lightPos1 - out_fragPos); // direcao da luz
                float diff1 = max(dot(norm1, lightDir1), 0.0); // verifica limite angular (entre 0 e 90)
                vec3 diffuse1 = kd * diff1 * lightColor1; // iluminacao difusa
                
                // calculando reflexao especular
                vec3 viewDir1 = normalize(viewPos - out_fragPos); // direcao do observador/camera
                vec3 reflectDir1 = reflect(-lightDir1, norm1); // direcao da reflexao
                float spec1 = pow(max(dot(viewDir1, reflectDir1), 0.0), ns);
                vec3 specular1 = ks * spec1 * lightColor1;    
                
                
                ////////////////////////
                // Luz #2
                ////////////////////////
                
                // calculando reflexao difusa
                vec3 norm2 = normalize(out_normal); // normaliza vetores perpendiculares
                vec3 lightDir2 = normalize(lightPos2 - out_fragPos); // direcao da luz
                float diff2 = max(dot(norm2, lightDir2), 0.0); // verifica limite angular (entre 0 e 90)
                vec3 diffuse2 = kd * diff2 * lightColor2; // iluminacao difusa
                
                // calculando reflexao especular
                vec3 viewDir2 = normalize(viewPos - out_fragPos); // direcao do observador/camera
                vec3 reflectDir2 = reflect(-lightDir2, norm2); // direcao da reflexao
                float spec2 = pow(max(dot(viewDir2, reflectDir2), 0.0), ns);
                vec3 specular2 = ks * spec2 * lightColor2;   


                ////////////////////////
                // Luz #3
                ////////////////////////
                
                // calculando reflexao difusa
                vec3 norm3 = normalize(out_normal); // normaliza vetores perpendiculares
                vec3 lightDir3 = normalize(lightPos3 - out_fragPos); // direcao da luz
                float diff3 = max(dot(norm3, lightDir3), 0.0); // verifica limite angular (entre 0 e 90)
                vec3 diffuse3 = kd * diff3 * lightColor3; // iluminacao difusa
                
                // calculando reflexao especular
                vec3 viewDir3 = normalize(viewPos - out_fragPos); // direcao do observador/camera
                vec3 reflectDir3 = reflect(-lightDir3, norm3); // direcao da reflexao
                float spec3 = pow(max(dot(viewDir3, reflectDir3), 0.0), ns);
                vec3 specular3 = ks * spec3 * lightColor3;  
                
                ////////////////////////
                // Combinando as duas fontes
                ////////////////////////
                
                // aplicando o modelo de iluminacao
                vec4 texture = texture2D(samplerTexture, out_texture);
                vec4 result = vec4((ambient + diffuse1 + diffuse2 + diffuse3 + specular1 + specular2 + specular3),1.0) * texture; // aplica iluminacao
                gl_FragColor = result;

            }
            """

    # Request a program and shader slots from GPU
    program  = glCreateProgram()
    vertex   = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)

    # Set shaders source
    glShaderSource(vertex, vertex_code)
    glShaderSource(fragment, fragment_code)

    # Compile shaders
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

    # Attach shader objects to the program
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)

    # Build program
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program))
        raise RuntimeError('Linking error')
    glUseProgram(program)
    return program
