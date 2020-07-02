# 프로젝트 6일 - 인트로 창 생성
# 및 적 국가 생성

from tkinter import *
import time
import math
import random

window = Tk()
window.title("Asia War")   # 게임 이름
window.resizable(0,0)
canvas = Canvas(window, width = 640, height = 640, bg ="black")   # 창 생성
objects, enemyObjects, score = set(), set(), 0   # 오브젝트 세트, 점수 선언


bullet_bluecircle = PhotoImage(file = "circle.png").subsample(100)
icon_SouthKorea = PhotoImage(file = "resize_southkorea.png")  # 이미지 추가 및 크기 조정
icon_Japan = PhotoImage(file = "resize_japan.png")   # 이미지 추가 및 크기 조정
icon_NorthKorea = PhotoImage(file = "resize_northkorea.png")    # 이미지 추가 및 크기 조정
icon_China = PhotoImage(file = "resize_china.png")    # 이미지 추가 및 크기 조정
icon_Indian = PhotoImage(file = "resize_indian.png")    # 이미지 추가 및 크기 조정
# southkorea = canvas.create_image(350, 350, anchor = NW, image = icon_SouthKorea)    # 이미지 추가
# korea = Image.open('southkorea.png')

class Game:   # 게임 클래스
    def __init__(self):
        global objects, enemyObjects, score
        self.keys = set()   # 버튼 세트 생성
        self.mx, self.my, self.mPressed = 0, 0, 0   # 마우스 좌표, 클릭 여부
        self.runtime, self.spontime = 0, 300   # 런타임, 스폰타임
        self.hp_before, self.score_before = 0, 0   # 갱신용 지역변수
        self.enemyvalue = [[8, icon_NorthKorea], [15, icon_Japan], [10, icon_Indian], [25, icon_China]]   # 적 정보
        # self.enemyvalue = [[8, "red"], [15, "blue"], [10, "green"], [25, "gold"]]   # 적 정보

        window.bind("<KeyPress>", self.keyPressHandler)   # 버튼 클릭시 함수호출
        window.bind("<KeyRelease>", self.keyReleaseHandler)   # 버튼 뗄 시 함수호출
        canvas.bind("<Button-1>", self.mousePress)   # 마우스 클릭시 함수호출
        canvas.bind("<B1-Motion>", self.mousePress)
        canvas.bind("<ButtonRelease-1>", self.mouseRelease)   # 마우스 뗄 시 함수호출
        canvas.pack()

        canvas.create_text(320, 60, text ="A S I A   W A R", fill = "white", font = ("둥근모꼴", 28))   # 설명
        canvas.create_rectangle(100, 200, 135, 235, fill = "gray22", outline = "white"); canvas.create_text(117, 217, text ="A", fill = "white", font = ("둥근모꼴", 16))
        canvas.create_rectangle(143, 200, 178, 235, fill = "gray22", outline = "white"); canvas.create_text(160, 217, text ="S", fill = "white", font = ("둥근모꼴", 16))
        canvas.create_rectangle(186, 200, 221, 235, fill = "gray22", outline = "white"); canvas.create_text(203, 217, text ="D", fill = "white", font = ("둥근모꼴", 16))
        canvas.create_rectangle(143, 157, 178, 192, fill = "gray22", outline = "white"); canvas.create_text(160, 174, text ="W", fill = "white", font = ("둥근모꼴", 16))
        canvas.create_text(160, 270, text ="< 이동 키 >", fill = "white", font = ("둥근모꼴", 12))
        canvas.create_rectangle(450, 157, 510, 235, outline = "white"); canvas.create_line(480, 187, 510, 187, fill = "white"); canvas.create_rectangle(450, 157, 480, 187, fill = "gray22", outline = "white")
        canvas.create_text(480, 270, text ="< 공격 키 >", fill = "white", font = ("둥근모꼴", 12))
        canvas.create_text(300, 400, text ="           국가들을 처치하고 점수를 얻으세요!\n\n      시간이 지날수록 강한 국가들이 등장합니다.", fill = "white", font = ("둥근모꼴", 12))
        self.textblinker()   # 시작 대기

        # test = canvas.create_rectangle(310, 310, 330, 330, fill = "black") # 테스트용 canvas 생성
        obj_SouthKorea = object_main(300, 300, icon_SouthKorea)
        # obj_Japan = element(340, 340, icon_Japan)
 
        score_view = canvas.create_text(540, 15, text = "SCORE: " + str(score), fill = "white", font = ("둥근모꼴", 16))   # 점수 드로우
        canvas.create_rectangle(5, 5, 420, 25, fill = "gray22")   # HP바 바탕 드로우
        hpbar = canvas.create_rectangle(5, 5, 420, 25, fill = "springGreen2", width =0)   # HP바 드로우
        hptext = canvas.create_text(200, 15, text ="HP: (" + str(obj_SouthKorea.hp) + " / 1000)", font = ("둥근모꼴", 8))   # HP 숫자 드로우
 

        while(True):  # 메인 루프
            if obj_SouthKorea in objects:
                for key in self.keys:   # 버튼 체킹
                    if key == ord('A') and obj_SouthKorea.x_accel > -3: obj_SouthKorea.x_accel -= 1   # A
                    if key == ord('D') and obj_SouthKorea.x_accel < 3: obj_SouthKorea.x_accel += 1   # D
                    if key == ord('W') and obj_SouthKorea.y_accel > -3: obj_SouthKorea.y_accel -= 1   # W
                    if key == ord('S') and obj_SouthKorea.y_accel < 3: obj_SouthKorea.y_accel += 1   # S
 
                # if self.mPressed == 1:   # 마우스 클릭 시
                #     obj_attack = object_attack(canvas.coords(obj_SouthKorea.canvas_id)[0]+8, canvas.coords(obj_SouthKorea.canvas_id)[1]+8, bullet_bluecircle, 120)
                #     obj_attack.x_accel, obj_attack.y_accel = self.movePoint(canvas.coords(obj_attack.canvas_id)[0] + 10, canvas.coords(obj_attack.canvas_id)[1] + 10, self.mx, self.my, 25)
 
                if self.mPressed == 1 and obj_SouthKorea.coolt == obj_SouthKorea.cool:   # 마우스 클릭 시
                    obj_attack = object_attack(canvas.coords(obj_SouthKorea.canvas_id)[0]+7, canvas.coords(obj_SouthKorea.canvas_id)[1]+7, bullet_bluecircle, 120)    # 공격 오브젝트 생성
                    obj_attack.x_accel, obj_attack.y_accel = self.movePoint(canvas.coords(obj_attack.canvas_id)[0]+10, canvas.coords(obj_attack.canvas_id)[1]+10, self.mx+random.randrange(-5,5), self.my+random.randrange(-5,5), 25)
                    # obj_attack.x_accel, obj_attack.y_accel = self.movePoint(canvas.coords(obj_attack.canvas_id)[0] + 10, canvas.coords(obj_attack.canvas_id)[1] + 10, self.mx, self.my, 25)
                    obj_SouthKorea.coolt, obj_SouthKorea.hp = 0, obj_SouthKorea.hp - 0.1   # 쿨타임 초기화

                if self.hp_before != obj_SouthKorea.hp:   # hp 갱신
                    canvas.delete(hpbar); canvas.delete(hptext)
                    hpbar = canvas.create_rectangle(5, 5, 420 * obj_SouthKorea.hp / obj_SouthKorea.mhp, 25, fill = "springGreen2", width =0)
                    hptext = canvas.create_text(200, 15, text ="HP: (" + str(obj_SouthKorea.hp) + " / 1000)", font = ("나눔고딕코딩", 8))
                    # hpbar = canvas.create_rectangle(5, 5, 420 * obj_SouthKorea.hp / obj_SouthKorea.mhp, 25, fill = "springGreen2", width =0)
                    # hptext = canvas.create_text(200, 15, text ="HP: (" + str(obj_SouthKorea.hp) + " / 1000)", font = ("둥근모꼴", 12))
                    self.hp_before = obj_SouthKorea.hp

                if self.score_before != score:   # 점수 갱신
                    canvas.itemconfig(score_view, text = "SCORE: " + str(score))
                    self.score_before = score

                self.runtime += 1   # 런타임 증가
                if len(enemyObjects) < 25:   # 적 개체 수 제한
                    if self.runtime % self.spontime == 0:
                        for i in range(4):
                            if self.runtime % (self.spontime * (i + 1) ** 2) == 0: 
                                obj_enemy = object_enemy(random.choice([-100, 740])+random.randrange(-50,50), random.choice([-100, 740])+random.randrange(-50,50), self.enemyvalue[i][1], obj_SouthKorea, i)   # enemy 오브젝트 스폰
                        self.spontime = max([random.randrange(self.spontime - 2, self.spontime), 50])   # 스폰시간 초기화
                    
                for obj in enemyObjects.copy():
                    degree = math.atan2(canvas.coords(obj_SouthKorea.canvas_id)[0] - canvas.coords(obj.canvas_id)[0], canvas.coords(obj_SouthKorea.canvas_id)[1] - canvas.coords(obj.canvas_id)[1])
                    obj.x_accel, obj.y_accel = -obj.enemy_stat[obj.enemy_type][1] * math.cos(degree), 5 * math.sin(degree)   # main 오브젝트 공전
                    if obj.coolt == obj.cool:
                        obj_enemyAttack = object_enemyAttack(canvas.coords(obj.canvas_id)[0]+(obj.enemy_stat[obj.enemy_type][3])/2, 
                                                            canvas.coords(obj.canvas_id)[1]+(obj.enemy_stat[obj.enemy_type][3])/2,
                                                            obj.image, 
                                                            100, 
                                                            obj_SouthKorea, 
                                                            obj.enemy_stat[obj.enemy_type][5])    # obj_enemyAttack 생성
                        obj_enemyAttack.x_accel, obj_enemyAttack.y_accel = self.movePoint(canvas.coords(obj_enemyAttack.canvas_id)[0]+random.randrange(-5,5), canvas.coords(obj_enemyAttack.canvas_id)[1]+random.randrange(-5,5), canvas.coords(obj_SouthKorea.canvas_id)[0]+10, canvas.coords(obj_SouthKorea.canvas_id)[1]+10, obj.enemy_stat[obj.enemy_type][4])
                        obj.coolt = 0    
 
                # canvas.itemconfig(score_view, text = "SCORE: " + str(score))   # 점수 갱신
 
            for obj in objects.copy():
                obj.move(); obj.step()
            if not obj_SouthKorea in objects:
                canvas.delete("all"); break
            window.update(); time.sleep(0.01)   # 0.01초 만큼 sleep

        canvas.create_text(320, 260, text = "Game Over...", fill= "white", font = ("둥근모꼴", 38)); canvas.create_text(320, 370, text = str(score) + " 점", fill = "white", font = ("둥근모꼴", 28))
        self.textblinker("exit")   # 종료 대기
        sys.exit(1)    
                        
    def keyPressHandler(self, event):   # 버튼 세트에 버튼추가
        self.keys.add(event.keycode)
 
    def keyReleaseHandler(self, event):   # 버튼 세트에 버튼 제거
        if event.keycode in self.keys:
            self.keys.remove(event.keycode)

    def mousePress(self, event):   # 마우스 왼쪽 누를시 좌표 반환, 클릭값 1
        self.mx, self.my, self.mPressed = event.x, event.y, 1
 
    def mouseRelease(self, event):   # 마우스 왼쪽 땔시 좌표 반환, 클릭값 0
        self.mx, self.my, self.mPressed = event.x, event.y, 0
    
    def movePoint(self, x1, y1, x2, y2, spd):   # 해당 좌표로 이동
        return (x2 - x1) * spd / math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2), (y2 - y1) * spd / math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    def textblinker(self, sentance = "start"):   # 대기 텍스트
        menuToggle = True; blinkerText = canvas.create_text(320, 580, text ="< Press Spacebar to " + sentance + ". >", fill = "red", font = ("둥근모꼴", 12))   # 깜박이 canvas 생성
        while(True):   # 대기
            self.runtime += 1
            for key in self.keys:   # spacebar 누를시 다음으로
                if key == 32:
                    canvas.delete("all"); return
            if self.runtime % 60 == 0:
                if menuToggle == True:
                    canvas.itemconfig(blinkerText, text = ""); menuToggle = False
                else:
                    canvas.itemconfig(blinkerText, text = "< Press Spacebar to " + sentance + ". >"); menuToggle = True
            window.update(); time.sleep(0.01)
    

