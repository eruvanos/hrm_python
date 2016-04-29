import unittest
import logging as log
from hrmengine import cpu, level
from hrmengine.cpu import ExecutionExceptin

log.basicConfig(level=log.INFO)


class Inbox(unittest.TestCase):
    def testInbox(self):
        inbox = iter([1])
        ops = [
            ["INBOX"]
        ]
        state = cpu.create_state(inbox, ops)
        state = cpu.tick(state)
        self.assertEqual(list(state.inbox), [])
        self.assertEqual(state.pointer, 1)
        self.assertEqual(state.pc, 1)

    def testInboxWithouPointerRaiseException(self):
        inbox = iter([])
        ops = [
            ["INBOX"]
        ]
        state = cpu.create_state(inbox, ops)
        with self.assertRaises(ExecutionExceptin):
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
        state = cpu.tick(state)

        state.pointer = "A"
        state = cpu.tick(state)

        self.assertEqual(list(state.outbox), [1, "A"])
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


class Add(unittest.TestCase):
    def testAdd(self):
        inbox = iter([])
        ops = [
            ["ADD", '0']
        ]
        state = cpu.create_state(inbox, ops)

        state.pointer = 1
        state.regs[0] = 2
        state = cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.pointer, 3)
        self.assertEqual(state.pc, 1)

    def testAddWithNegativeValue(self):
        inbox = iter([])
        ops = [
            ["ADD", '0']
        ]
        state = cpu.create_state(inbox, ops)

        state.pointer = 1
        state.regs[0] = -2
        state = cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.pointer, -1)
        self.assertEqual(state.pc, 1)

    def testAddWithoutPointerRaiseException(self):
        inbox = iter([])
        ops = [
            ["ADD", '0']
        ]
        state = cpu.create_state(inbox, ops)
        state.regs[0] = 2

        with self.assertRaises(ExecutionExceptin):
            cpu.tick(state)

    def testAddWithCharacter(self):
        inbox = iter([])
        ops = [
            ["ADD", '0']
        ]
        state = cpu.create_state(inbox, ops)
        state.pointer = 'A'
        state.regs[0] = 2

        with self.assertRaises(ExecutionExceptin):
            cpu.tick(state)


class Sub(unittest.TestCase):
    def testSub(self):
        inbox = iter([])
        ops = [
            ["SUB", '0']
        ]
        state = cpu.create_state(inbox, ops)

        state.pointer = 1
        state.regs[0] = 2
        state = cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.pointer, -1)
        self.assertEqual(state.pc, 1)

    def testSubWithNegativeValue(self):
        inbox = iter([])
        ops = [
            ["SUB", '0']
        ]
        state = cpu.create_state(inbox, ops)

        state.pointer = 1
        state.regs[0] = -2
        state = cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.pointer, 3)
        self.assertEqual(state.pc, 1)

    def testSubWithoutPointerRaiseException(self):
        inbox = iter([])
        ops = [
            ["SUB", '0']
        ]
        state = cpu.create_state(inbox, ops)
        state.regs[0] = 2

        with self.assertRaises(ExecutionExceptin):
            cpu.tick(state)

    def testSubWithNumberAndCharRaiseException(self):
        inbox = iter([])
        ops = [
            ["SUB", '0']
        ]
        state = cpu.create_state(inbox, ops)

        state.pointer = 1
        state.regs[0] = 'A'
        with self.assertRaises(ExecutionExceptin):
            cpu.tick(state)

    def testSubWithTwoEqualChars(self):
        inbox = iter([])
        ops = [
            ["SUB", '0']
        ]
        state = cpu.create_state(inbox, ops)

        state.pointer = 'A'
        state.regs[0] = 'A'
        state = cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.pointer, 0)
        self.assertEqual(state.pc, 1)

    def testSubWithSmallerChars(self):
        inbox = iter([])
        ops = [
            ["SUB", '0']
        ]
        state = cpu.create_state(inbox, ops)

        state.pointer = 'X'
        state.regs[0] = 'B'
        state = cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.pointer, 22)
        self.assertEqual(state.pc, 1)


