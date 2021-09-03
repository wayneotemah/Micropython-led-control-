# ************************
# Web Server in ESP32 using
# web sockets (wifi station)
# Author: George Bantique
# Date: October 28, 2020
# Feel free to modify it
# according to your needs
# ************************

import machine

led1 = machine.Pin(5, machine.Pin.OUT)
led2 = machine.Pin(16, machine.Pin.OUT)
led3 = machine.Pin(4, machine.Pin.OUT)
led1.off()
led2.off()
led3.off()

# ************************
# Configure the ESP32 wifi
# as Station mode.
import network


sta = network.WLAN(network.STA_IF)
if not sta.isconnected():
    print('connecting to network...')
    sta.active(True)
    sta.connect('you wifi name ', 'your wifi password')
    while not sta.isconnected():
        pass
print('network config:', sta.ifconfig())

# ************************
# Configure the socket connection
# over TCP/IP
import socket

# AF_INET - use Internet Protocol v4 addresses
# SOCK_STREAM means that it is a TCP socket.
# SOCK_DGRAM means that it is a UDP socket.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))  # specifies that the socket is reachable
#                 by any address the machine happens to have
s.listen(5)  # max of 5 socket connections


# ************************

def web_page():
    # Function for generate a webpage and responsive labels

    # for led1
    if led1.value() == 1:
        led_state1 = 'ON'
        print('led is ON')
    elif led1.value() == 0:
        led_state1 = 'OFF'
        print('led is OFF')
    #  for led2
    if led2.value() == 1:
        led_state2 = 'ON'
        print('led is ON')
    elif led2.value() == 0:
        led_state2 = 'OFF'
        print('led is OFF')
    # for led3
    if led3.value() == 1:
        led_state3 = 'ON'
        print('led is ON')
    elif led3.value() == 0:
        led_state3 = 'OFF'
        print('led is OFF')



    html_page = """   
      <html>   
      <head>   
       <meta content="width=device-width, initial-scale=1" name="viewport"></meta>   
      </head>   
      <body>   
        <center><h2>MicroPy ESP8266 IOT</h2></center>
        <center>The 'hello world' of IOT and Microcontrollers </center>   
        <center>   
         <form>   
          <button name="LED1" type="submit" value="1"> LED1 ON </button>   
          <button name="LED1" type="submit" value="0"> LED1 OFF </button> <br><br><br>
          <button name="LED2" type="submit" value="1"> LED2 ON </button>   
          <button name="LED2" type="submit" value="0"> LED2 OFF </button><br><br><br>
          <button name="LED3" type="submit" value="1"> LED3 ON </button>   
          <button name="LED3" type="submit" value="0"> LED3 OFF </button><br><br><br>
         </form>   
        </center>   
        <center><p>LED 1 is now <strong>""" + led_state1 + """</strong>.</p>
        </center> 
        </center>   
        <center><p>LED 2 is now <strong>""" + led_state2 + """</strong>.</p>
        </center> 
        </center>   
        <center><p>LED 3 is now <strong>""" + led_state3 + """</strong>.</p>
        </center>   
      </body>   
      </html>"""
    return html_page


while True:
    # Socket accept()
    conn, addr = s.accept()
    print("Got connection from %s" % str(addr))

    # Socket receive()
    request = conn.recv(1024)
    print("")
    print("")
    print("Content %s" % str(request))

    # Socket send()
    request = str(request)
    # led1_on = request.find('/?LED1=1')
    # led1_off = request.find('/?LED1=0')

    if request.find('/?LED1=1') == 6:
        print('LED1 ON')
        print(str(request.find('/?LED1=0')))
        led1.value(1)

    elif request.find('/?LED1=0') == 6:
        print('LED1 OFF')
        print(str(request.find('/?LED1=0')))
        led1.value(0)

    elif request.find('/?LED2=1') == 6:
        print('LED2 ON')
        print(str(request.find('/?LED2=1')))
        led2.value(1)

    elif request.find('/?LED2=0') == 6:
        print('LED2 OFF')
        print(str(request.find('/?LED2=0')))
        led2.value(0)

    elif request.find('/?LED3=1') == 6:
        print('LED3 ON')
        print(str(request.find('/?LED3=1')))
        led3.value(1)

    elif request.find('/?LED3=0') == 6:
        print('LED3 OFF')
        print(str(request.find('/?LED3=0')))
        led3.value(0)


    response = web_page()

    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)

    # Socket close()
    conn.close()