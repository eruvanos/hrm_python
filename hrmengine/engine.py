import hrmengine.cpu as cpu
import logging as log

def toOp(string):
    string = string.split(' ')
    return list(filter(lambda l: l != '', string))

def isKnownOp(op):
    return op in cpu.knownOps or op.endswith(':')

def readFile(file):
    # read file:
    with open(file) as f:
        lines = f.readlines()
    #trim
    lines = list(map(lambda x:x.strip(), lines))
    #filter empty
    return list(filter(lambda x: len(x) > 0, lines))


def convertToOps(lines):
    # split command and parameter
    ops = list(map(toOp, lines))
    # filter unknown ops
    return list(filter(lambda op: isKnownOp(op[0]), ops))


def main(filepath):
    lines = readFile(filepath)
    ops = convertToOps(lines)
    state = cpu.create_state((n for n in "0123"), ops)

    while cpu.tick(state) != -1:
        pass

    print("Result:")
    print(state.outbox)

if __name__ == "__main__":
    log.basicConfig(level=log.DEBUG)
    main("../resources/demo.txt")
    # main("../resources/dummy.txt")
    # main("../resources/justPrint.txt")
