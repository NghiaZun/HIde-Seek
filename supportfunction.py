def add_obstacles_to_map(game_state, obstacle_info):
    for (x1, y1, x2, y2) in obstacle_info:
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                game_state.game_map[i][j] = 14

def area_which_have_point(obstacles_info, point):
    for obstacle in obstacles_info:
        top = obstacle[0]
        left = obstacle[1]
        bottom = obstacle[2]
        right = obstacle[3]
        for row in range(top, bottom + 1):
            for col in range(left, right + 1):
                if row == point[0] and col == point[1]:
                    return obstacle
    return None

def find_move_direction(start_point, end_point):
    d_row = end_point[0] - start_point[0]
    d_col = end_point[1] - start_point[1]
    return d_row, d_col

def find_obstacle_move(obstacle_info, point):
    top, left, bottom, right = obstacle_info[0], obstacle_info[1], obstacle_info[2], obstacle_info[3]
    row, col = point[0], point[1]
    if top <= row <= bottom:
        return "row"
    if left <= col <= right:
        return "col"

def clearObstacle(game_map, obstacle_info):
    top = obstacle_info[0]
    left = obstacle_info[1]
    bottom = obstacle_info[2]
    right = obstacle_info[3]
    for row in range(top, bottom + 1):
        for col in range(left, right + 1):
            game_map[row][col] = 0
    return game_map

def updateObstacle(game_map, obstacle_info):
    top = obstacle_info[0]
    left = obstacle_info[1]
    bottom = obstacle_info[2]
    right = obstacle_info[3]
    for row in range(top, bottom + 1):
        for col in range(left, right + 1):
            game_map[row][col] = 14
    return game_map

def choose_another_end_point(matrix, start_point, end_point):
    start_row = start_point[0]
    start_col = start_point[1]
    end_row = end_point[0]
    end_col = end_point[1]
    if start_row > end_row:
        start_row, end_row = end_row, start_row
    if start_col > end_col:
        start_col, end_col = end_col, start_col
    for row in range(start_row, end_row + 1):
        for col in range(start_col, end_col + 1):
            if matrix[row][col] == 14:
                return (row, col)
    return None 