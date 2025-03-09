import time
import threading
import pygame
import tkinter as tk
import keyboard
from tkinter import messagebox

# 타이머 실행 여부 체크 변수
running_1min = False
running_g_sequence = False
start_time_1min = None  # 1분 타이머 시작 시간
start_time_g_sequence = None  # G 타이머 시작 시간
timer_running = False  # 타이머 실행 중인지 체크하는 변수

# 기본 음량 설정 (기본값은 100%)
volume_level = 1.0

def play_audio(file):
    """음성 파일 재생"""
    pygame.mixer.init()  # pygame mixer 초기화
    pygame.mixer.music.load(file)  # 오디오 파일 로드
    pygame.mixer.music.set_volume(volume_level)  # 현재 음량 설정
    pygame.mixer.music.play()  # 오디오 재생

def update_timer_label():
    """타이머가 동작하는 동안 UI에 타이머 상태를 업데이트"""
    if running_1min:
        elapsed_time = time.time() - start_time_1min
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        timer_label_1min.config(text=f"1분 타이머: {minutes}분 {seconds}초")
    if running_g_sequence:
        elapsed_time = time.time() - start_time_g_sequence
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        timer_label_g_sequence.config(text=f"75초 + 2분 타이머: {minutes}분 {seconds}초")
    
    # UI 업데이트가 계속되도록 1000ms(1초) 후에 다시 호출
    window.after(1000, update_timer_label)

def start_1min_timer():
    """1분 주기로 YANUS.mp3 반복 실행"""
    global running_1min, start_time_1min
    if running_1min:
        return  # 이미 실행 중이면 무시

    running_1min = True
    start_time_1min = time.time()  # 타이머 시작 시간 기록
    play_audio("YANUS.mp3")  # 첫 번째 YANUS.mp3 음성 재생
    time.sleep(60)  # 60초 후에 두 번째 YANUS.mp3 실행
    if running_1min:
        play_audio("YANUS.mp3")  # 두 번째 YANUS.mp3 음성 재생
    running_1min = False  # 타이머 종료

def start_g_sequence():
    """G 버튼을 눌렀을 때, SWORD.mp3 + ERDA.mp3 반복 실행"""
    global running_g_sequence, start_time_g_sequence
    if running_g_sequence:
        return  # 이미 실행 중이면 무시

    running_g_sequence = True
    start_time_g_sequence = time.time()  # 타이머 시작 시간 기록
    # 첫 번째 SWORD.mp3
    play_audio("SWORD.mp3")
    time.sleep(75)  # 75초 후 ERDA.mp3 실행

    if running_g_sequence:
        play_audio("ERDA.mp3")  # ERDA.mp3 음성 재생
    time.sleep(45)  # 45초 후 다시 SWORD.mp3 실행
    if running_g_sequence:
        play_audio("SWORD.mp3")  # 두 번째 SWORD.mp3 음성 재생
    running_g_sequence = False  # 타이머 종료

def stop_timers():
    """타이머 중지"""
    global running_1min, running_g_sequence, timer_running
    running_1min = False
    running_g_sequence = False
    timer_running = False  # 타이머 중지 상태로 설정
    timer_label_1min.config(text="1분 타이머 중지됨.")
    timer_label_g_sequence.config(text="G 타이머 중지됨.")
    print("타이머가 중지되었습니다.")

def handle_keypress(event):
    """키 입력 감지 후 타이머 실행"""
    global running_1min, running_g_sequence, timer_running
    key = event.name.lower()  # 대소문자 구분 없이 처리
    if timer_running:  # 타이머가 실행 중일 때만 입력을 처리
        if key == 'y' and not running_1min:
            threading.Thread(target=start_1min_timer, daemon=True).start()  # Y 눌렀을 때 1분 타이머 시작
        elif key == 'g' and not running_g_sequence:
            threading.Thread(target=start_g_sequence, daemon=True).start()  # G 눌렀을 때 75초 + 2분 타이머 시작

def update_volume(val):
    """슬라이더 값에 따라 음량 조절"""
    global volume_level
    volume_level = float(val)  # 슬라이더 값을 0.0에서 1.0 사이로 설정
    pygame.mixer.music.set_volume(volume_level)  # 새로운 음량 적용

def start_timer():
    """타이머 시작 함수"""
    global timer_running
    timer_running = True  # 타이머 실행 상태로 설정
    keyboard.hook(handle_keypress)  # 키보드 입력 감지 시작
    timer_label_1min.config(text="1분 타이머 대기 중...")  # 1분 타이머 대기 상태로 텍스트 변경
    timer_label_g_sequence.config(text="G 타이머 대기 중...")  # G 타이머 대기 상태로 텍스트 변경

    update_timer_label()  # 타이머 상태 업데이트 함수 호출

def stop_timer_button():
    """타이머 시작 버튼을 눌렀을 때의 중지 함수"""
    stop_timers()
    start_button.grid(row=4, column=0, pady=10, padx=10, sticky="ew")  # 중지 후, '시작' 버튼 보이게 하기
    stop_button.grid_forget()  # '중지' 버튼 숨기기

def start_button_function():
    """타이머 시작 버튼을 눌렀을 때의 함수"""
    start_button.grid_forget()  # '시작' 버튼 숨기기
    stop_button.grid(row=4, column=0, pady=10, padx=10, sticky="ew")  # '중지' 버튼 보이게 하기
    start_timer()  # 타이머 시작

# GUI 구성
window = tk.Tk()
window.title("hunt_timer")
window.geometry("300x350")  # 창 크기 설정

# 창 상단 아이콘 설정
window.iconphoto(True, tk.PhotoImage(file="./mainIcon.png"))  # your_icon.png 파일을 아이콘으로 사용

# 타이머 상태 표시 레이블 (각각 1분 타이머와 G 타이머)
timer_label_1min = tk.Label(window, text="1분 타이머 대기 중...", font=("Arial", 12))
timer_label_1min.grid(row=0, column=0, pady=10, sticky="nsew")

timer_label_g_sequence = tk.Label(window, text="G 타이머 대기 중...", font=("Arial", 12))
timer_label_g_sequence.grid(row=1, column=0, pady=10, sticky="nsew")

# 타이머 시작 버튼
start_button = tk.Button(window, text="타이머 시작", font=("Arial", 12), command=start_button_function)
start_button.grid(row=2, column=0, pady=10, sticky="ew", padx=10)

# 타이머 중지 버튼
stop_button = tk.Button(window, text="타이머 중지", font=("Arial", 12), command=stop_timer_button)
stop_button.grid_forget()  # 처음에는 중지 버튼을 숨겨둠

# 음량 조절 슬라이더
volume_slider = tk.Scale(window, from_=0, to=1, orient="horizontal", resolution=0.01, label="음량 조절", command=update_volume)
volume_slider.set(1.0)  # 기본 음량은 100%
volume_slider.grid(row=5, column=0, pady=10, sticky="nsew", padx=10)

# 창 내용 중앙 정렬을 위한 row, column 설정
window.grid_rowconfigure(0, weight=1)
window.grid_rowconfigure(1, weight=1)
window.grid_rowconfigure(2, weight=1)
window.grid_rowconfigure(3, weight=1)
window.grid_rowconfigure(4, weight=1)
window.grid_rowconfigure(5, weight=1)
window.grid_columnconfigure(0, weight=1)

# GUI 이벤트 루프
window.mainloop()