class Bumpup(unittest.TestCase):
    def testBumpup(self):
        inbox = iter([])
        ops = [
            ["BUMPUP", '0']
        ]
        state = cpu.create_state(inbox, ops)

        state.regs[0] = 2
        state = cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.pointer, 3)
        self.assertEqual(state.regs[0], 3)
        self.assertEqual(state.pc, 1)

    def testBumpupWithoutValue(self):
        inbox = iter([])
        ops = [
            ["BUMPUP", '0']
        ]
        state = cpu.create_state(inbox, ops)

        with self.assertRaises(ExecutionExceptin):
            cpu.tick(state)

    def testBumpupWithCharacter(self):
        inbox = iter([])
        ops = [
            ["BUMPUP", '0']
        ]
        state = cpu.create_state(inbox, ops)
        state.regs = ['A']

        with self.assertRaises(ExecutionExceptin):
            cpu.tick(state)


class Bumpdn(unittest.TestCase):
    def testBumpdn(self):
        inbox = iter([])
        ops = [
            ["BUMPDN", '0']
        ]
        state = cpu.create_state(inbox, ops)

        state.regs[0] = 2
        state = cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.pointer, 1)
        self.assertEqual(state.regs[0], 1)
        self.assertEqual(state.pc, 1)

    def testBumpdnWithoutValue(self):
        inbox = iter([])
        ops = [
            ["BUMPDN", '0']
        ]
        state = cpu.create_state(inbox, ops)

        with self.assertRaises(ExecutionExceptin):
            cpu.tick(state)

    def testBumpdnWithCharacter(self):
        inbox = iter([])
        ops = [
            ["BUMPDN", '0']
        ]
        state = cpu.create_state(inbox, ops)
        state.regs = ['A']

        with self.assertRaises(ExecutionExceptin):
            cpu.tick(state)


class AllJumps(unittest.TestCase):
    def testJump(self):
        inbox = iter([])
        ops = [
            ["JUMP", 'a'],
            ["BUMPUP", '0'],
            ["a:"]
        ]
        state = cpu.create_state(inbox, ops)
        state.regs[0] = 0

        while state.pc != -1:
            state = cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.pointer, None)
        self.assertEqual(state.regs[0], 0)

    def testJumpWithoutLabel(self):
        inbox = iter([])
        ops = [
            ["JUMP", 'a'],
        ]
        state = cpu.create_state(inbox, ops)

        with self.assertRaises(ExecutionExceptin):
            cpu.tick(state)

    def testJumpzGreaterNull(self):
        inbox = iter([])
        ops = [
            ["JUMPZ", 'a'],
            ["BUMPUP", '0'],
            ["a:"],
        ]

        state = cpu.create_state(inbox, ops)
        state.pointer = 1
        state.regs[0] = 0

        while state.pc != -1:
            state = cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.regs[0], 1)

    def testJumpzLessNull(self):
        inbox = iter([])
        ops = [
            ["JUMPZ", 'a'],
            ["BUMPUP", '0'],
            ["a:"],
        ]

        state = cpu.create_state(inbox, ops)
        state.pointer = -1
        state.regs[0] = 0

        while state.pc != -1:
            state = cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.regs[0], 1)

    def testJumpzIsNull(self):
        inbox = iter([])
        ops = [
            ["JUMPZ", 'a'],
            ["BUMPUP", '0'],
            ["a:"],
        ]

        state = cpu.create_state(inbox, ops)
        state.pointer = 0
        state.regs[0] = 0

        while state.pc != -1:
            state = cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.regs[0], 0)

    def testJumpnGreaterNull(self):
        inbox = iter([])
        ops = [
            ["JUMPN", 'a'],
            ["BUMPUP", '0'],
            ["a:"],
        ]

        state = cpu.create_state(inbox, ops)
        state.pointer = 1
        state.regs[0] = 0

        while state.pc != -1:
            state = cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.regs[0], 1)

    def testJumpnLessNull(self):
        inbox = iter([])
        ops = [
            ["JUMPN", 'a'],
            ["BUMPUP", '0'],
            ["a:"],
        ]

        state = cpu.create_state(inbox, ops)
        state.pointer = -1
        state.regs[0] = 0

        while state.pc != -1:
            state = cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.regs[0], 0)

    def testJumpnIsNull(self):
        inbox = iter([])
        ops = [
            ["JUMPN", 'a'],
            ["BUMPUP", '0'],
            ["a:"],
        ]

        state = cpu.create_state(inbox, ops)
        state.pointer = 0
        state.regs[0] = 0

        while state.pc != -1:
            state = cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.regs[0], 1)

