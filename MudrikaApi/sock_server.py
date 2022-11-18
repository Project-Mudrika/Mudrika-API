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
        class_list['action'] = temp[0]
        if(temp[0]=='update'):

            class_list['latitude'] = temp[2]
            class_list['longitude'] = temp[3]
            class_list['driver_id'] = temp[1]
            location_data.update({temp[1]: [temp[2], temp[3]]})
            await websocket.send('jiii')
        elif(temp[0]=='get'):
            print(location_data.get(temp[1]))
            loc=location_data.get(temp[1])
            location=f"{temp[1]}:{loc[0]}:{loc[1]}"
            await websocket.send(location)
        

async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
