import numpy as np

class Triangle:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program('default')
        self.vao = self.get_vao()
    
    def render(self): # 모델 렌더링 위해서 Vertex array object 렌더링
        self.vao.render()
    
    def destroy(self): # opengl에 garbage collector 등 없으므로 수동으로 리소스 해제 필요
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()
            
    
    def get_vao(self): # Vertex Array object. Vertex Buffer object 에서 Vertex Array object 추출하는 느낌 
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '3f', 'in_position')]) # VBO, Data format 3f, Attributes in position.
        # 버퍼에서 각 3자리씩 요소 묶어서  in position이라는 input attribute로 전달.
        return vao
        
    def get_vertex_data(self):
        vertex_data = [(-0.6, -0.8, 0.0), (0.6, -0.8, 0.0), (0.0, 0.8, 0.0)]
        vertex_data = np.array(vertex_data, dtype='f4') # float32 > 4바이트(32비트) 설정. np array 변형
        return vertex_data
    
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
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader = fragment_shader) # Shader program object.
        # shader 컴파일 시 필요. CPU 사용해서 컴파일하고 GPU에 전달 준비
    
        return program