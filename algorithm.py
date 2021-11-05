class edge(object):
    def __init__(self, distance, vertex):
        self.distance = distance
        self.vertex = vertex
 
class request(object):
    def __init__(self, x, y, time):
        self.x = x #широта
        self.y = y #долгота
        self.time = time
 
requests = []
edges = []
 
parsoch = []
used = []
 
def get_distance(i, j):
    return ((requests[i].x - requests[j].x)**2 + (requests[i].y - requests[j].y)**2)**0.5
 
def find_ways(requests):
    for i in range(len(requests)):
        for j in range(len(requests)):
            if i != j:
                length = get_distance(i, j)
                if (requests[i].time + 60 + length + length / 4 <= requests[j].time):
                    edges[i].append(edge(length, j + len(requests)))
 
def get_ddist(a):
    return a.distance
 
def try_kynh(v):
    if used[v] == 1:
        return 0
    used[v] = 1
    for i in range(len(edges[v])):
        it = edges[v][i].vertex
        if parsoch[it] == -1:
            parsoch[it] = v
            return 1
    for i in range(len(edges[v])):
        it = edges[v][i].vertex
        if try_kynh(parsoch[it]):
            parsoch[it] = v
            return 1
    return 0
 
 
 
def find_optimal_alloc(requests):
    find_ways(requests)
    for i in range(len(requests)):
        edges[i].sort(key=get_ddist)
    for i in range(len(requests)):
        for j in range(len(requests) * 2):
            used[j] = 0
        try_kynh(i)
    answer = []
    unused = []
    for i in range(len(requests) * 2):
        unused.append(0)
 
    for i in range(len(requests), len(requests) * 2):
        if parsoch[i] != -1:
            answer.append([])
            unused[parsoch[i]] = 1
            unused[i - len(requests)] = 1
            answer[len(answer) - 1].append(parsoch[i])
            answer[len(answer) - 1].append(i - len(requests))
    for i in range(len(requests)):
        if unused[i] == 0:
            answer.append([])
            answer[len(answer) - 1].append(i)
    changes = 1
    while (changes == 1):
        answer1 = []
        changes = 0
        position = -1
        for i in range(len(answer)):
            if position == -1:
                for j in range(i + 1, len(answer)):
                    if i != j:
                        if answer[i][0] == answer[j][len(answer[j]) - 1]:
                            for k in range(len(answer[j]) - 1):
                                answer[i].append(answer[j][k])
                            position = j
                            break
                        elif answer[j][0] == answer[i][len(answer[i]) - 1]:
                            current = []
                            for k in range(len(answer[i]) - 1):
                                current.append(answer[i][k])
                            for k in range(len(answer[j])):
                                current.append(answer[j][k])
                            answer[i] = current
                            position = j
                            break
            if position != -1:
                changes = 1
            if position != i:
                answer1.append(answer[i])
        answer = answer1
    return answer
 
def init():
    n = int(input())
 
    for i in range(n):
        x, y, time = map(int, input().split())
        requests.append(request(x, y, time))
        
    for i in range(len(requests) * 2):
        parsoch.append(-1)
 
    for i in range(len(requests) * 2):
        used.append(0)
 
    for i in range(len(requests) * 2):
        edges.append([])
 
    ans = find_optimal_alloc(requests)
 
    for i in ans:
        print(*i)
init()