
class Animation:
    """A class to simplify the act of adding animations to sprites."""
    def __init__(self, frames, fps, loops=-1):
        """
        The argument frames is a list of frames in the correct order;
        fps is the frames per second of the animation;
        loops is the number of times the animation will loop (a value of -1
        will loop indefinitely).
        """
        self.frames = frames
        self.fps = fps
        self.frame = 0
        self.timer = None
        self.loops = loops
        self.loop_count = 0
        self.done = False

    def get_next_frame(self, now):
        """
        Advance the frame if enough time has elapsed and the animation has
        not finished looping.
        """
        if not self.timer:
            self.timer = now
        if not self.done and now - self.timer > 1000.0 / self.fps:
            self.frame = (self.frame + 1) % len(self.frames)
            if not self.frame:
                self.loop_count += 1
                if self.loops != -1 and self.loop_count >= self.loops:
                    self.done = True
                    self.frame -= 1
            self.timer = now
        return self.frames[self.frame]

    def reset(self):
        """Set frame, timer, and loop status back to the initialized state."""
        self.frame = 0
        self.timer = None
        self.loop_count = 0
        self.done = False
