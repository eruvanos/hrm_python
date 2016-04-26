import hrmengine.cpu as cpu
import logging as log


def to_op(string):
    string = string.split(' ')
    return list(filter(lambda l: l != '', string))


def is_known_op(op):
    """
    Checks if the given op is in knownOps or ends with ':'

    :param op: Operation without arguments like 'BUMP'
    :return: True or False
    """
    return op in cpu.knownOps or op.endswith(':')


def needs_param(opcode):
    return opcode not in ['INBOX', 'OUTBOX'] and not opcode.endswith(":")


def is_valid_op(op):
    """
    Checks the given op if it is valid

    :param op: [opcode, param]
    :return: True if given op is valid
    """
    if len(op) == 0 or not is_known_op(op[0]):
        return False

    if needs_param(op[0]) and len(op) == 2:
        return True
    elif not needs_param(op[0]) and len(op) == 1:
        return True
    else:
        return False


def readFile(filepath):
    # read file:
    with open(filepath) as f:
        lines = f.readlines()
    # trim
    lines = list(map(lambda x: x.strip(), lines))
    # filter empty
    return list(filter(lambda x: len(x) > 0, lines))


def convertToOps(lines):
    # split command and parameter
    ops = list(map(to_op, lines))
    # filter unknown ops
    return list(filter(lambda op: is_known_op(op[0]), ops))

def parseFile(filepath):
    """
    Parses a file and convert it to a list of ops like
    [['BUMPUP','[1]']]

    :return: list of operations ['opcode'(,'arg')]
    """
    lines = readFile(filepath)
    return convertToOps(lines)


def main(filepath):
    ops = parseFile(filepath)
    inbox = (n for n in "0123")
    state = cpu.create_state(inbox, ops)

    while cpu.tick(state) != -1:
        pass

    print("Result:")
    print(state.outbox)


if __name__ == "__main__":
    log.basicConfig(level=log.DEBUG)
    main("../resources/demo.txt")
    # main("../resources/dummy.txt")
    # main("../resources/justPrint.txt")
