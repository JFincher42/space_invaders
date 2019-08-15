"""Defines sprite subclasses for use in the Space Invaders game
"""

import arcade
from constants import SCALING

class Enemy(arcade.Sprite):
    """Displays an enemy on the screen
    """

    # Static variable to hold points for this enemy
    points = 0

    def __init__(self, texture_list, points):
        """Creates a new enemy sprite

        Arguments:
            texture_list {List} -- Images to show as enemy moves
            points {int} -- How many points is this enemy worth when destroyed
        """

        # super.__init__() needs an image, so we give it one.
        super().__init__("space_invaders/images/alien1.png", scale=SCALING)

        # Start at the first texture
        self.current_texture = 0
        self.textures = texture_list
        self.set_texture(self.current_texture)
        self.points = points

    def update(self):
        """Updates the current image to display
        """

        self.current_texture += 1
        if self.current_texture >= len(self.textures):
            self.current_texture = 0
        self.set_texture(self.current_texture)


class Explosion(arcade.Sprite):
    """Displays an explosion animation when required
    """

    # Static variable that holds all the explosion textures
    textures = []
    animation_repeat = 0

    def __init__(self, texture_list, repeat=10):
        """Create a new explosion sprite
        
        Arguments:
            texture_list {List} -- Images to show as we explode
        
        Keyword Arguments:
            repeat {int} -- How many times do we repeat the explosion animation (default: {10})
        """

        # super.__init__() needs an image, so give it one
        super().__init__("space_invaders/images/player.png", scale=SCALING)

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list
        self.set_texture(self.current_texture)
        self.animation_repeat = repeat
        # To count how many animations we've done
        self.count = 0

    def update(self):
        """Updates the current image to display
        """

        # Update to the next frame of the animation.
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)

        # If we are at the last frame, check if we still have animation to do
        # If so, start over
        else:
            self.count += 1
            if self.count < self.animation_repeat:
                self.current_texture = 0
                self.set_texture(self.current_texture)

            # If not, kill the sprite.
            else:
                self.kill()
