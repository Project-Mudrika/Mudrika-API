import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        print(message)
        class_list = dict() 
        temp = message.split(':') 
        class_list['latitude'] = temp[0]
        class_list['longitude'] = temp[1]
        class_list['driver_id'] = temp[2]
        print(class_list)
        await websocket.send(message)

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())