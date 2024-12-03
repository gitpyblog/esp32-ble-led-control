# ESP32 BLE LED Control

This project is a MicroPython-based Bluetooth Low Energy (BLE) application for the ESP32. It allows you to control an LED connected to the ESP32 board remotely via BLE commands.

## Features:
- **BLE Communication**: The ESP32 advertises itself as a Bluetooth device and accepts connections from central devices (e.g., smartphones, tablets).
- **LED Control**: The LED on GPIO pin 8 can be turned on and off using simple BLE commands ("on" to turn the LED off, "off" to turn the LED on).
- **Customizable Name**: The device advertises itself with a customizable name that can be specified during initialization.
- **Nordic UART Service**: Utilizes the Nordic UART Service (NUS) for receiving and sending data over BLE.

## Components:
- **ESP32**: The main microcontroller handling BLE communication and GPIO.
- **MicroPython**: Lightweight Python implementation for microcontrollers, used to write the application.
- **Bluetooth**: Communication protocol for wireless control of the LED.

## How It Works:
1. The ESP32 starts advertising as a BLE device.
2. Once connected to a central device, it listens for commands sent via BLE.
3. The received command is processed to control the LED (turn on or off).
4. If disconnected, the ESP32 resumes advertising to accept new connections.

## Setup:
1. Install MicroPython on your ESP32 device.
2. Upload the script to your ESP32 board.
3. Connect to the ESP32 via a Bluetooth-enabled app (like a BLE scanner or a custom app).
4. Send the commands "on" or "off" to control the LED.

## Requirements:
- ESP32 board
- MicroPython installed on the ESP32
- BLE-capable device (smartphone, tablet, etc.) for communication
