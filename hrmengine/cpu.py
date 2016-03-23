import logging as log


class State:
    def __init__(self, inbox, code):
        self.inbox = inbox
        self.code = code
        self.regs = [None] * 14
        self.pointer = None
        self.outbox = []
        self.pc = 0


class ExecutionExceptin(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def getRegIndexToRef(ref, regs):
    if ref.startswith('['):
        return int(regs[int(ref[1:-1])])
    else:
        return int(ref)


def exeInbox(state, params):
    state.pointer = state.inbox.__next__()


def exeOutbox(state, params):
    if state.pointer is None:
        raise ExecutionExceptin("OUTBOX without value pointer")
    state.outbox.append(state.pointer)
    state.pointer = None


def exeCopyfrom(state, params):
    index = getRegIndexToRef(params[0], state.regs)
    state.pointer = state.regs[index]


def exeCopyto(state, params):
    index = getRegIndexToRef(params[0], state.regs)
    state.regs[index] = state.pointer


def exeAdd(state, params):
    index = getRegIndexToRef(params[0], state.regs)
    state.pointer = state.pointer + state.regs[index]


def exeSub(state, params):
    index = getRegIndexToRef(params[0], state.regs)
    state.pointer = state.pointer - state.regs[index]


def exeBumpup(state, params):
    index = getRegIndexToRef(params[0], state.regs)
    state.regs[index] += 1
    state.pointer = state.regs[index]


def exeBumpdn(state, params):
    index = getRegIndexToRef(params[0], state.regs)
    state.regs[index] -= 1
    state.pointer = state.regs[index]


def exeJump(state, params):
    return list(map(lambda x: x[0], state.code)).index(params[0] + ':')


def exeJumpz(state, params):
    if state.pointer == 0:
        return list(map(lambda x: x[0], state.code)).index(params[0] + ':')


def exeJumpn(state, params):
    if state.pointer < 0:
        return list(map(lambda x: x[0], state.code)).index(params[0] + ':')


def isLabel(str):
    return str.endswith(':')


exes = {
    'INBOX': exeInbox,
    'OUTBOX': exeOutbox,
    'COPYFROM': exeCopyfrom,
    'COPYTO': exeCopyto,
    'ADD': exeAdd,
    'SUB': exeSub,
    'BUMPUP': exeBumpup,
    'BUMPDN': exeBumpdn,
    'JUMP': exeJump,
    'JUMPZ': exeJumpz,
    'JUMPN': exeJumpn
}
knownOps = exes.keys()


def create_state(inbox, code):
    return State(inbox, code)


def tick(state):
    if (state.pc >= len(state.code) or state.pc < 0):
        return -1
    else:
        log.debug('')
        log.debug("### PC:{}".format(state.pc))

        command = state.code[state.pc]
        op = command[0]

        if isLabel(op):
            log.debug("Skip {}".format(op))
            pass
        else:
            params = []
            if len(command) > 1:
                params = command[1:]

            log.debug("Execute {} with params {}".format(op, state.pc, params))
            nextPC = exes[op](state, params)

            log.debug("pointer: {}".format(state.pointer))
            log.debug("reg state: {}".format(state.regs))
            if nextPC is not None:
                state.pc = nextPC
                return

        state.pc += 1
