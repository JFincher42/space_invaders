# -*- coding: utf-8 -*-

# Imports
import arcade
import random

# Game Constants
SCALING = 6
SCREEN_WIDTH = 180 * SCALING
SCREEN_HEIGHT = 200 * SCALING
SCREEN_TITLE = "Space Invaders"
BACKGROUND_COLOR = arcade.csscolor.BLACK

# Classes


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
        super().__init__("space_invaders/images/alien1.png", scale=SCALING)

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list
        self.set_texture(self.current_texture)
        self.points = points

    def update(self):
        """Updates the current image to display
        """

        self.current_texture += 1
        if self.current_texture > len(self.textures):
            self.current_texture = 0
        self.set_texture(self.current_texture)


class Explosion(arcade.Sprite):
    """Displays an explosion animation when required
    """

    # Static variable that holds all the explosion textures
    textures = []
    animation_repeat = 0

    def __init__(self, texture_list, repeat=10):
        super().__init__("space_invaders/images/player.png", scale=SCALING)

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list
        self.set_texture(self.current_texture)
        self.animation_repeat = repeat
        # To count how many rotations we've done
        self.count = 0

    def update(self):

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


class SpaceInvadersGame(arcade.Window):
    """The Space Invaders game window. Subclass of arcade.Window.

    """

    def __init__(self):
        """Defines the game window and game variables
        """

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(BACKGROUND_COLOR)

        # Setup some basic game variables
        self.enemy_list = arcade.SpriteList()
        self.sprite_list = arcade.SpriteList()
        self.score = 0
        self.player = None

    def setup(self):
        """Sets up the game to play. To restart the game, this function is called.
        """

        # Reset the score
        self.score = 0

        # Clear the sprite lists
        for sprite in self.sprite_list:
            sprite.kill()

        # Create the player sprite
        self.player = arcade.Sprite(
            "space_invaders/images/player.png", scale=SCALING
        )
        self.player.center_x = 400
        self.player.center_y = 100
        self.sprite_list.append(self.player)

        # Create all the enemy sprites
        # Five rows of 11 enemies each
        alien_rows = [
            ("space_invaders/images/alien1.png", 30, 800),
            ("space_invaders/images/alien2.png", 20, 700),
            ("space_invaders/images/alien2.png", 20, 600),
            ("space_invaders/images/alien3.png", 10, 500),
            ("space_invaders/images/alien3.png", 10, 400),
        ]
        alien_locations = ((0, 0, 16, 8), (16, 0, 16, 8))
        for alien_data in alien_rows:
            alien_file_name, alien_points, alien_center_y = alien_data
            alien_texture = arcade.load_textures(
                alien_file_name, alien_locations, scale=SCALING
            )
            for i in range(10):
                alien = Enemy(alien_texture, alien_points)
                alien.center_x, alien.center_y = (
                    i * 16 * SCALING + 40,
                    alien_center_y,
                )
                self.enemy_list.append(alien)
                self.sprite_list.append(alien)

    def on_draw(self):

        arcade.start_render()
        self.sprite_list.draw()
        self.enemy_list.draw()


# Main code
if __name__ == "__main__":
    window = SpaceInvadersGame()
    window.setup()
    arcade.run()
