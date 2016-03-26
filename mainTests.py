import unittest
import logging as log
from hrmengine import cpu
from hrmengine.cpu import ExecutionExceptin

log.basicConfig(level=log.INFO)


class Inbox(unittest.TestCase):
    def testInbox(self):
        inbox = iter([1])
        ops = [
            ["INBOX"]
        ]
        state = cpu.create_state(inbox, ops)
        cpu.tick(state)
        self.assertEqual(list(state.inbox), [])
        self.assertEqual(state.pointer, 1)
        self.assertEqual(state.pc, 1)

    def testInboxWithouPointerRaiseException(self):
        inbox = iter([])
        ops = [
            ["INBOX"]
        ]
        state = cpu.create_state(inbox, ops)
        with self.assertRaises(StopIteration):
            cpu.tick(state)


class Outbox(unittest.TestCase):
    def testOutbox(self):
        inbox = iter([1])
        ops = [
            ["OUTBOX"],
            ["OUTBOX"]
        ]
        state = cpu.create_state(inbox, ops)

        state.pointer = 1
        cpu.tick(state)

        state.pointer = "A"
        cpu.tick(state)

        self.assertEqual(list(state.outbox), [1,"A"])
        self.assertEqual(state.pointer, None)
        self.assertEqual(state.pc, 2)

    def testOutboxWithoutPointerRaiseException(self):
        inbox = iter([])
        ops = [
            ["OUTBOX"]
        ]
        state = cpu.create_state(inbox, ops)
        with self.assertRaises(ExecutionExceptin):
            cpu.tick(state)

        self.assertEqual(state.outbox, [])


class Add(unittest.TestCase):
    def testAdd(self):
        inbox = iter([])
        ops = [
            ["ADD",'0']
        ]
        state = cpu.create_state(inbox, ops)

        state.pointer = 1
        state.regs[0] = 2
        cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.pointer, 3)
        self.assertEqual(state.pc, 1)

    def testAddWithNegativeValue(self):
        inbox = iter([])
        ops = [
            ["ADD",'0']
        ]
        state = cpu.create_state(inbox, ops)

        state.pointer = 1
        state.regs[0] = -2
        cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.pointer, -1)
        self.assertEqual(state.pc, 1)

    def testAddWithoutPointerRaiseException(self):
        inbox = iter([])
        ops = [
            ["ADD",'0']
        ]
        state = cpu.create_state(inbox, ops)
        state.regs[0] = 2

        with self.assertRaises(ExecutionExceptin):
            cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.pointer, None)
        self.assertEqual(state.pc, 0)


class Sub(unittest.TestCase):
    def testSub(self):
        inbox = iter([])
        ops = [
            ["SUB",'0']
        ]
        state = cpu.create_state(inbox, ops)

        state.pointer = 1
        state.regs[0] = 2
        cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.pointer, -1)
        self.assertEqual(state.pc, 1)

    def testSubWithNegativeValue(self):
        inbox = iter([])
        ops = [
            ["SUB",'0']
        ]
        state = cpu.create_state(inbox, ops)

        state.pointer = 1
        state.regs[0] = -2
        cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.pointer, 3)
        self.assertEqual(state.pc, 1)

    def testSubWithoutPointerRaiseException(self):
        inbox = iter([])
        ops = [
            ["SUB",'0']
        ]
        state = cpu.create_state(inbox, ops)
        state.regs[0] = 2

        with self.assertRaises(ExecutionExceptin):
            cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.pointer, None)
        self.assertEqual(state.pc, 0)


class Bumpup(unittest.TestCase):
    def testBumpup(self):
        inbox = iter([])
        ops = [
            ["BUMPUP",'0']
        ]
        state = cpu.create_state(inbox, ops)

        state.regs[0] = 2
        cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.pointer, 3)
        self.assertEqual(state.regs[0], 3)
        self.assertEqual(state.pc, 1)

    def testBumpupWithoutValue(self):
        inbox = iter([])
        ops = [
            ["BUMPUP",'0']
        ]
        state = cpu.create_state(inbox, ops)

        with self.assertRaises(ExecutionExceptin):
            cpu.tick(state)

        self.assertEqual(state.regs[0], None)


