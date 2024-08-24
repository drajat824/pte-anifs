import time
import struct
import socket
from huskylib import HuskyLensLibrary

# Socket Matlab
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_ip_matlab = "192.168.0.2"
udp_port_matlab = 27001

# Socket Internal
udp_ip_internal = "127.0.0.1"
udp_port_internal = 5001

def setup_husky():
    huskyLens = HuskyLensLibrary("SERIAL", "/dev/serial/by-id/usb-Silicon_Labs_CP2102N_USB_to_UART_Bridge_Controller_160c5e9a0d0bee11bbb44302f59e3369-if00-port0")
    huskyLens.algorthim("ALGORITHM_OBJECT_RECOGNITION")
    return huskyLens

while True:
    try:
        change_label = huskyLens.setCustomName("Orang Terdeteksi", 1)
        detected_person = huskyLens.getBlocksByID(1)
        data_husky = len(detected_person)

        sock.sendto(struct.pack('d', data_husky), (udp_ip_internal, udp_port_internal))
        sock.sendto(struct.pack('d', data_husky), (udp_ip_matlab, udp_port_matlab))

    except Exception as e:
        try:
            huskyLens = setup_husky()
        except Exception as e_setup:
            continue
        time.sleep(2)
        continue

    time.sleep(1)