def move_line_up(text):
    # text.config(state='normal')
    # get text on current and previous lines
    lineText = text.get("insert linestart", "insert lineend")
    prevLineText = text.get("insert linestart -1 line", "insert -1 line lineend")

    # delete the old lines
    text.delete("insert linestart -1 line", "insert -1 line lineend")
    text.delete("insert linestart", "insert lineend")

    # insert lines in swapped order
    text.insert("insert linestart -1 line", lineText)
    text.insert("insert linestart", prevLineText)

    #text.config(state='disabled')


def move_line_down(text):
    # text.config(state='normal')
    # get text on current and next lines
    lineText = text.get("insert linestart", "insert lineend")
    nextLineText = text.get("insert +1 line linestart", "insert +1 line lineend")

    # delete text on current and next lines
    text.delete("insert linestart", "insert lineend")
    text.delete("insert +1 line linestart", "insert +1 line lineend")

    # insert text in swapped order
    text.insert("insert linestart", nextLineText)
    text.insert("insert linestart + 1 line", lineText)
    #text.config(state='disabled')

def delete_line(text):
    text.delete("insert linestart", "insert lineend")
    text.mark_set("insert", "insert linestart + 1 line")
    text.see("insert")