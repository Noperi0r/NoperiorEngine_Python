import pygame as pg
import moderngl as mgl

class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='textures/test.png')
        self.textures[1] = self.get_texture(path='textures/wood.png')
        #self.textures[2] = self.get_texture(path='textures/test.png')
        
    def get_texture(self, path):
        texture = pg.image.load(path).convert() # image > display surface convert
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(),components=3, data=pg.image.tostring(texture,'RGB')) # openGL texture 생성. size는 이미지 크기, component는 텍스처 컬러 구성 요소 수, data는 이미지 데이터. pygame 이미지를 바이트 문자열로 변환
        return texture
    
    def destroy(self):
        [tex.release() for tex in self.textures.values()]