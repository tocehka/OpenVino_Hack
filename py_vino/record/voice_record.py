import sounddevice as sd
import numpy as np
import queue
import asyncio
from stream import connection
from datetime import datetime
import json

q = queue.Queue()
conn = connection.stream()

class record:

    samplerate = 44100
    channels = 2
    dtype = 'float32'
    blocksize = 1024 * 4

    data = np.array([[0,0]])
    

    async def audio_stream(self):
        def audio_callback(indata, frames, time, status):
            #print(indata)
            q.put(indata.copy())
            
        stream = sd.InputStream(blocksize=self.blocksize, dtype=self.dtype,
                channels=self.channels,
                samplerate=self.samplerate, callback=audio_callback)
        
        with stream:
            while True:
                try:
                    self.data = np.append(self.data,q.get_nowait(),axis=0)
                    await conn.send_audio(q.get_nowait())
                    #await conn.kek(q.get_nowait())
                except queue.Empty:
                    pass
    
    async def data_stream(self):
        while True:
            await asyncio.sleep(10)
            print(self.data)
            print(self.data.shape)
            dt = datetime.now()
            json_arr = {"timestamp":dt.isoformat(),"emotion":"angry","human":"Anton","data_quantity":self.data.shape[0]}
            self.data = np.array([[0,0]])
            await conn.send_data(json.dumps(json_arr))
