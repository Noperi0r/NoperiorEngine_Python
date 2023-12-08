class ShaderProgram:
    def __init__(self, ctx):
        self.ctx = ctx
        self.programs = {} #dictionary 
        self.programs['default'] = self.get_program('default')
        
    # Shader 로드
    def get_program(self, shader_name): 
        with open(f'shaders/{shader_name}.vert', 'rt', encoding='UTF8') as file:
            vertex_shader = file.read()
        with open(f'shaders/{shader_name}.frag', 'rt', encoding='UTF8') as file:
            fragment_shader = file.read()
            
        # context manager 통해 로드 ★★
        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader) # Shader program object.
        # shader 컴파일 시 필요. CPU 사용해서 컴파일하고 GPU에 전달 준비
        return program
    
    def destroy(self):
        [program.release() for program in self.programs.values()]
        