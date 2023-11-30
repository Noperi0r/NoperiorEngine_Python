import pygame as pg
import moderngl as mgl
import sys

class GraphicsEngine:
    def __init__(self, winSize=(1600,900)):
        # pygame init
        pg.init()
        # window size
        self.WINDOW_SIZE = winSize
        # set opengl attributes
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION,3) # major, minor 버전 설정 
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION,3) 
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE) # profile mask / profile core: 업데이트 되면서 사라질 함수들 사용 x 
        
        # Create opengl context > opengl 상태 설정
        pg.display.set_mode(self.WINDOW_SIZE, flags= pg.OPENGL | pg.DOUBLEBUF) # opengl, 더블버퍼 설정
        # opengl context(상태) 감지 > moderngl 사용
        self.ctx = mgl.create_context() # pygame 이용하여 context 감지 or 생성
        # framerate, deltatime 위해 clock class 생성
        self.clock = pg.time.Clock()
        
    def Check_Events(self): # 이벤트 감지
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
        
    def Render(self): # 렌더링 메소드
        # frame buffer clear
        self.ctx.clear(color=(0.08, 0.16, 0.18)) # 색깔은 0~255에서 0~1로 normalized.
        # screen 색 채우고, double buffer swap.
        pg.display.flip()
    
    def Run(self): # app 시작
        while True: # main loop
            self.Check_Events()
            self.Render()
            self.clock.tick(60) # framrate 60 설정

if __name__ == '__main__':
    app = GraphicsEngine() 
    app.Run()