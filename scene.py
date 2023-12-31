from model import *

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()
        
    def add_object(self, obj):
        self.objects.append(obj)
        
    def load(self):
        app = self.app
        add = self.add_object
        
        # add(Cube(app))
        # add(Cube(app, tex_id=1, pos=(-2.5, 0, 0), rot=(45,0,0), scale=(1,2,1)))
        # add(Cube(app, tex_id=1, pos=(2.5, 0, 0), rot=(0,0,45), scale=(1,1,2)))
        
        n, s = 30, 3
        for x in range(-n, n, s):
            for z in range (-n, n, s):
                add(Cube(app,tex_id=1 ,pos=(x,-s,z)))
        
        add(Cat(app, pos=(0,-2,-10)))
        self.moving_cube = MovingCube(app, pos=(0,6,8), scale=(3,3,3), tex_id=1)
        add(self.moving_cube)

        self.cat2 = Cat2(app, pos=(-10,2,-5))
        self.cat3 = Cat2(app, pos=(-10,14,-5))
        add(self.cat2)
        add(self.cat3)
    
    def render(self):
        for obj in self.objects:
            obj.render()
            
    def update(self):
        self.moving_cube.rot.xyz = self.app.time
        self.cat2.rot.z = self.app.time * 12
        self.cat3.rot.z = -self.app.time * 4
        
        