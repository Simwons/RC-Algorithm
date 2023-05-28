import csv

map_width = 100
map_height = 100

def_front = 180

#데이터 1만 존재하는 기본맵 생성
map_data = [['1'] * map_width for _ in range(map_height)]

#차량의 시작 위치 설정 (x, y)
car_pos = [map_width // 2, map_height // 2]

#장애물 인식
def detect_wall():
    if map_data[car_pos[1]][car_pos[0]] == '1':
        return True
    else:
        return False
    
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
def move_car():    
    global def_front
    car_front = None
    
    turn_R = False
    turn_L = False
    
    map_data[car_pos[1]][car_pos[0]] = '0'
    
    #차량 방향 변경
    if turn_R:
        if def_front == 0:
            def_front = 360
        car_front = def_front - 90        
        def_front = car_front
    if turn_L:
        if def_front == 360:
            def_front = 0
        car_front = def_front + 90
        def_front = car_front
    
    #차량 방향에 따른 이동
    if car_front == 180:
        new_x = car_pos[0] + 1
    if car_front == 270:
        new_y = car_pos[1] + 1
    if car_front == 90:
        new_y = car_pos[1] - 1
    if car_front == 360 or 0:
        new_x = car_pos[0] - 1
        
    car_pos[0] = new_x
    car_pos[1] = new_y

#맵데이터 제작
for _ in range(10000):
    move_car()

    if detect_wall():
        map_data[car_pos[1]][car_pos[0]] = '1'

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