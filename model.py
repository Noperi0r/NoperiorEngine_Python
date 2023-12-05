import numpy as np
import glm
import pygame as pg

class Cube:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program('default')
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        self.texture = self.get_texture(path='Textures/wood.png') 
        self.on_init()
    
    def get_texture(self, path):
        texture = pg.image.load(path).convert() # image > display surface convert
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        #texture.fill('red')
        texture = self.ctx.texture(size=texture.get_size(),components=3, data=pg.image.tostring(texture,'RGB')) # openGL texture 생성. size는 이미지 크기, component는 텍스처 컬러 구성 요소 수, data는 이미지 데이터. pygame 이미지를 바이트 문자열로 변환
        return texture
    
    def update(self):
        m_model = glm.rotate(self.m_model, self.app.time * 0.5, glm.vec3(0,1,0)) # model coordinates, 프레임마다 y축 기준으로 회전하게 함. 
        self.shader_program['m_model'].write(m_model) # shader의 m model 업데이트
        self.shader_program['m_view'].write(self.app.camera.m_view) # shader에 업데이트 된 view matrix 전달해 줘야 함 
        self.shader_program['camPos'].write(self.app.camera.position)
    def get_model_matrix(self):
        m_model = glm.mat4() # 우선 4 by 4 항등행렬 정의. 물체를 딱히 움직이거나 회전시키지 않는다는 뜻
        return m_model
    
    def on_init(self):
        #light
        self.shader_program['light.position'].write(self.app.light.position)
        self.shader_program['light.Ia'].write(self.app.light.Ia)
        self.shader_program['light.Id'].write(self.app.light.Id)
        self.shader_program['light.Is'].write(self.app.light.Is)
        #texture
        self.shader_program['u_texture_0'] = 0 
        self.texture.use()
        #mvp
        self.shader_program['m_proj'].write(self.app.camera.m_proj) # projection matrix를 camera에서 shader에게 넘겨줌
        self.shader_program['m_view'].write(self.app.camera.m_view) # view matrix를 camera에서 shader에게 넘겨줌
        self.shader_program['m_model'].write(self.m_model) # model matrix shader에게 전달
    
    
    def render(self): # 모델 렌더링 위해서 Vertex array object 렌더링
        self.update() # 렌더링 전 업데이트 하는 것이 좋음
        self.vao.render()
    
    def destroy(self): # opengl에 garbage collector 등 없으므로 수동으로 리소스 해제 필요
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()
            
    
    def get_vao(self): # Vertex Array object. Vertex Buffer object 에서 Vertex Array object 추출하는 느낌 
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '2f 3f 3f','in_texcoord_0','in_normal','in_position')]) # VBO, Data format 3f, Attributes in position.
        # 버퍼에서 각 3자리씩 요소 묶어서  in position이라는 input attribute로 전달.
        return vao
        
    def get_vertex_data(self):
        vertices = [(-1,-1,1), (1,-1,1), (1,1,1), (-1,1,1), (-1,1,-1), (-1,-1,-1), (1,-1,-1), (1,1,-1)] # 삼각형 정점 정의. 0~7 index 존재
        
        indices = [(0,2,3), (0,1,2),
                   (1,7,2), (1,6,7),
                   (6,5,4), (4,7,6),
                   (3,4,5), (3,5,0),
                   (3,7,4), (3,2,7),
                   (0,6,1), (0,5,6),] # 사각형 이루는 삼각형들 index로 정의 
        vertex_data = self.get_data(vertices, indices) # 큐브 정점 데이터 생성

        tex_coord = [(0,0), (1,0), (1,1), (0,1)] # texture coordinate from 0 to 1. 좌표에 인덱스 부여 0 1 2 3 
        tex_coord_indicies = [(0,2,3),(0,1,2),
                              (0,2,3),(0,1,2),
                              (0,1,2),(2,3,0),
                              (2,3,0),(2,0,1),
                              (0,2,3),(0,1,2),
                              (3,1,2),(3,0,1)]
        tex_coord_data = self.get_data(tex_coord, tex_coord_indicies)
        
        normals = [(0, 0, 1) * 6, # frag 구성하는 삼각형 vertice들의 normal. 각 면마다 6개의 polygon vert 존재
                   (1, 0, 0) * 6,
                   (0, 0,-1) * 6,
                   (-1, 0, 0) * 6,
                   (0, 1, 0) * 6,
                   (0, -1, 0) * 6]
        normals = np.array(normals, dtype='f4').reshape(36,3)
      
        vertex_data = np.hstack([normals, vertex_data]) 
        vertex_data = np.hstack([tex_coord_data, vertex_data]) # 배열 하나에 texture coord, 정점 coord 다 넣음
        return vertex_data
    
    @staticmethod
    def get_data(vertices, indices): # generate vertex data based on verticies and indicies
        data = [vertices[ind] for triangle in indices for ind in triangle] # 0 2 3 0 1 2 1 7 2 1 6 7 .... indicies 정렬
        return np.array(data, dtype='f4')
    
    def get_vbo(self): # vertex data GPU로 전송. Vertex buffer object 생성
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data) # Vertex buffer Object 생성
        return vbo
    
    # Shader 로드
    def get_shader_program(self, shader_name): 
        with open(f'shaders/{shader_name}.vert', 'rt', encoding='UTF8') as file:
            vertex_shader = file.read()
        with open(f'shaders/{shader_name}.frag', 'rt', encoding='UTF8') as file:
            fragment_shader = file.read()
            
        # context manager 통해 로드 ★★
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader) # Shader program object.
        # shader 컴파일 시 필요. CPU 사용해서 컴파일하고 GPU에 전달 준비
    
        return program