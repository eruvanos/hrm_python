from tkinter import *

from hrmengine import cpu

__inboxItemFrame = Frame
__outboxItemFrame = Frame
__regItemframe = Frame
__pointerFrame = Frame
__code_items = Text

__edit_mode = True

__actions_frame = Frame

__message_label = Label

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
    global __code_items
    __code_items = Text(codeFrame, width=15, bd=1, relief=SOLID)
    __code_items.pack(fill=X)

    # Space
    LabelFrame(root, width=2, bg="white").pack(side=RIGHT, fill=Y)

    # OUTBOX
    outboxFrame = Frame(root, bd=1, relief=SOLID)
    outboxFrame.pack(side=RIGHT, fill=Y)
    Label(outboxFrame, text="OUTBOX").pack()
    global __outboxItemFrame
    __outboxItemFrame = Text(outboxFrame)
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
    global __actions_frame
    __actions_frame = Frame(root, bd=1, relief=SOLID)
    __actions_frame.pack(side=BOTTOM)


    # Message
    message_frame = Frame(root, bd=1, relief=SOLID)
    message_frame.pack(side=BOTTOM, fill=X)
    global __message_label
    __message_label = Label(message_frame, text="")
    __message_label.pack()

    # Update with State
    update(state)

    root.mainloop()


def _show_error(error):
    pass


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

    __code_items. configure(state=NORMAL)
    __code_items.delete(0.0,END)
    for index, c in enumerate(state.code, start=0):

        if not __edit_mode:
            if index == state.pc:
                __code_items.insert(END, "x ")
            else:
                __code_items.insert(END, "  ")

        __code_items.insert(END, c[0])
        if len(c) > 1:
            __code_items.insert(END, " " + c[1])

        __code_items.insert(END, "\n")

    if __edit_mode:
        __code_items. configure(state=NORMAL)
    else:
        __code_items. configure(state=DISABLED)


def _update_actions(state):
    __clear_children(__actions_frame)

    #Prev
    prev_button = Button(__actions_frame, text='Prev', command=lambda: update(state.prev_state))
    prev_button.pack(side=LEFT)
    if state.prev_state is None:
        prev_button.configure(state=DISABLED)

    #Stop
    def find_first_state(state):
        if state.prev_state is not None:
            return find_first_state(state.prev_state)
        else:
            return state

    def stop():
        global __edit_mode
        __edit_mode = True
        update(find_first_state(state))

    reset_button = Button(__actions_frame, text='Stop', command=lambda: stop())
    if not __edit_mode:
        reset_button.pack(side=LEFT)

    #Start
    def start():
        global __edit_mode
        __edit_mode = False
        update(state)
    start_button = Button(__actions_frame, text='Start', command=lambda: start())
    if __edit_mode:
        start_button.pack(side=LEFT)


    #Start/Next
    def execute_tick(state):
        try:
            update(cpu.tick(state))
        except Exception as e:
            global __message_label
            __message_label.configure(text="Error")

    tick_button = Button(__actions_frame, text="Next", command=lambda: execute_tick(state))
    tick_button.pack(side=LEFT)
    if __edit_mode:
        tick_button.configure(state=DISABLED)



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
