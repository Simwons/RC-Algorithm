import csv
import sys
import serial

PORT = 'COM5'
BaudRate = 9600

ser = serial.Serial(PORT, BaudRate)


while True:
    command = input('차량 동작 (wasd or k): ')
    if (command == "k"):
        print("동작 종료")
        exit()
    ser.write(command.encode())
    
    
    

