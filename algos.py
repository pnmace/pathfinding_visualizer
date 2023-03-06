import queue
import heapq
import time
import canvas
import random

# drawpath
def drawpath(current, start):
    # so we don't change the color of the target node
    current = current.parent
    while current is not None:
        current.setState(5)
        current = current.parent
        time.sleep(0.005)
        canvas.root.update()
    return


def bfs(start, targ):
    q = queue.Queue()
    q.put(start)
    visited = set()
    while not q.empty():
        node = q.get()
        if node in visited or node.state == 3:
            continue
        if node == targ:
            node.setState(5)
            return
        visited.add(node)
        node.setState(4)
        time.sleep(0.005)
        canvas.root.update()
        for i in node.neighbors:
            q.put(i)
    return

def dfs(start, targ):
    stack = [start]
    path = set()
    while stack:
        node = stack.pop()
        if node in path or node.state == 3:
            continue
        if node == targ:
            node.setState(5)
            return
        path.add(node)
        node.setState(4)
        time.sleep(0.005)
        canvas.root.update()
        for i in node.neighbors:
            stack.append(i)
    return

# gcost = dist from starting node
# hcost = dist from goal node
# fcost = sum of the two
def astar(start, targ):
    #our starting node
    minheap = []
    visited = set()
    if start == targ:
        start.setState(5)
        return
    for i in start.neighbors:
        if i.state == 3:
            continue
        i.gcost = ((start.row-i.row)**2 + (start.col-i.col)**2)**(1/2.0)
        i.hcost = ((targ.row-i.row)**2 + (targ.col-i.col)**2)**(1/2.0)
        i.fcost = i.gcost + i.hcost
        heapq.heappush(minheap, (i.fcost, i))
    while minheap:
        current = heapq.heappop(minheap)[1]
        current.setState(4)
        time.sleep(0.005)
        canvas.root.update()
        visited.add(current)
        if current == targ:
            drawpath(current, start)
            return
        for i in current.neighbors:
            if i in visited or i.state == 3:
                continue
            if i not in minheap:
                # sometimes the parent nodes are getting stuck in an infinate loop
                i.gcost = ((start.row-i.row)**2 + (start.col-i.col)**2)**(1/2.0)
                i.hcost = ((targ.row-i.row)**2 + (targ.col-i.col)**2)**(1/2.0)
                i.fcost = i.gcost + i.hcost
                heapq.heappush(minheap, (i.fcost, i))
                i.parent = current
                visited.add(i)
            else:
                # we update the costs for this node in the heap then reinsert it
                # there's probably a much more efficient way to do this..?
                temp = (i.fcost, i)
                i.gcost = ((start.row-i.row)**2 + (start.col-i.col)**2)**(1/2.0)
                i.hcost = ((targ.row-i.row)**2 + (targ.col-i.col)**2)**(1/2.0)
                i.fcost = i.gcost + i.hcost
                minheap[minheap.index(temp)] = (i.fcost, i)
                heapq.heapify(minheap)
                visited.add(i)
    return

def generatemaze(nodes):
    unvisited = set()
    # locked = set()
    path = []
    for i in range(len(nodes)):
        for j in range(len(nodes[0])):
            nodes[i][j].setState(3)
            unvisited.add(nodes[i][j])

    for i in range(len(nodes)):
        for j in range(len(nodes[0])):
            if i % 2 == 0 and j % 2 == 0:
                unvisited.remove(nodes[i][j])

    curr = nodes[random.randrange(0, len(nodes))][random.randrange(0, len(nodes))]
    while curr not in unvisited:
        curr = nodes[random.randrange(0, len(nodes))][random.randrange(0, len(nodes))]
    unvisited.remove(curr)
    curr.setState(0)
    path.append(curr)

    # the above code is correct. disallows "corner" nodes,
    # populates the unvisited set, and picks a random start

    while unvisited:
        deadend = 1
        # can we continue or do we backtrack?
        for i in curr.neighbors:
            if i in unvisited:
                deadend = 0

        if deadend == 1:
            if not path:
                # exhausted all options; stack is empty
                return
            curr = path.pop()
            continue



    return
