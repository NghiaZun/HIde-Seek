import random    
import astar as a
import copy
import math
import supportfunction as sf

class GameState():
    
    def __init__(self):
        self.game_map = []
        self.is_hider_move = False
        self.score = 0
        self.previous_state = []
        self.obstacles_info = []

    def getSeekerPosition(self):
        for r in range(len(self.game_map)):
            for c in range(len(self.game_map[r])):
                if self.game_map[r][c] == 3:
                    return (r, c)
        return None

    def getHiderPositions(self):
        hider_positions = []
        for r in range(len(self.game_map)):
            for c in range(len(self.game_map[r])):
                if self.game_map[r][c] == 2:
                    hider_positions.append((r, c))
        return hider_positions

    def isValidUnitToMove(self, pos):
        row, col = pos
        if (0 <= row < len(self.game_map) and 0 <= col < len(self.game_map[0])):
            if not self.is_hider_move:
                return self.game_map[row][col] == 0 or self.game_map[row][col] == 2
            else:
                return self.game_map[row][col] == 0
        return False

    def evaluate(self):
        seeker_pos = self.getSeekerPosition()
        hider_positions = self.getHiderPositions()
        max_distance = abs(len(self.game_map) - 1) + abs(len(self.game_map[0]) - 1)

        if not hider_positions:
            return float('inf') if not self.is_hider_move else float('-inf')

        closest_distance = min(abs(seeker_pos[0] - h_pos[0]) + abs(seeker_pos[1] - h_pos[1]) for h_pos in hider_positions)
        distance_score = max_distance - closest_distance

        hider_caught_reward = 20 

        hider_penalty = -20 * len(hider_positions)

        final_score = self.score + distance_score + hider_penalty
        if not self.is_hider_move:
            for h_pos in hider_positions:
                if seeker_pos == h_pos:
                    final_score += hider_caught_reward
                    break

        return final_score

    def makeMove(self, move):
        self.game_map[move.startRow][move.startCol] = 0
        if self.is_hider_move == False:
            if self.game_map[move.endRow][move.endCol] == 2:
                self.score += 20
                self.game_map[move.endRow][move.endCol] = 3
            else:
                self.game_map[move.endRow][move.endCol] = move.pieceMoved
            self.score -= 1
        else:
            self.game_map[move.endRow][move.endCol] = move.pieceMoved
        self.previous_state.append(move)

    def makeMove_advanced(self, move):
        self.game_map[move.startRow][move.startCol] = 0
        if self.is_hider_move == False:
            temp_pos = sf.choose_another_end_point(self.game_map, (move.startRow, move.startCol), (move.endRow, move.endCol))
            if self.game_map[move.endRow][move.endCol] == 14 or temp_pos != None:
                if temp_pos != None:
                    move.updateEndPoint(temp_pos[0], temp_pos[1])
                obstacle_info = sf.area_which_have_point(self.obstacles_info, (move.endRow, move.endCol))
                obstacle_direction_move = sf.find_obstacle_move(obstacle_info, (move.endRow, move.endCol))
                d_row, d_col = sf.find_move_direction((move.startRow, move.startCol), (move.endRow, move.endCol))
                if obstacle_direction_move == 'row':
                    if d_row < 0:
                        move.endRow = move.startRow - 1
                        direct = "up"
                    else:
                        move.endRow = move.startRow + 1
                        direct = "down"
                else:
                    if d_col < 0:
                        move.endCol = move.startCol - 1
                        direct = "left"
                    else:
                        move.endCol = move.startCol + 1
                        direct = "right"
                self.game_map = sf.clearObstacle(self.game_map, obstacle_info)
                if direct == "up":
                    self.obstacles_info.remove(obstacle_info)
                    new_obstacle_info = (obstacle_info[0] - 1, obstacle_info[1], obstacle_info[2] - 1, obstacle_info[3])
                    self.obstacles_info.append(new_obstacle_info)
                    self.game_map = sf.updateObstacle(self.game_map, new_obstacle_info)
                    self.game_map[move.endRow][move.endCol] = 3
                elif direct == "down":
                    self.obstacles_info.remove(obstacle_info)
                    new_obstacle_info = (obstacle_info[0] + 1, obstacle_info[1], obstacle_info[2] + 1, obstacle_info[3])
                    self.obstacles_info.append(new_obstacle_info)
                    self.game_map = sf.updateObstacle(self.game_map, new_obstacle_info)
                    self.game_map[move.endRow][move.endCol] = 3
                elif direct == "left":
                    self.obstacles_info.remove(obstacle_info)
                    new_obstacle_info = (obstacle_info[0], obstacle_info[1] - 1, obstacle_info[2], obstacle_info[3] - 1)
                    self.obstacles_info.append(new_obstacle_info)
                    self.game_map = sf.updateObstacle(self.game_map, new_obstacle_info)
                    self.game_map[move.endRow][move.endCol] = 3
                elif direct == "right":
                    self.obstacles_info.remove(obstacle_info)
                    new_obstacle_info = (obstacle_info[0], obstacle_info[1] + 1, obstacle_info[2], obstacle_info[3] + 1)
                    self.obstacles_info.append(new_obstacle_info)
                    self.game_map = sf.updateObstacle(self.game_map, new_obstacle_info)
                    self.game_map[move.endRow][move.endCol] = 3
                
            elif self.game_map[move.endRow][move.endCol] == 2:
                self.score += 20
                self.game_map[move.endRow][move.endCol] = 3
            else:
                self.game_map[move.endRow][move.endCol] = move.pieceMoved
            self.score -= 1
        else:
            self.game_map[move.endRow][move.endCol] = move.pieceMoved
        self.previous_state.append(move)

    def undo_move(self):
        if self.previous_state:
            move = self.previous_state.pop()
            self.game_map[move.startRow][move.startCol] = move.pieceMoved
            self.game_map[move.endRow][move.endCol] = move.pieceCaptured

    def move_support(self, move):
        self.game_map[move.startRow][move.startCol] = 0
        if not self.is_hider_move:
            if self.game_map[move.endRow][move.endCol] == 2:
                self.game_map[move.endRow][move.endCol] = 3
            else:
                self.game_map[move.endRow][move.endCol] = move.pieceMoved
        else:
            self.game_map[move.endRow][move.endCol] = move.pieceMoved
        self.previous_state.append(move)

    def getAllPossibleMoves(self):
        moves = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for r in range(0, len(self.game_map)): 
            for c in range(0, len(self.game_map[r])):
                piece = self.game_map[r][c]
                if (piece == 2 and self.is_hider_move) or (piece == 3 and not self.is_hider_move):
                    for dr, dc in directions:
                        new_r = r + dr
                        new_c = c + dc
                        if 0 <= new_r < len(self.game_map) and 0 <= new_c < len(self.game_map[r]):
                            if piece == 3 and self.game_map[new_r][new_c] == 2:
                                moves.append(Move((r, c), (new_r, new_c), self.game_map))
                            elif self.game_map[new_r][new_c] == 0:
                                moves.append(Move((r, c), (new_r, new_c), self.game_map))
        return moves

    def getRandomPositionsAroundHiders(self, radius=3):
        random_positions = {}
        for hider in self.getHiderPositions():
            valid_positions = []
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    nx, ny = hider[0] + dx, hider[1] + dy
                    if 0 <= nx < len(self.game_map) and 0 <= ny < len(self.game_map[0]) and self.game_map[nx][ny] != 1:
                        valid_positions.append((nx, ny))

            if valid_positions:
                chosen_position = random.choice(valid_positions)
                random_positions[chosen_position] = hider
        return random_positions

class Move():
    def __init__(self,startSq,endSq,game_map):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = game_map[self.startRow][self.startCol]
        self.pieceCaptured = game_map[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    
    def updateEndPoint(self, row, col):
        self.endRow = row
        self.endCol = col