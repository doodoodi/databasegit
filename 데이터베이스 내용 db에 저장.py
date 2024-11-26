import sqlite3
import csv

# 데이터베이스 연결
conn = sqlite3.connect('C:/Users/user/Desktop/food_db.db')
cursor = conn.cursor()

# 테이블 생성 (식품코드를 자동 증가로 설정)
cursor.execute('''
CREATE TABLE IF NOT EXISTS food_data (
    음식명 TEXT,
    식품코드 INTEGER PRIMARY KEY AUTOINCREMENT,
    칼로리 REAL,
    탄수화물 REAL,
    단백질 REAL,
    지방 REAL,
    콜레스트롤 REAL,
    식이섬유 REAL,
    나트륨 REAL
);
''')

# CSV 파일 열기
with open('C:/Users/user/Desktop/database/databasegit/food_data.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # 헤더 건너뛰기

    # 각 행을 데이터베이스에 삽입
    for row in reader:
        cursor.execute('''
        INSERT INTO food_data (음식명, 칼로리, 탄수화물, 단백질, 지방, 콜레스트롤, 식이섬유, 나트륨)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))  # row[0]부터 row[8]까지 사용 (식품코드는 자동 증가)


# 변경사항 저장하고 연결 종료
conn.commit()
conn.close()