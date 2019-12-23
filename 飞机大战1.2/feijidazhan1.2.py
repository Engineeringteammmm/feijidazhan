import pygame
import time
import random
from pygame.locals import *
import time

#
# def judge(self):
#     if self.y < 0:
#         return True
#     else:
#         return False

#全局变量
#窗口
window_screen = None
#hero
hero = None
#得分
hit_score = 75
# 飞机最大子弹数
plane_maximum_bullet = [2, 5, 7, 12]  # enemy0, enemy1, enemy2, hero
#关于飞机
##飞机HP
HP_list = [1, 10, 45, 10]
#飞机大小
plane_size = [{"width":51, "height":39}, {"width":69, "height":89}, {"width":165, "height":246}, {"width":100, "height":124}]
#各种飞机爆炸效果换图片时间
plane_bomb_time = [5, 10, 18, 8]
#血量补给
blood_supply = None
#子弹补给
bullet_supply = None

#关于子弹
#敌机子弹类型
bullet_type = ["bullet1.png", "bullet-1.gif", "bullet2.png", "bullet.png"]
#子弹伤害值
bullet_damage_value = [1, 1, 2, 1]
#补给
supply_image = ["bomb-1.gif", "bomb-2.gif"]
#补给的大小
supply_size = [{"width":58, "height":88}, {"width":60, "height":103}]
#敌机引用列表
enemy0_list = []#小飞机
enemy0_maximum = 6
enemy1_list = []#boss1
enemy1_maximum = 1
enemy2_list = []#boss2
enemy2_maximum = 1

# def key_control(hero_temp):
#     #获取事件，比如按键等
#     for event in pygame.event.get():
#
#         #判断是否是点击了退出按钮
#         if event.type == QUIT:
#             print("exit")
#             exit()
#         #判断是否是按下了键
#         elif event.type == KEYDOWN:
#             #检测按键是否是left
#             if event.key == K_LEFT:
#                 print('left')
#                 hero_temp.key_down(K_LEFT)
#             #检测按键是否是right
#             elif event.key == K_RIGHT:
#                 print('right')
#                 hero_temp.key_down(K_RIGHT)
#             #检测按键是否是空格键
#             elif event.key == K_SPACE:
#                 print('space')
#                 hero_temp.fire()
#             elif event.key == K_b:#自爆
#                 print('b')
#                 hero_temp.bomb()
#         #判断是否是松开了键
#         elif event.type == KEYUP:
#             #检测松键是否是left
#             if event.key == K_LEFT:
#                 print('left')
#                 hero_temp.key_up(K_LEFT)
#             #检测按键是否是right
#             elif event.key == K_RIGHT:
#                 print('right')
#                 hero_temp.key_up(K_RIGHT)
class Base(object):
    """docstring for Base"""
    def __init__(self, screen_temp, x, y, image_name):
        self.x = x
        self.y = y
        self.screen = screen_temp
        self.image = pygame.image.load(image_name)


