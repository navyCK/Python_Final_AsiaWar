# 프로젝트 2일 - canvas 객체화
# 및 대한민국 아이콘 움직임 효과 추가


from tkinter import *
import time
 
window = Tk()
window.title("Asia War")   # 게임 이름
window.resizable(0,0)
canvas = Canvas(window, width = 750, height = 750, bg ="black")   # 창 생성
canvas.pack()
icon_SouthKorea = PhotoImage(file = "southkorea.png").subsample(5)    # 이미지 추가 및 크기 조정

 
class Game:   # 게임 클래스
    global objects
    objects = set()   # 오브젝트 세트 생성
    def __init__(self):
        self.keys = set()   # 버튼 세트 생성
        window.bind("<KeyPress>", self.keyPressHandler)
        window.bind("<KeyRelease>", self.keyReleaseHandler)
 
        obj_SouthKorea = element(340, 340, icon_SouthKorea)
 
        while(1):  # 메인 루프
            for key in self.keys:   # 버튼 체킹
                if key == ord('A'):
                   canvas.move(obj_SouthKorea.id, -5,  0)
                if key == ord('D'):
                   canvas.move(obj_SouthKorea.id, 5,  0)
                if key == ord('W'):
                   canvas.move(obj_SouthKorea.id, 0,  -5)
                if key == ord('S'):
                   canvas.move(obj_SouthKorea.id, 0,  5)
 
            for obj in objects.copy():   # 오브젝트 스텝
                obj.step()
                    
            window.update()   # 업데이트
            time.sleep(0.01)   # 0.01초 만큼 sleep
                        
    def keyPressHandler(self, event):   # 버튼 추가
        self.keys.add(event.keycode)
 
    def keyReleaseHandler(self, event):   # 버튼 제거
        if event.keycode in self.keys:
            self.keys.remove(event.keycode)

class element:   # 오브젝트 원형
    def __init__(self, x, y, image):
        self.x, self.y = x, y   # 생성 위치
        self.image = image   # 색
        objects.add(self)   # 오브젝트 세트에 자신 등록
        self.id = canvas.create_image(340, 340, anchor=NW, image = self.image)
 
    def destroy(self):   # 제거 함수
        objects.discard(self)   # 오브젝트 세트에서 자신 제거
        canvas.delete(self.id)   # 캠버스 제거
        del self
 
    def step(self):
        canvas.move(self.id, 0,  1)

Game()
