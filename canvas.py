from tkinter import *
import algos
import nodes

root = Tk()


canvaswidth = 31
canvasheight = 31
# targetnodes[0] = start; targetnodes[1] = end;
targetnodes = [None, None]
targeting = 0
changed = set()

#set the start/ending nodes
def setnodes(which, node):
    # 0=starting node; 1=ending node
    targetnodes[which] = node
    return

# a flag indicating which of the target nodes we are selecting
def settarg(val):
    global targeting
    targeting = val
    return

def start():
    if variable.get() == "bfs":
        algos.bfs(targetnodes[0], targetnodes[1])
    if variable.get() == "dfs":
        algos.dfs(targetnodes[0], targetnodes[1])
    if variable.get() == "A*":
        algos.astar(targetnodes[0], targetnodes[1])
    return

def clear():
    global targetnodes
    while changed:
        temp = changed.pop()
        temp.reset(0)
    targetnodes = [None, None]
    return

def clearothers():
    global targetnodes
    global changed
    walls = set()
    for i in changed:
        if i.state == 3:
            walls.add(i)
    changed.symmetric_difference_update(walls)
    while changed:
        temp = changed.pop()
        temp.reset(0)
    changed = walls.copy()
    targetnodes = [None, None]
    walls.clear()
    return

def selections():
    if targetnodes[0] is not None:
        targetnodes[0].setState(0)
        targetnodes[0] = None
    if targetnodes[1] is not None:
        targetnodes[1].setState(0)
        targetnodes[1] = None
    settarg(1)
    root.update()
    return

def generatemaze():
    algos.generatemaze(canvas)
    return

#create node objects
canvas = {}
for i in range(canvaswidth):
    column = {}
    for j in range(canvasheight):
        column[j] = nodes.GuiButton(i, j, [])
    canvas[i] = column

#set neighbor nodes
for i in range(len(canvas)):
    for j in range(len(canvas[0])):
        if i - 1 >= 0:
            canvas[i][j].neighbors.append(canvas[i-1][j])
        if i + 1 < len(canvas):
            canvas[i][j].neighbors.append(canvas[i+1][j])
        if j - 1 >= 0:
            canvas[i][j].neighbors.append(canvas[i][j-1])
        if j + 1 < len(canvas[0]):
            canvas[i][j].neighbors.append(canvas[i][j+1])





#algorithm options
options = [
    "A*",
    "bfs",
    "dfs"
]
variable = StringVar(root)
variable.set(options[0])
dropdown = OptionMenu(root, variable, *options)

#align buttons/nodes
selections = Button(root, command=selections, text="Select target nodes")
start = Button(root, command=start, text="Start!")
clear = Button(root, command=clear, text="Clear canvas")
clearother = Button(root, command=clearothers, text="Clear all but walls")
#generatemaze = Button(root, command=generatemaze, text="Random maze")

selections.grid(row=canvasheight+1, column=0, columnspan=5)
clear.grid(row=canvasheight+1, column=6, columnspan=4)
clearother.grid(row=canvasheight+1, column=10, columnspan=6)
start.grid(row=canvasheight+1, column=16, columnspan=4)
#generatemaze.grid(row=canvasheight+1, column=20, columnspan=4)
dropdown.grid(row=canvasheight+1, column=25, columnspan=3)
