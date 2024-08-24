import pygame
import time
import socket
import struct
import threading
import pigpio
import os

udp_ip = "127.0.0.1"

# DHT11
udp_port_dht11 = 5002
sock_dht11 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_dht11.bind((udp_ip, udp_port_dht11))
sock_dht11.settimeout(5)

# HUSKY
udp_port_husky = 5001
sock_husky = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_husky.bind((udp_ip, udp_port_husky))
sock_husky.settimeout(5)

# MQ2
udp_port_mq2 = 5000
sock_mq2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_mq2.bind((udp_ip, udp_port_mq2))
sock_mq2.settimeout(5)

# PWM
pi = pigpio.pi()
PWM_PIN = 12

PWM_HIJAU = 5
PWM_KUNING = 6
PWM_MERAH = 19

pi.set_mode(PWM_HIJAU, pigpio.OUTPUT)
pi.set_mode(PWM_KUNING, pigpio.OUTPUT)
pi.set_mode(PWM_MERAH, pigpio.OUTPUT)

def turn_on(pin):
    pi.write(pin, 1)

def turn_off(pin):
    pi.write(pin, 0)

# PYGAME
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Sensor Data Display')
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)

# FONT DAN WARNA
font = pygame.font.SysFont('DejaVu Sans Mono', 24, bold=True)
white = (255, 255, 255)
grey = (40, 39, 38)
green = (22, 196, 57)
blue = (22, 41, 196)

# DATA
temperature = None
gas = None
husky = None
pwm_dutycyle = None
pwm_frekuensi = None

def receive_temperature():
    while True:
        try:
            global temperature
            data_temperature, addr = sock_dht11.recvfrom(1024)
            temperature = str(int(struct.unpack('d', data_temperature)[0])) + "°C" 
            if temperature is None:
                continue
        except Exception as e:
            temperature = None
            continue

def receive_husky():
    while True:
        try:
            global husky
            data_husky, addr = sock_husky.recvfrom(1024)
            husky = str(int(struct.unpack('d', data_husky)[0]))
            if husky is None:
                continue
        except Exception as e:
            husky = None
            continue

def receive_gas():
    while True:
        try: 
            global gas
            data_gas, addr = sock_mq2.recvfrom(1024)
            data_gas2 = struct.unpack('?', data_gas)[0]
            if data_gas2:
                gas = "Ada"
            else :
                gas = "Tidak Ada"
        except Exception as e:
            gas = None
            continue

def get_pwm():
    while True:
        try:
            global pwm_dutycyle
            global pwm_frekuensi
            pwm_dutycyle = pi.get_PWM_dutycycle(PWM_PIN)
            pwm_dutycyle = int(pwm_dutycyle/100)

            # LED 
            if pwm_dutycyle <= 30:
                turn_on(PWM_HIJAU)
                turn_off(PWM_KUNING)
                turn_off(PWM_MERAH)
            elif pwm_dutycyle <= 70:
                turn_on(PWM_KUNING)
                turn_off(PWM_HIJAU)
                turn_off(PWM_MERAH)
            else:
                turn_on(PWM_MERAH)
                turn_off(PWM_HIJAU)
                turn_off(PWM_KUNING)

            pwm_dutycyle = str(pwm_dutycyle) + "%"

            pwm_frekuensi = pi.get_PWM_frequency(PWM_PIN)
            pwm_frekuensi = str(pwm_frekuensi) + " Hz"
        except Exception as e:
            pwm_dutycyle = None
            pwm_frekuensi = None
            continue
        time.sleep(1)
    pi.stop()

# THREAD FUNGSI
thread_temp = threading.Thread(target=receive_temperature)
thread_gas = threading.Thread(target=receive_gas)
thread_husky = threading.Thread(target=receive_husky)
thread_pwm = threading.Thread(target=get_pwm)

# MULAI THREAD
thread_temp.start()
thread_gas.start()
thread_husky.start()
thread_pwm.start()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(grey)

    # INPUT
    text_input = font.render("DATA INPUT", True, green)
    screen.blit(text_input, (20, 10))

    # MQ2
    text_mq2 = font.render("ASAP/GAS :", True, white)
    screen.blit(text_mq2, (20, 40))
    value_mq2 = font.render(gas, True, green)
    screen.blit(value_mq2, (170, 40))

    # HUSKY
    text_husky = font.render("JUMLAH ORANG :", True, white)
    screen.blit(text_husky, (20, 70))
    value_husky = font.render(husky, True, green)
    screen.blit(value_husky, (230, 70))

    # DHT11
    text_dht11 = font.render("SUHU :", True, white)
    screen.blit(text_dht11, (20, 100))
    value_dht11 = font.render(temperature, True, green)
    screen.blit(value_dht11, (115, 100))

    # OUTPUT
    text_output = font.render("DATA OUTPUT", True, blue)
    screen.blit(text_output, (20, 150))

    # FREKUENSI
    text_frek = font.render("FREKUENSI : ", True, white)
    screen.blit(text_frek, (20, 180))
    value_frek = font.render(pwm_frekuensi, True, blue)
    screen.blit(value_frek, (185, 180))

    # DUTYCYCLE
    text_duty = font.render("DUTYCYCLE : ", True, white)
    screen.blit(text_duty, (20, 210))
    value_duty = font.render(pwm_dutycyle, True, blue)
    screen.blit(value_duty, (185, 210))

    pygame.display.update()
    time.sleep(1)

pygame.quit()