class CopyFromTo(unittest.TestCase):
    def testCopyFromToWithNormalIndex(self):
        inbox = iter([])
        ops = [
            ["COPYFROM", '0'],
            ["COPYTO", '1']
        ]

        state = cpu.create_state(inbox, ops)
        state.regs[0] = 2

        while state.pc != -1:
            state = cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.regs[0], 2)
        self.assertEqual(state.regs[1], 2)

    def testCopyFromToWithNormalRef(self):
        inbox = iter([])
        ops = [
            ["COPYFROM", '[5]'],
            ["COPYTO", '[6]']
        ]

        state = cpu.create_state(inbox, ops)
        state.regs[0] = 2
        state.regs[5] = 0
        state.regs[6] = 1

        while state.pc != -1:
            state = cpu.tick(state)

        self.assertEqual(list(state.outbox), [])
        self.assertEqual(state.regs[0], 2)
        self.assertEqual(state.regs[1], 2)


class Tick(unittest.TestCase):
    def test_tick_return_new_state(self):
        inbox = iter([])
        ops = [
            ["BUMPUP", '3']
        ]
        state = cpu.create_state(inbox, ops)
        state.regs[3] = 4

        new_state = cpu.tick(state)

        self.assertNotEquals(state.pointer, new_state.pointer)
        self.assertNotEquals(state.regs[3], new_state.regs[3])
        self.assertNotEquals(str(state), str(new_state))

    def test_state_contains_prev_state(self):
        inbox = iter([])
        ops = [
            ["BUMPUP", '3']
        ]
        state = cpu.create_state(inbox, ops)
        state.regs[3] = 4

        new_state = cpu.tick(state)

        self.assertEquals(state.prev_state, None)
        self.assertEquals(state, new_state.prev_state)


class Level(unittest.TestCase):
    def test_level_mechanic(self):
        state = cpu.create_state(iter([]), [])

        test_level = level.get_test_level()
        self.assertTrue(test_level.check_function(state))

    def test_level_1(self):
        state = cpu.create_state(iter([]), [])

        l = level.get_level_1()
        self.assertFalse(l.check_function(state))

        state.outbox = [6, 7, 6]
        self.assertTrue(l.check_function(state))

        state.outbox = [6, 7, 6, 7]
        self.assertFalse(l.check_function(state))

    def test_level_2(self):
        state = cpu.create_state(iter([]), [])

        l = level.get_level_2()
        self.assertFalse(l.check_function(state))

        state.outbox = (n for n in "LOADPROGRAM")
        self.assertTrue(l.check_function(state))

        state.outbox = [6, 7, 6, 7]
        self.assertFalse(l.check_function(state))

    def test_level_3(self):
        state = cpu.create_state(iter([]), [])

        l = level.get_level_3()
        self.assertFalse(l.check_function(state))

        state.outbox = (n for n in "BUG")
        self.assertTrue(l.check_function(state))

        state.outbox = [6, 7, 6, 7]
        self.assertFalse(l.check_function(state))

    def test_level_4(self):
        state = cpu.create_state(iter([]), [])

        l = level.get_level_4()
        self.assertFalse(l.check_function(state))

        state.outbox = (n for n in "74OL74")
        self.assertTrue(l.check_function(state))

        state.outbox = [6, 7, 6, 7]
        self.assertFalse(l.check_function(state))
