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

    def testInboxWithoutValues(self):
        inbox = iter([])
        ops = [
            ["INBOX"]
        ]
        state = cpu.create_state(inbox, ops)
        try:
            cpu.tick(state)
        except StopIteration:
            return
        self.fail("StopIterator was expected when reading from inbox without any value in inbox")

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

    def testOutboxWithoutValues(self):
        inbox = iter([])
        ops = [
            ["OUTBOX"]
        ]
        state = cpu.create_state(inbox, ops)
        try:
            cpu.tick(state)
        except ExecutionExceptin:
            self.assertEqual(state.outbox, [])
            return

        self.fail("ExecutionExceptin was expected when writing to outbox without any value in pointer")
