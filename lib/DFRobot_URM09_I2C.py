from micropython import const
from machine import I2C, Pin
from utime import sleep_ms


URM09_I2C_ADDR = const(0x11)


class DFRobot_URM09_I2C:
    """
    MicroPython class for communication with the URM09 Ultrasonic Sensor from DFRobot via I2C
    """

    MEASURE_MODE_PASSIVE = const(0x00)
    MEASURE_MODE_AUTOMATIC = const(0x80)

    MEASURE_RANG_150 = const(0x00)
    MEASURE_RANG_300 = const(0x10)
    MEASURE_RANG_500 = const(0x20)

    DELAY_MEASURE = const(0xC8)

    CMD_DISTANCE_MEASURE = const(0x01)
    DIST_H_INDEX = const(0x03)
    TEMP_H_INDEX = const(0x05)
    CFG_INDEX = const(0x07)
    CMD_INDEX = const(0x08)

    def __init__(self, sda, scl, i2c_addr=URM09_I2C_ADDR, i2c_bus=0):
        """
        Initialize the URM09 I2C communication
        :param sda: I2C SDA pin
        :param scl: I2C SCL pin
        :param i2c_addr: I2C address
        :param i2c_bus: I2C bus number
        """
        self._addr = i2c_addr
        self._buffer = [0]

        try:
            self._i2c = I2C(i2c_bus, sda=Pin(sda), scl=Pin(scl))
        except Exception as err:
            print(f'Could not initialize i2c! bus: {i2c_bus}, sda: {sda}, scl: {scl}, error: {err}')

    def _write_reg(self, reg, data) -> None:
        """
        Writes data to the I2C register
        :param reg: register address
        :param data: data to write
        :return: None
        """
        if isinstance(data, int):
            data = [data]

        try:
            self._i2c.writeto_mem(self._addr, reg, bytearray(data))
        except Exception as err:
            print(f'Write issue: {err}')

    def _read_reg(self, reg, length) -> bytes:
        """
        Reads data from the I2C register
        :param reg: register address
        :param length: number of bytes to read
        :return: bytes or 0
        """
        try:
            result = self._i2c.readfrom_mem(self._addr, reg, length)
        except Exception as err:
            print(f'Read issue: {err}')
            result = [0, 0]

        return result

    def set_mode_range(self, mode: int, distance_range: int) -> None:
        """
        Sets operation mode (MEASURE_MODE_PASSIVE or MEASURE_MODE_AUTOMATIC) and distance range

        MEASURE_RANG_150 = 150 cm
        MEASURE_RANG_300 = 300 cm
        MEASURE_RANG_500 = 500 cm
        :param mode: mode to set
        :param distance_range: range to set
        :return: None
        """
        self._buffer = [distance_range | mode]
        self._write_reg(self.CFG_INDEX, self._buffer)

    def measurement_start(self) -> None:
        """
        Starts passive measure (MEASURE_MODE_PASSIVE only)
        :return: None
        """
        self._buffer = [self.CMD_DISTANCE_MEASURE]
        self._write_reg(self.CMD_INDEX, self._buffer)

    def get_temperature(self) -> float:
        """
        Get temperature in degrees Celsius
        :return: degree celsius as float
        """
        result = self._read_reg(self.TEMP_H_INDEX, 2)

        if result == -1:
            return 25.0

        return float(((result[0] << 8) + result[1]) / 10)

    def get_distance(self) -> int:
        """
        Get distance in cm
        :return: cm as integer
        """
        sleep_ms(self.DELAY_MEASURE)

        result = self._read_reg(self.DIST_H_INDEX, 2)

        if ((result[0] << 8) + result[1]) < 32768:
            return (result[0] << 8) + result[1]
        else:
            return ((result[0] << 8) + result[1]) - 65536
