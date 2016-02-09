import logging as log

pointer = None
regs = [None] * 14
code = []
inbox = None
pc = 0

def getRegIndexToRef(ref):
    if ref.startswith('['):
        return int(regs[int(ref[1:-1])])
    else:
        return int(ref)


def exeInbox(params):
    global pointer
    pointer = inbox.__next__()


def exeOutbox(params):
    print(pointer)


def exeCopyfrom(params):
    #log.warning("Function not implemented! Skip")
    index = getRegIndexToRef(params[0])
    pointer = regs[index]


def exeCopyto(params):
    # log.warning("Function not implemented! Skip")
    index = getRegIndexToRef(params[0])
    regs[index] = pointer


def exeAdd(params):
#    log.warning("Function not implemented! Skip")
    index = getRegIndexToRef(params[0])
    pointer = pointer + regs[index]
    #TODO nicht sicher wie das  programm arbeitet
    #regs[index] = pointer

def exeSub(params):
    #log.warning("Function not implemented! Skip")
    index = getRegIndexToRef(params[0])
    pointer = pointer - regs[index]
    #TODO nicht sicher wie das  programm arbeitet
    #regs[index] = pointer


def exeBumpup(params):
    #log.warning("Function not implemented! Skip")
    index = getRegIndexToRef(params[0])
    regs[index] += 1
    pointer = regs[index]

def exeBumpdn(params):
    #log.warning("Function not implemented! Skip")
    index = getRegIndexToRef(params[0])
    regs[index] -= 1
    pointer = regs[index]


def exeJump(params):
    return list(map(lambda x: x[0], code)).index(params[0]+':')


def exeJumpz(params):
    if pointer == 0:
        return list(map(lambda x: x[0], code)).index(params[0]+':')


def exeJumpn(params):
    if pointer != 0:
        return list(map(lambda x: x[0], code)).index(params[0]+':')

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


def tick():
    global pc
    if(pc >= len(code) or pc < 0):
        return -1
    else:
        log.debug('')
        log.debug("### PC:{}".format(pc))

        command = code[pc]
        op = command[0]

        if isLabel(op):
            log.debug("Skip {}".format(op))
            pass
        else:
            params = []
            if len(command) > 1:
                params = command[1:]

            log.debug("Execute {} with params {}".format(op, pc, params))
            nextPC = exes[op](params)

            log.debug("pointer: {}".format(pointer))
            log.debug("reg state: {}".format(regs))
            if nextPC is not None:
                pc = nextPC
                return

        pc += 1
