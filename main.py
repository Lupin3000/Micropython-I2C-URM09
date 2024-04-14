from micropython import const
from utime import sleep_ms

from lib.DFRobot_URM09_I2C import DFRobot_URM09_I2C


SDA_PIN = const(21)
SCL_PIN = const(22)
DELAY = const(500)


if __name__ == '__main__':
    sensor = DFRobot_URM09_I2C(sda=SDA_PIN, scl=SCL_PIN)
    sensor.set_mode_range(mode=sensor.MEASURE_MODE_AUTOMATIC, distance_range=sensor.MEASURE_RANG_150)

    while True:
        print(f"{'#' * 20}")
        print(f'Distance: {sensor.get_distance()} cm')
        print(f'Temperature: {sensor.get_temperature()} °C')

        sleep_ms(DELAY)
