def bresenham_line(x0, y0, x1, y1):

    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2 * dy - dx
    y = 0
    result = []
    for x in range(dx + 1):

        result.append((x0 + x * xx + y * yx, y0 + x * xy + y * yy))

        if D >= 0:
            y += 1
            D -= 2 * dx
        D += 2 * dy
    return result


def is_hider_in_vision(start, end, game_map):
    line_of_vision = bresenham_line(start[0], start[1], end[0], end[1])
    for point in line_of_vision:
        if game_map[point[0]][point[1]] == 1 :
            return False
    return True

def Seeker_See_Hider(start_pos, game_map, vision_range=3):
    visible_hiders = []
    (x, y) = start_pos
    for dx in range(-vision_range, vision_range + 1):
        for dy in range(-vision_range, vision_range + 1):
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < len(game_map) and 0 <= new_y < len(game_map[0]):
                line_of_sight = bresenham_line(x, y, new_x, new_y)
                if all(game_map[point[0]][point[1]] != 1 for point in line_of_sight):
                    if game_map[new_x][new_y] == 2:
                        visible_hiders.append((new_x, new_y))
    return visible_hiders

def Hider_See_Seeker(start_pos, game_map, vision_range=2):
    visible_seeker = ()
    (x, y) = start_pos
    for dx in range(-vision_range, vision_range + 1):
        for dy in range(-vision_range, vision_range + 1):
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < len(game_map) and 0 <= new_y < len(game_map[0]):
                line_of_sight = bresenham_line(x, y, new_x, new_y)
                if all(game_map[point[0]][point[1]] != 1 for point in line_of_sight):
                    if game_map[new_x][new_y] == 3:
                        visible_seeker = (new_x, new_y)
    return visible_seeker