class BasePlane(Base):
    """docstring for BasePlane"""
    def __init__(self, plane_type, screen_temp, x, y, image_name, picture_num, HP_temp):
        Base.__init__(self, screen_temp, x, y, image_name)
        self.bullet_list = [] #存储发射出去的子弹的引用
        self.plane_type = plane_type #飞机类型标示, 3是hero
        #爆炸效果用的如下属性
        self.hitted = False #表示是否要爆炸
        self.bomb_picture_list = [] #用来存储爆炸时需要的图片
        self.bomb_picture_num = picture_num #飞机爆炸效果的图片数量
        self.picture_count = 0#用来记录while True的次数,当次数达到一定值时才显示一张爆炸的图,然后清空,,当这个次数再次达到时,再显示下一个爆炸效果的图片
        self.image_index = 0#用来记录当前要显示的爆炸效果的图片的序号
        self.HP = HP_temp
        self.fire_bullet_count = 0

    def display(self):
        """显示玩家的飞机"""
        global hit_score
        global HP_list
        global plane_bomb_time
        #如果被击中,就显示爆炸效果,否则显示普通的飞机效果
        if self.hitted == True and self.image_index < self.bomb_picture_num and self.HP <= 0:
            if self.plane_type != 3 and self.image_index == 0 and self.picture_count == 0:
                hit_score += HP_list[self.plane_type]#得分加上被击毁飞机的HP
            self.screen.blit(self.bomb_picture_list[self.image_index], (self.x, self.y))
            self.picture_count += 1
            if self.picture_count == plane_bomb_time[self.plane_type]: #根据飞机类型不同，爆炸效果持续的时间不同
                self.picture_count = 0
                self.image_index += 1
        elif self.image_index < self.bomb_picture_num:
            self.screen.blit(self.image, (self.x, self.y)) #显示原图
        if self.hitted == True and not self.bullet_list and self.image_index >= self.bomb_picture_num:
            del_plane(self) #删除被击中敌机的对象
        #敌机飞出window后删除
        if self.y > 860:
            del_plane(self)
        bullet_list_out = []#越界子弹
        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()
            if bullet.judge(): #判断子弹是否越界
                bullet_list_out.append(bullet)
        #删除越界子弹
        for bullet in bullet_list_out:
            self.bullet_list.remove(bullet)
    #创建出爆炸效果的图片的引用
    def crate_images(self, bomb_picture_name):
            for i in range(1, self.bomb_picture_num + 1):
                self.bomb_picture_list.append(pygame.image.load("./feiji/" + bomb_picture_name + str(i) + ".gif"))

    #判断是否被击中
    def isHitted(self, plane, width, height):# widht和height表示范围
        if plane.bullet_list and self.HP:
            for bullet in plane.bullet_list:
                if bullet.x >= self.x-50 and bullet.x <= self.x+width and bullet.y+0.1*height > self.y and bullet.y < self.y + 1*height:
                    # (hero.y <= self.y and self.y <= hero.y + 40) and (hero.x <= self.x and self.x <= hero.x + 100):
                    self.HP -= bullet.damage_value#hero的HP减去子弹的伤害值
                    if self.plane_type == 3:
                        show_score_HP()
                    plane.bullet_list.remove(bullet) #删除击中的子弹
                    self.hitted = True
    #飞机开火
    def fire(self, bullet_maximun):
        if self.HP:
            random_num = random.randint(1, 60)
            if (random_num == 10 or random_num == 45) and len(self.bullet_list) < bullet_maximun:
                self.bullet_list.append(EnemyBullet(self.screen, self.x, self.y, self))
                self.fire_bullet_count += 1

# class Bullet(object):
#     def __init__(self, screen_temp, x, y):
#         self.x = x + 40
#         self.y = y - 20
#         self.screen = screen_temp
#         self.image = pygame.image.load("./feiji/bullet.png")
#
#     def display(self):
#         self.screen.blit(self.image, (self.x, self.y))
#
#     def move(self):
#         self.y -= 10

