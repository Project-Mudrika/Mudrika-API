import asyncio
from time import sleep
import websockets

location_data = {}
USERS = set()


async def echo(websocket):
    global location_data
    USERS.add(websocket)
    async for message in websocket:
        try:
            print(message)
            class_list = dict()
            temp = message.split(':')
            class_list['action'] = temp[0]
            if (temp[0] == 'update'):
                class_list['latitude'] = temp[2]
                class_list['longitude'] = temp[3]
                class_list['driver_id'] = temp[1]
                location_data.update({temp[1]: [temp[2], temp[3]]})
                USERS.remove(websocket)
                # await websocket.send('jiii')
            elif (temp[0] == 'get'):
                print(location_data.get(temp[1]))
                loc = location_data.get(temp[1])
                location = f"{temp[1]}:{loc[0]}:{loc[1]}"
                await websocket.send(location)
                try:
                    USERS.remove(websocket)
                except:
                    pass
        except:
            pass

        finally:
            # Unregister user
            try:
                # USERS.remove(websocket)
                pass
            except:
                pass


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
