import numpy as np

class VBO: # Access VBO of what we want
    def __init__(self, ctx):
        self.vbos = {}
        self.vbos['cube'] = CubeVBO(ctx)
        
    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]


class BaseVBO: # interface
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = self.get_vbo()
        self.format: str = None
        self.attrib: list = None
        
    def get_vertex_data(self):...
    
    def get_vbo(self): # vertex data GPU로 전송. Vertex buffer object 생성
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data) # Vertex buffer Object 생성
        return vbo
    
    def destroy(self):
        self.vbo.release()
        
class CubeVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']
        
    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')
    
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