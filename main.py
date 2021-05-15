import random
import math

_goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


def index(item, seq):
    if item in seq:
        return seq.index(item)
    else:
        return -1


class EightPuzzle:
    def __init__(self):
        self._hval = 0
        self._depth = 0
        self._parent = None
        self.adj_matrix = []
        for i in range(3):
            self.adj_matrix.append(_goal_state[i][:])

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.adj_matrix == other.adj_matrix

    def __str__(self):
        res = ''
        for row in range(3):
            res += ' '.join(map(str, self.adj_matrix[row]))
            res += '\r\n'
        return res

    def _clone(self):
        p = EightPuzzle()
        for i in range(3):
            p.adj_matrix[i] = self.adj_matrix[i][:]
        return p

    def _get_legal_moves(self):
        row, col = self.find(0)
        free = []

        if row > 0:
            free.append((row - 1, col))
        if col > 0:
            free.append((row, col - 1))
        if row < 2:
            free.append((row + 1, col))
        if col < 2:
            free.append((row, col + 1))

        return free

    def _generate_moves(self):
        free = self._get_legal_moves()
        zero = self.find(0)

        def swap_and_clone(a, b):
            p = self._clone()
            p.swap(a, b)
            p._depth = self._depth + 1
            p._parent = self
            return p

        return map(lambda pair: swap_and_clone(zero, pair), free)

    def _generate_solution_path(self, path):
        if self._parent == None:
            return path
        else:
            path.append(self)
            return self._parent._generate_solution_path(path)

    def solve(self, h):
        def is_solved(puzzle):
            return puzzle.adj_matrix == _goal_state

        openl = [self]
        closedl = []
        move_count = 0
        while len(openl) > 0:
            x = openl.pop(0)
            move_count += 1
            if (is_solved(x)):
                if len(closedl) > 0:
                    return x._generate_solution_path([]), move_count
                else:
                    return [x]

            succ = x._generate_moves()
            idx_open = idx_closed = -1
            for move in succ:
                idx_open = index(move, openl)
                idx_closed = index(move, closedl)
                hval = h(move)
                fval = hval + move._depth

                if idx_closed == -1 and idx_open == -1:
                    move._hval = hval
                    openl.append(move)
                elif idx_open > -1:
                    copy = openl[idx_open]
                    if fval < copy._hval + copy._depth:
                        copy._hval = hval
                        copy._parent = move._parent
                        copy._depth = move._depth
                elif idx_closed > -1:
                    copy = closedl[idx_closed]
                    if fval < copy._hval + copy._depth:
                        move._hval = hval
                        closedl.remove(copy)
                        openl.append(move)

            closedl.append(x)
            openl = sorted(openl, key=lambda p: p._hval + p._depth)

        return [], 0

    def shuffle(self, step_count):
        for i in range(step_count):
            row, col = self.find(0)
            free = self._get_legal_moves()
            target = random.choice(free)
            self.swap((row, col), target)
            row, col = target

    def find(self, value):
        if value < 0 or value > 8:
            raise Exception("value out of range")

        for row in range(3):
            for col in range(3):
                if self.adj_matrix[row][col] == value:
                    return row, col

    def peek(self, row, col):
        return self.adj_matrix[row][col]

    def poke(self, row, col, value):
        self.adj_matrix[row][col] = value

    def swap(self, pos_a, pos_b):
        temp = self.peek(*pos_a)
        self.poke(pos_a[0], pos_a[1], self.peek(*pos_b))
        self.poke(pos_b[0], pos_b[1], temp)


def heur(puzzle, item_total_calc, total_calc):
    t = 0
    for row in range(3):
        for col in range(3):
            val = puzzle.peek(row, col) - 1
            target_col = val % 3
            target_row = val / 3

            if target_row < 0:
                target_row = 2
            t += item_total_calc(row, target_row, col, target_col)
    return total_calc(t)


def h_manhattan(puzzle):
    return heur(puzzle, lambda r, tr, c, tc: abs(tr - r) + abs(tc - c),
                lambda t: t)


def h_linear(puzzle):
    return heur(
        puzzle,
        lambda r, tr, c, tc: math.sqrt(math.sqrt((tr - r)**2 +
                                                 (tc - c)**2)), lambda t: t)


def h_default(puzzle):
    return 0


def main():
    nodesExplored = []
    distanceSum = []
    countSum = []
    for i in range(20):
        mcount = 0
        p = EightPuzzle()
        p.shuffle(20)
        if p.adj_matrix[0][0] == 1 and p.adj_matrix[0][0] != 0:
            mcount += 1
        if p.adj_matrix[0][1] == 2 and p.adj_matrix[0][1] != 0:
            mcount += 1
        if p.adj_matrix[0][2] == 3 and p.adj_matrix[0][2] != 0:
            mcount += 1
        if p.adj_matrix[1][0] == 4 and p.adj_matrix[1][0] != 0:
            mcount += 1
        if p.adj_matrix[1][1] == 5 and p.adj_matrix[1][1] != 0:
            mcount += 1
        if p.adj_matrix[1][2] == 6 and p.adj_matrix[1][2] != 0:
            mcount += 1
        if p.adj_matrix[2][0] == 7 and p.adj_matrix[2][0] != 0:
            mcount += 1
        if p.adj_matrix[2][1] == 8 and p.adj_matrix[2][1] != 0:
            mcount += 1
        if p.adj_matrix[2][2] != 0:
            mcount += 1
        countSum.append(mcount)
        print(p)

        path, count = p.solve(h_manhattan)
        path.reverse()
        for i in path:
            print(i)
        nodesExplored.append(count)
        print("Solved by exploring", count, "states")
        path, count = p.solve(h_linear)
        distanceSum.append(count)
        print(
            "Sum of the distances of the tiles from their goal positions is: ",
            count)
    print(
        "Iteration Index\tStates/Nodes Explored\tSum of Distances from the Goals State\tNo. of Misplaced Tiles"
    )
    for i in range(20):
        print((i + 1), "\t\t\t\t", nodesExplored[i], "\t\t\t\t\t\t",
              distanceSum[i], "\t\t\t\t\t", countSum[i])
    print("Average number of nodes vistied in 20 iterations is: ",
          math.floor(sum(nodesExplored) / 20))
    print("Avg sum of distance from goal state is: ",
          math.floor(sum(distanceSum) / 20))


if __name__ == "__main__":
    main()