class HeroPlane(BasePlane):
    global supply_size

    def __init__(self, screen_temp):
        BasePlane.__init__(self, 3, screen_temp, 190, 650, "./feiji/feijidazhan1.png", 4, HP_list[3])  # super().__init__()
        BasePlane.crate_images(self, "hero_blowup_n")
        self.key_down_list = []  # 用来存储键盘左右移动键
        self.is_three_bullet = False
        self.space_key_list = []  # 保存space键
    #单键移动
    def move_left(self):
        self.x -= 7

    def move_right(self):
        self.x += 7
    def move_up(self):
        self.y -= 6

    def move_down(self):
        self.y += 6
    # 双键移动方向
    def move_left_and_up(self):
        self.x -= 5
        self.y -= 6

    def move_right_and_up(self):
        self.x += 5
        self.y -= 6

    def move_lef_and_down(self):
        self.x -= 5
        self.y += 6

    def move_right_and_down(self):
        self.x += 5
        self.y += 6

    # 控制飞机左右移动范围
    def move_limit(self):
        if self.x < 0:
            self.x = -2
        elif self.x + 100 > 480:
            self.x = 380
        if self.y > 650:
            self.y = 650
        elif self.y < 40:
            self.y += 6
    # def fire(self):
    #     global plane_maximum_bullet
    #     if len(self.bullet_list) < plane_maximum_bullet[self.plane_type]:  # 单发炮台子弹限制为8
    #         self.bullet_list.append(Bullet(self.screen, self.x + 10 , self.y - 14, self))

    # 键盘按下向列表添加左右按键
    def key_down(self, key):
        self.key_down_list.append(key)

    # 键盘松开向列表删除左右按键
    def key_up(self, key):
        if len(self.key_down_list) != 0:  # 判断是否为空
            self.key_down_list.pop(0)

    # 当一直按下键盘时调用移动函数
    def press_move(self):
        # if len(self.key_down_list) != 0:
        #     if self.key_down_list[0] == K_LEFT:
        #         self.move_left()
        #     elif self.key_down_list[0] == K_RIGHT:
        #         self.move_right()
        #     elif self.key_down_list[0] == K_UP:
        #         self.move_up()
        #     elif self.key_down_list[0] == K_DOWN:
        #         self.move_down()
        if len(self.key_down_list) != 0:
            if len(self.key_down_list) == 2:  # 两个键
                if (self.key_down_list[0] == K_LEFT and self.key_down_list[1] == K_UP) or (
                        self.key_down_list[1] == K_LEFT and self.key_down_list[
                    0] == K_UP):  # key_down_list列表存在按键为left,up 或 up,left时调用move_left_and_up()方法
                    self.move_left_and_up()
                elif (self.key_down_list[0] == K_RIGHT and self.key_down_list[1] == K_UP) or (
                        self.key_down_list[1] == K_RIGHT and self.key_down_list[0] == K_UP):
                    self.move_right_and_up()
                elif (self.key_down_list[0] == K_LEFT and self.key_down_list[1] == K_DOWN) or (
                        self.key_down_list[1] == K_LEFT and self.key_down_list[0] == K_DOWN):
                    self.move_lef_and_down()
                elif (self.key_down_list[0] == K_RIGHT and self.key_down_list[1] == K_DOWN) or (
                        self.key_down_list[1] == K_RIGHT and self.key_down_list[0] == K_DOWN):
                    self.move_right_and_down()
            else:  # 一个键
                if self.key_down_list[0] == K_LEFT:
                    self.move_left()
                elif self.key_down_list[0] == K_RIGHT:
                    self.move_right()
                elif self.key_down_list[0] == K_UP:
                    self.move_up()
                elif self.key_down_list[0] == K_DOWN:
                    self.move_down()

    def fire(self):
        global plane_maximum_bullet
        if len(self.bullet_list) < plane_maximum_bullet[self.plane_type]:  # 单发炮台子弹限制为8
            self.bullet_list.append(Bullet(self.screen, self.x-3, self.y - 14, self))

    def bomb(self):
        self.hitted = True
        self.HP = 0

        # 键盘按下向列表添加space
    def space_key_down(self, key):
        self.space_key_list.append(key)
        # 键盘松开向列表删除space
    def space_key_up(self, key):
        if len(self.space_key_list) != 0:  # 判断是否为空
            try:
                self.space_key_list.pop(0)
            except Exception:
                raise
    # 按键space不放,持续开火
    def press_fire(self):
        if len(self.bullet_list) == 0 and len(self.space_key_list):
            self.fire()
        else:
            if len(self.space_key_list) != 0:
                if self.bullet_list[len(self.bullet_list) - 1].y < self.y - 14 - 60:
                    self.fire()
    # 是否吃到补给
    def supply_hitted(self, supply_temp, width, height):  # widht和height表示范围
        if supply_temp and self.HP:
            # 更加精确的判断是否吃到补给
            supply_temp_left_x = supply_temp.x + supply_size[supply_temp.supply_type]["width"] * 0.15
            supply_temp_right_x = supply_temp.x + supply_size[supply_temp.supply_type]["width"] * 0.85
            supply_temp_top_y = supply_temp.y + supply_size[supply_temp.supply_type]["height"] * 0.4
            supply_temp_bottom_y = supply_temp.y + supply_size[supply_temp.supply_type]["height"] * 0.9
            # 测试
            # print("="*50)
            # print("supply_temp_left_x=%f"%supply_temp_left_x)
            # print("supply_temp_right_x=%f"%supply_temp_right_x)
            # print("supply_temp_top_y=%f"%supply_temp_top_y)
            # print("supply_temp_bottom_y=%f"%supply_temp_bottom_y)
            # print("1=%f"%(self.x+0.05*width))
            # print("2=%f"%(self.x+0.95*width))
            # print("3=%f"%(self.y+0.1*height))
            # print("4=%f"%(self.y+0.9*height))
            # print("="*50)
            if supply_temp_left_x > self.x + 0.05 * width and supply_temp_right_x < self.x + 0.95 * width and supply_temp_top_y < self.y + 0.95 * height and supply_temp_bottom_y > self.y + 0.1 * height:
                self.HP -= supply_temp.supply_HP
                if self.HP > 15:
                    self.HP = 15
                show_score_HP()
                del_supply(supply_temp)

    # #是否击中hero判断
    # def hitHero(self, enemy_temp):
    #     if enemy_temp.bullet_list is not None:
    #         for bullet in enemy_temp.bullet_list:
    #             if bullet.x > self.x and bullet.x < self.x+100 and bullet.y > self.y and bullet.y < self.y + 124:
    #                 enemy_temp.bullet_list.remove(bullet)
    #                 self.bomb()
