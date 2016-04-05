from hrmengine.cpu import State


class Level:
    def __init__(self, state, welcome_message, check_function):
        self.state = state
        self.welcome_message = welcome_message
        self.check_function = check_function


def get_test_level():
    def check(state_to_test):
        return state_to_test is not None

    state = State(iter([]), [])
    state.outbox = []
    state.regs = []
    return Level(state,"",check)


def get_level_1():
    def check(state_to_test):
        return ''.join(map(str,state_to_test.outbox)) == "676"

    state = State(iter([6, 7, 6]), [])
    state.outbox = []
    state.regs = []
    return Level(state,"Ihr Programm sollte Ihrem Arbeiter befehlen, jedes Ding aus der INBOx zu nehmen und in die OUTBOX zu legen.",check)


def get_level_2():
    def check(state_to_test):
        return ''.join(map(str,state_to_test.outbox)) == "LOADPROGRAM"

    state = State((n for n in "LOADPROGRAM"), [])
    state.outbox = []
    state.regs = []
    return Level(state,"Nehmen Sie jedes Ding aus der INBOX und legen es in die OUTBOX",check)


def get_level_3():
    def check(state_to_test):
        return ''.join(map(str,state_to_test.outbox)) == "BUG"

    state = State(iter([-99,-99,-99,-99]), [])
    state.outbox = []
    state.regs = ['U', 'J', 'X', 'G', 'B', 'E']
    return Level(state,"Ignorieren Sie die INBOX erstmal und legen Sie die folgenden 3 Buchstaben in die OUTBOX: B U G ",check)


def get_level_4():
    def check(state_to_test):
        # 74OL74
        return ''.join(map(str,state_to_test.outbox)) == "74OL74"

    state = State((n for n in "47LO47"), [])
    state.outbox = []
    state.regs = []
    return Level(state,"Nehmen Si edie BEIDEN ersten Dinge aus der INBOX und legen Sie sie in umgekehrter Rewihenfolge in die OUTBOX. Wiederholen Sie, bis die INBOX leer ist.",check)