class element:   # 오브젝트 원형
    def __init__(self, x, y, image):
        self.x, self.y = x, y   # 생성 위치
        self.image = image
        self.x_accel, self.y_accel = 0, 0   # 가속도
        objects.add(self)   # 오브젝트 세트에 자신 등록
        self.canvas_id = canvas.create_image(x, y, anchor = NW, image = self.image)
 
    def destroy(self):   # 제거 함수
        objects.discard(self)   # 오브젝트 세트에서 자신 제거
        canvas.delete(self.canvas_id)   # 캔버스 제거
        del self

    def move(self):   # 움직임 계산(이동, 가속도, 중력) 함수
        x_value, y_value = self.x_accel, self.y_accel
        
        if x_value != 0 or y_value != 0:   # 좌표 갱신
            if canvas.coords(self.canvas_id)[0] + x_value < 0:
                x_value = -canvas.coords(self.canvas_id)[0]   # 창나감 방지
                self.x_accel = -self.x_accel   # 튕김
            if canvas.coords(self.canvas_id)[1] + y_value < 0:
                y_value = -canvas.coords(self.canvas_id)[1]
                self.y_accel = -self.y_accel
            if canvas.coords(self.canvas_id)[0] + x_value > 600:
                x_value = 600 - canvas.coords(self.canvas_id)[0]
                self.x_accel = -self.x_accel
            if canvas.coords(self.canvas_id)[1] + y_value > 600:
                y_value = 600 - canvas.coords(self.canvas_id)[1]
                self.y_accel = -self.y_accel
            canvas.move(self.canvas_id, x_value,  y_value)   # 수치만큼 이동
            self.mx, self.my = 0, 0   # 이동값 초기화
            self.x_accel, self.y_accel = self.x_accel * 0.98, self.y_accel * 0.98    # 가속도 감소
    
    def collision(self, obj):   # 충돌 검사 - 점검
        return True if (canvas.coords(self.canvas_id)[0] <= canvas.coords(self.canvas_id)[0] + 10 and 
            canvas.coords(self.canvas_id)[0] + 10 >= canvas.coords(obj.canvas_id)[0] and 
            canvas.coords(self.canvas_id)[1] <= canvas.coords(self.canvas_id)[1] + 10 and 
            canvas.coords(self.canvas_id)[1] + 10 >= canvas.coords(obj.canvas_id)[1]) else False
 
        
