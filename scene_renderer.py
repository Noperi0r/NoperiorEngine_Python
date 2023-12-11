class SceneRenderer:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.mesh = app.mesh
        self.scene = app.scene
        
    def main_render(self):
        self.app.ctx.screen.use()
        for obj in self.scene.objects:
            obj.render()
        
    def render(self):
        self.scene.update()
        self.main_render()
        
    def destroy(self):
        pass
        