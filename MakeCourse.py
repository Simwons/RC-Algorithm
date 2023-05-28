import csv
import os

#코스데이터
course_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 0, 0, 3, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 6, 0, 0, 0, 0, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

def save_course_data(course_data):
    #중복된 숫자 체크
    numbers = set()
    duplicates = set()
    for i in range(len(course_data)):
        for j in range(len(course_data[i])):
            if course_data[i][j] != 0:
                if course_data[i][j] in numbers:
                    duplicates.add((course_data[i][j], (i, j)))
                else:
                    numbers.add(course_data[i][j])
    
    #중복된 숫자가 있으면 경고 메시지 출력
    if duplicates:
        print('코스데이터에 중복된 값이 있습니다.')
        for number, position in duplicates:
            print('숫자 {}가 다음의 위치에 중복됩니다. {}'.format(number, position))
        print('코스데이터가 저장되지 않았습니다.')
        return
    
    #저장 경로 및 파일 이름 지정
    save_path = 'C:\RaceProject\RC-Algorithm\CourseData'
    course_data_files = os.listdir(save_path)
    if len(course_data_files) == 0:
        new_file_num = 1
    else:
        new_file_num = len(course_data_files) + 1
    new_file_name = 'CourseData{}.csv'.format(new_file_num)
    save_file_path = os.path.join(save_path, new_file_name)
        
    #CSV 파일 저장
    with open(save_file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in course_data:
            writer.writerow(row)
            
    print('새로운 코스데이터가 저장되었습니다:', new_file_name)

save_course_data(course_data)