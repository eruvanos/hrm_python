import cpuEmulator as cpu
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


def main():
    lines = readFile("../resources/demo.txt")
    # lines = readFile("../resources/dummy.txt")
    # lines = readFile("../resources/justPrint.txt")
    ops = convertToOps(lines)

    cpu.code = ops
    cpu.inbox = (n for n in "0123")

    while cpu.tick() != -1:
        pass


log.basicConfig(level=log.DEBUG)
main()