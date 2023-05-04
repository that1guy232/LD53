from Collider import Collider
from RopeSegment import RopeSegment
class Rope:
    # rope will have a x, y, and length.
    # This will be a line that will be made up of segments
    # the top segment will be attached to the player and the bottom will be able to attach to other objects
    def __init__(self, anchor, segment_lenght=8, segment_count=5):
        self.anchor = anchor
        # position
        self.x = anchor.x
        self.y = anchor.y

        # length
        self.segment_length = segment_lenght
        self.segment_count = segment_count

        # set up a collider x, y, width, height

        # create the rope segments
        self.rope_segments = []
        for i in range(self.segment_count):
            self.rope_segments.append(
                RopeSegment(self.x, self.y + i * self.segment_length, sway_offset=i * 8)
            )
        pass

        # collider around the last rope segment
        self.collder_width = 32
        self.collder_height = 32
        self.collider = Collider(
            self.rope_segments[-1].x - self.collder_width / 2,
            self.rope_segments[-1].y - self.collder_height / 2,
            self.collder_width,
            self.collder_height,
        )

    def render(self, rendered_screen, camera):
        # apply the camera transform
        draw_x, draw_y = camera.apply_camera_transform(self)

        # draw the rope segments
        for segment in self.rope_segments:
            segment.render(rendered_screen, camera)

        pass

    def update(self, delta_time):
        # update the rope position based on the anchor
        self.x = self.anchor.x + self.anchor.width / 2
        self.y = self.anchor.y + self.anchor.height

        # update the rope segments
        for i in range(self.segment_count):
            self.rope_segments[i].x = self.x
            self.rope_segments[i].y = self.y + i * self.segment_length

            if i == 0:
                parent_x, parent_y = self.x, self.y - self.segment_length
            else:
                parent_x, parent_y = (
                    self.rope_segments[i - 1].x,
                    self.rope_segments[i - 1].y,
                )
                self.rope_segments[i].update(parent_x, parent_y, delta_time)

        # update the collider position to keep it around the last rope segment
        self.collider.x = self.rope_segments[-1].x - self.collder_width / 2
        self.collider.y = self.rope_segments[-1].y - self.collder_height / 2

        pass

    def attach_collectable(self, collectable):
        collectable.connected_to = self.rope_segments[-1]
        pass

    def check_collision(self, obj):
        pass

    def handle_events(self, delta_time):
        pass