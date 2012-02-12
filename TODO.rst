CRY§TAL§ TODO
=============

    * Extend the game's infobox.
        * Text that, after wrapping, doesn't fit vertically prompts the
          user to scroll by pressing space.

    * Change entities file to employ direct instantiation of world.Entity
      for entity definitions.
        * Change Entity to class to take an image name instead of an image,
          and have the initializer load the image.
            * This can be possibly be achieved by using pyglet's default
              loader, and manually changing its _script_home attribute to
              '.'.

    * Implement complex interactions between PC and NPCs.
        * Actions can be executed in a given order, a given number of
          times each.
        * 'RequireState' action ends action sequence if given plot state
          is not found True.
        * Write class Interaction in world.entity to coordinate actions.
          
    * Prepare and send the game to Julian Wass, asking for his approval.
        * Write a demonstration world.
        * Get everything working on Windows.
        * Create a Windows executable for the game.
        * Email everything to Julian with a verbose explanation.

    * Implement the pause menu.
        * Can be opened anytime in world mode.
        * Lets the user check her party's information, save the game,
          and quit the game.

    * Implement game saves.
        * Use the cpickle module to serialize WorldMode instance game.wmode.
        * Add 'load game' button to main menu that only appears when a pickled
          WorldMode instance exists.

    * Implement game overs.
        * Add a 'GameOver' entry to the plot set to False.
        * At the end of each iteration of the main loop, if 'GameOver'
          is False, end the game.

    * Implement visual effects.
        * Entities smoothly "scroll" between tiles as they move.
        * Entities can have animated images.
        * Entity animations can be repeated in sequence, paused, or set
          to a particular frame.
        * Entities visually rotate to match the direction of their last
          movement.
            * Most will only have right and left rotations.
            * The player and party members will have all four directions.

    * Beautify interface.
        * Add background image to main menu.
        * Replace boring line border panels with graphical panels in all
          gui elements.
