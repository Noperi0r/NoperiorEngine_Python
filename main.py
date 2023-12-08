import pygame as pg
import moderngl as mgl
import sys
from model import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene

class GraphicsEngine:
    def __init__(self, winSize=(1600,900)):
        # pygame init
        pg.init()
        # window size
        self.WIN_SIZE = winSize
        # set opengl attributes
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION,3) # major, minor 버전 설정 
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION,3) 
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE) # profile mask / profile core: 업데이트 되면서 사라질 함수들 사용 x 
        # Create opengl context > opengl 상태 설정
        pg.display.set_mode(self.WIN_SIZE, flags= pg.OPENGL | pg.DOUBLEBUF) # opengl, 더블버퍼 설정
        # mouse settings > To not make mouse out of the border of screen
        pg.event.set_grab(True) 
        pg.mouse.set_visible(False)
        # opengl context(상태) 감지 > moderngl 사용
        self.ctx = mgl.create_context() # pygame 이용하여   context 감지 or 생성
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE) # depth test 실시. cull face 추가 시 invisible한 face들 렌더 안함
        # framerate, deltatime 위해 clock class 생성
        self.clock = pg.time.Clock()
        self.time = 0 # tracking time
        self.delta_time = 0
        # light
        self.light = Light()
        
        # 모델을 엔진에 나오게 하려면 모델 객체를 만들고 렌더링 메소드 호출하면 됨 
        # camera
        self.camera = Camera(self)
        #mesh
        self.mesh = Mesh(self)
        # scene
        self.scene = Scene(self)

        
    def check_events(self): # 이벤트 감지
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                #self.scene.destroy() # 종료 시 리소스 해제
                self.mesh.destroy()
                pg.quit()
                sys.exit()
        
    def render(self): # 렌더링 메소드
        # frame buffer clear
        self.ctx.clear(color=(0.08, 0.16, 0.18)) # 색깔은 0~255에서 0~1로 normalized.
        #render scene
        self.scene.render()        
        # screen 색 채우고, double buffer swap.
        pg.display.flip()
     
    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001 # seconds로 시간 줌
     
    def run(self): # app 시작
        while True: # main loop
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60) # framrate 60 설정

if __name__ == '__main__':
    app = GraphicsEngine() 
    app.run()