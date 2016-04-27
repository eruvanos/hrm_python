import hrmengine.cpu as cpu
import logging as log


def _to_op(string):
    string = string.split(' ')
    return list(filter(lambda l: l != '', string))


def is_known_op(opcode):
    """
    Checks if the given op is in knownOps or ends with ':'

    :param opcode: Operation without arguments like 'BUMP'
    :return: True or False
    """
    return opcode in cpu.knownOps or opcode.endswith(':')


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


def _read_file(filepath):
    # read file:
    with open(filepath) as f:
        lines = f.readlines()
    # trim
    lines = list(map(lambda x: x.strip(), lines))
    # filter empty
    return list(filter(lambda x: len(x) > 0, lines))


def _read_string(clipboard_string):
    # split lines (detecting linebreaks from hrm format)
    line_break = "\n"
    if "\r\n" in clipboard_string:
        line_break = "\r\n"
    lines = clipboard_string.split(line_break)
    # trim
    lines = list(map(lambda x: x.strip(), lines))
    # filter empty
    return list(filter(lambda x: len(x) > 0, lines))


def _convert_to_ops(lines):
    # split command and parameter
    ops = list(map(_to_op, lines))
    # filter unknown ops
    return list(filter(lambda op: is_known_op(op[0]), ops))


def parse_file(filepath):
    """
    Parses a file and convert it to a list of ops like
    [['BUMPUP','[1]']]

    :return: list of operations ['opcode'(,'arg')]
    """
    lines = _read_file(filepath)
    return _convert_to_ops(lines)


def parse_clipboard_string(clipboard_string):
    """
    Parses the string (normally from clipboard) and convert it to a list of ops like
    [['BUMPUP','[1]']]

    :return: list of operations ['opcode'(,'arg')]
    """
    lines = _read_string(clipboard_string)
    return _convert_to_ops(lines)


def main(filepath):
    ops = parse_file(filepath)
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
