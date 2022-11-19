import asyncio
import websockets


async def hello():
    async with websockets.connect("ws://localhost:8765") as websocket:
        while (True):
            data = input(
                'Enter latitude,longitude & driverid separated by ":" ')

            await websocket.send(data)
            msg = await websocket.recv()
            print(msg)

asyncio.run(hello())
