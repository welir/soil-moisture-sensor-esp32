# main.py -- put your code here!
from machine import ADC
from machine import deepsleep
import time
import neopixel
from machine import Pin
print('Start main.py')
import urequests as requests
from time import sleep
import ujson

def valmap(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))


'''
Max ~ 850mV (dry)

Low ~ 250mV (in water)
'''

MOISTURE_SENSOR_PIN = 34
LED_SENSOR_PIN = 16
last_message = time.time()
counter = 0
message_interval = 10

min_moisture=2578
max_moisture=850

# время в миллисекундах
time_to_sleep = 1

# Read Ntfy server URL and default topic from config
with open('config.json', 'r') as config_file:
    config = ujson.load(config_file)
ntfy_srv_url = config.get("ntfy_server", {}).get("url", '')
default_topic = config.get("ntfy_server", {}).get("topic", 'default_topic')


def set_led_color(percent):
    # Установите количество светодиодов в ленте
    num_leds = 1

    # Установите пин для подключения ленты
    pin = Pin(LED_SENSOR_PIN, Pin.OUT)

    # Создайте объект ленты
    np = neopixel.NeoPixel(pin, num_leds)

    # Вычислите значение цвета в зависимости от процента
    r = int(255 * ( 100 - percent) / 100)
    g = int(165 *(   percent) / 100)
    b = int(255 *(   percent) / 100)

    # Установите цвет светодиода
    np[0] = (r, g, b)

    # Обновите ленту
    np.write()

def set_led_red():
    # Установите количество светодиодов в ленте
    num_leds = 1

    # Установите пин для подключения ленты
    pin = Pin(LED_SENSOR_PIN, Pin.OUT)

    # Создайте объект ленты
    np = neopixel.NeoPixel(pin, num_leds)

    # Вычислите значение цвета в зависимости от процента
    r = 255
    g = 0
    b = 0

    # Установите цвет светодиода
    np[0] = (r, g, b)

    # Обновите ленту
    np.write()
    
def set_led_off():
    # Установите количество светодиодов в ленте
    num_leds = 1

    # Установите пин для подключения ленты
    pin = Pin(LED_SENSOR_PIN, Pin.OUT)

    # Создайте объект ленты
    np = neopixel.NeoPixel(pin, num_leds)
    for i in range(1):
       np[i] = (0, 0, 0)
       np.write()
       
def read_sensors_and_publish(min_moisture=min_moisture,max_moisture=max_moisture):
    #sensor_dht11 = dht.DHT11(Pin(13, mode=Pin.OPEN_DRAIN))
    pin = Pin(MOISTURE_SENSOR_PIN, Pin.IN)
    adc = ADC(pin)
    soil_sensor = adc
    soil_sensor.atten(ADC.ATTN_11DB)
    #Full range: 3.3v   #range 0 to 4095
    try:
            #sensor_dht11.measure()
            temp = 0#sensor_dht11.temperature()
            hum = 0#sensor_dht11.humidity()
           
            moisture_in_soil =  100 - (max_moisture-soil_sensor.read())*100/(max_moisture-min_moisture)
            if moisture_in_soil < 20:
              set_led_red()
            else:
              set_led_off()
            print('Soil value: '+ str(soil_sensor.read()))
            print('Soil %: '+ str(moisture_in_soil) + "%")
            #print('Temperature: %3.1f C' %temp)
            #print('Humidity: %3.1f %%' %hum)
            publish_sensor_data(create_json(temperature=temp, humidity=hum, soil_moisture=moisture_in_soil), "fikus")
            return moisture_in_soil
    except OSError as e:
            print(e)
            print('Failed to read sensor.')


def create_json(**kwargs):
    try:
        print(dict(kwargs))
        return ujson.dumps(dict(kwargs))
    except Exception as e:
        return None

def publish_sensor_data(data, topic):
    try:
        print(data)
        send_to_ntfy(topic=topic, msg=data)
    except Exception as e:
        print("failed sending sensor data..")
        
def send_to_ntfy(topic='Epmty topic', msg=''):
    # Use the Ntfy server URL from config
    url = f"http://{ntfy_srv_url}/{topic}"  # Замените на корректный URL
    # Создание JSON-данных для отправки
    notification_data = {
      "orange_sensor": msg
    }
    # Отправка POST-запроса на сервер ntfy
    response = requests.post( url, json=notification_data)
    # Проверка статуса ответа
    if response.status_code == 200:
        print("Уведомление успешно отправлено")
    else:
        print(f"Произошла ошибка при отправке уведомления {response.status_code}")
    # Закрытие соединения
    response.close()
                


