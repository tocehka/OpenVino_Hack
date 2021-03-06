import sounddevice as sd
import numpy as np
import queue
import asyncio
from stream import connection
from datetime import datetime
import json
import wave

q = queue.Queue()
conn = connection.stream()

class record:

    samplerate = 44100
    channels = 1
    dtype = 'float32'
    blocksize = 960

    data = np.array([[0]])
    
    #Юзайте данный подход для записи аудио с микрофона, ибо он полностью рабочий, то бишь полноценный стриминг,
    #время не ограничено заданным, как ранее. Также выход получется уже в рабочем np.array, который можно легко
    #переконвертить в байт массив bytearray(...) и работать уже непосредственно с ним, поля выше в качестве конфигов
    #тоже можно менять.
    async def audio_stream(self):
        def audio_callback(indata, frames, time, status):
            q.put(indata.copy())
            
        stream = sd.InputStream(blocksize=self.blocksize, dtype=self.dtype,
                channels=self.channels,
                samplerate=self.samplerate, callback=audio_callback)
        
        with stream:
            while True:
                try:
                    self.data = np.append(self.data,q.get_nowait(),axis=0)
                    #await conn.send_audio(np.concatenate(q.get_nowait(),axis = None))
                    await conn.send_audio(q.get_nowait())
                except queue.Empty:
                    pass
    
    async def data_stream(self):
        while True:
            await asyncio.sleep(10)
            print('Saving as wav file...')
            wf = wave.open("kek.wav", 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(4)
            wf.setframerate(44100)
            wf.writeframes(b''.join(bytearray(np.concatenate(self.data,axis = None))))
            wf.close()
            print(self.data)
            print(self.data.shape)
            dt = datetime.now()
            json_arr = {"timestamp":dt.isoformat(),"emotion":"angry","human":"Anton","data_quantity":self.data.shape[0]}
            self.data = np.array([[0]])
            #await conn.send_data(json.dumps(json_arr))
