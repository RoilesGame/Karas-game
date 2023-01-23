import pygame

from core import state_machine


# In milliseconds
TIME_PER_UPDATE = 16.0


class Control:
    """
    Control class for entire project. Contains the game loop, and contains
    the event_loop which passes events to States as needed.
    """
    def __init__(self, caption):
        self.screen = pygame.display.get_surface()
        self.caption = caption
        self.done = False
        self.clock = pygame.time.Clock()
        self.fps = 60.0
        self.fps_visible = True
        self.now = 0.0
        self.keys = pygame.key.get_pressed()
        self.state_machine = state_machine.StateMachine()

    def update(self):
        """
        Updates the currently active state.
        """
        self.now = pygame.time.get_ticks()
        self.state_machine.update(self.keys, self.now)

    def draw(self, interpolate):
        if not self.state_machine.state.done:
            self.state_machine.draw(self.screen, interpolate)
            pygame.display.update()
            self.show_fps()

    def event_loop(self):
        """
        Process all events and pass them down to the state_machine.
        The f5 key globally turns on/off the display of FPS in the caption
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                self.keys = pygame.key.get_pressed()
                self.toggle_show_fps(event.key)
            elif event.type == pygame.KEYUP:
                self.keys = pygame.key.get_pressed()
            self.state_machine.get_event(event)

    def toggle_show_fps(self, key):
        """Press f5 to turn on/off displaying the framerate in the caption."""
        if key == pygame.K_F5:
            self.fps_visible = not self.fps_visible
            if not self.fps_visible:
                pygame.display.set_caption(self.caption)

    def show_fps(self):
        """
        Display the current FPS in the window handle if fps_visible is True.
        """
        if self.fps_visible:
            fps = self.clock.get_fps()
            with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
            pygame.display.set_caption(with_fps)

    def main(self):
        """Main loop for entire program. Uses a constant timestep."""
        lag = 0.0
        while not self.done:
            lag += self.clock.tick(self.fps)
            self.event_loop()
            while lag >= TIME_PER_UPDATE:
                self.update()
                lag -= TIME_PER_UPDATE
            self.draw(lag/TIME_PER_UPDATE)
