import pyaudio
import numpy as np
import matplotlib.pyplot as pylab
import time

RATE = 44100
CHUNK = int(RATE/20) # RATE / number of updates per second

def soundplot(stream):
    t1=time.time()
    raw_data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)#fromstring was giving errors so ı changed it
    data = np.clip(raw_data, 0, 32767)
    pylab.plot(data)
    pylab.title(i)
    pylab.grid()
    pylab.axis([0,len(data),-2**16/2,2**16/2])
    
    pylab.savefig("03.png",dpi=50)
    pylab.close('all')
    print("took %.02f ms"%((time.time()-t1)*1000))

if __name__=="__main__":
    p=pyaudio.PyAudio()
    stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
                  frames_per_buffer=CHUNK)
    for i in range(int(20*RATE/CHUNK)): #do this for 10 seconds
        soundplot(stream)
    stream.stop_stream()
    stream.close()
    p.terminate()
### Code sourced from the personal website of Scott W. Harden, available at: https://swharden.com/blog/2016-07-19-realtime-audio-visualization-in-python/ with the smallest fix ever