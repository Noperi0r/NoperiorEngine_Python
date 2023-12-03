import glm
import pygame as pg 

# View frustrum 정의
FOV = 50
NEAR = 0.1
FAR = 100
SPEED = 0.01
SENSITIVITY = 0.05 # 마우스 감도. 회전에 사용
  
class Camera:
    def __init__(self, app, position=(0,0,4), yaw=-90, pitch=0): 
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1] # 화면 비율 정의 
        self.position = glm.vec3(position) # 카메라 위치 정의 
        self.up = glm.vec3(0,1,0) # y 
        self.right = glm.vec3(1,0,0) # x
        self.forward = glm.vec3(0,0,-1) # z. right hand coordinate이므로 -1이 됨
        self.yaw = yaw
        self.pitch = pitch
        # view matrix >> 카메라가 원점인 공간 형성.
        self.m_view = self.get_view_matrix()
        # perspective projection marix 생성 >> 원근감 만들어냄
        self.m_proj = self.get_projection_matrix()
        
    def rotate(self):
        rel_x, rel_y = pg.mouse.get_rel() # relative movement of the mouse
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY
        self.pitch = max(-89, min(89, self.pitch)) # limit so there's no unnatural up and down movement
    
    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)
        self.forward.x = glm.cos(yaw) * glm.cos(pitch) # 구한 회전값 통해 카메라의 forward 벡터 조정 = 카메라 방향 조정
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)
        
        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0,1,0))) # fake up vector 통해 right 벡터 cross product 통해 구함
        self.up = glm.normalize(glm.cross(self.right, self.forward)) # 일단 그래서 구한 right vector 통해서 다시 진짜 up vector 구함

        
    def update(self):
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix() # 이동하는 위치에 따른 view matrix 최신화
        
    def move(self):
        velocity = SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.position += self.forward * velocity
        if keys[pg.K_s]:
            self.position -= self.forward * velocity
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
        if keys[pg.K_q]:
            self.position += self.up * velocity
        if keys[pg.K_e]:
            self.position -= self.up * velocity
        
        
    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward , self.up) # eye: position of the camera / center: position where the camera is looking at / up: normalized up vector, how the camera is oriented
    
    def get_projection_matrix(self):
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)
        