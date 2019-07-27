from utils import *
import math


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

    def has_in_neighbor(self, v):
        if v in self.in_neighbors:
            return True

        return False

    def has_out_neighbor(self, v):
        if v in self.out_neighbors:
            return True

        return False

    def has_neighbor(self, v):
        if self.has_in_neighbor(v) or self.has_out_neighbor(v):
            return True

        return False

    def get_in_neighbors(self):
        return self.in_neighbors

    def get_out_neighbors(self):
        return self.out_neighbors

    def __str__(self):
        return str(self.value)


class WeightedVertex(Vertex):
    def __init__(self, v):
        super(WeightedVertex, self).__init__(v)
        self.parent = None
        self.est_dist = math.inf

    def add_weighted_in_neighbor(self, v, wt):
        self.in_neighbors.append((v, wt))

    def add_weighted_out_neighbor(self, v, wt):
        self.out_neighbors.append((v, wt))

    def get_in_neighbors(self):
        return [v[0] for v in self.in_neighbors]

    def get_out_neighbors(self):
        return [v[0] for v in self.out_neighbors]

    def get_weighted_in_neighbors(self):
        return self.in_neighbors

    def get_weighted_out_neighbors(self):
        return self.out_neighbors

    def get_weight(self, v):
        in_neighbors = self.get_weighted_in_neighbors()

        for u, wt in in_neighbors:
            if u.value == v.value:
                return wt

        else:
            return 0


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

    def reverse_edge(self, u: Vertex, v: Vertex):
        if u.has_out_neighbor(v) and v.has_in_neighbor(u):
            if v.has_out_neighbor(u) and u.has_in_neighbor(v):
                return

            self.add_dir_edge(v, u)
            u.out_neighbors.remove(v)
            v.in_neighbors.remove(u)

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


class WeightedGraph(Graph):
    def __init__(self):
        super(WeightedGraph, self).__init__()

    def add_weighted_dir_edge(self, u: WeightedVertex, v: WeightedVertex, wt=1):
        u.add_weighted_out_neighbor(v, wt)
        v.add_weighted_in_neighbor(u, wt)

    def add_weighted_edge(self, u: WeightedVertex, v: WeightedVertex, wt=1):
        self.add_weighted_dir_edge(u, v, wt)
        self.add_weighted_dir_edge(v, u, wt)

    def get_dir_edges(self):
        ret = []

        for v in self.vertices:
            for u, wt in v.get_weighted_out_neighbors():
                ret.append([v, u, wt])

        return ret

    def __str__(self):
        ret = '     - Graph with:\n'
        ret += '     - Vertices:\n          '

        for v in self.vertices:
            ret += str(v) + ', '

        ret += '\n'
        ret += '     - Edges:\n          '

        for a in self.vertices:
            for b, wt in a.get_weighted_out_neighbors():
                ret += '(' + str(a) + ', ' + str(b) + ', wt:' + str(wt) + ') '

            ret += '\n          '

        return ret


def dfs(w: Vertex, cur_time, order, verbose):
    if verbose:
        print('     - Time %2d' % cur_time, ': entering', w)

    w.in_time = cur_time
    cur_time += 1
    w.status = 'In progress'

    for v in w.get_out_neighbors():
        if v.status == 'Unvisited':
            cur_time = dfs(v, cur_time, order, verbose)
            cur_time += 1

    w.out_time = cur_time
    w.status = 'Done'
    order.insert(0, w)

    if verbose:
        print('     - Time %2d' % cur_time, ': leaving ', w)

    return cur_time


def depth_first_search(w: Vertex, G: Graph, verbose=False):
    for v in G.vertices:
        v.status = 'Unvisited'
        v.in_time = None
        v.out_time = None

    return dfs(w, 0, [], verbose)


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


def weighted_bfs(w: WeightedVertex, G: WeightedGraph):
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
                    v.parent = u
                    levels[i+1].append(v)

    return levels


