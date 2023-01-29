from game.control import Control
from composite_root import (
    composite_root
)
from settings import CAPTION


if '__main__' == __name__:
    composite_root.initialize()
    control = Control(CAPTION)
    control.state_machine.setup_states(composite_root.states(), "SPLASH")
    control.main()
