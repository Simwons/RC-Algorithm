import os
import csv

def resize_map(map, new_n, new_m):
    n, m = len(map), len(map[0])
    #new_map에 추가할 값 위치 저장
    x_val = [int(i*n/new_n) for i in range(new_n)]
    y_val = [int(j*m/new_m) for j in range(new_m)]
    
    new_map = [[0] * new_m for _ in range(new_n)]
    
    for i in range(new_n):
        for j in range(new_m):
            new_map[i][j] = map[x_val[i]][y_val[j]]
    
    return new_map

def check_course(map, course):
    #코스 데이터의 첫번째 위치 설정
    current_pos = tuple(course[0][:2])
    
    #순서대로 장애물이 있는지 확인
    for next_pos in course[1:]:
        #현재 위치와 다음 위치 사이 확인
        if check_walls(map, current_pos, tuple(next_pos[:2])):
            return False #장애물이 있으면 False
        #현재 위치를 갱신
        current_pos = tuple(next_pos[:2])
        
    return True #전체확인후 장애물이 없다면 True

def check_walls(map, current_pos, next_pos):
    # 현재 위치와 다음 위치의 좌표
    x1, y1 = current_pos
    x2, y2 = next_pos
    
    #각 좌표간의 차이
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    # 이동방향 결정
    if x1 < x2:
        x_step = 1  #x축 상에서 +1
    else:
        x_step = -1 #x축 상에서 -1
    if y1 < y2:
        y_step = 1  #y축 상에서 +1
    else:
        y_step = -1 #y축 상에서 -1
        
    #브레젠험 알고리즘 사용해 코스확인
    courseway = dx - dy
    while x1 != x2 or y1 != y2:
        if map[y1][x1] == 1:
            return True #장애물이 있다면 while문 종료
        courseway2 = courseway * 2
        if courseway2 > -dy:
            courseway -= dy
            x1 += x_step
        if courseway2 < dx:
            courseway += dx
            y1 += y_step
    return False #장애물이 없다면 반복

def assign_course_to_map(map, course_list):
    matched_course_data = None  #적합한 코스가 없을 경우 반환할 값
    
    for i, (file_name, course_data) in enumerate(course_list, start=1):
        if check_course(map, course_data):
            for j, pos in enumerate(course_data):
                x, y = pos[:2]
                map[int(y)][int(x)] = j + i * 10
            matched_course_data = (file_name, course_data)  #적합한 코스가 발견되면 저장
            break # 첫 번째로 매칭된 코스 데이터 반환 후 종료
            
    return matched_course_data  #모든 코스 확인후 반환


def main():
    #맵데이터 가져오기
    map_data = []
    with open('C:\RaceProject\RC-Algorithm\MapData\map_data.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            map_data.append([int(cell) for cell in row])
    
    new_map_data = resize_map(map_data, 10, 10)
    print("10x10으로 변경된 맵데이터 :")
    for row in new_map_data:
        print(row)
        
    #코스데이터 가져오기
    course_data_list = []
    for file_name in os.listdir('C:\RaceProject\RC-Algorithm\CourseData'):
        if file_name.endswith('.csv'):
            with open(os.path.join('C:\RaceProject\RC-Algorithm\CourseData', file_name), 'r') as csvfile:
                course_data = list(csv.reader(csvfile))
                course_data = list(map(tuple, [map(int, row) for row in course_data]))
                course_data_list.append((file_name, course_data))
                
    matched_course_data = assign_course_to_map(new_map_data, course_data_list)

    if matched_course_data:
        print("다음 코스가 적합합니다:", matched_course_data[0])
    else:
        print("적합한 코스가 없습니다")

if __name__ == '__main__':
    main()