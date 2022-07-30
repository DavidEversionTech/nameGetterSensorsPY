import asyncio
from bleak import BleakScanner


async def main():
    eversion = []

    devices = await BleakScanner.discover(timeout=7)
    for d in devices:
        if d.name == 'Feather nRF52832 Express' or d.name == 'SENSOR_L' or d.name == 'SENSOR_R':
            print(d)
            eversion.append(d)


asyncio.run(main())
