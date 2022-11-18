import asyncio
import websockets

location_data = {}
USERS = set()


async def echo(websocket):
    global location_data
    USERS.add(websocket)
    async for message in websocket:
        print(message)
        class_list = dict()
        temp = message.split(':')
        class_list['latitude'] = temp[0]
        class_list['longitude'] = temp[1]
        class_list['driver_id'] = temp[2]
        print(class_list)
        location_data.update({temp[2]: [temp[0], temp[1]]})
        await websocket.send(message)
        print(location_data.get(temp[2]))


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
