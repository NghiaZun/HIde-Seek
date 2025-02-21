import math as m
import heapq as h

def heuristic(point_a, point_b): 
    return m.sqrt((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)

def a_star_search(start_node, target_nodes, state):
    open_heap = []
    h.heappush(open_heap, (0, start_node))
    came_from = {}
    g_score = {start_node: 0}
    f_score = {start_node: float("inf")}
    f_score[start_node] = min(heuristic(start_node, goal) for goal in target_nodes)
    while open_heap:
        current_node = h.heappop(open_heap)[1]
        if current_node in target_nodes:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start_node)
            path.reverse()
            return path
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)]:
            neighbor_node = (current_node[0] + dx, current_node[1] + dy)
            if not 0 <= neighbor_node[0] < len(state.game_map) or not 0 <= neighbor_node[1] < len(state.game_map[0]) or state.game_map[neighbor_node[0]][neighbor_node[1]] == 1:
                continue
            tentative_g_score = g_score[current_node] + 1
            if tentative_g_score < g_score.get(neighbor_node, float('inf')):
                came_from[neighbor_node] = current_node
                g_score[neighbor_node] = tentative_g_score
                f_score[neighbor_node] = tentative_g_score + min(heuristic(neighbor_node, goal) for goal in target_nodes)
                if neighbor_node not in [i[1] for i in open_heap]:
                    h.heappush(open_heap, (f_score[neighbor_node], neighbor_node))
    return []

def a_star_search_sub(start_node, target_nodes, state):
    open_heap = []
    h.heappush(open_heap, (0, start_node))
    came_from = {}
    g_score = {start_node: 0}
    f_score = {start_node: float("inf")}
    f_score[start_node] = min(heuristic(start_node, goal) for goal in target_nodes)
    while open_heap:
        current_node = h.heappop(open_heap)[1]
        if current_node in target_nodes:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start_node)
            path.reverse()
            return path
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)]:
            neighbor_node = (current_node[0] + dx, current_node[1] + dy)
            if not 0 <= neighbor_node[0] < len(state.game_map) or not 0 <= neighbor_node[1] < len(state.game_map[0]) or state.game_map[neighbor_node[0]][neighbor_node[1]] == 1 or state.game_map[neighbor_node[0]][neighbor_node[1]] == 14:
                continue
            tentative_g_score = g_score[current_node] + 1
            if tentative_g_score < g_score.get(neighbor_node, float('inf')):
                came_from[neighbor_node] = current_node
                g_score[neighbor_node] = tentative_g_score
                f_score[neighbor_node] = tentative_g_score + min(heuristic(neighbor_node, goal) for goal in target_nodes)
                if neighbor_node not in [i[1] for i in open_heap]:
                    h.heappush(open_heap, (f_score[neighbor_node], neighbor_node))
    return []