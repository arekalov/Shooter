import tkinter as tk
import time
import winsound
import random


# Закрытие игры
def close_game():
    global running
    running = False


# Панель счета
def status_bar():
    canvas.create_rectangle(0, 0, WIN_W, 45, fill='navy')
    canvas.create_text(300, 5, text="Gamer Score:", anchor=tk.NW,
                       font="Andale 25", fill='peru')
    canvas.create_text(510, 5, text=str(gamer_score), anchor=tk.NW,
                       font="Andale 25", fill='peru')
    canvas.create_text(10, 5, text="Enemy Score:", anchor=tk.NW,
                       font="Andale 25", fill='peru')
    canvas.create_text(220, 5, text=str(enemy_score), anchor=tk.NW,
                       font="Andale 25", fill='peru')


# движение врага
def enemy_move(enemy_speed):
    enemy_coords = canvas.coords(enemy)
    if enemy_coords[0] < 0 or enemy_coords[0] > WIN_W - enemy_width:
        enemy_speed = -enemy_speed
    canvas.move(enemy, enemy_speed, 0)
    return enemy_speed


# Движение корабля
def gamer_move(event):
    gamer_coords = canvas.coords(gamer)
    if event.keysym == 'a':
        if gamer_coords[0] >= 20:
            canvas.move(gamer, -gamer_speed, 0)
    if event.keysym == 'd':
        if gamer_coords[0] <= WIN_W - (gamer_width + 20):
            canvas.move(gamer, gamer_speed, 0)


