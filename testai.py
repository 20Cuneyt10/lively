import pyaudio
import numpy as np
import turtle
import time

RATE = 44100 #Standard audio sampling frequency
CHUNK = int(RATE / 20)  # 2205 samples per frame (~50ms chunks)
WIDTH, HEIGHT = 800, 400
#Normal setup for the turtle library
def setup_turtle():
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.bgcolor("black")
    screen.title("Soundy thing")
    screen.tracer(0, 0)  # Disable auto-animation for computational saving 
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.color("#00FF00")  
    t.pensize(2)
    return screen, t

def draw_waveform(t, screen, data):
    t.clear()
    if len(data) == 0:
        return
    t.penup()
    # Map array indices to Screen X coordinates (-WIDTH/2 to WIDTH/2)
    x_step = WIDTH / len(data)
    start_x = -WIDTH / 2
    
    # Normalize 16-bit signed int (-32768 to 32767) to fit window HEIGHT
    y_scale = (HEIGHT / 2) / 32768.0 

    # Main drawing system
    for i, sample in enumerate(data):
        x = start_x + (i * x_step)
        y = sample * y_scale
        t.goto(x, y)
        if i == 0:
            t.pendown()
            
    screen.update()  #Manual update every loop to ensure we get 20FPS

if __name__ == "__main__":
    screen, t = setup_turtle()
    
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )
    
    print("Recording and rendering...")
    try:
        while True:
            t1 = time.time()
            
            raw_str = stream.read(CHUNK, exception_on_overflow=False)#makes sure the program doesnt give errors when we get over 50ms
            data = np.frombuffer(raw_str, dtype=np.int16)
            
            draw_waveform(t, screen, data)
            
            
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        