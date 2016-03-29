from hrmengine.cpu import State


class Level:
    def __init__(self, state, welcome_message, check_function):
        self.state = state
        self.welcome_message = welcome_message
        self.check_function = check_function

def checkLevel1():
    return False


def getLevel1():
    state = State(iter([]), [])
    state.outbox = []
    state.regs = []
    return Level(state,"",checkLevel1)
