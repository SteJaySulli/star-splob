from sprite import Sprite

class PlayerShip(Sprite):
    def __init__(self, engine):
        super().__init__(engine, {
            "right": {
                "frames": [
                    'assets/ship-1-right.png'
                ],
                "default": True
            },
            "left": {
                "frames": [
                    'assets/ship-1-left.png'
                ]
            }
        })
        self.health = 100
        