def strongly_connected_components(G: Graph, verbose=False):
    order = []

    for v in G.vertices:
        v.status = 'Unvisited'
        v.in_time = None
        v.out_time = None

    cur_time = 0

    for w in G.vertices:
        if w.status == 'Unvisited':
            cur_time = dfs(w, cur_time, order, verbose)

        cur_time += 1

    E = G.get_dir_edges()

    print('\n     - Reverse:\n')

    for x, y in E:
        G.reverse_edge(x, y)

    scc = []

    for v in order:
        v.status = 'Unvisited'
        v.in_time = None
        v.out_time = None

    cur_time = 0

    for w in order:
        visited = []

        if w.status == 'Unvisited':
            cur_time = dfs(w, cur_time, visited, verbose)
            scc.append(visited[:])

    return scc


def dijkstra(w: WeightedVertex, G: WeightedGraph):
    for v in G.vertices:
        v.est_dist = math.inf

    w.est_dist = 0
    unsure_vertices = G.vertices[:]

    while len(unsure_vertices) > 0:
        u = None
        min_dist = math.inf

        for x in unsure_vertices:
            if x.est_dist < min_dist:
                min_dist = x.est_dist
                u = x

        if u is None:
            return

        for v, wt in u.get_weighted_out_neighbors():
            if u.est_dist + wt < v.est_dist:
                v.est_dist = u.est_dist + wt
                v.parent = u

        unsure_vertices.remove(u)


def dijkstra_shortest_path(w: WeightedVertex, G: WeightedGraph):
    dijkstra(w, G)

    for v in G.vertices:
        if v.est_dist == math.inf:
            print('     - Cannot reach %s!' % str(v))
            continue

        path = []
        len_path = 0
        current = v

        while current != w:
            path.append(current)
            len_path += current.get_weight(current.parent)
            current = current.parent

        path.append(current)
        path.reverse()

        print('     - Shortest path from %s to %s is %d:\n'
              '          %s' % (str(w), str(v), len_path, [str(u) for u in path]))


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

    print('=============== Process of Depth First Search ===============\n')
    depth_first_search(G.vertices[4], G, verbose=True)

    print('\n============== Process of Breadth First Search ==============\n')
    breadth_first_search(G.vertices[4], G)

    print('\n=============== Strongly Connected Components ===============\n')
    stanford = Vertex('Stanford')
    wiki = Vertex('Wikipedia')
    nytimes = Vertex('NYTimes')
    cal = Vertex('Berkeley')
    puppies = Vertex('Puppies')
    google = Vertex('Google')

    G = Graph()
    V = [stanford, wiki, nytimes, cal, puppies, google]

    for v in V:
        G.add_vertex(v)

    E = [(stanford, wiki), (stanford, puppies), (wiki, stanford), (wiki, nytimes), (nytimes, stanford), (cal, stanford),
         (cal, puppies), (wiki, puppies), (nytimes, puppies), (puppies, google), (google, puppies)]

    for x, y in E:
        G.add_dir_edge(x, y)

    print(G)
    scc = strongly_connected_components(G, verbose=True)

    print('')

    for X in scc:
        print('     -', [str(x) for x in X])

    print('\n==================== Dijkstra\'s Algorithm ===================\n')
    gates = WeightedVertex('Gates')
    packard = WeightedVertex('Packard')
    cs161 = WeightedVertex('CS161')
    union = WeightedVertex('Union')
    dish = WeightedVertex('Dish')
    hospital = WeightedVertex('Hospital')
    caltrain = WeightedVertex('Caltrain')
    stadium = WeightedVertex('Stadium')

    G = WeightedGraph()
    V = [gates, packard, cs161, union, dish, hospital, caltrain, stadium]

    for v in V:
        G.add_vertex(v)

    E = [(gates, packard, 1), (packard, cs161, 1), (cs161, union, 4), (union, dish, 20), (packard, dish, 22),
         (gates, dish, 25), (gates, hospital, 10), (gates, caltrain, 17), (caltrain, stadium, 15), (gates, stadium, 10)]

    for x, y, wt in E:
        G.add_weighted_edge(x, y, wt)

    print(G)
    dijkstra_shortest_path(V[0], G)

    print('\n=============================================================\n')



