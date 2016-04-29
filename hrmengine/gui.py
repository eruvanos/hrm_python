from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfile

from hrmengine import cpu, parser
from hrmengine.level import levels
from hrmengine.tkutils import move_line_up, move_line_down, delete_line

__inboxItemFrame = Frame
__outboxItemFrame = Frame
__regItemframe = Frame
__pointerFrame = Frame
__code_items = Text
__actions_frame = Frame
__message_label = Label
__welcome_text = LabelFrame
__menubar = Menu
__edit_mode = True
__programm_state = Label
__clipboard_frame = Frame

__paste_image = PhotoImage
__copy_image = PhotoImage

__prev_image = PhotoImage
__start_image = PhotoImage
__stop_image = PhotoImage
__next_image = PhotoImage


def main(state):
    root = Tk()
    root.title("HRM P3")
    root.minsize(width=700, height=500)
    center(root)

    # Menubar
    global __menubar
    __menubar = Menu(root)

    generalmenu = Menu(__menubar, tearoff=0)
    generalmenu.add_command(label="Load")
    generalmenu.add_command(label="Save to")
    __menubar.add_cascade(label="General", menu=generalmenu)

    levelmenu = Menu(__menubar, tearoff=0)

    def load_level_data(level):
        return lambda: load_level(levels[level]())

    for l in range(1, len(levels) + 1):
        levelmenu.add_command(label="Level %s" % l, command=load_level_data('level%s' % l))
    __menubar.add_cascade(label="Load Level", menu=levelmenu)
    root.config(menu=__menubar)

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

    scrollbar = Scrollbar(codeFrame)
    scrollbar.pack(side=RIGHT, fill=Y)
    Label(codeFrame, text="Code", width=15).pack(side=TOP)
    global __code_items
    __code_items = Text(codeFrame, width=15, bd=1, relief=SOLID)
    __code_items.pack(fill=BOTH)
    __code_items.bind('<<Modified>>', lambda e: __render_highlighting(e))

    __code_items.bind('<Command-Up>', lambda e: move_line_up(__code_items))
    __code_items.bind('<Command-Down>', lambda e: move_line_down(__code_items))
    __code_items.bind('<Command-BackSpace>', lambda e: delete_line(__code_items))

    __code_items.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=__code_items.yview)

    # Clipboard
    global __clipboard_frame
    __clipboard_frame = Frame(codeFrame, bd=1, relief=SOLID)
    __clipboard_frame.pack(fill=X)

    # Processing State
    global __programm_state
    __programm_state = Label(codeFrame)
    __programm_state.pack(fill=X)

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


def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w / 2 - size[0] / 2
    y = h / 2 - size[1] / 2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))


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
    _update_menu(state)
    _update_actions(state)
    _update_program_state(state)
    _update_clipboard_button(state)


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
    __code_items.configure(state=NORMAL)
    __code_items.delete(0.0, END)
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
        __code_items.configure(state=NORMAL)
    else:
        __code_items.configure(state=DISABLED)


def _update_clipboard_button(state):
    __clear_children(__clipboard_frame)

    button_state = NORMAL
    if not __edit_mode:
        button_state = DISABLED

    def from_cb(current_state):
        clipboard_string = __clipboard_frame.clipboard_get()
        current_state.code = parser.parse_clipboard_string(clipboard_string)
        update(current_state)

    global __paste_image
    __paste_image = PhotoImage(file="../resources/icons/new/paste-colored-sized.gif")
    Button(__clipboard_frame,
           text="PASTE",
           image=__paste_image,
           width="32", height="32",
           command=lambda: from_cb(state),
           state=button_state
           ).pack(side=LEFT)

    def to_cb(current_state):
        __update_state_from_codetext(current_state)
        __clipboard_frame.clipboard_clear()
        for row in current_state.code:
            __clipboard_frame.clipboard_append(row[0])
            if len(row) > 1:
                __clipboard_frame.clipboard_append(" %s" % row[1])
            __clipboard_frame.clipboard_append("\n")

    global __copy_image
    __copy_image = PhotoImage(file="../resources/icons/new/copy-colored-sized.gif")
    Button(__clipboard_frame,
           text="COPY",
           command=lambda: to_cb(state),
           image=__copy_image,
           width="32", height="32",
           state=button_state
           ).pack(side=RIGHT)


