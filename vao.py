from vbo import VBO
from shader_program import ShaderProgram

class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx) #vbo에서부터 buffer 가져옴
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        # Cube VAO
        self.vaos['cube'] = self.get_vao(program=self.program.programs['default'], vbo=self.vbo.vbos['cube'])
        
    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)])
        return vao
    
    # def get_vao(self): # Vertex Array object. Vertex Buffer object 에서 Vertex Array object 추출하는 느낌 
    # vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '2f 3f 3f','in_texcoord_0','in_normal','in_position')]) # VBO, Data format 3f, Attributes in position.
    # # 버퍼에서 각 3자리씩 요소 묶어서  in position이라는 input attribute로 전달.
    # return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()