# class HeroPlane(BasePlane):
#     def __init__(self, screen_temp):
#         BasePlane.__init__(self, screen_temp, 210, 700, "./feiji/hero1.png", 4) #super().__init__()
#         BasePlane.crate_images(self, "hero_blowup_n")
#
#     def move_left(self):
#         self.x -= 5
#
#     def move_right(self):
#         self.x += 5
#
#     #控制飞机左右移动范围
#     def move_limit(self):
#         if self.x < 0:
#             self.x = -2
#         elif self.x+100 > 480:
#             self.x = 386
#
#     def fire(self):
#         self.bullet_list.append(Bullet(self.screen, self.x, self.y))
#
#     #键盘按下向列表添加左右按键
#     def key_down(self, key):
#         self.key_down_list.append(key)
#
#     #键盘松开向列表删除左右按键
#     def key_up(self, key):
#         if len(self.key_down_list) != 0: #判断是否为空
#             self.key_down_list.pop(0)
#
#     #当一直按下键盘时调用移动函数
#     def press_move(self):
#         if len(self.key_down_list) != 0:
#             if self.key_down_list[0] == K_LEFT:
#                 self.move_left()
#             elif self.key_down_list[0] == K_RIGHT:
#                 self.move_right()
#     def bomb(self):
#         self.hit = True
#
#     #是否击中hero判断
#     def hitHero(self, enemy_temp):
#         if enemy_temp.bullet_list is not None:
#             for bullet in enemy_temp.bullet_list:
#                 if bullet.x > self.x and bullet.x < self.x+100 and bullet.y > self.y and bullet.y < self.y + 124:
#                     enemy_temp.bullet_list.remove(bullet)
#                     self.bomb()
class Enemy0Plane(BasePlane):
    """敌机的类"""

    def __init__(self, screen_temp):
        random_num_x = random.randint(0, 430)
        random_num_y = random.randint(-50, -40)
        BasePlane.__init__(self, 0, screen_temp, random_num_x+10, random_num_y, "./feiji/diji0.png", 4, HP_list[0])
        BasePlane.crate_images(self, "enemy0_down")
        BasePlane.fire(self, 2)

    def move(self):
        self.y += 4


