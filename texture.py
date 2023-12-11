import pygame as pg
import moderngl as mgl

class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='textures/test.png') # 텍스처 종류들 로드.
        self.textures[1] = self.get_texture(path='textures/wood.png')
        #self.textures[2] = self.get_texture(path='textures/test.png')
        self.textures['cat'] = self.get_texture(path='objects/cat/20430_cat_diff_v1.jpg')
        
    def get_texture(self, path):
        texture = pg.image.load(path).convert() # image > display surface convert
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(),components=3, data=pg.image.tostring(texture,'RGB')) # openGL texture 생성. size는 이미지 크기, component는 텍스처 컬러 구성 요소 수, data는 이미지 데이터. pygame 이미지를 바이트 문자열로 변환
        
        #mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        #AF
        texture.anisotropy = 32.0
        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]