def _update_program_state(state):
    if __edit_mode:
        __programm_state.configure(text="EDIT")
    elif state.pc == -1:
        __programm_state.configure(text="STOPPED")
    else:
        __programm_state.configure(text="RUNNING")


def __update_state_from_codetext(state):
    code_lines = __code_items.get("1.0", END).split("\n")
    code_lines = filter(lambda line: len(line) > 0, code_lines)
    code_lines = map(lambda line: line.replace("x", "").strip(), code_lines)
    state.code = parser._convert_to_ops(code_lines)


def _update_menu(state):
    def load_from_file(current_state):
        filename = askopenfilename(title="Choose file")
        current_state.code = parser.parse_file(filename)
        update(current_state)

    general_menu = __menubar.winfo_children()[0]
    general_menu.entryconfigure(0, command=lambda: load_from_file(state))

    def save_to_file(current_state):
        __update_state_from_codetext(current_state)

        f = asksaveasfile(mode='w', defaultextension=".txt")
        if f is None:
            return
        else:
            f.write("-- HUMAN RESOURCE MACHINE PROGRAM --\n\n")
            for row in current_state.code:
                f.write(row[0])
                if len(row) > 1:
                    f.write(" %s" % row[1])
                f.write("\n")
            f.close()

    general_menu.entryconfigure(1, command=lambda: save_to_file(state))


def _update_actions(state):
    __clear_children(__actions_frame)

    # Prev
    global __prev_image
    __prev_image = PhotoImage(file="../resources/icons/new/prev-colored-sized.gif")
    prev_button = Button(__actions_frame,
                         text='Prev',
                         image=__prev_image,
                         width="32", height="32",
                         command=lambda: update(state.prev_state))
    prev_button.pack(side=LEFT)
    if state.prev_state is None:
        prev_button.configure(state=DISABLED)

    # Stop
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

    global __stop_image
    __stop_image = PhotoImage(file="../resources/icons/new/stop-colored-sized.gif")
    reset_button = Button(__actions_frame,
                          text='Stop',
                          image=__stop_image,
                          width="32", height="32",
                          command=lambda: stop())
    if not __edit_mode:
        reset_button.pack(side=LEFT)

    # Start
    def start():
        global __edit_mode
        __edit_mode = False

        codeLines = __code_items.get("1.0", END).split("\n")
        codeLines = filter(lambda line: len(line) > 0, codeLines)
        state.code = parser._convert_to_ops(codeLines)

        update(state)

    global __start_image
    __start_image = PhotoImage(file="../resources/icons/new/play-colored-sized.gif")
    start_button = Button(__actions_frame,
                          text='Start',
                          image=__start_image,
                          width="32", height="32",
                          command=lambda: start())
    if __edit_mode:
        start_button.pack(side=LEFT)

    # Start/Next
    def execute_tick(state):
        try:
            update(cpu.tick(state))
        except Exception as e:
            _show_error(e)

    global __next_image
    __next_image = PhotoImage(file="../resources/icons/new/next-colored-sized.gif")
    tick_button = Button(__actions_frame,
                         text="Next",
                         image=__next_image,
                         width="32", height="32",
                         command=lambda: execute_tick(state))
    tick_button.pack(side=LEFT)
    if __edit_mode or state.pc == -1:
        tick_button.configure(state=DISABLED)


__reset_modified = False


def __render_highlighting(e):
    global __reset_modified

    if not __reset_modified:
        # Render Highlighting
        __code_items.tag_delete("KEYWORD")
        __code_items.tag_delete("ERROR")

        numLines = int(__code_items.index('end-1c').split('.')[0])

        for l in range(1, numLines + 1):
            line = __code_items.get("%d.0" % l, "%d.end" % l)
            op = parser._to_op(line)
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
    inbox = iter([])
    ops = [
    ]
    state = cpu.create_state(inbox, ops)
    state.pointer = 1
    state.regs[0] = 1
    state.outbox = [1, 2, 3, 4]

    # inbox = iter([])
    # ops = [
    #     ["ADD", '0']
    # ]
    # state = cpu.create_state(inbox, ops)
    # state.pointer = 'A'
    # state.regs[0] = 'A'

    main(state)
