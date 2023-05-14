import os
import random
import numpy as np
import csv

def resize_course(course, map_n, map_m):
    #코스 데이터 크기를 맵 데이터와 동일하게 변경
    n, m = len(course), len(course[0])
    x_val = np.linspace(0, n-1, map_n, dtype=int)
    y_val = np.linspace(0, m-1, map_m, dtype=int)

    new_course = np.zeros((map_n, map_m))
    for i in range(map_n):
        for j in range(map_m):
            new_course[i][j] = course[x_val[i]][y_val[j]]
            
    for row in range(len(new_course)):
        for col in range(len(new_course[0])):
            value = new_course[row][col]
            if value != 0:
                for i in range(row, len(new_course)):
                    for j in range(col, len(new_course[0])):
                        if new_course[i][j] == value and (i != row or j != col):
                            new_course[i][j] = 0

    return new_course

def check_course(map_data, course_data):
    #각 코너의 위치를 positions에 저장
    positions = []
    for i in range(1, 101):
        found = False
        for y, row in enumerate(course_data):
            for x, value in enumerate(row):
                if value == i:
                    positions.append((x+1, y+1))
                    found = True
                    break
            if found:
                break
        if not found:
            break
    
    #각 코너 사이에 장애물이 있는지 확인    
    for i in range(1, len(positions)-1):
        current_pos = positions[i]
        next_pos = positions[i+1]
        if check_walls(map_data, current_pos, next_pos):
            return False #장애물이 있다면 False 반환
    return True #장애물이 없다면 True 반환



def check_walls(map, current_pos, next_pos):
    #현재 위치와 다음 위치의 좌표
    x1, y1 = current_pos
    x2, y2 = next_pos
    
    
    #각 좌표간의 차이
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
        
    #이동방향 결정
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
        courseway2 = courseway * 2
        if courseway2 > dy:
            courseway -= dy
            x1 += x_step
        if courseway2 < dx:
            courseway += dx
            y1 += y_step
            
        if map[y1][x1] == 1:
            return True #장애물이 있다면 while문 종료
            
    return False #장애물이 없다면 반복

def assign_course(map_data, course_data_list):
    #적합한 코스 저장할 리스트 생성
    matched_courses = []

    #코스 데이터와 맵 데이터 비교
    for course_data in course_data_list:
        course = course_data[1]
        is_matched = check_course(map_data, course)
        if is_matched:
            matched_courses.append(course_data)

    #적합한 코스 중 랜덤으로 선택
    if matched_courses:
        matched_course_data = random.choice(matched_courses)
        return matched_course_data
    else:
        return None



def main():
    #맵데이터 가져오기
    map_data = np.loadtxt('C:\RaceProject\RC-Algorithm\MapData\map_data.csv', delimiter=',')
    n, m = map_data.shape
        
    #코스데이터 가져오기
    course_data_list = []
    for file_name in os.listdir('C:\RaceProject\RC-Algorithm\CourseData'):
        if file_name.endswith('.csv'):
            with open(os.path.join('C:\RaceProject\RC-Algorithm\CourseData', file_name), 'r') as csvfile:
                course_data = list(csv.reader(csvfile))
                course_data = list(map(tuple, [map(int, row) for row in course_data]))
                course_data = resize_course(course_data, n, m)
                course_data_list.append((file_name, course_data))
                
    matched_course_data = assign_course(map_data, course_data_list)

    if matched_course_data:
        print("다음 코스가 적합합니다:")
        print(matched_course_data)
    else:
        print("적합한 코스가 없습니다")

if __name__ == '__main__':
    main()