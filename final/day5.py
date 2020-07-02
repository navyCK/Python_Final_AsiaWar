# 프로젝트 5일 - HP바와 SCORE보드 생성
# 및 투사체 발사 시 HP가 50씩 감소하도록 수정
# 움직임도 약간 조정


from tkinter import *
import time
import math

window = Tk()
window.title("Asia War")   # 게임 이름
window.resizable(0,0)
canvas = Canvas(window, width = 750, height = 750, bg ="black")   # 창 생성
objects, score = set(), 0   # 오브젝트 세트, 점수 선언

# canvas.pack()
bullet_bluecircle = PhotoImage(file = "circle.png").subsample(100)
icon_SouthKorea = PhotoImage(file = "southkorea.png").subsample(5)    # 이미지 추가 및 크기 조정
icon_Japan = PhotoImage(file = "japan.png").subsample(5)    # 이미지 추가 및 크기 조정
# southkorea = canvas.create_image(350, 350, anchor = NW, image = icon_SouthKorea)    # 이미지 추가
# korea = Image.open('southkorea.png')

class Game:   # 게임 클래스
    global objects, score
    def __init__(self):
        self.keys = set()   # 버튼 세트 생성
        self.mx, self.my, self.mPressed = 0, 0, 0   # 마우스 좌표, 클릭 여부
        window.bind("<KeyPress>", self.keyPressHandler)   # 버튼 클릭시 함수호출
        window.bind("<KeyRelease>", self.keyReleaseHandler)   # 버튼 뗄 시 함수호출
        canvas.bind("<Button-1>", self.mousePress)   # 마우스 클릭시 함수호출
        canvas.bind("<B1-Motion>", self.mousePress)
        canvas.bind("<ButtonRelease-1>", self.mouseRelease)   # 마우스 뗄 시 함수호출
        canvas.pack()

        # test = canvas.create_rectangle(310, 310, 330, 330, fill = "black") # 테스트용 canvas 생성
        obj_SouthKorea = object_main(340, 340, icon_SouthKorea)
        # obj_Japan = element(340, 340, icon_Japan)
 
        score_view = canvas.create_text(540, 15, text = "SCORE: " + str(score), font = ("나눔고딕코딩", 12), fill = "red")   # 점수 드로우
        canvas.create_rectangle(5, 5, 420, 25, fill = "gray82", width =0)   # HP바 바탕 드로우
        hpbar = canvas.create_rectangle(5, 5, 420, 25, fill = "springGreen2", width =0)   # HP바 드로우
        hptext = canvas.create_text(200, 15, text ="HP: (" + str(obj_SouthKorea.hp) + " / 1000)", font = ("나눔고딕코딩", 8))   # HP 숫자 드로우
 

        while(1):  # 메인 루프
            if obj_SouthKorea in objects:
                for key in self.keys:   # 버튼 체킹
                    if key == ord('A') and obj_SouthKorea.x_accel > -4: obj_SouthKorea.x_accel -= 1   # A
                    if key == ord('D') and obj_SouthKorea.x_accel < 4: obj_SouthKorea.x_accel += 1   # D
                    if key == ord('W') and obj_SouthKorea.y_accel > -4: obj_SouthKorea.y_accel -= 1   # W
                    if key == ord('S') and obj_SouthKorea.y_accel < 4: obj_SouthKorea.y_accel += 1   # S
 
                # if self.mPressed == 1:   # 마우스 클릭 시
                #     obj_attack = object_attack(canvas.coords(obj_SouthKorea.canvas_id)[0]+8, canvas.coords(obj_SouthKorea.canvas_id)[1]+8, bullet_bluecircle, 120)
                #     obj_attack.x_accel, obj_attack.y_accel = self.movePoint(canvas.coords(obj_attack.canvas_id)[0] + 10, canvas.coords(obj_attack.canvas_id)[1] + 10, self.mx, self.my, 25)
 
                if self.mPressed == 1 and obj_SouthKorea.coolt == obj_SouthKorea.cool:   # 마우스 클릭 시
                    obj_attack = object_attack(canvas.coords(obj_SouthKorea.canvas_id)[0]+7, canvas.coords(obj_SouthKorea.canvas_id)[1]+7, bullet_bluecircle, 120)    # 공격 오브젝트 생성
                    obj_attack.x_accel, obj_attack.y_accel = self.movePoint(canvas.coords(obj_attack.canvas_id)[0] + 10, canvas.coords(obj_attack.canvas_id)[1] + 10, self.mx, self.my, 25)
                    obj_SouthKorea.coolt, obj_SouthKorea.hp = 0 , obj_SouthKorea.hp - 50

                canvas.delete(hpbar); canvas.delete(hptext)   # hp 갱신
                hpbar = canvas.create_rectangle(5, 5, 420 * obj_SouthKorea.hp / obj_SouthKorea.mhp, 25, fill = "springGreen2", width =0)
                hptext = canvas.create_text(200, 15, text ="HP: (" + str(obj_SouthKorea.hp) + " / 1000)", font = ("나눔고딕코딩", 8))
 
                canvas.itemconfig(score_view, text = "SCORE: " + str(score))   # 점수 갱신
 
            for obj in objects.copy(): obj.step()   # 스텝 함수 호출
 
            window.update()   # 업데이트
            time.sleep(0.01)   # 0.01초 만큼 sleep
                        
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
 
    # def movePoint(self, x1, y1, x2, y2, spd):   # 해당 좌표로 이동
    #     distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    #     if spd < distance:
    #         return (x2 - x1) * spd / distance, (y2 - y1) * spd / distance
    #     else:
    #         return 0, 0





