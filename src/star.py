from sprite import Sprite

class Star(Sprite):
    def __init__(self, engine):
        super().__init__(engine, {
            "right": {
                "frames": [
                    'assets/star-1.png'
                ],
                "default": True
            }
        })
        self.space = {
            "left": 500,
            "right": 500,
            "top": 0,
            "bottom": 0
        }
    def onPastXEdge(self):
        self.y = self.engine.random(0, self.engine.screenHeight)
