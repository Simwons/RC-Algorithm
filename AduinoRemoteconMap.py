import csv
import serial

map_width = 100
map_height = 100

PORT = 'COM5'
BaudRate = 9600

ser = serial.Serial(PORT, BaudRate)


while True:
    command = input('차량 동작 (wasd or k): ')
    ser.write(command.encode())
    
    
    