# Стрельба ракетами
def gamer_shoot2(event):
    missile_coords = canvas.coords(gamer)
    missile_coords[0] += (gamer_width // 2 - missile_width // 2)
    missile = canvas.create_image(missile_coords[0], missile_coords[1],
                                  anchor=tk.NW, image=imgMissile)
    missiles.add(missile)
    winsound.PlaySound('missile1.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)


# Стрельба лазерами
def gamer_shoot1(event):
    laser_coords = canvas.coords(gamer)
    laser_coords[0] += (gamer_width - (laser_width + 12))
    laser_coords[1] += 25
    laser = canvas.create_image(laser_coords[0], laser_coords[1],
                                anchor=tk.NW, image=imgGamerLaser)
    lasers.add(laser)

    winsound.PlaySound('avtomat.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)


def enemy_shoot():
    enemy_laser_coords = canvas.coords(enemy)
    enemy_laser_coords[0] += (enemy_width // 2 - laser_width // 2)
    enemy_laser = canvas.create_image(enemy_laser_coords[0], enemy_laser_coords[1] + 175,
                                      anchor=tk.NW, image=imgEnemyLaser)
    enemy_lasers.add(enemy_laser)
    winsound.PlaySound('прыг.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)


# Движение лазеров врага
def enemy_laser_move():
    enemy_lasers_delete = set()
    for i in enemy_lasers:
        enemy_lasers_coords = canvas.coords(i)
        if enemy_lasers_coords[1] < gamer_y + 10:
            canvas.move(i, 0, 10)
        else:
            canvas.delete(i)
            enemy_lasers_delete.add(i)

    for j in enemy_lasers_delete:
        enemy_lasers.remove(j)


# Движение лазеров
def laser_move():
    laser_delete = set()
    for laser in lasers:
        laser_coords = canvas.coords(laser)
        if laser_coords[1] > enemy_y:
            canvas.move(laser, 0, -5)
        else:
            canvas.delete(laser)
            laser_delete.add(laser)

    for laser in laser_delete:
        lasers.remove(laser)


# Движение ракет
def missile_move():
    missile_delete = set()
    for missile in missiles:
        missile_coords = canvas.coords(missile)
        if missile_coords[1] > enemy_y:
            canvas.move(missile, 0, -3)
        else:
            canvas.delete(missile)
            missile_delete.add(missile)

    for missile in missile_delete:
        missiles.remove(missile)


def missile_destroy():
    global gamer_score
    missile_delete = set()
    for missile in missiles:
        missile_coords = canvas.coords(missile)
        enemy_coords = canvas.coords(enemy)
        if (missile_coords[0] + missile_width // 2) >= enemy_coords[0] and (missile_coords[0] + missile_width // 2) <= \
                enemy_coords[0] + enemy_width:
            if missile_coords[1] >= enemy_coords[1] and (missile_coords[1] <= enemy_coords[1] + enemy_height):
                gamer_score += 5
                canvas.delete(missile)
                missile_delete.add(missile)
                status_bar()
                explode = canvas.create_image(enemy_coords[0] + 80, enemy_coords[1] + 160,
                                              anchor=tk.NW, image=imgExplode)
                explodes[explode] = game_time
                winsound.PlaySound('explode2.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

    for missile in missile_delete:
        missiles.remove(missile)


def explodes_delete():
    explode_delete = set()
    for explode in explodes:
        if game_time - explodes[explode] > 20:
            canvas.delete(explode)
            explode_delete.add(explode)

    for explode in explode_delete:
        explodes.pop(explode)


def laser_destroy():
    global gamer_score
    laser_delete = set()
    for laser in lasers:
        laser_coords = canvas.coords(laser)
        enemy_coords = canvas.coords(enemy)
        if (laser_coords[0] + laser_width // 2) >= enemy_coords[0] and (laser_coords[0] + laser_width // 2) <= \
                enemy_coords[0] + enemy_width:
            if laser_coords[1] >= enemy_coords[1] and (laser_coords[1] <= enemy_coords[1] + enemy_height):
                gamer_score += 1
                canvas.delete(laser)
                laser_delete.add(laser)
                status_bar()
                explode = canvas.create_image(enemy_coords[0] + 80, enemy_coords[1] + 160,
                                              anchor=tk.NW, image=imgExplode1)
                explodes[explode] = game_time
                winsound.PlaySound('hit1.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

    for laser in laser_delete:
        lasers.remove(laser)


def gamer_destroy():
    global enemy_score
    laser_delete = set()
    for laser in enemy_lasers:
        laser_coords = canvas.coords(laser)
        gamer_coords = canvas.coords(gamer)
        if (laser_coords[0] + laser_width // 2) >= gamer_coords[0] and (laser_coords[0] + laser_width // 2) <= \
                gamer_coords[0] + gamer_width:
            if laser_coords[1] >= gamer_coords[1] and (laser_coords[1] <= gamer_coords[1] + gamer_height):
                enemy_score += 10
                canvas.delete(laser)
                laser_delete.add(laser)
                status_bar()
                explode = canvas.create_image(gamer_coords[0] + 30, gamer_coords[1],
                                              anchor=tk.NW, image=imgExplode1)
                explodes[explode] = game_time
                winsound.PlaySound('hit1.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)

    for laser in laser_delete:
        enemy_lasers.remove(laser)


# Размеры игрового окна
WIN_H = 700
WIN_W = 1200

# Параметры Игрока
gamer_x = WIN_W / 2
gamer_y = WIN_H - 130
gamer_speed = 10

# Параметры противника
enemy_x = WIN_W / 2
enemy_y = 33
enemy_speed = 5

# Параметры Игрока
gamer_score = 0

# Параметры противника
enemy_score = 0

# Создание игрового окна
win = tk.Tk()
win.title('Paper Shooter')
win.config(width=WIN_W, height=WIN_H)
win.resizable(False, False)

win.protocol("WM_DELETE_WINDOW", close_game)

# Создание холста
canvas = tk.Canvas(win, bg='white', highlightthickness=0)
canvas.place(x=0, y=0, width=WIN_W, height=WIN_H)

# Создание фона
background_image = tk.PhotoImage(file="cletka.gif")
background = canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

# Загрузка изображений
imgGamer = tk.PhotoImage(file="man3.png")
gamer_width = imgGamer.width()
gamer_height = imgGamer.height()

imgEnemy = tk.PhotoImage(file="monster.png")
enemy_width = imgEnemy.width()
enemy_height = imgEnemy.height()

# Загрузка изображений
imgMissile = tk.PhotoImage(file="missile2.png")
missile_width = imgMissile.width()
missile_height = imgMissile.height()

imgGamerLaser = tk.PhotoImage(file="pulya.png")
laser_width = imgGamerLaser.width()
laser_height = imgGamerLaser.height()

imgEnemyLaser = tk.PhotoImage(file="pulya_enemy.png")
enemy_laser_width = imgGamerLaser.width()
enemy_laser_height = imgGamerLaser.height()

imgExplode = tk.PhotoImage(file="boom.png")
explode_width = imgExplode.width()
explode_height = imgExplode.height()

imgExplode1 = tk.PhotoImage(file="boom.png")
explode1_width = imgExplode1.width()
explode1_height = imgExplode1.height()

# Создание пустых множеств ракет и лазеров
missiles = set()
lasers = set()
enemy_lasers = set()
explodes = dict()

# Создание игрока и противника
gamer = canvas.create_image(gamer_x, gamer_y, anchor=tk.NW, image=imgGamer)
enemy = canvas.create_image(enemy_x, enemy_y, anchor=tk.NW, image=imgEnemy)

# Создание панели состояния игры
status_bar()

# Привязка событий к действиям
canvas.bind_all('<Key>', gamer_move)
canvas.bind_all('<Button-1>', gamer_shoot1)
canvas.bind_all('<Button-3>', gamer_shoot2)

game_time = 0
frame_count = 0
laser_count = 0
flag = False
# Игровой цикл
running = True
while running:
    # Управление объектами окна

    d = random.randint(0, 200)
    if d < 1:
        enemy_speed = -enemy_speed
    f = random.randint(0, 200)
    if f < 1:
        flag = True
    if flag:
        frame_count += 1
        if frame_count % 10 == 0:
            if laser_count < 5:
                enemy_shoot()
                laser_count += 1
            else:
                flag = False
                laser_count = 0

    enemy_speed = enemy_move(enemy_speed)
    missile_move()
    laser_move()
    enemy_laser_move()
    missile_destroy()
    laser_destroy()
    gamer_destroy()
    explodes_delete()

    # Обновление окна
    win.update()
    time.sleep(0.01)
    game_time += 1

# Завершение программы
win.destroy()
