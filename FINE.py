from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# 데이터베이스에서 데이터를 가져오는 함수
def get_food_data():
    conn = sqlite3.connect('food_db.db')  # SQLite 데이터베이스 연결
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_data")  # food_data 테이블의 모든 데이터 가져오기
    data = cursor.fetchall()
    conn.close()
    return data

# 특정 검색어로 데이터를 필터링하는 함수
def search_food_data(keyword):
    conn = sqlite3.connect('food_db.db')
    cursor = conn.cursor()
    query = "SELECT * FROM food_data WHERE 식품명 LIKE ?"
    cursor.execute(query, (f"%{keyword}%",))
    data = cursor.fetchall()
    conn.close()
    return data

# 메인 페이지
@app.route('/')
def home():
    return render_template('food_web_startpage.html')

# 식사 관리 페이지
@app.route('/siksa')
def siksa():
    menu_data = {
        "breakfast": get_food_data(),
        "lunch": get_food_data(),
        "dinner": get_food_data(),
    }
    return render_template('siksa.html', menu_data=menu_data)

# 아침 메뉴 관리 페이지
@app.route('/breakfast', methods=['GET', 'POST'])
def breakfast():
    food_data = get_food_data()  # 모든 데이터를 가져옴
    error_message = None
    if request.method == 'POST':
        keyword = request.form.get('keyword')  # 검색어 가져오기
        if not keyword:  # 검색어가 없는 경우
            error_message = "검색어를 입력해주세요."
        else:
            food_data = search_food_data(keyword)  # 검색어에 해당하는 데이터 가져오기
            if not food_data:  # 검색 결과가 없는 경우
                error_message = "검색 결과가 없습니다."
    return render_template('breakfast.html', food_data=food_data, error_message=error_message)

# 점심 메뉴 관리 페이지
@app.route('/lunch', methods=['GET', 'POST'])
def lunch():
    food_data = get_food_data()
    error_message = None
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        if not keyword:
            error_message = "검색어를 입력해주세요."
        else:
            food_data = search_food_data(keyword)
            if not food_data:
                error_message = "검색 결과가 없습니다."
    return render_template('lunch.html', food_data=food_data, error_message=error_message)

# 저녁 메뉴 관리 페이지
@app.route('/dinner', methods=['GET', 'POST'])
def dinner():
    food_data = get_food_data()
    error_message = None
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        if not keyword:
            error_message = "검색어를 입력해주세요."
        else:
            food_data = search_food_data(keyword)
            if not food_data:
                error_message = "검색 결과가 없습니다."
    return render_template('dinner.html', food_data=food_data, error_message=error_message)

# 추가 페이지
@app.route('/food_add_todb', methods=['GET', 'POST'])
def food_add_todb():
    if request.method == 'POST':
        # 추가할 데이터를 처리하는 로직 추가
        food_name = request.form.get('food_name')
        calories = request.form.get('calories')
        # 데이터베이스에 삽입
        conn = sqlite3.connect('food_db.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO food_data (식품명, 칼로리) VALUES (?, ?)", (food_name, calories))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('food_add_todb.html')

# 제거 페이지
@app.route('/food_delete_fromdb', methods=['GET', 'POST'])
def food_delete_fromdb():
    if request.method == 'POST':
        # 삭제할 데이터를 처리하는 로직 추가
        food_name = request.form.get('food_name')
        # 데이터베이스에서 삭제
        conn = sqlite3.connect('food_db.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM food_data WHERE 식품명 = ?", (food_name,))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('food_delete_fromdb.html')

if __name__ == '__main__':
    app.run(debug=True)
