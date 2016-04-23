from tkinter import *

from hrmengine import cpu, parser
from hrmengine.level import levels

__inboxItemFrame = Frame
__outboxItemFrame = Frame
__regItemframe = Frame
__pointerFrame = Frame
__code_items = Text
__actions_frame = Frame
__message_label = Label
__welcome_text = LabelFrame

__edit_mode = True

def main(state):
    root = Tk()
    root.title("HRM P3")
    root.minsize(width=500, height=500)

    def hello():
        print("hello!")

    # Menubar
    menubar = Menu(root)
    levelmenu = Menu(menubar, tearoff=0)

    def load_level_data(level):
        return lambda: load_level(levels[level]())

    for l in range(1, len(levels)+1):
        levelmenu.add_command(label="Level %s" % l, command=load_level_data('level%s' % l))
    menubar.add_cascade(label="Load Level", menu=levelmenu)
    root.config(menu=menubar)

    # Title
    title = Label(root, text="Human Resource Machine in Python", font="times 40")
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
    __code_items.bind('<<Modified>>', lambda e: __render_highlighting(e))

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
    global __actions_frame
    __actions_frame = Frame(root, bd=1, relief=SOLID)
    __actions_frame.pack(side=BOTTOM)

    # Message
    message_frame = Frame(root, bd=1, relief=SOLID)
    message_frame.pack(side=BOTTOM, fill=X)
    global __message_label
    __message_label = Label(message_frame, text="")
    __message_label.pack()

    # Welcome/Level text
    global __welcome_text
    welcome_frame = Frame(root, bd=1, relief=SOLID).pack(side=BOTTOM)
    __welcome_text = Message(welcome_frame, text="No level loaded.", width=350)
    __welcome_text.pack(side=BOTTOM)

    # Update with State
    update(state)

    root.mainloop()


def _show_error(error):
    __message_label.configure(text=error)


def load_level(level):
    __welcome_text.configure(text=level.welcome_message)
    update(level.state)


def update(state):
    _update_inbox_frame(state)
    _update_outbox_frame(state)
    _update_reg_frame(state)
    _update_pointer_frame(state)
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


def _update_pointer_frame(state):
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
        _show_error("")
        update(find_first_state(state))

    reset_button = Button(__actions_frame, text='Stop', command=lambda: stop())
    if not __edit_mode:
        reset_button.pack(side=LEFT)

    #Start
    def start():
        global __edit_mode
        __edit_mode = False

        codeLines = __code_items.get("1.0", END).split("\n")
        codeLines = filter(lambda line: len(line) > 0, codeLines)
        state.code = parser.convertToOps(codeLines)

        update(state)
    start_button = Button(__actions_frame, text='Start', command=lambda: start())
    if __edit_mode:
        start_button.pack(side=LEFT)


    #Start/Next
    def execute_tick(state):
        try:
            update(cpu.tick(state))
        except Exception as e:
            _show_error(e)

    tick_button = Button(__actions_frame, text="Next", command=lambda: execute_tick(state))
    tick_button.pack(side=LEFT)
    if __edit_mode:
        tick_button.configure(state=DISABLED)


__reset_modified = False
def __render_highlighting(e):
    global __reset_modified

    if not __reset_modified:
        #Render Highlighting
        __code_items.tag_delete("KEYWORD")
        __code_items.tag_delete("ERROR")

        numLines = int(__code_items.index('end-1c').split('.')[0])

        for l in range(1, numLines+1):
            line = __code_items.get("%d.0" % l, "%d.end" % l)
            op = parser.to_op(line)
            if parser.is_valid_op(op):
                __code_items.tag_add("KEYWORD", "%d.0" % l, "%d.end" % l)
                pass
            else:
                __code_items.tag_add("ERROR", "%d.0" % l, "%d.end" % l)
                pass

        __code_items.tag_configure("KEYWORD", foreground="blue")
        __code_items.tag_configure("ERROR", foreground="red")

    __reset_modified = True
    __code_items.edit_modified(False)
    __reset_modified = False


def __clear_children(widget):
    for s in widget.pack_slaves():
        s.pack_forget()


if __name__ == "__main__":
    # inbox = iter([1, 2, 3, 4, 5, 6])
    inbox = iter([])
    ops = [
        # ["BUMPUP", '0'],
        # ["OUTBOX", '0'],
        # ["a:"],
        # ["INBOX"],
        # ["OUTBOX"],
        # ["JUMP", "a"]
    ]

    state = cpu.create_state(inbox, ops)

    # state.pointer = 1
    # state.regs[0] = 1
    # state.outbox = [1, 2, 3, 4]

    main(state)
