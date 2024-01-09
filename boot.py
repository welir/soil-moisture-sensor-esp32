# This file is executed on every boot (including wake-boot from deepsleep)
import esp
import ubinascii
import machine
import micropython
import esp
import gc
import webrepl
import network
import json
import os
import time
from time import sleep
from main import read_sensors_and_publish
from machine import deepsleep
time_to_deep_sleep = 3600000

def do_connect(ssid, password):
    wlan_sta = network.WLAN(network.STA_IF)
    wlan_sta.active(True)
    if wlan_sta.isconnected():
        return True
    print('Trying to connect to %s...' % ssid)
    wlan_sta.connect(ssid, password)
    for retry in range(200):
        connected = wlan_sta.isconnected()
        if connected:
            break
        time.sleep(0.1)
        print('.', end='')
    if connected:
        connected_handler()
        print('\nConnected. Network config: ', wlan_sta.ifconfig())
        
    else:
        not_connected_handler()
        print('\nFailed. Not Connected to: ' + ssid)
    return connected

def connected_handler():
    print("Подключено к Wi-Fi")
    # Здесь можно включить светодиод, например, путем установки пина в состояние HIGH
    machine.Pin(22, machine.Pin.OUT).on()
    
def not_connected_handler():
    print("Подключено к Wi-Fi")
    # Здесь можно включить светодиод, например, путем установки пина в состояние HIGH
    machine.Pin(22, machine.Pin.OUT).off()
    
def init():
    try:
        with open('config.json', 'r') as fd:
            cfg = json.load(fd)
    except (OSError, ValueError):
        print("error webrepl config start")
        
    
    if 'wlan' in cfg:
        if do_connect(cfg['wlan']['ssid'], cfg['wlan']['password']):
             if read_sensors_and_publish(min_moisture=cfg['calibrated_moisture_limits']['min_moisture'], max_moisture=cfg['calibrated_moisture_limits']['max_moisture']) > 10:
                 print(f"Переход в режим сна на {time_to_deep_sleep/1000} сек")
                 deepsleep(time_to_deep_sleep) 
   
while True:
  init()
  sleep(30)
