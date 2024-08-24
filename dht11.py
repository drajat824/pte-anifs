import time
import adafruit_dht
import board
import struct
import socket

sensor = adafruit_dht.DHT11(board.D21)
data_temperature = None

# Socket Matlab
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_ip_matlab = "192.168.0.2"
udp_port_matlab = 27002

# Socket Internal
udp_ip_internal = "127.0.0.1"
udp_port_internal = 5002

while True:
    try:
        data_temperature = sensor.temperature
        if data_temperature is None:
            raise

        if data_temperature is not None:
            sock.sendto(struct.pack('d', data_temperature), (udp_ip_internal, udp_port_internal))
            sock.sendto(struct.pack('d', data_temperature), (udp_ip_matlab, udp_port_matlab))
    except RuntimeError as e:
        continue
    except Exception as e:
        continue

    time.sleep(1)