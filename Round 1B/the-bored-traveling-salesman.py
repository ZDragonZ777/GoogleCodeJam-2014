# Copyright (c) 2016 kamyu. All rights reserved.
#
# Google Code Jam 2016 Round 1B - Problem C. The Bored Traveling Salesman
# https://code.google.com/codejam/contest/2994486/dashboard#s=p2
#
# Time:  O(N^3)
# Space: O(M + N)
#

def connectivity_check(neighbors, source, DEAD):
    visited = set()
    def dfs(u):
        if u in DEAD or u in visited:
            return
        visited.add(u)
        for v in neighbors[u]:
            dfs(v)

    dfs(source)
    return len(visited) == len(neighbors) - len(DEAD)
 

def next_smallest_feasible_node_to_visit(zipcode, neighbors, ACTIVE, DEAD, visiting):
    best = None
    temp = []
    source = ACTIVE[0]
    while ACTIVE:  # O(N) time
        HEAD = ACTIVE[-1]
        # Check the neighbors of HEAD and record the 
        # next smallest node as best.
        for i in neighbors[HEAD]:  # O(N) time
            if i in visiting or i in DEAD:
                continue
            if best is None or zipcode[i] < zipcode[best]:
                best = i

        # Abandon HEAD and go back up in the ACTIVE stack.
        DEAD.add(HEAD)
        temp.append(HEAD)
        visiting.discard(HEAD)
        ACTIVE.pop()

        if not connectivity_check(neighbors, source, DEAD):  # O(N) time
            break

    # Restore the ACTIVE nodes and the DEAD set.
    while temp:
        HEAD = temp.pop()
        DEAD.discard(HEAD)
        visiting.add(HEAD)
        ACTIVE.append(HEAD)

    return best


def the_bored_traveling_salesman():
    N, M = map(int, raw_input().strip().split())

    root, zipcode = None, []
    for i in xrange(N):
        zipcode.append(raw_input().strip())
        if root is None or zipcode[i] < zipcode[root]:
            root = i

    neighbors = [set() for _ in xrange(N)]
    for _ in xrange(M):
        i, j = map(int, raw_input().strip().split())
        neighbors[i - 1].add(j - 1)
        neighbors[j - 1].add(i - 1)

    ACTIVE, DEAD, visiting = [root], set(), set()
    res = [zipcode[root]]
    next = None
    while ACTIVE:  # O(N) time
        HEAD = ACTIVE[-1]
        if next is None:
            next = next_smallest_feasible_node_to_visit(zipcode, neighbors, ACTIVE, DEAD, visiting)
        if next is None or next not in neighbors[HEAD]:
            # Leave the HEAD node.
            DEAD.add(HEAD)
            visiting.discard(HEAD)
            ACTIVE.pop()
        else:
            # Visit the next node.
            visiting.add(next)
            ACTIVE.append(next)
            res += zipcode[next]
            next = None

    return "".join(res)
    
    
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, the_bored_traveling_salesman())
