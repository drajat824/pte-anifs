from gpiozero import InputDevice, Buzzer
import time
import struct
import socket

# Socket Matlab
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_ip_matlab = "192.168.0.2"
udp_port_matlab = 27000

# Socket Internal
udp_ip_internal = "127.0.0.1"
udp_port_internal = 5000

GPIO_PIN = 20
BZ = Buzzer(16)
sensor = InputDevice(GPIO_PIN)

while True:
	try:
		data = sensor.is_active
		if data:
			BZ.off()
			data_gas = 0
		else:
			BZ.on()
			data_gas = 1

		print(data_gas)
		sock.sendto(struct.pack('?', data_gas), (udp_ip_internal, udp_port_internal))
		sock.sendto(struct.pack('d', data_gas), (udp_ip_matlab, udp_port_matlab))
	except Exception as e:
		data_gas = 0
		continue

	time.sleep(1)