class object_main(element):   # main 오브젝트
    def __init__(self, x, y, image):
        super().__init__(x, y, image)   # 상속
        self.mhp, self.hp = 1000, 1000   # 체력
        self.cool, self.coolt = 5, 0   # 쿨타임
 
    def step(self):   # 스텝 함수
        # global score
        # score += 1
        # self.move()
        if self.coolt < self.cool: self.coolt += 1  # 쿨타임 감소
        if self.hp < 0: self.destroy()   # HP 0일시 제거

class object_enemy(element):   # enemy 오브젝트
    def __init__(self, x, y, image, obj_SouthKorea, enemy_type):
        super().__init__(x, y, image)   # 상속
        self.enemy_stat = [[100, 2, 30, 3, 10, 15], [500, 1, 75, 5, 11, 50], [150, 3, 10, 3, 15, 8], [2500, 1, 30, 6, 12, 33]]   # HP, 속도, 공격속도, 투사체 크기, 투사체 속도, 데미지
        self.enemy_type = enemy_type
        self.mhp = self.enemy_stat[self.enemy_type][0]; self.hp = self.mhp   # 체력
        self.cool, self.coolt = self.enemy_stat[self.enemy_type][2], 0   # 쿨타임
        enemyObjects.add(self)   # enemy 오브젝트 세트에 자신 등록
        self.obj_SouthKorea = obj_SouthKorea   # obj_SouthKorea 오브젝트 받기
 
    def step(self):   # 스텝 함수
        if self.coolt < self.cool: self.coolt += 1  # 쿨타임 감소
        if self.hp <= 0:   # HP <= 0일시 제거
            global score
            self.destroy(); enemyObjects.discard(self); score += self.mhp


