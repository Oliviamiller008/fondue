import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.sensor import Sensor
from kasa import Discover, SmartPlug

async def client():
  creds = Credentials(
      type='robot-location-secret',
      payload='lauqrt4op4x6ubhji867wue0qsnqdq76x00ljfv7vcoyq7mi')
  opts = RobotClient.Options(
      refresh_interval=0,
      dial_options=DialOptions(credentials=creds)
  )
  async with await RobotClient.at_address(
    'tempbot-main.rdt5n4brox.local.viam.cloud:8080',
    opts) as robot:
      print('Resources:')
      print(robot.resource_names)

      sensor = Sensor.from_robot(robot, "sensor")


      # getting device address
      # devices = await Discover.discover()
      # for addr, dev in devices.items():
      #     await dev.update()
      #     print(addr)
      #     print(dev)

      plug = SmartPlug('10.1.11.221')
      await plug.update()


      while(1):
        temp = await sensor.get_readings() 
        print(temp[0])
        ison = plug.is_on

        if(temp[0] > 62 and ison):
          await plug.turn_off()
          await plug.update()
          print("turning off")
        
        if(temp[0] < 55 and not ison):
          await plug.turn_on()
          await plug.update()
          print("turning on")

        await asyncio.sleep(5)





if __name__ == '__main__':
  asyncio.run(client())
