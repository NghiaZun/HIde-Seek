import pygame as p
import astar as a
import vision as v
import kit as k
import random
import time
import threading
import tkinter as tk
import smartmove as s
import supportfunction as sf

WIDTH = 0
HEIGHT = 0
DIMENSION = []
UNIT_HEIGHT = 0
UNIT_WIDTH = 0
MAX_FPS = 120
VISION = (144, 238, 144)
IMAGES = {}
seeker_position = (0, 0)
delay = 200
selected_level = None
flag = True
endTime = 120

# Define RGB code of the color.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BACKGROUND = (226, 173, 110)


def load_map(game_state, file_path):
    global DIMENSION, UNIT_HEIGHT, UNIT_WIDTH
    with open(file_path, 'r') as file:
        dimensions = file.readline().strip().split()
        DIMENSION = [int(dimensions[0]), int(dimensions[1])]
        UNIT_HEIGHT = HEIGHT // DIMENSION[0]
        UNIT_WIDTH = WIDTH // DIMENSION[1]
        for r in range(DIMENSION[0]):
            row = [int(x) for x in file.readline().strip().split()]
            game_state.game_map.append(row)
        obstacles_info = []
        for line in file:
            obstacle = [int(x) for x in line.strip().split()]
            obstacles_info.append(tuple(obstacle))
        sf.add_obstacles_to_map(game_state,obstacles_info)
        game_state.obstacles_info = obstacles_info

def load_images():
    units = ['0', '1', '2', '3', '4', '5', '6', '14','15']
    for unit in units:
        IMAGES[unit] = p.image.load("images/" + unit + ".png")

def draw_game_state(screen, gs, start_pos, vision_distance, goals):
    draw_game_map(screen)
    draw_unit(screen, gs.game_map, goals)
    draw_vision(screen, gs.game_map, start_pos, vision_distance)

def draw_game_map(screen):
    colors = p.Color("white")
    for r in range(DIMENSION[0]):
        for c in range(DIMENSION[1]):
            p.draw.rect(screen, colors, p.Rect(c * UNIT_WIDTH, r * UNIT_HEIGHT, UNIT_WIDTH, UNIT_HEIGHT))

def draw_unit(screen, game_map, goals):
    for r in range(len(game_map)):
        for c in range(len(game_map[0])):
            if str(game_map[r][c]) in IMAGES:
                image = IMAGES[str(game_map[r][c])]
                scaled_image = p.transform.scale(image, (UNIT_WIDTH, UNIT_HEIGHT))
                screen.blit(scaled_image, p.Rect(c * UNIT_WIDTH, r * UNIT_HEIGHT, UNIT_WIDTH, UNIT_HEIGHT))
    if goals:
        for (r, c) in goals:
            if game_map[r][c] == 0:
                image = IMAGES["5"]
                scaled_image = p.transform.scale(image, (UNIT_WIDTH, UNIT_HEIGHT))
                screen.blit(scaled_image, p.Rect(c * UNIT_WIDTH, r * UNIT_HEIGHT, UNIT_WIDTH, UNIT_HEIGHT))

def draw_vision(screen, game_map, seeker_pos, sight_distance):
    (x0, y0) = seeker_pos
    for dx in range(-sight_distance, sight_distance + 1):
        for dy in range(-sight_distance, sight_distance + 1):
            x1, y1 = x0 + dx, y0 + dy
            if 0 <= x1 < len(game_map) and 0 <= y1 < len(game_map[0]):
                line_points = v.bresenham_line(x0, y0, x1, y1)
                for (x, y) in line_points:
                    if game_map[x][y] == 1 or game_map[x][y] == 14:
                        break
                    elif game_map[x][y] in [2, 3]:
                        if game_map[x][y] == 2:
                            image = IMAGES["4"]
                            scaled_image = p.transform.scale(image, (UNIT_WIDTH, UNIT_HEIGHT))
                            screen.blit(scaled_image, p.Rect(y * UNIT_WIDTH, x * UNIT_HEIGHT, UNIT_WIDTH, UNIT_HEIGHT))
                        elif game_map[x][y] == 3:
                            image = IMAGES["15"]
                            scaled_image = p.transform.scale(image, (UNIT_WIDTH, UNIT_HEIGHT))
                            screen.blit(scaled_image, p.Rect(y * UNIT_WIDTH, x * UNIT_HEIGHT, UNIT_WIDTH, UNIT_HEIGHT))
                        continue
                    else:
                        image = IMAGES["6"]
                        scaled_image = p.transform.scale(image, (UNIT_WIDTH, UNIT_HEIGHT))
                        screen.blit(scaled_image, p.Rect(y * UNIT_WIDTH, x * UNIT_HEIGHT, UNIT_WIDTH, UNIT_HEIGHT))

