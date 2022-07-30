import asyncio
import struct
import csv
import os

from bleak import BleakClient

addressx1 = "353B35F3-9B98-D9DE-0646-124A57432475"
addressx2 = "3A79B83B-4A84-FDF2-2EE2-971924DC9631"
UUID = "19b10000-5001-537e-4f6c-d104768a1214"
os.remove("data-shuffle.txt")


def callback(x, data):
    time_loc = str(int.from_bytes(data[0:4], byteorder='little', signed=False))
    ax = str(int.from_bytes(data[4:8], byteorder='little', signed=True))
    ay = str(int.from_bytes(data[8:12], byteorder='little', signed=True))
    az = str(int.from_bytes(data[12:16], byteorder='little', signed=True))
    gx = str(int.from_bytes(data[16:20], byteorder='little', signed=True))
    gy = str(int.from_bytes(data[20:24], byteorder='little', signed=True))
    gz = str(int.from_bytes(data[24:28], byteorder='little', signed=True))
    mx = str(int.from_bytes(data[28:32], byteorder='little', signed=True))
    my = str(int.from_bytes(data[32:36], byteorder='little', signed=True))
    mz = str(int.from_bytes(data[36:40], byteorder='little', signed=True))
    qw = str(int.from_bytes(data[40:44], byteorder='little', signed=True))
    qx = str(int.from_bytes(data[44:48], byteorder='little', signed=True))
    qy = str(int.from_bytes(data[48:52], byteorder='little', signed=True))
    qz = str(int.from_bytes(data[52:56], byteorder='little', signed=True))
    roll = str(struct.unpack('f', data[56:60])[0])
    pitch = str(struct.unpack('f', data[60:64])[0])
    yaw = str(struct.unpack('f', data[64:68])[0])

    row = []
    row.append(time_loc)
    row.append(ax)
    row.append(ay)
    row.append(az)
    row.append(gx)
    row.append(gy)
    row.append(gz)
    row.append(mx)
    row.append(my)
    row.append(mz)
    row.append(qw)
    row.append(qx)
    row.append(qy)
    row.append(qz)
    row.append(roll)
    row.append(pitch)
    row.append(yaw)

    f = open("data-shuffle.txt", "a")
    writer = csv.writer(f)
    writer.writerow(row)
    print(x, row)
    f.close()




async def main(address1, address2):
    client1 = BleakClient(address1)
    client2 = BleakClient(address2)
    try:
        await client1.connect()
        await client2.connect()
        await client1.start_notify(UUID, callback)
        await client2.start_notify(UUID, callback)
        await asyncio.sleep(40)
    except Exception as e:
        print(e)
    finally:
        await client1.stop_notify(UUID)
        await client2.stop_notify(UUID)
        await client1.disconnect()
        await client2.disconnect()


asyncio.run(main(addressx1, addressx2))