class Enemy1Plane(BasePlane):
    """敌机的类"""

    def __init__(self, screen_temp):
        BasePlane.__init__(self, 1, screen_temp, 205, -90, "./feiji/diji2.png", 4, HP_list[1])
        BasePlane.crate_images(self, "enemy1_down")
        self.direction = "right"  # 用来存储飞机默认显示方向
        self.num_y = random.randint(20, 150)

    def move(self):
        if self.direction == "right":
            self.x += 4
        elif self.direction == "left":
            self.x -= 4
        # 方向判断
        if self.x + 70 > 480:
            self.direction = "left"
        elif self.x < 0:
            self.direction = "right"
        if self.y < self.num_y:
            self.y += 3
        elif self.fire_bullet_count > 15:
            self.y += 3


class Enemy2Plane(BasePlane):
    """敌机的类"""

    def __init__(self, screen_temp):
        BasePlane.__init__(self, 2, screen_temp, 158, -246, "./feiji/enemy2.png", 5, HP_list[2])
        BasePlane.crate_images(self, "enemy2_down")
        self.direction = "right"  # 用来存储飞机默认显示方向

    def move(self):
        if self.direction == "right":
            self.x += 5
        elif self.direction == "left":
            self.x -= 5
        # 方向判断
        if self.x + 165 > 480:
            self.direction = "left"
        elif self.x < 0:
            self.direction = "right"
        if self.y < 0:
            self.y += 4
        elif self.fire_bullet_count > 25:
            self.y += 3


# class EnemyBullet(object):
#     def __init__(self, screen_temp, x, y):
#         self.x = x + 25
#         self.y = y + 40
#         self.screen = screen_temp
#         self.image = pygame.image.load("./feiji/bullet1.png")
#
#     def display(self):
#         self.screen.blit(self.image, (self.x, self.y))
#
#
#     def move(self):
#         self.y += 5
#
#     def judge(self):
#         if self.y > 852:
#             return True
#         else:
#             return False
class BaseBullet(Base):
    """docstring for BaseBullet"""
    global bullet_damage_value
    def __init__(self, screen_temp, x, y, image_name, plane):
        Base.__init__(self, screen_temp, x, y, image_name)
        if plane:
            self.damage_value = bullet_damage_value[plane.plane_type]
    # def __init__(self, screen_temp, x, y, image_name):
    #     Base.__init__(self, screen_temp, x, y, image_name)

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))


class Bullet(BaseBullet):
    def __init__(self, screen_temp, x, y,plane):
        BaseBullet.__init__(self, screen_temp, x+20, y-14, "./feiji/zi.png",plane)

    def move(self):
        self.y -= 12

    def judge(self):
        if self.y < 0:
            return True
        else:
            return False

class supply_2_hero(BaseBullet):
    def __init__(self, screen_temp, x, y, type, speed_temp, s_HP, suppl_type_temp):
        BaseBullet.__init__(self, screen_temp, x, y, "./feiji/"+supply_image[type], None)
        self.speed = speed_temp
        self.supply_HP = s_HP
        self.supply_type = suppl_type_temp

    def move(self):
        self.y += self.speed

    def judge(self):
        if self.y > 852:
            return True
        else:
            return False

class EnemyBullet(BaseBullet):
    global bullet_type
    global plane_size
    def __init__(self, screen_temp, x, y, plane):
        BaseBullet.__init__(self, screen_temp, x+plane_size[plane.plane_type]["width"]/2, y+plane_size[plane.plane_type]["height"]/2, "./feiji/"+bullet_type[plane.plane_type],plane)

    def move(self):
        self.y += 5

    def judge(self):
        if self.y > 852:
            return True
        else:
            return False
