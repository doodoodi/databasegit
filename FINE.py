from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# 데이터베이스에서 데이터를 가져오는 함수
def get_food_data():
    conn = sqlite3.connect('food_db.db')
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

#---------------------------------------------------------------------------------------------------------------------------------

# breakfast 테이블에 데이터 추가
def insert_into_breakfast(data):
    conn = sqlite3.connect('food_db.db')
    cursor = conn.cursor()
    query = """
        INSERT INTO breakfast (음식명, 식품코드, 칼로리, 탄수화물, 단백질, 지방, 콜레스테롤, 식이섬유, 나트륨)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, data)
    conn.commit()
    conn.close()

# lunch 테이블에 데이터 추가
def insert_into_lunch(data):
    conn = sqlite3.connect('food_db.db')
    cursor = conn.cursor()
    query = """
        INSERT INTO lunch (음식명, 식품코드, 칼로리, 탄수화물, 단백질, 지방, 콜레스테롤, 식이섬유, 나트륨)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, data)
    conn.commit()
    conn.close()

# dinner 테이블에 데이터 추가
def insert_into_dinner(data):
    conn = sqlite3.connect('food_db.db')
    cursor = conn.cursor()
    query = """
        INSERT INTO dinner (음식명, 식품코드, 칼로리, 탄수화물, 단백질, 지방, 콜레스테롤, 식이섬유, 나트륨)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(query, data)
    conn.commit()
    conn.close()

# ---------------------------------------------------------------------------------------------------------

# 메인 페이지
@app.route('/')
def home():
    return render_template('food_web_startpage.html')

# 식사 관리 페이지
@app.route('/siksa')
def siksa():
    breakfast_data = get_table_data('breakfast')
    lunch_data = get_table_data('lunch')
    dinner_data = get_table_data('dinner')
    return render_template(
        'siksa.html',
        breakfast_data=breakfast_data,
        lunch_data=lunch_data,
        dinner_data=dinner_data,
    )

# 각 테이블 데이터를 가져오는 함수
def get_table_data(table_name):
    conn = sqlite3.connect('food_db.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

# ---------------------------------------------------------------------------------------------------------------------------------

# 아침 메뉴 관리 페이지
@app.route('/breakfast', methods=['GET', 'POST'])
def breakfast():
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
    return render_template('breakfast.html', food_data=food_data, error_message=error_message)

def get_breakfast_data(): #테이블 데이터 표시 해주는 함수
    conn = sqlite3.connect('food_db.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM breakfast")  # breakfast 테이블의 모든 데이터 가져오기
    data = cursor.fetchall()
    conn.close()
    return data

# "추가" 버튼 클릭 시 데이터를 breakfast 테이블에 삽입
@app.route('/add-to-breakfast', methods=['POST'])
def add_to_breakfast():
    try:
        # 클라이언트에서 전송된 JSON 데이터 가져오기
        data = request.json
        # 필요한 데이터를 튜플 형태로 변환
        row_data = (
            data['name'],
            data['code'],
            float(data['calories']),
            float(data['carbs']),
            float(data['protein']),
            float(data['fat']),
            float(data['cholesterol']),
            float(data['fiber']),
            float(data['sodium']),
        )
        # 데이터베이스에 삽입
        insert_into_breakfast(row_data) #데이터를 breakfast 테이블에 추가 
        return jsonify({"message": "Data added to breakfast successfully!"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------------------------------------------------------------------------------------

# 점심 메뉴 관리 페이지
@app.route('/lunch', methods=['GET', 'POST'])
def lunch():
    food_data = get_food_data()
    lunch_data = get_table_data('lunch')  # lunch 테이블 데이터 가져오기
    error_message = None
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        if not keyword:
            error_message = "검색어를 입력해주세요."
        else:
            food_data = search_food_data(keyword)
            if not food_data:
                error_message = "검색 결과가 없습니다."
    return render_template('lunch.html', food_data=food_data, lunch_data=lunch_data, error_message=error_message)

# "추가" 버튼 클릭 시 데이터를 lunch 테이블에 삽입
@app.route('/add-to-lunch', methods=['POST'])
def add_to_lunch():
    try:
        # 클라이언트에서 전송된 JSON 데이터 가져오기
        data = request.json
        # 필요한 데이터를 튜플 형태로 변환
        row_data = (
            data['name'],
            data['code'],
            float(data['calories']),
            float(data['carbs']),
            float(data['protein']),
            float(data['fat']),
            float(data['cholesterol']),
            float(data['fiber']),
            float(data['sodium']),
        )
        # 데이터베이스에 삽입
        insert_into_lunch(row_data)  # 데이터 lunch 테이블에 추가
        return jsonify({"message": "Data added to lunch successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#---------------------------------------------------------------------------------------------------------------------------------

# 저녁 메뉴 관리 페이지
@app.route('/dinner', methods=['GET', 'POST'])
def dinner():
    food_data = get_food_data()
    dinner_data = get_table_data('dinner')  # dinner 테이블 데이터 가져오기
    error_message = None
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        if not keyword:
            error_message = "검색어를 입력해주세요."
        else:
            food_data = search_food_data(keyword)
            if not food_data:
                error_message = "검색 결과가 없습니다."
    return render_template('dinner.html', food_data=food_data, dinner_data=dinner_data, error_message=error_message)

# "추가" 버튼 클릭 시 데이터를 dinner 테이블에 삽입
@app.route('/add-to-dinner', methods=['POST'])
def add_to_dinner():
    try:
        # 클라이언트에서 전송된 JSON 데이터 가져오기
        data = request.json
        # 필요한 데이터를 튜플 형태로 변환
        row_data = (
            data['name'],
            data['code'],
            float(data['calories']),
            float(data['carbs']),
            float(data['protein']),
            float(data['fat']),
            float(data['cholesterol']),
            float(data['fiber']),
            float(data['sodium']),
        )
        # 데이터베이스에 삽입
        insert_into_dinner(row_data)  # 데이터 dinner 테이블에 추가
        return jsonify({"message": "Data added to dinner successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#---------------------------------------------------------------------------------------------------------------------------------

# 추가 페이지
@app.route('/food_add_todb', methods=['GET', 'POST'])
def food_add_todb():
    if request.method == 'POST':
        food_name = request.form.get('food_name')
        food_code = request.form.get('food_code')
        calories = request.form.get('calories')
        carbs = request.form.get('carbs')
        protein = request.form.get('protein')
        fat = request.form.get('fat')
        cholesterol = request.form.get('cholesterol')
        fiber = request.form.get('fiber')
        sodium = request.form.get('sodium')

        conn = sqlite3.connect('food_db.db')
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO food_data (음식명, 식품코드, 칼로리, 탄수화물, 단백질, 지방, 콜레스테롤, 식이섬유, 나트륨)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                       """, (food_name, food_code, calories, carbs, protein, fat, cholesterol, fiber, sodium))
        conn.commit()
        conn.close()
        return redirect(url_for('food_add_todb'))
    return render_template('food_add_todb.html')

# --------------------------------------------------------------------------------------------------------------------------------

# 제거 페이지
@app.route('/food_delete_fromdb', methods=['GET', 'POST'])
def food_delete_fromdb():
    error_message = None
    food_data = get_food_data()
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        if not keyword:
            error_message = "검색어를 입력해주세요."
        else:
            food_data = search_food_data(keyword)
            if not food_data:
                error_message = "검색 결과가 없습니다."

        food_name = request.form.get('food_name')
        food_code = request.form.get('food_code')
        if food_name:
            conn = sqlite3.connect('food_db.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM food_data WHERE 음식명 = ? and 식품코드 = ?", (food_name, food_code))
            conn.commit()
            conn.close()
            return redirect(url_for('food_delete_fromdb'))

    return render_template('food_delete_fromdb.html', food_data=food_data, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
