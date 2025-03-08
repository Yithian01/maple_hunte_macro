import time
import threading
import pygame
import tkinter as tk
import keyboard  # 키보드 입력 감지 추가
from tkinter import messagebox

# 타이머 실행 여부 체크 변수
running_1min = False
running_g_sequence = False
start_time = None  # 타이머 시작 시간

def play_audio(file):
    """음성 파일 재생"""
    pygame.mixer.init()  # pygame mixer 초기화
    pygame.mixer.music.load(file)  # 오디오 파일 로드
    pygame.mixer.music.play()  # 오디오 재생

def update_timer_label():
    """타이머가 동작하는 동안 UI에 타이머 상태를 업데이트"""
    if running_1min:
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        timer_label.config(text=f"1분 타이머: {minutes}분 {seconds}초")
    if running_g_sequence:
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        timer_label.config(text=f"75초 + 2분 타이머: {minutes}분 {seconds}초")
    
    # UI 업데이트가 계속되도록 1000ms(1초) 후에 다시 호출
    window.after(1000, update_timer_label)

def start_1min_timer():
    """1분 주기로 YANUS.mp3 반복 실행"""
    global running_1min, start_time
    if running_1min:
        return  # 이미 실행 중이면 무시

    running_1min = True
    start_time = time.time()  # 타이머 시작 시간 기록
    while running_1min:
        play_audio("YANUS.mp3")  # YANUS.mp3 음성 재생
        time.sleep(60)  # 1분 간격으로 반복 실행
        window.update()  # UI 업데이트

def start_g_sequence():
    """G 버튼을 눌렀을 때, SWORD.mp3 + ERDA.mp3 반복 실행"""
    global running_g_sequence, start_time
    if running_g_sequence:
        return  # 이미 실행 중이면 무시

    running_g_sequence = True
    start_time = time.time()  # 타이머 시작 시간 기록
    # 첫 번째 SWORD.mp3
    play_audio("SWORD.mp3")
    timer_label.config(text="SWORD 타이머 시작")
    window.update()

    # 75초 후 ERDA.mp3
    time.sleep(75)
    while running_g_sequence:
        play_audio("ERDA.mp3")  # ERDA.mp3 음성 재생
        time.sleep(75)  # 75초 간격으로 반복 실행
        window.update()  # UI 업데이트

def stop_timers():
    """타이머 중지"""
    global running_1min, running_g_sequence
    running_1min = False
    running_g_sequence = False
    timer_label.config(text="타이머 중지됨.")
    print("타이머가 중지되었습니다.")

def handle_keypress(event):
    """키 입력 감지 후 타이머 실행"""
    global running_1min, running_g_sequence
    key = event.name.lower()  # 대소문자 구분 없이 처리
    if key == 'y' and not running_1min:
        threading.Thread(target=start_1min_timer, daemon=True).start()  # Y 눌렀을 때 1분 타이머 시작
    elif key == 'g' and not running_g_sequence:
        threading.Thread(target=start_g_sequence, daemon=True).start()  # G 눌렀을 때 75초 + 2분 타이머 시작

def start_timer():
    """타이머 시작 버튼 클릭 시 호출되는 함수"""
    start_button.pack_forget()  # 타이머 시작 버튼 숨기기
    keyboard.hook(handle_keypress)  # 키보드 입력 감지 시작
    timer_label.config(text="타이머 대기 중...")  # 타이머 대기 상태로 텍스트 변경

    update_timer_label()  # 타이머 상태 업데이트 함수 호출

# GUI 구성
window = tk.Tk()
window.title("hunt_timer")
window.geometry("300x200")  # 창 크기 설정

# 창 상단 아이콘 설정
window.iconphoto(True, tk.PhotoImage(file="./mainIcon.png"))  # your_icon.png 파일을 아이콘으로 사용

timer_label = tk.Label(window, text="Made for 빡법사", font=("Arial", 12))
timer_label.pack(pady=10)

# 타이머 시작 버튼
start_button = tk.Button(window, text="타이머 시작", font=("Arial", 12), command=start_timer)
start_button.pack(pady=10)

# 타이머 중지 버튼
button_stop = tk.Button(window, text="타이머 중지", font=("Arial", 12), command=stop_timers)
button_stop.pack(pady=5)

# GUI 이벤트 루프
window.mainloop()
