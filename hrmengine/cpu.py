import logging as log
from copy import deepcopy


class State:
    def __init__(self, inbox, code):
        self.inbox = inbox
        self.code = code
        self.regs = [None] * 14
        self.pointer = None
        self.outbox = []
        self.pc = 0
        self.prev_state = None


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
        raise ExecutionExceptin("OUTBOX without pointer")
    state.outbox.append(state.pointer)
    state.pointer = None


def exeCopyfrom(state, params):
    index = getRegIndexToRef(params[0], state.regs)
    state.pointer = state.regs[index]


def exeCopyto(state, params):
    index = getRegIndexToRef(params[0], state.regs)
    state.regs[index] = state.pointer


def exeAdd(state, params):
    if state.pointer is None:
        raise ExecutionExceptin("ADD without pointer")
    index = getRegIndexToRef(params[0], state.regs)
    state.pointer = state.pointer + state.regs[index]


def exeSub(state, params):
    if state.pointer is None:
        raise ExecutionExceptin("Sub without pointer")
    index = getRegIndexToRef(params[0], state.regs)
    state.pointer = state.pointer - state.regs[index]


def exeBumpup(state, params):
    index = getRegIndexToRef(params[0], state.regs)

    if state.regs[index] is None:
        raise ExecutionExceptin("Reg doesn't contain a value")

    state.regs[index] += 1
    state.pointer = state.regs[index]


def exeBumpdn(state, params):
    index = getRegIndexToRef(params[0], state.regs)

    if state.regs[index] is None:
        raise ExecutionExceptin("Reg doesn't contain a value")

    state.regs[index] -= 1
    state.pointer = state.regs[index]


def exeJump(state, params):
    label = params[0] + ':'
    code_list = list(map(lambda x: x[0], state.code))

    if label not in code_list:
        raise ExecutionExceptin("Label for target not found")
    return code_list.index(label)


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


def tick(given_state):
    state = deepcopy(given_state)
    state.prev_state = given_state

    if state.pc >= len(state.code) or state.pc < 0:
        state.pc = -1
        return state
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

            if op not in exes:
                raise ExecutionExceptin("Unkown command " + op)

            log.debug("Execute {} with params {}".format(op, state.pc, params))
            nextPC = exes[op](state, params)

            log.debug("pointer: {}".format(state.pointer))
            log.debug("reg state: {}".format(state.regs))
            if nextPC is not None:
                state.pc = nextPC
                return state

        state.pc += 1
        return state
