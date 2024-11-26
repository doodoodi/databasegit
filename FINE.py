from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# 데이터베이스에서 데이터를 가져오는 함수
def get_food_data():
    conn = sqlite3.connect('food_db.db')  # SQLite 데이터베이스 연결ㄴ
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_data")  # food_data 테이블의 모든 데이터 가져오기
    data = cursor.fetchall()
    conn.close()
    return data

# 특정 검색어로 데이터를 필터링하는 함수
def search_food_data(keyword):
    conn = sqlite3.connect('food_db.db')
    cursor = conn.cursor()
    query = "SELECT * FROM food_data WHERE 음식명 LIKE ?"
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
        # 폼에서 전달된 데이터 가져오기
        food_name = request.form.get('food_name')
        food_code = request.form.get('food_code')
        calories = request.form.get('calories')
        carbs = request.form.get('carbs')
        protein = request.form.get('protein')
        fat = request.form.get('fat')
        cholesterol = request.form.get('cholesterol')
        fiber = request.form.get('fiber')
        sodium = request.form.get('sodium')

        # 데이터베이스에 저장
        conn = sqlite3.connect('food_db.db')
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO food_data (음식명, 칼로리, 탄수화물, 단백질, 지방, 콜레스테롤, 식이섬유, 나트륨)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                       """, (food_name, calories, carbs, protein, fat, cholesterol, fiber, sodium))
        conn.commit()  # 변경사항 저장
        conn.close()   # 닫기

        return redirect(url_for('food_add_todb'))  # 삭제 후 페이지 리로드

    # POST 요청이 아닌 경우에는 이 부분이 실행
    return render_template('food_add_todb.html')



# 제거 페이지
@app.route('/food_delete_fromdb', methods=['GET', 'POST'])
def food_delete_fromdb():
    error_message = None
    food_data = get_food_data()  # 기본 데이터 표시
    
    # 검색 및 검색 결과 없을 때 조건 처리
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        if not keyword:
            error_message = "검색어를 입력해주세요."
        else:
            food_data = search_food_data(keyword)
            if not food_data:
                error_message = "검색 결과가 없습니다."
        
        # 삭제 요청 처리
        food_name = request.form.get('food_name')
        food_code = request.form.get('food_code')
        if food_name:  # 삭제 동작 처리
            conn = sqlite3.connect('food_db.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM food_data WHERE 음식명 = ? and 식품코드 = ?", (food_name, food_code))
            conn.commit()
            conn.close()
            return redirect(url_for('food_delete_fromdb'))  # 삭제 후 페이지 리로드

    return render_template('food_delete_fromdb.html', food_data=food_data, error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)