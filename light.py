import network
import socket
import machine
import time
# Connect to Wi-Fi
ssid = 'vivo Y75'
password = 'gayatri23'
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, password)
while not sta_if.isconnected():
    pass
print('Network config:', sta_if.ifconfig())
# Setup socket for UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 12345))
# Setup LEDs
builtin_led = machine.Pin(2, machine.Pin.OUT)  # Built-in LED on GPIO2
external_led = machine.Pin(5, machine.Pin.OUT)  # External LED on GPIO5, change according to your setup
while True:
    data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
    message = data.decode('utf-8')
    
    if message == 'CLOSED':
        builtin_led.value(1)  # Turn on built-in LED
        external_led.value(0)  # Turn off external LED
    elif message == 'OPEN':
        builtin_led.value(0)  # Turn off built-in LED
        external_led.value(1)  # Turn on external LED
    time.sleep(0.1)

