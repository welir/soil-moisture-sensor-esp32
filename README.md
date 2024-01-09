# ESP32 Capacitive Soil Moisture IoT Project

A project for ESP32 designed to collect data from an analog capacitive soil moisture sensor and send notifications to the Ntfy server. The device goes into sleep mode every hour to optimize power consumption.

## Project Overview

The project allows monitoring soil moisture levels using ESP32, sending notifications to the Ntfy server. The device enters sleep mode every hour, saving energy.

## Key Features

- **MicroPython:** The project is developed using MicroPython, a lightweight implementation of Python 3 for microcontrollers.
- **Soil Moisture Sensor:** Monitors soil moisture levels using an analog capacitive soil moisture sensor.
 ![image](https://github.com/welir/soil-moisture-sensor-esp32/assets/7795803/866537a6-aa77-4406-84f6-49629a3e7753)
- **Ntfy Server Integration:** Sends notifications to the Ntfy server to keep you informed.
- **Power Optimization:** The device goes into sleep mode every hour to conserve energy.

## Key Files

- `main.py`: The main project code, including reading data from the sensor and sending notifications.
- `boot.py`: Configuration file executed on every boot, ensuring Wi-Fi connection and calling the main function.
## Ntfy Docker Compose Setup

To set up the Ntfy server using Docker Compose, follow these steps:

1. Install Docker and Docker Compose on your server.

2. Create a `docker-compose.yml` file with the following content:

```yaml
version: "2.7"

services:
  ntfy:
    image: binwiederhier/ntfy
    container_name: ntfy
    command:
      - serve
    environment:
      - TZ=MOSCOW    # optional: set desired timezone
    user: 1000:1000 # optional: replace with your own user/group or uid/gid
    volumes:
      - /var/cache/ntfy:/var/cache/ntfy
      - /etc/ntfy:/etc/ntfy
    ports:
      - 80:80
    healthcheck: # optional: remember to adapt the host:port to your environment
        test: ["CMD-SHELL", "wget -q --tries=1 http://localhost:80/v1/health -O - | grep -Eo '\"healthy\"\\s*:\\s*true' || exit 1"]
        interval: 60s
        timeout: 10s
        retries: 3
        start_period: 40s
    restart: unless-stopped
```
3. Run the following command to start the Ntfy server:
```bash
docker-compose up -d
```
4. Access the Ntfy server at `http://your_server_ip:80`.
   
## Usage

1. Install the necessary libraries (don't forget to install `urequests`).
2. Create a `config.json` file with Wi-Fi settings, moisture limits, Ntfy server URL, and default topic.
3. Upload the `main.py` and `boot.py` files to your ESP32.
4. Connect the soil moisture sensor and LED indicator to ESP32.
5. Enjoy monitoring soil moisture using the Ntfy server!

## File Descriptions

### `main.py`

The main code, including reading data from the soil moisture sensor, controlling the LED indicator, and sending notifications to the Ntfy server.

### `boot.py`

The configuration file executed on every device boot. It ensures Wi-Fi connection, initializes the device, and transitions it to sleep mode.

## Configuration (config.json)

```json
{
  "wlan": {
    "ssid": "Your_WiFi_SSID",
    "password": "Your_WiFi_Password"
  },
  "calibrated_moisture_limits": {
    "min_moisture": 2578,
    "max_moisture": 850
  },
  "ntfy_server": {
    "url": "http://your_ntfy_server_ip",
    "topic": "your_default_topic"
  }
}
```
## Dependencies
* The `urequests` library for making HTTP requests.
* The `config.json` file with Wi-Fi settings, moisture limits, Ntfy server URL, and default topic.
* The `main.py` file for the `read_sensors_and_publish` function.

## Tags
`ESP32`, `MicroPython`, `Soil Moisture Sensor`, `IoT`, `Ntfy Server Integration`, `Power Optimization`
## License
This project is distributed under the MIT License - see the LICENSE file for details.
