from record import voice_record
from stream import connection
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import struct
import asyncio
import threading

record = voice_record.record()

async def recording():
    print("Starting record...\n")

    await record.audio_stream()

async def data_worker():

    await record.data_stream()
    
def audio_sending():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.ensure_future(recording())
    loop.run_forever()

def data_sending():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.ensure_future(data_worker())
    loop.run_forever()

if __name__ == "__main__":
    tr1 = threading.Thread(target=audio_sending)
    tr2 = threading.Thread(target=data_sending)
    tr1.start()
    tr2.start()
    tr1.join()
    tr2.join()