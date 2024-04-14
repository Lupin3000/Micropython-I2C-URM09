# MicroPython I2C library and example for Gravity: URM09 Ultrasonic Sensor

This repository contains the MicroPython I2C library for the Gravity: URM09 Ultrasonic Sensor from DFRobot, as well as a very simple example of how to use it. The original repository from DFRobot is located [here](https://github.com/DFRobot/DFRobot_URM09) (_for Arduino and Raspberry Pi_).

## Why this repository?

The original version of DFRobot uses Python serial (_UART_) and Python SMBus (_I2C_), which are not compatible with MicroPython. Also, I was not so happy with the Python code style/quality. That's why I created this version.

## Prerequisite

- [Gravity: URM09 Ultrasonic Sensor](https://www.dfrobot.com/product-1832.html?tracking=Mszf2HlGMStAAKkFfhNgg3QhFFchlilhR47u9vXX9o9Ko6giJYRJQdmwZjbDIvMV)
- ESP32 (_MicroPython compatible device_)
- MicroPython firmware installed (_min. 1.20.0.*_)
- USB cable (_for connection between ESP32 and sensor_)
- latest [VCP](https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers?tab=downloads) driver installed

![Ultrasonic.jpg](img/Ultrasonic.jpg)

## Installation

Clone this repository to your local computer.

```shell
# clone repository
$ git clone https://github.com/Lupin3000/Micropython-I2C-URM09.git

# change into local repository folder
$ cd Micropython-I2C-URM09/
```

You can optionally install other helpful Python packages.

- esptool (_to flash the MicroPython firmware to the ESP32_)
- rshell (_to establish a serial connection between the local computer and the ESP32 and to transfer data_)
- micropython-esp32-stubs (_to facilitate local development, for example: code completion_)

```shell
# install python packages (optional)
$ pip install -r requirements.txt
```

Connect the sensor to the ESP32. Make sure that you have set the communication mode on the sensor to I2C and use the correct connections (_ESP GPIO's/Sensor interface_)! Only then connect the ESP32 to your local computer via USB.

> In the example `main.py`, the GPIOs pins 21 (_SDA_) and 22 (_SCL_) are used. However, you can adapt these to your needs at any time.

Then start the serial connection and load the example and the library onto the ESP32 device.

```shell
# start rshell connection
$ rshell -p /dev/cu.usbserial-0001

# upload files and folder
/YOUR/LOCAL/PATH> cp main.py /pyboard/
/YOUR/LOCAL/PATH> cp -r lib/ /pyboard/
```

> The example device/path `/dev/cu.usbserial-0001` could be different for you! Please adapt before your execute the commands!

## Usage

```shell
# start the Python REPL
/YOUR/LOCAL/PATH> repl
```

Now press the keys `CTRL` + `d` on your local device, to trigger the soft-reset of the ESP32. If there are no errors, you should see the GNSS values in the terminal after a very short time.

```python
Entering REPL. Use Control-X to exit.
>
MicroPython v1.22.1 on 2024-01-05; Generic ESP32 module with ESP32
Type "help()" for more information.
>>> 
>>> 
MPY: soft reboot
```

If you have an object in given range (_no object in range means -1_), the output looks similar to this example:

```python
---
####################
Distance: 18 cm
Temperature: 24.9 °C
```

Additional information:

- [DFRobot: Product Wiki](https://wiki.dfrobot.com/URM09_Ultrasonic_Sensor_(Gravity-I2C)_(V1.0)_SKU_SEN0304)
