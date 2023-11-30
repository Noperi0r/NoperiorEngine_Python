import numpy as np

class Triangle:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        
    def Get_Vertex_Data(self):
        vertex_data = [(-0.6, -0.8, 0.0), (0.6, -0.8, 0.0), (0.0, -0.8, 0.0)]
        vertex_data = np.array(vertex_data, dtype='f4') # float32 > 4바이트(32비트) 설정. np array 변형
        return vertex_data
    
    def Get_Vbo(self): # vertex data GPU로 전송. Vertex buffer object 생성
        vertex_data = self.Get_Vertex_Data()
        vbo = self.ctx.buffer(vertex_data) # Vertex buffer Object 생성
        return vbo