import csv
import serial

map_width = 100
map_height = 100

onMaking = 1

PORT = 'COM4'
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
def move_car(mapCount, turnDir, seqCount, onMaking, nowSeq):
    new_x = car_pos[0]
    new_y = car_pos[1]  
    
    map_data[car_pos[1]][car_pos[0]] = '0'
    
    if nowSeq == seqCount:
        if turnDir == 0:
            #수평으로 직진하여 맵그림
            new_x = new_x - mapCount #이동 
            map_data[new_y][new_x:car_pos[0] + 1] = ['0'] * (car_pos[0] - new_x + 1)  #수평맵 업데이트
            new_y = new_y + 1
    
        else:
            #수평으로 직진하여 맵 그림
            new_x = new_x + mapCount  #이동
            map_data[new_y][car_pos[0]:new_x + 1] = ['0'] * (new_x - car_pos[0] + 1)  #수평맵 업데이트
            new_y = new_y - 1
    
    else:
        new_y = new_y - mapCount #이동
        map_data[new_y:car_pos[1]][new_x] = ['0'] * (car_pos[0] - new_y + 1) #수직맵 업데이트
        nowSeq = seqCount
    
    car_pos[0] = new_x
    car_pos[1] = new_y
        
    if nowSeq == 2:
        onMaking = 0
    
    return onMaking, nowSeq
        
#맵데이터 제작
while (onMaking):
    if ser.in_waiting:
        data = ser.readline().decode().rstrip()
        mapCount, turnDir, seqCount = map(int, data.split(","))
        onMaking = move_car(mapCount, turnDir, seqCount, onMaking)

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