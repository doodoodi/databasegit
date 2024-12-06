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

# 최대 칼로리를 기준으로 음식을 검색하는 함수
@app.route('/max_calories_search', methods=['GET'])
def max_calories_search():
    max_calories = request.args.get('calories')  # 입력된 최대 칼로리 값 가져오기
    if not max_calories:
        return jsonify({"error": "No calorie value provided"}), 400

    try:
        # 데이터베이스 연결
        conn = sqlite3.connect('food_db.db')
        cursor = conn.cursor()

        # 최대 칼로리 이하의 음식 검색
        query = """
            SELECT 음식명, 칼로리, 탄수화물, 단백질, 지방
            FROM food_data
            WHERE 칼로리 <= ?
        """
        cursor.execute(query, (max_calories,))
        foods = cursor.fetchall()
        conn.close()

        # JSON으로 결과 반환
        return jsonify([
            {
                "name": food[0],
                "calories": food[1],
                "carbs": food[2],
                "protein": food[3],
                "fat": food[4]
            }
            for food in foods
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------------------------------------------------------------------------------------------------------------------------
# 테이블 초기화 함수
def clear_table(table_name):
    try:
        conn = sqlite3.connect('food_db.db')
        cursor = conn.cursor()
        query = f"DELETE FROM {table_name}"  # 테이블의 모든 데이터 삭제
        cursor.execute(query)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error clearing table {table_name}: {e}")
        return False

# 아침 테이블 초기화
@app.route('/reset_breakfast', methods=['POST'])
def reset_breakfast():
    if clear_table('breakfast'):
        return jsonify({"message": "Breakfast table cleared successfully!"}), 200
    else:
        return jsonify({"error": "Failed to clear breakfast table."}), 500

# 점심 테이블 초기화
@app.route('/reset_lunch', methods=['POST'])
def reset_lunch():
    if clear_table('lunch'):
        return jsonify({"message": "Lunch table cleared successfully!"}), 200
    else:
        return jsonify({"error": "Failed to clear lunch table."}), 500

# 저녁 테이블 초기화
@app.route('/reset_dinner', methods=['POST'])
def reset_dinner():
    if clear_table('dinner'):
        return jsonify({"message": "Dinner table cleared successfully!"}), 200
    else:
        return jsonify({"error": "Failed to clear dinner table."}), 500

#---------------------------------------------------------------------------------------------------------------------------------

# 아침 메뉴 칼로리, 탄수화물, 단백질, 지방 총합 계산
@app.route('/breakfast_totals', methods=['GET'])
def get_breakfast_totals():
    try:
        conn = sqlite3.connect('food_db.db')
        cursor = conn.cursor()
        query = """
        SELECT 
            SUM(칼로리) as total_calories, 
            SUM(탄수화물) as total_carbs, 
            SUM(단백질) as total_protein, 
            SUM(지방) as total_fat 
        FROM breakfast
        """
        cursor.execute(query)
        totals = cursor.fetchone()
        conn.close()
        return jsonify({
            "total_calories": totals[0] or 0,
            "total_carbs": totals[1] or 0,
            "total_protein": totals[2] or 0,
            "total_fat": totals[3] or 0
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 점심 메뉴 칼로리, 탄수화물, 단백질, 지방 총합 계산
@app.route('/lunch_totals', methods=['GET'])
def get_lunch_totals():
    try:
        conn = sqlite3.connect('food_db.db')
        cursor = conn.cursor()
        query = """
        SELECT 
            SUM(칼로리) as total_calories, 
            SUM(탄수화물) as total_carbs, 
            SUM(단백질) as total_protein, 
            SUM(지방) as total_fat 
        FROM lunch
        """
        cursor.execute(query)
        totals = cursor.fetchone()
        conn.close()
        return jsonify({
            "total_calories": totals[0] or 0,
            "total_carbs": totals[1] or 0,
            "total_protein": totals[2] or 0,
            "total_fat": totals[3] or 0
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#저녁 메뉴 칼로리, 탄수화물, 단백질, 지방 총합 계산
@app.route('/dinner_totals', methods=['GET'])
def get_dinner_totals():
    try:
        conn = sqlite3.connect('food_db.db')
        cursor = conn.cursor()
        query = """
        SELECT 
            SUM(칼로리) as total_calories, 
            SUM(탄수화물) as total_carbs, 
            SUM(단백질) as total_protein, 
            SUM(지방) as total_fat 
        FROM dinner
        """
        cursor.execute(query)
        totals = cursor.fetchone()
        conn.close()
        return jsonify({
            "total_calories": totals[0] or 0,
            "total_carbs": totals[1] or 0,
            "total_protein": totals[2] or 0,
            "total_fat": totals[3] or 0
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
        food_name_d = request.form.get('food_name_d')
        food_code_d = request.form.get('food_code_d')
        if food_name_d:  # 삭제 동작 처리
            conn = sqlite3.connect('food_db.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM food_data WHERE 음식명 = ? and 식품코드 = ?", (food_name_d, food_code_d))
            conn.commit()
            conn.close()
            return redirect(url_for('food_delete_fromdb'))  # 삭제 후 페이지 리로드
        
        # 업데이트 요청 처리
        food_name = request.form.get('food_name')
        food_code = request.form.get('food_code')
        calories = request.form.get('calories')
        carbs = request.form.get('carbs')
        protein = request.form.get('protein')
        fat = request.form.get('fat')
        cholesterol = request.form.get('cholesterol')
        fiber = request.form.get('fiber')
        sodium = request.form.get('sodium')
        if food_name or calories or carbs or protein or fat or cholesterol or fiber or sodium:
            conn = sqlite3.connect('food_db.db')
            cursor = conn.cursor()
            cursor.execute('''
                            UPDATE food_data
                            SET 음식명 = ?, 칼로리 = ?, 탄수화물 = ?, 단백질 = ?, 지방 = ?, 콜레스테롤 = ?, 식이섬유 = ?, 나트륨 = ?
                            WHERE 식품코드 = ?
                            ''', (food_name, calories, carbs, protein, fat, cholesterol, fiber, sodium, food_code))
            conn.commit()
            conn.close()           
        
            return redirect(url_for('food_delete_fromdb'))  # 삭제 후 페이지 리로드

    return render_template('food_delete_fromdb.html', food_data=food_data, error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)