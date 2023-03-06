from tkinter import *
import canvas

unblocked = "gray"
blocked = "black"
target = "red"
searching = "cyan"
found = "green"

class GuiButton:
    # states:
    # 0: empty
    # 1: start
    # 2: end
    # 3: blocked
    # 4: searching
    # 5: found path
    def __init__(self, row, col, neighbors, state=0, gcost=0, hcost=0, fcost=0, parent=None):
        self.row = row
        self.col = col
        self.button = Button(canvas.root, command=self.toggle, bg=unblocked)
        self.button.grid(row=row, column=col)
        self.neighbors = neighbors
        self.state = state
        self.gcost = gcost
        self.hcost = hcost
        self.fcost = fcost
        self.parent = parent

    # sketchy hack to allow equal sorting in a minheap
    # for various algos. if duplicate 0 index of tuples
    # are encountered, min heap tries to compare
    # the second object which is an instance of this class
    # maybe just allow this to return self.fcost < other.fcost?
    def __lt__(self, other):
        return 0

    def reset(self, val):
        self.setState(val)
        self.gcost = 0
        self.hcost = 0
        self.fcost = 0
        self.parent = [None]
        return

    def toggle(self):
        if canvas.targeting == 1:
            self.setState(1)
            canvas.setnodes(0, self)
            canvas.settarg(2)
            return
        if canvas.targeting == 2:
            self.setState(2)
            canvas.setnodes(1, self)
            canvas.settarg(0)
            return
        if self.button.cget("bg") == unblocked:
            self.button.configure(bg=blocked)
            self.setState(3)
        elif self.button.cget("bg") == blocked:
            self.button.configure(bg=unblocked)
            self.setState(0)
        return

    def setState(self, val):
        self.state = val
        if val == 0:
            self.button.configure(bg=unblocked, text="")
            canvas.changed.discard(self)
            return
        canvas.changed.add(self)
        if val == 1:
            self.button.configure(bg=target, text="")
            return
        if val == 2:
            self.button.configure(bg=target, text="")
            return
        if val == 3:
            self.button.configure(bg=blocked)
            return
        if val == 4:
            # do not cover up the start/end when showing node traversal
            if self.button.cget("bg") == target:
                return
            self.button.configure(bg=searching)
            return
        if val == 5:
            self.button.configure(bg=found)
            return
        return