def del_plane(plane):
    """回收被击中的敌机的对象"""
    global hit_score
    global enemy0_list
    global enemy1_list
    global enemy2_list

    if plane in enemy0_list:
        enemy0_list.remove(plane)
    elif plane in enemy1_list:
        enemy1_list.remove(plane)
    elif plane in enemy2_list:
        enemy2_list.remove(plane)
def del_plane(plane):
    """回收被击中的敌机的对象"""
    global hero
    global hit_score
    global enemy0_list
    global enemy1_list
    global enemy2_list
    if plane in enemy0_list: #回收对象为enemy0
        enemy0_list.remove(plane)
    elif plane in enemy1_list:
        enemy1_list.remove(plane)
    elif plane in enemy2_list:
        enemy2_list.remove(plane)
    elif plane == hero:
        hit_score = 0
        show_score_HP()
        hero = None

def del_supply(s_or_b):
    """回收补给"""
    global blood_supply
    global bullet_supply
    if s_or_b == blood_supply:
        blood_supply = None
    elif s_or_b == bullet_supply:
        bullet_supply = None


def reborn():
    """Hero重生"""
    global hero
    global window_screen
    hero = HeroPlane(window_screen)
    show_score_HP()

def show_score_HP():
    global hero
    global hit_score
    print("-"*60)
    print("\t\t\tscore: %d"%hit_score)
    print("\t\t\t   HP:　%d"%hero.HP)

pygame.mixer.init()
def music_load():
    pygame.mixer.music.load("./music/PlaneWarsBackgroundMusic.mp3")
    pygame.mixer.music.play(-1)


def key_control():
    global hero
    global is_pause
    global hero_fire_music
    global plane_maximum_bullet
    global enemy0_list
    global enemy1_list
    global enemy2_list
    global blood_supply
    global bullet_supply
    global hit_score
    # 获取事件，比如按键等
    for event in pygame.event.get():
        # 判断是否是点击了退出按钮
        if event.type == QUIT:
            print("exit")
            exit()
        # 判断是否是按下了键
        elif event.type == KEYDOWN:
            # 检测按键是否是left
            if hero:
                if event.key == K_LEFT:
                    hero.key_down(K_LEFT)
                # 检测按键是否是right
                elif event.key == K_RIGHT:
                    hero.key_down(K_RIGHT)
                elif event.key == K_UP:
                    hero.key_down(K_UP)
                # 检测按键是否是right
                elif event.key == K_DOWN:
                    hero.key_down(K_DOWN)
                # 检测按键是否是空格键
                # elif event.key == K_SPACE and hero.HP:
                #     hero.fire()
                elif event.key == K_b:  # 自爆
                    print("--------自爆-------")
                    hero.bomb()
                    # 检测按键是否是空格键
                elif event.key == K_SPACE and hero.HP:
                    hero.space_key_down(K_SPACE)  # 想space列表添加k_space
            if event.key == K_r:
                print("--------重生-------")
                reborn()

        # 判断是否是松开了键
        elif event.type == KEYUP and hero:
            # 检测松键是否是left
            if event.key == K_LEFT:
                hero.key_up(K_LEFT)
            # 检测按键是否是right
            elif event.key == K_RIGHT:
                hero.key_up(K_RIGHT)
            elif event.key == K_SPACE:
                hero.space_key_up(K_SPACE)
            # 检测按键是否是up
            elif event.key == K_UP:
                hero.key_up(K_UP)
            # 检测按键是否是down
            elif event.key == K_DOWN:
                hero.key_up(K_DOWN)