def countdown():

    def seconds_to_hhmmss(seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def support(remaining_time):
        global flag
        if remaining_time > 0 and flag == True:
            formatted_time = seconds_to_hhmmss(remaining_time)
            label.config(text=f"Remaining time: {formatted_time}")
            label.after(1000, support, remaining_time - 1)
        else:
            label.config(text="Time's up!")
            root.after(0, close_window)
            flag = False

    def close_window():
        global flag
        flag = False
        root.destroy()

    root = tk.Tk()
    root.title("Countdown timer")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    root.geometry(f"225x50+0+0")

    label = tk.Label(root, text="Counting down...", font=("Helvetica", 14))
    label.pack(pady=10)

    support(endTime)

    root.mainloop()

def main():
    p.init()
    global WIDTH, HEIGHT
    screen_info = p.display.Info()
    WIDTH = screen_info.current_w
    HEIGHT = screen_info.current_h
    screen = p.display.set_mode((WIDTH, HEIGHT))
    font = p.font.Font(None, 36)
    global selected_level

    def draw_level_buttons():
        screen.fill(BACKGROUND)

        left_image = p.image.load("images/8.png")
        desired_size = (300, 300)
        left_image = p.transform.scale(left_image, desired_size)
        left_image_rect = left_image.get_rect()
        left_image_rect.topleft = (50, 450)
        screen.blit(left_image, left_image_rect)

        right_image = p.image.load("images/9.png")
        right_image = p.transform.scale(right_image, desired_size)
        right_image_rect = right_image.get_rect()
        right_image_rect.topright = (screen.get_width() - 50, 450)
        screen.blit(right_image, right_image_rect)

        left_image = p.image.load("images/12.png")
        desired_size = (21, 250)
        left_image = p.transform.scale(left_image, desired_size)
        left_image_rect = left_image.get_rect()
        left_image_rect.topleft = (50, 0)
        screen.blit(left_image, left_image_rect)

        right_image = p.image.load("images/12.png")
        right_image = p.transform.scale(right_image, desired_size)
        right_image_rect = right_image.get_rect()
        right_image_rect.topright = (screen.get_width() - 50, 0)
        screen.blit(right_image, right_image_rect)

        left_image = p.image.load("images/12.png")
        desired_size = (21, 250)
        left_image = p.transform.scale(left_image, desired_size)
        left_image_rect = left_image.get_rect()
        left_image_rect.topleft = (325, 0)
        screen.blit(left_image, left_image_rect)

        right_image = p.image.load("images/12.png")
        right_image = p.transform.scale(right_image, desired_size)
        right_image_rect = right_image.get_rect()
        right_image_rect.topright = (screen.get_width() - 325, 0)
        screen.blit(right_image, right_image_rect)

        left_image = p.image.load("images/10.png")
        desired_size = (300, 300)
        left_image = p.transform.scale(left_image, desired_size)
        left_image_rect = left_image.get_rect()
        left_image_rect.topleft = (50, 100)
        screen.blit(left_image, left_image_rect)

        right_image = p.image.load("images/11.png")
        right_image = p.transform.scale(right_image, desired_size)
        right_image_rect = right_image.get_rect()
        right_image_rect.topright = (screen.get_width() - 50, 100)
        screen.blit(right_image, right_image_rect)

        image = p.image.load("images/7.png")
        desired_size = (500, 500)
        image = p.transform.scale(image, desired_size)

        image_rect = image.get_rect()
        image_rect.centerx = screen.get_rect().centerx
        screen.blit(image, image_rect)

        button_width = 200
        button_height = 40
        button_x = (screen.get_width() - button_width) / 2

        button_y_offset = image_rect.bottom

        p.draw.rect(screen, WHITE, (button_x, button_y_offset, button_width, button_height))
        p.draw.rect(screen, WHITE, (button_x, button_y_offset + 75, button_width, button_height))
        p.draw.rect(screen, WHITE, (button_x, button_y_offset + 150, button_width, button_height))
        p.draw.rect(screen, WHITE, (button_x, button_y_offset + 225, button_width, button_height))

        text_surface = font.render("Level 1", True, BLACK)
        screen.blit(text_surface, (button_x + (button_width - text_surface.get_width()) / 2, button_y_offset + 5))
        text_surface = font.render("Level 2", True, BLACK)
        screen.blit(text_surface, (button_x + (button_width - text_surface.get_width()) / 2, button_y_offset + 80))
        text_surface = font.render("Level 3", True, BLACK)
        screen.blit(text_surface, (button_x + (button_width - text_surface.get_width()) / 2, button_y_offset + 155))
        text_surface = font.render("Level 4", True, BLACK)
        screen.blit(text_surface, (button_x + (button_width - text_surface.get_width()) / 2, button_y_offset + 230))

    def handle_click(mouse_pos):
        global selected_level
        button_width = 200
        button_height = 40
        button_x = (screen.get_width() - button_width) / 2
        if button_x <= mouse_pos[0] <= button_x + button_width:
            button_y_offset = 500
            if button_y_offset <= mouse_pos[1] <= button_y_offset + button_height:
                selected_level = 1
            elif button_y_offset + 75 <= mouse_pos[1] <= button_y_offset + 75 + button_height:
                selected_level = 2
            elif button_y_offset + 150 <= mouse_pos[1] <= button_y_offset + 150 + button_height:
                selected_level = 3
            elif button_y_offset + 225 <= mouse_pos[1] <= button_y_offset + 225 + button_height:
                selected_level = 4

    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            elif event.type == p.MOUSEBUTTONDOWN:
                mouse_pos = p.mouse.get_pos()
                handle_click(mouse_pos)

        if selected_level is not None:
            running = False
        else:
            draw_level_buttons()
            p.display.flip()

    p.quit()

    if (selected_level == 1):
        global seeker_position
        p.init()
        screen_info = p.display.Info()
        WIDTH = screen_info.current_w
        HEIGHT = screen_info.current_h
        screen = p.display.set_mode((WIDTH, HEIGHT))
        clock = p.time.Clock()
        screen = p.display.set_mode((WIDTH, HEIGHT))
        screen.fill(p.Color("white"))
        gs = k.GameState()
        load_map(gs, "maps/map1.txt")
        load_images()
        running = True
        move_count = 0
        goals = []
        while running:
            if not gs.getHiderPositions():
                print(move_count)
                print("Game End. Final Score:", gs.score)
                running = False
                draw_game_map(screen)
                draw_unit(screen,gs.game_map,goals)
                p.display.flip()
                p.time.delay(delay)
                break
                clock.tick(MAX_FPS)
            if move_count % 4 == 0 and move_count != 0:
                goals = {}
                goals = gs.getRandomPositionsAroundHiders()
            start_pos = gs.getSeekerPosition()
            visible_hiders = v.Seeker_See_Hider(start_pos, gs.game_map)
            if visible_hiders:
                closest_hider = min(visible_hiders, key=lambda h: a.heuristic(start_pos, h))
                main_path = a.a_star_search(start_pos, [closest_hider], gs)
                if main_path:
                    move = k.Move(start_pos, main_path[1], gs.game_map)
                    gs.makeMove(move)
                    start_pos = main_path[1]
                    draw_game_state(screen, gs, start_pos, 3, goals)
                    p.display.flip()
                    p.time.delay(delay)
                    move_count += 1
            else:
                if goals:
                    closest_announcement = min(goals.keys(), key=lambda h: a.heuristic(start_pos, h))
                    sub_path = a.a_star_search(start_pos, [closest_announcement], gs)
                    if sub_path and len(sub_path) > 1:
                        move = k.Move(start_pos, sub_path[1], gs.game_map)
                        gs.makeMove(move)
                        start_pos = sub_path[1]
                        draw_game_state(screen, gs, start_pos, 3, goals)
                        p.display.flip()
                        p.time.delay(delay)
                        move_count += 1
                    elif len(sub_path) == 0:
                        index = list(goals).index(closest_announcement)
                        goals.pop(index)
                    else:
                        dx = random.choice([-1, 0, 1])
                        dy = random.choice([-1, 0, 1])
                        new_position = (start_pos[0] + dx, start_pos[1] + dy)
                        if gs.isValidUnitToMove(new_position):
                            move = k.Move(start_pos, new_position, gs.game_map)
                            gs.makeMove(move)
                            move_count += 1
                            draw_game_state(screen, gs, start_pos, 3, goals)
                            p.display.flip()
                            p.time.delay(delay)
                else:
                    dx = random.choice([-1, 0, 1])
                    dy = random.choice([-1, 0, 1])
                    new_position = (start_pos[0] + dx, start_pos[1] + dy)
                    if gs.isValidUnitToMove(new_position):
                        move = k.Move(start_pos, new_position, gs.game_map)
                        gs.makeMove(move)
                        move_count += 1
                        draw_game_state(screen, gs, start_pos, 3, goals)
                        p.display.flip()
                        p.time.delay(delay)

    if (selected_level == 2):
        global seeker_position
        p.init()
        screen_info = p.display.Info()
        WIDTH = screen_info.current_w
        HEIGHT = screen_info.current_h
        screen = p.display.set_mode((WIDTH, HEIGHT))
        clock = p.time.Clock()
        screen = p.display.set_mode((WIDTH, HEIGHT))
        screen.fill(p.Color("white"))
        gs = k.GameState()
        load_map(gs, "maps/map2.txt")
        load_images()
        running = True
        move_count = 0
        goals = []
        while running: 
            if not gs.getHiderPositions():
                print(move_count)
                print("Game End. Final Score:", gs.score)
                running = False
                draw_game_map(screen)
                draw_unit(screen,gs.game_map,goals)
                p.display.flip()
                p.time.delay(delay)
                break
                clock.tick(MAX_FPS)
            if move_count % 4 == 0 and move_count != 0:
                goals = {}
                goals = gs.getRandomPositionsAroundHiders()
            start_pos = gs.getSeekerPosition()
            visible_hiders = v.Seeker_See_Hider(start_pos, gs.game_map)
            if visible_hiders:
                closest_hider = min(visible_hiders, key=lambda h: a.heuristic(start_pos, h))
                main_path = a.a_star_search(start_pos, [closest_hider], gs)
                if main_path:
                    move = k.Move(start_pos, main_path[1], gs.game_map)
                    gs.makeMove(move)
                    start_pos = main_path[1]
                    draw_game_state(screen, gs, start_pos, 3, goals)
                    p.display.flip()
                    p.time.delay(delay)
                    move_count += 1
            else:
                if goals:
                    closest_announcement = min(goals.keys(), key=lambda h: a.heuristic(start_pos, h))
                    sub_path = a.a_star_search(start_pos, [closest_announcement], gs)
                    if sub_path and len(sub_path) > 1:
                        move = k.Move(start_pos, sub_path[1], gs.game_map)
                        gs.makeMove(move)
                        start_pos = sub_path[1]
                        draw_game_state(screen, gs, start_pos, 3, goals)
                        p.display.flip()
                        p.time.delay(delay)
                        move_count += 1
                    elif len(sub_path) == 0:
                        index = list(goals).index(closest_announcement)
                        print(goals)
                        goals.pop(index)
                    else:
                        dx = random.choice([-1, 0, 1])
                        dy = random.choice([-1, 0, 1])
                        new_position = (start_pos[0] + dx, start_pos[1] + dy)
                        if gs.isValidUnitToMove(new_position):
                            move = k.Move(start_pos, new_position, gs.game_map)
                            gs.makeMove(move)
                            move_count += 1
                            draw_game_state(screen, gs, start_pos, 3, goals)
                            p.display.flip()
                            p.time.delay(delay)
                else:
                    dx = random.choice([-1, 0, 1])
                    dy = random.choice([-1, 0, 1])
                    new_position = (start_pos[0] + dx, start_pos[1] + dy)
                    if gs.isValidUnitToMove(new_position):
                        move = k.Move(start_pos, new_position, gs.game_map)
                        gs.makeMove(move)
                        move_count += 1
                        draw_game_state(screen, gs, start_pos, 3, goals)
                        p.display.flip()
                        p.time.delay(delay)
    
    if (selected_level == 3):
        global seeker_position
        p.init()
        screen_info = p.display.Info()
        WIDTH = screen_info.current_w
        HEIGHT = screen_info.current_h
        screen = p.display.set_mode((WIDTH, HEIGHT))
        clock = p.time.Clock()
        screen.fill(p.Color("white"))
        gs = k.GameState()
        list_map = ["maps/map3.txt", "maps/map5.txt"]
        random_map = random.choice(list_map)
        load_map(gs, random_map)
        load_images()
        running = True
        move_count = 0
        goals = {}
        while running:
            
            if not gs.getHiderPositions():
                print(move_count)
                print("Game End. Final Score:", gs.score)
                running = False
                draw_game_map(screen)
                draw_unit(screen,gs.game_map,goals)
                p.display.flip()
                p.time.delay(delay)
                break
                clock.tick(MAX_FPS)

            gs.is_hider_move = False
            start_pos = gs.getSeekerPosition()
            if move_count % 4 == 0 and move_count != 0:
                goals = {}
                goals = gs.getRandomPositionsAroundHiders()
            if not gs.is_hider_move:
                draw_game_state(screen, gs, start_pos, 3, goals)
                p.display.flip()
                p.time.delay(delay)
                visible_hiders = v.Seeker_See_Hider(start_pos, gs.game_map)
                if visible_hiders:
                    valid_moves = gs.getAllPossibleMoves()
                    best_move = s.findBestMove(gs, valid_moves)
                    gs.makeMove(best_move)
                    move_count += 1
                else:
                    if goals:
                        closest_announcement = min(goals.keys(), key=lambda h: a.heuristic(start_pos, h))
                        sub_path = a.a_star_search(start_pos, [closest_announcement], gs)
                        if sub_path and len(sub_path) > 1:
                            move = k.Move(start_pos, sub_path[1], gs.game_map)
                            gs.makeMove(move)
                            start_pos = sub_path[1]
                            move_count += 1
                        elif len(sub_path) == 0:
                            index = list(goals).index(closest_announcement)
                            goals.pop(index)
                        else:
                            directions = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)])
                            new_position = (start_pos[0] + directions[0], start_pos[1] + directions[1])
                            if gs.isValidUnitToMove(new_position):
                                move = k.Move(start_pos, new_position, gs.game_map)
                                gs.makeMove(move)
                                move_count += 1
                                    
                    else:
                        directions = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)])
                        new_position = (start_pos[0] + directions[0], start_pos[1] + directions[1])
                        if gs.isValidUnitToMove(new_position):
                            move = k.Move(start_pos, new_position, gs.game_map)
                            gs.makeMove(move)
                            move_count += 1
                
                end_pos = gs.getSeekerPosition()
                draw_game_state(screen, gs, end_pos, 3, goals)
                p.display.flip()
                p.time.delay(delay)

            gs.is_hider_move = True
            if gs.is_hider_move:
                for start_pos_hider in gs.getHiderPositions():
                    draw_game_state(screen, gs, start_pos_hider, 2, goals)
                    p.display.flip()
                    p.time.delay(delay)
                    visible_seeker = v.Hider_See_Seeker(start_pos_hider,gs.game_map)
                    if visible_seeker:
                        valid_moves = gs.getAllPossibleMoves()
                        #print(valid_moves)
                        best_move = s.findBestMove(gs, valid_moves)
                        gs.makeMove(best_move)
                    else:
                        directions = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)])
                        new_position = (start_pos_hider[0] + directions[0], start_pos_hider[1] + directions[1])
                        if gs.isValidUnitToMove(new_position):
                            move = k.Move(start_pos_hider, new_position, gs.game_map)
                            gs.makeMove(move)

            gs.is_hider_move = False

    if (selected_level == 4):

        def level_4():

            global flag # Multithread
            global seeker_position
            p.init()
            screen_info = p.display.Info()
            WIDTH = screen_info.current_w
            HEIGHT = screen_info.current_h
            screen = p.display.set_mode((WIDTH, HEIGHT))
            clock = p.time.Clock()
            screen.fill(p.Color("white"))
            gs = k.GameState()
            load_map(gs, "maps/map4.txt")
            load_images()
            running = True
            move_count = 0
            goals = {}

            while running and flag:
                gs.is_hider_move = False
                start_pos = gs.getSeekerPosition()
                if move_count % 4 == 0 and move_count != 0:
                    goals = {}
                    goals = gs.getRandomPositionsAroundHiders()
                if not gs.is_hider_move:
                    draw_game_state(screen, gs, start_pos, 3, goals)
                    p.display.flip()
                    p.time.delay(delay)
                    visible_hiders = v.Seeker_See_Hider(start_pos, gs.game_map)
                    if visible_hiders:
                        valid_moves = gs.getAllPossibleMoves()
                        best_move = s.findBestMove(gs, valid_moves)
                        gs.makeMove(best_move)
                    else:
                        if goals:
                            closest_announcement = min(goals.keys(), key=lambda h: a.heuristic(start_pos, h))
                            
                            sub_path = a.a_star_search_sub(start_pos, [closest_announcement], gs)
                            if len(sub_path) == 0:
                                sub_path = a.a_star_search(start_pos, [closest_announcement], gs)
                            if sub_path and len(sub_path) > 1:
                                move = k.Move(start_pos, sub_path[1], gs.game_map)
                                gs.makeMove_advanced(move)
                                start_pos = sub_path[1]
                            elif len(sub_path) == 0:
                                index = list(goals).index(closest_announcement)
                                goals.pop(index)
                            else:
                                while True:
                                    directions = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)])
                                    new_position = (start_pos[0] + directions[0], start_pos[1] + directions[1])
                                    if gs.isValidUnitToMove(new_position):
                                        move = k.Move(start_pos, new_position, gs.game_map)
                                        gs.makeMove_advanced(move)
                                        break
                        else:
                            while True:
                                directions = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)])
                                new_position = (start_pos[0] + directions[0], start_pos[1] + directions[1])
                                if gs.isValidUnitToMove(new_position):
                                    move = k.Move(start_pos, new_position, gs.game_map)
                                    gs.makeMove(move)
                                    break
                    move_count += 1
                    end_pos = gs.getSeekerPosition()
                    draw_game_state(screen, gs, end_pos, 3, goals)
                    p.display.flip()
                    p.time.delay(delay)

                gs.is_hider_move = True
                if gs.is_hider_move:
                    for start_pos_hider in gs.getHiderPositions():
                        draw_game_state(screen, gs, start_pos_hider, 2, goals)
                        p.display.flip()
                        p.time.delay(delay)
                        visible_seeker = v.Hider_See_Seeker(start_pos_hider,gs.game_map)
                        if visible_seeker:
                            valid_moves = gs.getAllPossibleMoves()
                            best_move = s.findBestMove(gs, valid_moves)
                            gs.makeMove(best_move)
                        else:
                            while True:
                                directions = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)])
                                new_position = (start_pos_hider[0] + directions[0], start_pos_hider[1] + directions[1])
                                if gs.isValidUnitToMove(new_position):
                                    move = k.Move(start_pos_hider, new_position, gs.game_map)
                                    gs.makeMove(move)
                                    break

                gs.is_hider_move = False
                
                
                if not gs.getHiderPositions() or not flag:
                    print("Game End. Final Score:", gs.score)
                    running = False
                    flag = False
                    clock.tick(MAX_FPS)

        main_thread = threading.Thread(target = level_4)
        sub_thread = threading.Thread(target = countdown)

        main_thread.start()
        sub_thread.start()

        main_thread.join()
        sub_thread.join()

if __name__ == "__main__":
    main()