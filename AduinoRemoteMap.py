import csv
import serial

map_width = 100
map_height = 100

PORT = 'COM5'
BaudRate = 9600

ser = serial.Serial(PORT, BaudRate)

#동작 시작 명령
ser.write(b'StartSequence')
response = ser.readline().decode().rstrip()
print(response)

#데이터 1만 존재하는 기본맵 생성
map_data = [['1'] * map_width for _ in range(map_height)]

#차량의 시작 위치 설정 (x, y)
car_pos = [map_width // 2, map_height // 2]

#벽 제거 - 행
def remove_rows():
    global map_data
    map_data = [row for row in map_data if '0' in row]

#벽 제거 - 열
def remove_columns():
    global map_data
    transposed_map = list(map(list, zip(*map_data)))
    transposed_map = [col for col in transposed_map if '0' in col]
    map_data = list(map(list, zip(*transposed_map)))
           
#차량 이동
def move_car(mapCount, turnDir):
    new_x = car_pos[0]
    new_y = car_pos[1]  
    
    map_data[car_pos[1]][car_pos[0]] = '0'
    
    if turnDir == 1:
        #x가 증가하는 방향으로 맵그림
        new_x = new_x + mapCount #이동 
        map_data[new_y][new_x:car_pos[0]] = ['0'] * (new_x - car_pos[0] + 1)
            
    elif turnDir == 2:
        #y가 감소하는 방향으로 맵그림
        new_y = new_y - mapCount  #이동
        map_data[car_pos[1]:new_y][new_x] = ['0'] * (car_pos[1] - new_y + 1)
    
    elif turnDir == 3:
        #x가 감소하는 방향으로 맵그림
        new_x = new_x - mapCount #이동
        map_data[new_y][car_pos[0]:new_x] = ['0'] * (car_pos[0] - new_x + 1)
            
    else:
        #y가 증가하는 방향으로 맵그림
        new_y = new_y + mapCount  #이동
        map_data[new_y:car_pos[1]][new_x] = ['0'] * (new_y - car_pos[1] + 1)
    
    car_pos[0] = new_x
    car_pos[1] = new_y
        
#맵데이터 제작
while True:
    if ser.in_waiting:
        data = ser.readline().decode().rstrip()
        mapCount, turnDir = map(int, data.split(","))
        move_car(mapCount, turnDir)

        #루프 탎출
        if "SequenceEnd" in data:
            break
    

#벽 제거
remove_rows()
remove_columns()

#맵 데이터 출력
for row in map_data:
    print(' '.join(row))

#CSV 파일로 저장
with open('C:\RaceProject\RC-Algorithm\MapData\map_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for row in map_data:
        writer.writerow(row)

print('맵 데이터가 생성되었습니다')