class Timer:
    """
    A very simple timer for events that are not directly tied to animation.
    """

    def __init__(self, delay, ticks=-1):
        """
        The delay is given in milliseconds; ticks is the number of ticks the
        timer will make before flipping self.done to True.  Pass a value
        of -1 to bypass this.
        """
        self.delay = delay
        self.ticks = ticks
        self.tick_count = 0
        self.timer = None
        self.done = False

    def check_tick(self, now):
        """Returns true if a tick worth of time has passed."""
        if not self.timer:
            self.timer = now
            return True
        elif not self.done and now - self.timer > self.delay:
            self.tick_count += 1
            self.timer = now
            if self.ticks != -1 and self.tick_count >= self.ticks:
                self.done = True
            return True
        return False
