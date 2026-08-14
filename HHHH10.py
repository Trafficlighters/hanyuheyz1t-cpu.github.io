import turtle
import random

# ----------------- 游戏初始化 -----------------
screen = turtle.Screen()
screen.title("Three Chambers - 10. Hell Mode: Finale")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)

# ----------------- 绘制迷宫边界与障碍 -----------------
drawer = turtle.Turtle()
drawer.hideturtle()
drawer.speed(0)
drawer.color("red")
drawer.pensize(3)

def draw_borders():
    drawer.penup()
    drawer.goto(-250, 250)
    drawer.pendown()
    for _ in range(4):
        drawer.forward(500)
        drawer.right(90)

draw_borders()

# ----------------- 玩家设置 -----------------
player = turtle.Turtle()
player.shape("square")
player.color("green")
player.color("yellow")
player.color("blue")
player.penup()
player.speed(0)
player.goto(-200, 200)

# ----------------- 敌人设置 (地狱模式多重追击) -----------------
enemies = []
colors = ["purple", "orange", "magenta"]
for i in range(3):
    en = turtle.Turtle()
    en.shape("square")
    en.color(colors[i])
    en.penup()
    en.speed(0)
    en.goto(150 + i * 30, -150)
    enemies.append(en)

# 15x15 宏大世界地图
original_map = [
    ["1","P","1","1","1","1","1","1","1","1","1","1","1","1","1"],
    ["1","0","0","1","1","1","B","T","0","1","1","0","0","2","1"], 
    ["1","0","1","1","1","1","0","1","0","1","1","0","1","1","1"], 
    ["1","0","1","1","1","1","0","1","0","1","1","0","1","0","1"], 
    ["1","0","1","1","1","1","1","1","0","1","1","0","1","0","1"], 
    ["1","0","1","0","1","1","0","0","0","0","0","0","0","0","1"], 
    ["1","0","1","0","0","1","0","0","1","1","1","1","1","0","1"], 
    ["1","0","1","1","0","1","0","0","0","1","1","0","0","0","1"], 
    ["1","0","1","1","1","1","0","0","1","1","1","0","1","1","1"], 
    ["P","0","1","1","1","1","0","0","0","1","1","0","0","0","1"], 
    ["1","0","1","1","1","1","1","0","1","1","1","0","0","0","1"], 
    ["1","0","1","1","1","1","1","0","1","1","S","0","0","0","1"], 
    ["1","0","1","1","1","1","1","0","1","1","0","1","1","1","1"], 
    ["1","0","0","0","1","0","0","0","0","0","0","0","0","0","1"], 
    ["1","1","1","1","1","1","1","1","1","1","1","1","1","1","1"]
]


# --- 2. 核心判定与随机陷阱刷新 ---
def get_current_room(col):
    if col <= 4: return 1
    elif 5 <= col <= 9: return 2
    else: return 3

def grid_to_screen(col, row):
    return -210 + (col * tile_size), 210 - (row * tile_size)

def draw_square(col, row, color):
    sx, sy = grid_to_screen(col, row)
    drawer.penup()
    drawer.goto(sx, sy)
    drawer.setheading(0) 
    drawer.color(color)
    drawer.begin_fill()
    for _ in range(4):
        drawer.forward(tile_size - 1)
        drawer.right(90)
    drawer.end_fill()

def randomize_hazards():
    """硬核：每次行动动态搅乱地图陷阱"""
    global maze_map
    for r in range(1, 14):
        for c in range(1, 14):
            if original_map[r][c] in ("T", "X") and maze_map[r][c] in ("0", "T", "X"):
                maze_map[r][c] = random.choice(["T", "X", "0"])

def draw_game():
    drawer.clear()
    for r in range(15):
        for c in range(15):
            tile_room = get_current_room(c)
            distance = abs(r - player_row) + abs(c - player_col)
            
            if tile_room == 2 and distance > 2:
                draw_square(c, r, "#111111")
                continue
            if tile_room == 3:
                if room3_light_mode == 0:
                    draw_square(c, r, "#111111")
                    continue
                elif room3_light_mode == 1 and distance > 2:
                    draw_square(c, r, "#111111")
                    continue

            tile = maze_map[r][c]
            if tile == "1": draw_square(c, r, "#2c3e50")       
            elif tile == "2": draw_square(c, r, "#f1c40f") 
            elif tile == "0": draw_square(c, r, "#222222")   

# ----------------- 游戏状态变量 -----------------
score = 0
game_over = False

# ----------------- 移动控制函数 -----------------
def move_up():
    y = player.ycor()
    if y < 230:
        player.sety(y + 20)

def move_down():
    y = player.ycor()
    if y > -230:
        player.sety(y - 20)

def move_left():
    x = player.xcor()
    if x > -230:
        player.setx(x - 20)

def move_right():
    x = player.xcor()
    if x < 230:
        player.setx(x + 20)

# 特殊技能按键模拟 (Q 键推开敌人 / E 键清除障碍提示)
def special_push():
    for en in enemies:
        if player.distance(en) < 50:
            en.backward(40)

def restart_game():
    global game_over
    game_over = False
    player.goto(-200, 200)
    for i, en in enumerate(enemies):
        en.goto(150 + i * 30, -150)

# ----------------- 键盘绑定 -----------------
screen.listen()
screen.onkey(move_up, "w")
screen.onkey(move_down, "s")
screen.onkey(move_left, "a")
screen.onkey(move_right, "d")
screen.onkey(move_up, "Up")
screen.onkey(move_down, "Down")
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")
screen.onkey(special_push, "q")
screen.onkey(restart_game, "r")

# ----------------- 游戏主循环 -----------------
def game_loop():
    global game_over
    if not game_over:
        # 敌人的追踪逻辑
        for en in enemies:
            en.setheading(en.towards(player))
            en.forward(1.5)  # 地狱模式敌人的移动速度较快
            
            # 检测碰撞
            if player.distance(en) < 15:
                game_over = True
                
        screen.update()
        screen.ontimer(game_loop, 20)
    else:
        drawer.penup()
        drawer.goto(0, 0)
        drawer.color("white")
        drawer.write("GAME OVER - 按 R 键重试", align="center", font=("Arial", 20, "bold"))
        screen.update()

game_loop()
screen.mainloop()