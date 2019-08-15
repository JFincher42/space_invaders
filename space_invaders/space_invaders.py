# -*- coding: utf-8 -*-

# Imports
import arcade
import random

from constants import *
from si_sprites import Enemy, Explosion


# Classes


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

        # Variable for keypresses
        self.left_pressed = False
        self.right_pressed = False
        self.space_pressed = False

        # Set the alien direction - right is True, left is False
        self.alien_direction = True

        # How many seconds between alien moves?
        self.alien_speed = 1.0
        self.alien_last_time_moved = 0.0
        self.alien_acceleration = 0.05
        # Did the aliens last move down?
        self.alien_moved_down = False

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
                    i * 16 * SCALING + 120,
                    alien_center_y,
                )
                self.enemy_list.append(alien)
                self.sprite_list.append(alien)

    def on_key_press(self, symbol: int, modifiers: int):
        """Processes a key press for the game
        
        Arguments:
            symbol {int} -- The keys currently being pressed
            modifiers {int} -- Any key modifierd being pressed
        
        Returns:
            [type] -- [description]
        """
        # return super().on_key_press(symbol, modifiers)
        if arcade.key.LEFT == symbol:
            self.left_pressed = True
        if arcade.key.RIGHT == symbol:
            self.right_pressed = True
        if arcade.key.SPACE == symbol:
            self.space_pressed = True

    def on_key_release(self, symbol: int, modifiers: int):
        """Handles key release events
        
        Arguments:
            symbol {int} -- The key which was released
            modifiers {int} -- Any modifiers active when the key was released
        """
        # return super().on_key_release(symbol, modifiers)
        if arcade.key.LEFT == symbol:
            self.left_pressed = False
        if arcade.key.RIGHT == symbol:
            self.right_pressed = False
        if arcade.key.SPACE == symbol:
            self.space_pressed = False

    def on_draw(self):
        """Draws everything on the screen
        """
        arcade.start_render()
        self.sprite_list.draw()

    def on_update(self, delta_time):
        """Updates the position of all on screen items

        Arguments:
            delta_time {float} -- How much time has passed since our last call
        """
        # return super().on_update(delta_time)

        # First check for collisions between player shots and aliens
        # TBD

        # Next check for collisions between player shots and alien shots
        # TBD

        # Now check for collisions between alien shots and the player
        # TBD

        # Time to move the aliens?
        self.alien_last_time_moved += delta_time
        if self.alien_last_time_moved > self.alien_speed:
            # If we last moved down, we shouldn't check again
            if self.alien_moved_down:
                self.alien_moved_down = False

            else:
                # Do we need to switch alien direction?
                if (
                    self.alien_direction
                    and self.find_max_x(self.enemy_list) >= RIGHT_EDGE
                ):
                    self.alien_moved_down = True
                elif (
                    not self.alien_direction
                    and self.find_min_x(self.enemy_list) <= LEFT_EDGE
                ):
                    self.alien_moved_down = True

            # Now we can move the aliens
            if self.alien_moved_down:
                self.alien_direction = not self.alien_direction
                self.move_down(self.enemy_list, 1 * SCALING)
                self.alien_speed -= self.alien_acceleration
            else:
                if self.alien_direction:
                    self.move_right(self.enemy_list, 1 * SCALING)
                else:
                    self.move_left(self.enemy_list, 1 * SCALING)

            # Don't forget to update the sprite textures as well
            self.enemy_list.update()

            # Finally, reset the timer
            self.alien_last_time_moved = 0.0

        # And then the player
        if self.left_pressed and not self.right_pressed:
            self.player.center_x -= PLAYER_MOVE
        if self.right_pressed and not self.left_pressed:
            self.player.center_x += PLAYER_MOVE
        if self.player.left < LEFT_EDGE:
            self.player.left = LEFT_EDGE
        if self.player.right > RIGHT_EDGE:
            self.player.right = RIGHT_EDGE

    def find_max_x(self, spr_list: arcade.SpriteList):
        """Finds the right-most edge of the sprites in the given list
        
        Arguments:
            spr_list {arcade.SpriteList} -- A list of sprites to check
        
        Returns:
            int -- The largest X coordinate where a sprite will be drawn
        """
        x = LEFT_EDGE
        for sprite in spr_list:
            if sprite.right > x:
                x = sprite.right
        return x

    def find_min_x(self, spr_list: arcade.SpriteList):
        """Finds the left-most edge of the sprites in the given list
        
        Arguments:
            spr_list {arcade.SpriteList} -- A list of sprites to check
        
        Returns:
            int -- The smallesdt X coordinate where a sprite will be drawn
        """
        x = RIGHT_EDGE
        for sprite in spr_list:
            if sprite.left < x:
                x = sprite.left
        return x

    def move_down(self, spr_list: arcade.SpriteList, amount: int):
        """Move a set of sprites down
        
        Arguments:
            spr_list {arcade.SpriteList} -- The list of sprites to move
            amount {int} -- How much to move them
        """
        for sprite in spr_list:
            sprite.center_y -= amount

    def move_right(self, spr_list: arcade.SpriteList, amount: int):
        """Move a set of sprites to the right
        
        Arguments:
            spr_list {arcade.SpriteList} -- The list of sprites to move
            amount {int} -- How much to move them
        """
        for sprite in spr_list:
            sprite.center_x += amount

    def move_left(self, spr_list: arcade.SpriteList, amount: int):
        """Move a set of sprites to the left
        
        Arguments:
            spr_list {arcade.SpriteList} -- The list of sprites to move
            amount {int} -- How much to move them
        """
        for sprite in spr_list:
            sprite.center_x -= amount


# Main code
if __name__ == "__main__":
    window = SpaceInvadersGame()
    window.setup()
    arcade.run()
