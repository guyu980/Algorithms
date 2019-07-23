class Vertex:
    def __init__(self, v):
        self.in_neighbors = []
        self.out_neighbors = []
        self.value = v
        self.in_time = None
        self.out_time = None
        self.status = 'Unvisited'

    def add_in_neighbor(self, v):
        self.in_neighbors.append(v)

    def add_out_neighbor(self, v):
        self.out_neighbors.append(v)

    def is_in_neighbor(self, v):
        if v in self.in_neighbors:
            return True

        return False

    def is_out_neighbor(self, v):
        if v in self.out_neighbors:
            return True

        return False

    def is_neighbor(self, v):
        if self.is_in_neighbor(v) or self.is_out_neighbor(v):
            return True

        return False

    def get_in_neighbors(self):
        return self.in_neighbors

    def get_out_neighbors(self):
        return self.out_neighbors

    def __str__(self):
        return str(self.value)


class Graph:
    def __init__(self):
        self.vertices = []

    def add_vertex(self, n):
        self.vertices.append(n)

    def add_dir_edge(self, u: Vertex, v: Vertex):
        u.add_out_neighbor(v)
        v.add_in_neighbor(u)

    def add_edge(self, u: Vertex, v: Vertex):
        self.add_dir_edge(u, v)
        self.add_dir_edge(v, u)

    def get_dir_edges(self):
        ret = []

        for v in self.vertices:
            ret += [[v, u] for u in v.get_out_neighbors()]

        return ret

    def __str__(self):
        ret = '     - Graph with:\n'
        ret += '     - Vertices:\n          '

        for v in self.vertices:
            ret += str(v) + ', '

        ret += '\n'
        ret += '     - Edges:\n          '

        for a in self.vertices:
            for b in a.get_out_neighbors():
                ret += '(' + str(a) + ', ' + str(b) + ') '

            ret += '\n          '

        return ret


def dfs(w: Vertex, cur_time, verbose):
    if verbose:
        print('     - Time %2d' % cur_time, ': entering', w)

    w.in_time = cur_time
    cur_time += 1
    w.status = 'In progress'

    for v in w.get_out_neighbors():
        if v.status == 'Unvisited':
            cur_time = dfs(v, cur_time, verbose)
            cur_time += 1

    w.out_time = cur_time
    w.status = 'Done'

    if verbose:
        print('     - Time %2d' % cur_time, ': leaving ', w)

    return cur_time


def depth_first_search(w: Vertex, G: Graph, verbose=False):
    for v in G.vertices:
        v.status = 'Unvisited'
        v.in_time = None
        v.out_time = None

    return dfs(w, 0, verbose)


def bfs(w: Vertex, G: Graph):
    for v in G.vertices:
        v.status = 'Unvisited'

    levels = [[] for i in range(len(G.vertices))]
    levels[0] = [w]
    w.status = 'Visited'

    for i in range(len(G.vertices)):
        for u in levels[i]:
            for v in u.get_out_neighbors():
                if v.status == 'Unvisited':
                    v.status = 'Visited'
                    levels[i+1].append(v)

    return levels


def breadth_first_search(w: Vertex, G: Graph):
    levels = bfs(w, G)

    for i in range(len(levels)):
        if len(levels[i]) == 0:
            continue

        print('     - Level', i, ':')

        for j in levels[i]:
            print('          ', j)

    return levels


if __name__ == '__main__':
    print('====================== Example of Graph =====================')
    print('                              4                              \n'
          '                             / \\                             \n'
          '                            /   \\                            \n'
          '                           2     5                           \n'
          '                          / \\     \\                          \n'
          '                         /   \\     \\                         \n'
          '                        1     3     6                        \n'
          '                       /                                     \n'
          '                      /                                      \n'
          '                     0                                       \n')
    G = Graph()

    for item in range(7):
        G.add_vertex(Vertex(item))

    V = G.vertices

    for pair in [(4, 2), (4, 5), (2, 1), (2, 3), (5, 6), (1, 0)]:
        G.add_edge(V[pair[0]], V[pair[1]])

    print(G)

    print('=============== Process of Depth First Search ===============')
    depth_first_search(G.vertices[4], G, verbose=True)

    print('============== Process of Breadth First Search ==============')
    breadth_first_search(G.vertices[4], G)

    print('=============================================================\n')