class element:   # 오브젝트 원형
    def __init__(self, x, y, image):
        self.x, self.y = x, y   # 생성 위치
        # self.size_x, self.size_y = size_x, size_y   # 크기
        # self.color = color   # 색
        self.image = image
        self.x_accel, self.y_accel = 0, 0   # 가속도
        objects.add(self)   # 오브젝트 세트에 자신 등록
        # self.canvas_id = canvas.create_rectangle(x, y, x + self.size_x, y + self.size_y, fill = self.color, width =0)   # 캠버스 추가
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
            if canvas.coords(self.canvas_id)[0] + x_value > 750:
                x_value = 750 - canvas.coords(self.canvas_id)[0]
                self.x_accel = -self.x_accel
            if canvas.coords(self.canvas_id)[1] + y_value > 750:
                y_value = 750 - canvas.coords(self.canvas_id)[1]
                self.y_accel = -self.y_accel
            canvas.move(self.canvas_id, x_value,  y_value)   # 수치만큼 이동
            self.mx, self.my = 0, 0   # 이동값 초기화
            self.x_accel, self.y_accel = self.x_accel * 0.98, self.y_accel * 0.98    # 가속도 감소
 
            # self.x_accel -= self.x_accel/50   # 가속도 감소
            # self.y_accel -= self.y_accel/50    
        
class object_main(element):   # main 오브젝트
    def __init__(self, x, y, image):
        super().__init__(x, y, image)   # 상속
        self.mhp, self.hp = 1000, 1000   # 체력
        self.cool, self.coolt = 25, 0   # 쿨타임
 
    def step(self):   # 스텝 함수
        global score
        score += 1
        self.move()
        if self.coolt < self.cool: self.coolt += 1  # 쿨타임 감소
        if self.hp < 0: self.destroy()   # HP 0일시 제거

    # def step(self):   # 스텝 함수
    #     self.move()
    #     if self.coolt < self.cool:  # 쿨타임 감소
    #         self.coolt += 1 

class object_attack(element):   # attack 오브젝트
    def __init__(self, x, y, image, livetime):
        super().__init__(x, y, image)   # 상속
        self.livetime = livetime   # 동작 시간
        self.fortime = 0   # 지난 시간
 
    def step(self):   # 스텝 함수
        self.move()
        if self.livetime <= self.fortime:   # 동작 시간 오버 or 멈출시 파괴
            self.destroy()
        self.fortime += 1    # 지난 시간 ++

Game()