import pygame
import pygame_gui
import time
import random
# количество клеток в строке
field_size = 10
gamer_symbol = "-"
ai_symbol = "-"
free_fields = []
danger_fields = []
def get_ai_step_coordinate():
    to_find = True
    while to_find:
        pos = (0,0)
        if len(danger_fields) > 0:
            buf = random.choice(danger_fields)
            pos = (buf[1],buf[0])
            danger_fields.remove(buf)
        else:
            pos = random.choice(free_fields)
        if check_field(pos[0], pos[1]):
            to_find = False
            return pos

def check_field(x, y):
    # print(field_array[y][x])
    if field_array[y][x] == "-":
        return True
    else: 
        try:
            free_fields.remove((x,y))
        except:
            print()
        return False
        

def output_array(array):
    for i in range(field_size):
        print(array[i])
    print()
    pass

def check_players_win(x, y, check_symbol):
    playerwins = False
    
    maxvalue = 0
    counter = 0
    counter_changed = False
    first_dangerous_pos = (0,0)
    #по горизонтали
    for i in range(field_size):
        if field_array[x][i] == check_symbol:
            if counter == 0 and not counter_changed:
                counter_changed = True
                first_dangerous_pos = (x,i-1)
            counter += 1
            maxvalue = counter
        else:
            counter = 0
            if maxvalue > 2:
                if (x,i) not in danger_fields:
                    danger_fields.append((x,i))
                if first_dangerous_pos not in danger_fields and first_dangerous_pos != (0,0):
                    danger_fields.append(first_dangerous_pos)
                    print("Горизонтально: " + str(first_dangerous_pos))
                if maxvalue > 1:
                    danger_fields.append((x,i))
            if maxvalue > 4:
                playerwins = True
            maxvalue = 0 

    #по вертикали
    maxvalue = 0
    counter = 0
    counter_changed = False
    first_dangerous_pos = (0,0)
    for j in range(field_size):
        if field_array[j][y] == check_symbol:
            if counter == 0 and not counter_changed:
                counter_changed = True
                first_dangerous_pos = (j-1,y)
            counter += 1
            maxvalue = counter
        else:
            counter = 0
            if maxvalue > 2:
                if (j,y) not in danger_fields:
                    danger_fields.append((j,y))
                if first_dangerous_pos not in danger_fields and first_dangerous_pos != (0,0):
                    danger_fields.append(first_dangerous_pos)
                    print("Вертикально: " + str(first_dangerous_pos))
            if maxvalue > 4:
                playerwins = True
            if maxvalue > 1:
                danger_fields.append((j,y))
            maxvalue = 0
    
    maxvalue = 0
    counter = 0
    counter_rl = 0
    counter_lr = 0
    pos_x = 0
    pos_y = 0
    steps = 0
    counter_changed = False
    first_dangerous_pos = (0,0)
    # по диагонали справа налево
    if (x+y) > 9:
        pos_x = 9
        pos_y = x+y-9
    else:
        pos_x = x+y
        pos_y = 0
    pos_rl = (pos_x, pos_y)
    
    if (x+y < 10):
        steps = pos_x
    else:
        steps = pos_x - pos_y

    for i in range(steps+1):
        if field_array[pos_x][pos_y] == check_symbol:
            if counter == 0 and not counter_changed:
                counter_changed = True
                first_dangerous_pos = (pos_x+1,pos_y-1)
            counter += 1
            maxvalue = counter
            if maxvalue > 4:
                playerwins = True
        else:
            counter = 0
            if maxvalue > 2:
                if (pos_x,pos_y) not in danger_fields and first_dangerous_pos != (0,0):
                    danger_fields.append((pos_x,pos_y))
                if first_dangerous_pos not in danger_fields:
                    danger_fields.append(first_dangerous_pos)
                    print("Диагональ справа налево: " + str(first_dangerous_pos))
            if maxvalue > 1:
                danger_fields.append((pos_x,pos_y))
            maxvalue = 0
        pos_x -=1
        pos_y +=1
            
    # по диагонали слева направо
    pos_x = 0
    pos_y = abs(y-x)
    pos_lr = (pos_x, pos_y)
    steps = 10 - pos_y
    counter_changed = False
    first_dangerous_pos = (0,0)
    
    for i in range(steps):
        if field_array[pos_x][pos_y] == check_symbol:
            if counter == 0 and not counter_changed:
                counter_changed = True
                first_dangerous_pos = (pos_x-1,pos_y-1)
            counter_lr += 1
            maxvalue = counter_lr
            if maxvalue > 4:
                playerwins = True
        else:
            counter_lr = 0
            if maxvalue > 2:
                if (pos_x,pos_y) not in danger_fields:
                    danger_fields.append((pos_x,pos_y))
                if first_dangerous_pos not in danger_fields and first_dangerous_pos != (0,0):
                    danger_fields.append(first_dangerous_pos)
                    print("Диагональ слева направо: " + str(first_dangerous_pos))
            if maxvalue > 1:
                danger_fields.append((pos_x,pos_y))
            maxvalue = 0
        pos_x +=1
        pos_y +=1
    return playerwins
    
def distance(point_1, point_2):
    return ((point_2[0] - point_1[0]) ** 2 + (point_2[1] - point_1[1]) ** 2) ** 0.5
    

print('Добро пожаловать в игру Крестики-Нолики!')

field_array = ["-"] * field_size
for i in range(field_size):
    field_array[i] = ["-"] * field_size
    for j in range(field_size):
        free_fields.append((i,j))

pygame.init()
pygame.font.init()
window_size = (404, 404)
pygame.display.set_caption("Крестики-Нолики")
screen = pygame.display.set_mode(window_size)
background_color = (255, 255, 255)
screen.fill(background_color)