def main():
    global window_screen
    global hero
    global hit_score
    global HP_list
    global blood_supply

    global enemy0_list
    global enemy0_maximum
    global enemy1_list
    global enemy1_maximum
    global enemy2_list
    global enemy2_maximum

    hit_score_temp = hit_score

    # 1. 创建窗口
    window_screen = pygame.display.set_mode((480, 750), 0, 32)
    # 2. 创建一个背景图片
    background = pygame.image.load("./feiji/beijing1.jpg")
    # 3. 创建一个飞机对象
    reborn()
    # 4. 导入背景音乐
    # music_load()

    while True:
        if hit_score > hit_score_temp and hero:
            hit_score_temp = hit_score
            show_score_HP()
        elif hit_score < hit_score_temp:
            hit_score_temp = 0
        # 创建敌机
        random_num = random.randint(1, 70)
        random_appear_boss1 = random.randint(19, 26)
        random_appear_boss2 = random.randint(80, 100)
        if (random_num == 29 or random == 50) and len(enemy0_list) < enemy0_maximum:
            enemy0_list.append(Enemy0Plane(window_screen))
        if (hit_score >= random_appear_boss1 and (hit_score % random_appear_boss1) == 0) and len(
                enemy1_list) < enemy1_maximum:
            enemy1_list.append(Enemy1Plane(window_screen))
        if (hit_score >= random_appear_boss2 and (hit_score % random_appear_boss2) == 0) and len(
                enemy2_list) < enemy2_maximum:
            enemy2_list.append(Enemy2Plane(window_screen))
        # 血量补给
        if not blood_supply:
            random_supply = random.randint(1, 1500)
            if (random_supply % 241) == 0:
                random_x = random.randint(0, 480 - 58)
                random_y = random.randint(-105, -95)
                blood_supply = supply_2_hero(window_screen, random_x, random_y, 0, 3, -3,
                                             0)  # 0-补给类型, 3-速度, -3-补给血量值(用的是减法), 0-补给类型
        window_screen.blit(background, (0, 0))

        # hero
        if hero:
            hero.display()  # hero展示
            if hero:
                hero.press_move()
                hero.press_fire()
                hero.move_limit()  # hero移动范围判断
        # blood_supply
        if blood_supply:
            blood_supply.display()
            blood_supply.move()
            if blood_supply.judge():
                del_supply(blood_supply)
        if hero and blood_supply:
            hero.supply_hitted(blood_supply, plane_size[hero.plane_type]["width"],
                               plane_size[hero.plane_type]["height"])
        # enemy0
        if enemy0_list:
            for enemy0 in enemy0_list:
                enemy0.display()  # enemy展示
                enemy0.move()  # 控制敌机的移动
                enemy0.fire(2)  # 敌机开火
                if hero:
                    hero.isHitted(enemy0, plane_size[hero.plane_type]["width"],
                                  plane_size[hero.plane_type]["height"])  # 是否击中hero
                    enemy0.isHitted(hero, plane_size[enemy0.plane_type]["height"],
                                    plane_size[enemy0.plane_type]["height"])  # 是否击中enemy
        # enemy1
        if enemy1_list:
            for enemy1 in enemy1_list:
                enemy1.display()  # enemy展示
                enemy1.move()  # 控制敌机的移动
                enemy1.fire(4)  # 敌机开火
                if hero:
                    hero.isHitted(enemy1, plane_size[hero.plane_type]["width"],
                                  plane_size[hero.plane_type]["height"])  # 是否击中hero
                    enemy1.isHitted(hero, plane_size[enemy1.plane_type]["height"],
                                    plane_size[enemy1.plane_type]["height"])  # 是否击中enemy
        # enemy2
        if enemy2_list:
            for enemy2 in enemy2_list:
                enemy2.display()  # enemy展示
                enemy2.move()  # 控制敌机的移动
                enemy2.fire(6)  # 敌机开火
                if hero:
                    hero.isHitted(enemy2, plane_size[hero.plane_type]["width"],
                                  plane_size[hero.plane_type]["height"])  # 是否击中hero
                    enemy2.isHitted(hero, plane_size[enemy2.plane_type]["height"],
                                    plane_size[enemy2.plane_type]["height"])  # 是否击中enemy

        pygame.display.update()
        key_control()
        time.sleep(0.01)


if __name__ == "__main__":
    main()


