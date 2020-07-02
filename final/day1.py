# 프로젝트 1일 - 대한민국 아이콘을 움직이게 만들기


from tkinter import *
import time
 
window = Tk()
window.title("Asia War")   # 게임 이름
window.resizable(0,0)
canvas = Canvas(window, width = 750, height = 750, bg ="black")   # 창 생성
canvas.pack()
icon_SouthKorea = PhotoImage(file = "southkorea.png").subsample(5)    # 이미지 추가 및 크기 조정

 
class Game:   # 게임 클래스
    def __init__(self):
        self.keys = set()   # 버튼 세트 생성
        window.bind("<KeyPress>", self.keyPressHandler)
        window.bind("<KeyRelease>", self.keyReleaseHandler)
 
        test = canvas.create_image(340, 340, anchor = NW, image = icon_SouthKorea)
 
        while(1):  
            for key in self.keys:   # 버튼 생성   
                if key == ord('A'):
                    canvas.move(test, -5,  0)
                if key == ord('D'):
                    canvas.move(test, 5,  0)
                if key == ord('W'):
                    canvas.move(test, 0,  -5)
                if key == ord('S'):
                    canvas.move(test, 0,  5)
 
            window.update()   # 업데이트
            time.sleep(0.01)   # 0.01초 만큼 sleep
                        
    def keyPressHandler(self, event):   # 버튼 추가
        self.keys.add(event.keycode)
 
    def keyReleaseHandler(self, event):   # 버튼 제거
        if event.keycode in self.keys:
            self.keys.remove(event.keycode)
 
Game()
