class Camera:
    def __init__(self, anchor):
        # position
        self.x = 0
        self.y = 0

        self.width = 800
        self.height = 600

        # lerp speed (between 0 and 1)
        self.lerp_speed = 0.25

        self.anchor = anchor

    def lerp(self, start, end, speed):
        return start + (end - start) * speed

    def update(self):
        # update the camera position based on the anchor

        target_x = self.anchor.x - self.width / 2
        target_y = self.anchor.y - self.height / 2
        # apply the lerp function to smoothly move the camera
        self.x = self.lerp(self.x, target_x, self.lerp_speed)
        self.y = self.lerp(self.y, target_y, self.lerp_speed)

        pass

    def apply_camera_transform(self, object):
        obj_x, obj_y = object.x, object.y

        # apply the camera transform
        obj_x -= self.x
        obj_y -= self.y

        # return the transfrom
        return obj_x, obj_y

    pass