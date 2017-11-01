import sys
import pygame as pg
from settings import *
from spritesheet import *
from button import *

class Game(object):
    """
    A single instance of this class is responsible for
    managing which individual game state is active
    and keeping it updated. It also handles many of
    pygame's nuts and bolts (managing the event
    queue, framerate, updating the display, etc.).
    and its run method serves as the "game loop".
    """
    def __init__(self, screen, states, start_state):
        """
        Initialize the Game object.

        screen: the pygame display surface
        states: a dict mapping state-names to GameState objects
        start_state: name of the first active game state
        Game(screen, states, "SPLASH")
        """
        self.done = False
        self.screen = screen
        self.clock = pg.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]
        self.state.startup()

    def events(self):
        """Events are passed for handling to the current state."""
        for event in pg.event.get():
            self.state.events(event)

    def flip_state(self, state_name):
        """Switch to the next game state."""
        self.state.done[state_name] = False
        self.state_name = state_name
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

    def update(self, dt):
        """
        Check for state flip and update active state.

        dt: milliseconds since last frame
        """
        if self.state.quit:
            self.done = True
        else:
            for key, value in self.state.done.items():
                if value:
                    self.flip_state(key)
        self.state.update(dt)

    def draw(self):
        """Pass display surface to active state for drawing."""
        self.state.draw(self.screen)

    def run(self):
        """
        Pretty much the entirety of the game's runtime will be
        spent inside this while loop.
        """
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.events()
            self.update(dt)
            self.draw()
            pg.display.update()


class GameState(object):
    """
    Parent class for individual game states to inherit from.
    """
    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.persist = {}
        self.font = pg.font.Font(None, 24)

    def startup(self, persistent = {}):
        """
        Called when a state resumes being active.
        Allows information to be passed between states.

        persistent: a dict passed from state to state
        """
        self.persist = persistent

    def events(self, event):
        """
        Handle a single event passed by the Game object.
        """
        pass


    def update(self, dt):
        """
        Update the state. Called by the Game object once
        per frame.

        dt: time since last frame
        """
        pass

    def draw(self, surface):
        """
        Draw everything to the screen.
        """
        pass

class MainScreen(GameState):
    def __init__(self):
        super().__init__()
        self.spritesheet = SpriteSheet.get_instance()
        self.image_bg_name = "Background.jpg"
        self.image_text_name = "Title.png"
        self.done = {"GAMEPLAY": False,
                     "TUTORIAL": False,
                     "QUIT": False}
        self.load_buttons()

    def load_buttons(self):
        self.buttons = {"GAMEPLAY": Button("Nueva Partida"),
                        "TUTORIAL": Button("Tutorial"),
                        "SALIR": Button("Salir")}
        x = WIDTH / 2
        y = 0.3
        for button in self.buttons.values():
            button.set_pos(x, HEIGHT * y)
            y += 0.25

    def startup(self, persistent = {}):
        self.spritesheet.clear_sprites()
        self.spritesheet.add_sprite(self, INTRO_FOLDER, self.image_bg_name, True)
        self.text_image = pg.image.load(path.join(INTRO_FOLDER, self.image_text_name)).convert()
        self.text_image.set_colorkey(BLACK)
        for button in self.buttons.values():
            button.clicked = False

    def events(self, event):
        if event.type == pg.QUIT:
            self.quit = True

        for key, button in self.buttons.items():
            if button.clicked:
                self.done[key] = True

    def update(self, dt):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        for key, button in self.buttons.items():
            button.update(mouse, click)

    def draw(self, screen):
        screen.fill(WHITE)
        screen.blit(self.spritesheet.get_sprite(self), (0, 0))
        screen.blit(self.text_image, (0, 0))
        for key, button in self.buttons.items():
            screen.blit(button.surface, button.rect)

class Gameplay(GameState):
    def __init__(self):
        super().__init__()
        self.rect = pg.Rect((0, 0), (128, 128))
        self.x_velocity = 1

    def startup(self, persistent):
        self.persist = persistent
        color = self.persist["screen_color"]
        self.screen_color = pg.Color(color)
        if color == "dodgerblue":
            text = "You clicked the mouse to get here"
        elif color == "gold":
            text = "You pressed a key to get here"
        self.title = self.font.render(text, True, pg.Color("gray10"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)

    def events(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.title_rect.center = event.pos

    def update(self, dt):
        self.rect.move_ip(self.x_velocity, 0)
        if (self.rect.right > self.screen_rect.right
            or self.rect.left < self.screen_rect.left):
            self.x_velocity *= -1
            self.rect.clamp_ip(self.screen_rect)

    def draw(self, surface):
        surface.fill(self.screen_color)
        surface.blit(self.title, self.title_rect)
        pg.draw.rect(surface, pg.Color("darkgreen"), self.rect)


if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    #self.states["GAMEPLAY"]
    states = {"MAINSCREEN": MainScreen(),
              "GAMEPLAY": Gameplay()}
    game = Game(screen, states, "MAINSCREEN")
    game.run()
    pg.quit()
    sys.exit()