class object_attack(element):   # attack 오브젝트
    def __init__(self, x, y, image, livetime):
        super().__init__(x, y, image)   # 상속
        self.livetime = livetime   # 동작 시간
        self.fortime = 0   # 지난 시간

    def step(self):   # 스텝 함수
        for obj_s in enemyObjects:
            if self.collision(obj_s):   # 충돌시
                obj_s.hp -= 50; self.destroy(); break
        if self.livetime <= self.fortime: self.destroy()   # 동작 시간 오버시 파괴 
        self.fortime += 1
 
    # def step(self):   # 스텝 함수
    #     self.move()
    #     if self.livetime <= self.fortime:   # 동작 시간 오버 or 멈출시 파괴
    #         self.destroy()
    #     self.fortime += 1    # 지난 시간 ++

class object_enemyAttack(element):   # enemyAttack 오브젝트
    def __init__(self, x, y, image, livetime, obj_SouthKorea, damage):
        super().__init__(x, y, image)   # 상속
        self.livetime, self.fortime = livetime, 0   # 동작 시간
        self.obj_SouthKorea = obj_SouthKorea   # obj_SouthKorea 받기
        self.damage = damage   # 데미지
 
    def step(self):   # 스텝 함수
        if self.obj_SouthKorea in objects:   # 충돌시
            if self.collision(self.obj_SouthKorea):
                self.obj_SouthKorea.hp -= self.damage; self.destroy()
        if self.livetime <= self.fortime: self.destroy()   # 동작 시간 오버시 파괴 
        self.fortime += 1    

Game()