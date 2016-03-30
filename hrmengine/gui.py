from tkinter import *
from hrmengine import cpu

__inboxItemFrame = Frame
__outboxItemFrame = Frame
__regItemframe = Frame
__pointerFrame = Frame
__code_item_frame = Frame

__tick_button = Button
__prev_button = Button


def main(state):
    root = Tk()
    root.title("HRM P3")
    root.minsize(width=500, height=500)

    # Title
    title = Label(root, text="Human Resource Machine in Python", font="times 50")
    title.pack()

    # INBOX
    inboxFrame = Frame(root, bd=1, relief=SOLID)
    inboxFrame.pack(side=LEFT, fill=Y)
    Label(inboxFrame, text="INBOX").pack()
    global __inboxItemFrame
    __inboxItemFrame = Frame(inboxFrame)
    __inboxItemFrame.pack()

    # Code
    codeFrame = Frame(root, bd=1, relief=SOLID)
    codeFrame.pack(side=RIGHT, fill=Y)
    Label(codeFrame, text="Code", width=20).pack(side=TOP)
    global __code_item_frame
    __code_item_frame = Frame(codeFrame, bd=1, relief=SOLID)
    __code_item_frame.pack(fill=X)

    # Space
    LabelFrame(root, width=2, bg="white").pack(side=RIGHT, fill=Y)

    # OUTBOX
    outboxFrame = Frame(root, bd=1, relief=SOLID)
    outboxFrame.pack(side=RIGHT, fill=Y)
    Label(outboxFrame, text="OUTBOX").pack()
    global __outboxItemFrame
    __outboxItemFrame = Frame(outboxFrame)
    __outboxItemFrame.pack(fill=X)

    # Pointer
    global __pointerFrame
    __pointerFrame = Label(root, bd=1, relief=SOLID)
    __pointerFrame.pack(fill=X)

    # Reg Frame
    regFrame = Frame(root, bd=1, relief=SOLID)
    regFrame.pack(fill=BOTH)
    Label(regFrame, text="REGISTER", font="times 15").pack()
    global __regItemframe
    __regItemframe = Frame(regFrame)
    __regItemframe.pack()

    # Actions
    actionsFrame = Frame(root, bd=1, relief=SOLID)
    actionsFrame.pack(side=BOTTOM)
    global __prev_button
    __prev_button = Button(actionsFrame, text='Prev')
    __prev_button.pack(side=LEFT)
    global __tick_button
    __tick_button = Button(actionsFrame, text='Next')
    __tick_button.pack(side=LEFT)

    # Update with State
    update(state)

    root.mainloop()


def update(state):
    _update_inbox_frame(state)
    _update_outbox_frame(state)
    _update_reg_frame(state)
    _update_pointer_Frame(state)
    _update_code_frame(state)
    _update_actions(state)


def _update_inbox_frame(state):
    __clear_children(__inboxItemFrame)

    peek = list(state.inbox)
    state.inbox = iter(peek)
    for i in peek:
        Label(__inboxItemFrame, text=i).pack()


def _update_outbox_frame(state):
    __clear_children(__outboxItemFrame)

    for i in state.outbox:
        Label(__outboxItemFrame, text=i).pack()


def _update_reg_frame(state):
    __clear_children(__regItemframe)

    for i in state.regs:
        if i is None:
            i = "-"
        Label(__regItemframe, text=i, width=2, bd=2, relief=RAISED).pack(side=LEFT, padx=3)


def _update_pointer_Frame(state):
    __pointerFrame.configure(text="Pointer: {}".format(state.pointer))


def _update_code_frame(state):
    __clear_children(__code_item_frame)

    for index, c in enumerate(state.code, start=0):

        container = Frame(__code_item_frame, bd=1, relief=SOLID)
        container.pack(fill=BOTH)

        Label(container, text=c[0], width=8, anchor=W).pack(side=LEFT)
        if len(c) > 1:
            Label(container, text=c[1], width=3).pack(side=LEFT, fill=X)

        if index == state.pc:
            Label(container, text="x").pack(side=RIGHT)


def _update_actions(state):
    __tick_button.configure(command=lambda: update(cpu.tick(state)))
    __prev_button.configure(command=lambda: update(state.prev_state))


def __clear_children(widget):
    for s in widget.pack_slaves():
        s.pack_forget()


if __name__ == "__main__":
    inbox = iter([1, 2, 3, 4, 5, 6])
    ops = [
        ["BUMPUP", '0'],
        ["OUTBOX", '0'],
        ["a:"],
        ["INBOX"],
        ["OUTBOX"],
        ["JUMP", "a"]
    ]

    state = cpu.create_state(inbox, ops)

    state.pointer = 1
    state.regs[0] = 1
    state.outbox = [1, 2, 3, 4]

    main(state)