class Bumpdn(unittest.TestCase):
    def testBumpdn(self):
        inbox = iter([])
        ops = [
            ["BUMPDN",'0']
        ]
        state = cpu.create_state(inbox, ops)

        state.regs[0] = 2
        cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.pointer, 1)
        self.assertEqual(state.regs[0], 1)
        self.assertEqual(state.pc, 1)

    def testBumpdnWithoutValue(self):
        inbox = iter([])
        ops = [
            ["BUMPDN",'0']
        ]
        state = cpu.create_state(inbox, ops)

        with self.assertRaises(ExecutionExceptin):
            cpu.tick(state)

        self.assertEqual(state.regs[0], None)


class AllJumps(unittest.TestCase):
    def testJump(self):
        inbox = iter([])
        ops = [
            ["JUMP",'a'],
            ["BUMPUP",'0'],
            ["a:"]
        ]
        state = cpu.create_state(inbox, ops)
        state.regs[0] = 0

        while cpu.tick(state) != -1:
            pass

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.pointer, None)
        self.assertEqual(state.regs[0], 0)

    def testJumpWithoutLabel(self):
        inbox = iter([])
        ops = [
            ["JUMP",'a'],
        ]
        state = cpu.create_state(inbox, ops)

        with self.assertRaises(ExecutionExceptin):
            cpu.tick(state)

    def testJumpzGreaterNull(self):
        inbox = iter([])
        ops = [
            ["JUMPZ",'a'],
            ["BUMPUP",'0'],
            ["a:"],
        ]

        state = cpu.create_state(inbox, ops)
        state.pointer = 1
        state.regs[0] = 0

        while cpu.tick(state) != -1:
            pass

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.regs[0], 1)

    def testJumpzLessNull(self):
        inbox = iter([])
        ops = [
            ["JUMPZ",'a'],
            ["BUMPUP",'0'],
            ["a:"],
        ]

        state = cpu.create_state(inbox, ops)
        state.pointer = -1
        state.regs[0] = 0

        while cpu.tick(state) != -1:
            pass

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.regs[0], 1)

    def testJumpzIsNull(self):
        inbox = iter([])
        ops = [
            ["JUMPZ",'a'],
            ["BUMPUP",'0'],
            ["a:"],
        ]

        state = cpu.create_state(inbox, ops)
        state.pointer = 0
        state.regs[0] = 0

        while cpu.tick(state) != -1:
            pass

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.regs[0], 0)

    def testJumpnGreaterNull(self):
        inbox = iter([])
        ops = [
            ["JUMPN",'a'],
            ["BUMPUP",'0'],
            ["a:"],
        ]

        state = cpu.create_state(inbox, ops)
        state.pointer = 1
        state.regs[0] = 0

        while cpu.tick(state) != -1:
            pass

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.regs[0], 1)

    def testJumpnLessNull(self):
        inbox = iter([])
        ops = [
            ["JUMPN",'a'],
            ["BUMPUP",'0'],
            ["a:"],
        ]

        state = cpu.create_state(inbox, ops)
        state.pointer = -1
        state.regs[0] = 0

        while cpu.tick(state) != -1:
            pass

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.regs[0], 0)

    def testJumpnIsNull(self):
        inbox = iter([])
        ops = [
            ["JUMPN",'a'],
            ["BUMPUP",'0'],
            ["a:"],
        ]

        state = cpu.create_state(inbox, ops)
        state.pointer = 0
        state.regs[0] = 0

        while cpu.tick(state) != -1:
            pass

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.regs[0], 1)

    def testCopyFromToWithNormalIndex(self):
        inbox = iter([])
        ops = [
            ["COPYFROM",'0'],
            ["COPYTO",'1']
        ]

        state = cpu.create_state(inbox, ops)
        state.regs[0] = 2

        while cpu.tick(state) != -1:
            pass

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.regs[0], 2)
        self.assertEqual(state.regs[1], 2)

    def testCopyFromToWithNormalRef(self):
        inbox = iter([])
        ops = [
            ["COPYFROM",'[5]'],
            ["COPYTO",'[6]']
        ]

        state = cpu.create_state(inbox, ops)
        state.regs[0] = 2
        state.regs[5] = 0
        state.regs[6] = 1

        while cpu.tick(state) != -1:
            pass

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.regs[0], 2)
        self.assertEqual(state.regs[1], 2)