#
question_font = pygame.font.SysFont('Monotxt_IV50', 29)
question = question_font.render("Выбери своего бойца", False, (0, 0, 0))
screen.blit(question, (5, 60))
pygame.draw.circle(screen, (0,0,0), (290, 230), 50, 4)
pygame.draw.line(screen, (0,0,0), (64, 184), (164, 280), 6)
pygame.draw.line(screen, (0,0,0), (64, 280), (164, 184), 6)
#x центр: (114, 232)
#y центр: (290, 230)

pygame.display.flip()
user_not_check = True
while user_not_check:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                user_not_check = False
                x_dist = distance(event.pos, (114, 232))
                zero_dist = distance(event.pos, (290, 230))
                if x_dist<zero_dist:
                    gamer_symbol = "X"
                    ai_symbol = "0"
                else: 
                    gamer_symbol = "0"
                    ai_symbol = "X"

screen.fill(background_color)

pygame.draw.line(screen,(0, 0, 0), (0, 0), (0, screen.get_height()), 2)
pygame.draw.line(screen,(0, 0, 0), (0, 0), (screen.get_width(), 0), 2)
pygame.draw.line(screen,(0, 0, 0), (screen.get_width()-2, screen.get_height()), (screen.get_width()-2, 0), 2)
pygame.draw.line(screen,(0, 0, 0), (screen.get_width(), screen.get_height()-2), (0, screen.get_height()-2), 2)

step = screen.get_width() / field_size
for i in range(field_size):
    start_pos = step * (i+1)
    pygame.draw.line(screen,(0, 0, 0), (start_pos, 0), (start_pos, screen.get_height()), 2)
    pygame.draw.line(screen,(0, 0, 0), (0, start_pos), (screen.get_width(), start_pos), 2)

pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x_array = int(event.pos[1] // step)
                y_array = int(event.pos[0] // step)
                if field_array[x_array][y_array] == "-":
                    field_array[x_array][y_array] = gamer_symbol
                    if (x_array, y_array) in danger_fields:
                        danger_fields.remove((x_array, y_array))
                    if gamer_symbol == "X":
                        draw_pos_x = (event.pos[0] // step) * step + 1
                        draw_pos_y = (event.pos[1] // step) * step + 1
                        pygame.draw.line(screen, (0,0,0), (draw_pos_x, draw_pos_y), (draw_pos_x+step, draw_pos_y+step), 5)
                        pygame.draw.line(screen, (0,0,0), (draw_pos_x, draw_pos_y+step), (draw_pos_x+step, draw_pos_y), 5)
                    elif gamer_symbol == "0":
                        draw_pos_x = (event.pos[0] // step) * step + step/2 + 1
                        draw_pos_y = (event.pos[1] // step) * step + step/2 + 1
                        pygame.draw.circle(screen, (0,0,0), (draw_pos_x, draw_pos_y), step/2, 4)
                    pygame.display.update()

                    gamer_win = check_players_win(x_array, y_array, gamer_symbol)
                    
                    
                    ai_pos = get_ai_step_coordinate()
                    ai_x = ai_pos[0]
                    ai_y = ai_pos[1]
                    field_array[ai_y][ai_x] = ai_symbol
                    if gamer_symbol == "X":
                        pygame.draw.circle(screen, (0,0,0), (ai_x*step + step/2, ai_y*step + step/2), step/2, 4)
                    elif gamer_symbol == "0":
                        pygame.draw.line(screen, (0,0,0), (ai_x*step, ai_y*step), (ai_x*step+step, ai_y*step+step), 5)
                        pygame.draw.line(screen, (0,0,0), (ai_x*step, ai_y*step+step), (ai_x*step+step, ai_y*step), 5)
                    time.sleep(0.500)
                    pygame.display.update()
                    ai_win = check_players_win(ai_y, ai_x, ai_symbol)
                    
                    output_array(field_array)
                    if gamer_win:
                        print("Игрок выиграл")
                        screen.fill(background_color)
                        pygame.display.update()
                        time.sleep(0.300)
                        win_font = pygame.font.SysFont('Monotxt_IV50', 70)
                        win_text = win_font.render("ПОБЕДА", False, (0, 0, 0))
                        screen.blit(win_text, (50, 65))
                        pygame.display.update()
                        time.sleep(0.500)
                        screen.blit(win_text, (50, 125))
                        pygame.display.update()
                        time.sleep(0.500)
                        win_text2 = win_font.render("ВРЕМЯ", False, (0, 0, 0))
                        screen.blit(win_text2, (75, 185))
                        pygame.display.update()
                        time.sleep(0.500)
                        win_text3 = win_font.render("ОБЕДА", False, (0, 0, 0))
                        screen.blit(win_text3, (75, 245))
                        pygame.display.update()
                        

                    elif ai_win:
                        print("Компьютер победил")
                        screen.fill(background_color)
                        pygame.display.update()
                        time.sleep(0.300)
                        win_font = pygame.font.SysFont('Monotxt_IV50', 40)
                        win_text = win_font.render("В ДРУГОЙ РАЗ", False, (0, 0, 0))
                        screen.blit(win_text, (28, 65))
                        win_text2 = win_font.render("ПОВЕЗЕТ", False, (0, 0, 0))
                        screen.blit(win_text2, (103, 125))
                        pygame.display.update()
                        time.sleep(0.300)
                        win_text2 = win_font.render("Ты проиграл", False, (0, 0, 0))
                        screen.blit(win_text2, (45, 230))
                        pygame.display.update()
        
                    
                        
                #для нолика расчет координат центра:
                # draw_pos_x = (event.pos[0] // step) * step + step/2 + 1
                # draw_pos_y = (event.pos[1] // step) * step + step/2 + 1
                # радиус = step/2

                

        pygame.display.update()