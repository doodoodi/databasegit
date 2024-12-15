from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
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

# 음식명과 칼로리 제한으로 데이터를 필터링하는 함수
def search_foods(keyword=None, calorie_limit=None):
    conn = sqlite3.connect('food_db.db')
    cursor = conn.cursor()
    
    query = "SELECT * FROM food_data WHERE 1=1"
    params = []
    
    if keyword:  # 음식명 조건 추가
        query += " AND 음식명 LIKE ?"
        params.append(f"%{keyword}%")
    
    if calorie_limit is not None:  # 칼로리 제한 조건 추가
        query += " AND 칼로리 <= ?"
        params.append(calorie_limit)
    
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data

# 음식명과 칼로리 제한으로 데이터를 검색하는 API
@app.route('/search-foods', methods=['GET'])
def search_foods_api():
    try:
        # 클라이언트 요청에서 keyword와 calorieLimit 가져오기
        keyword = request.args.get('keyword', '').strip()
        calorie_limit = request.args.get('calorieLimit', type=float)

        # 검색 함수 호출
        results = search_foods(keyword, calorie_limit)

        # JSON 응답 데이터 생성
        data = [
            {
                'name': row[0],
                'code': row[1],
                'calories': row[2],
                'carbs': row[3],
                'protein': row[4],
                'fat': row[5],
                'cholesterol': row[6],
                'fiber': row[7],
                'sodium': row[8],
            }
            for row in results
        ]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


#----------------------------------------------------------------------------------------------------------------------------------
# 자동으로 데이터를 최신화하는 함수
def auto_update_table(table_name):
    try:
        conn = sqlite3.connect('food_db.db')
        cursor = conn.cursor()

        # 최신 food_db 테이블과 비교하여 업데이트
        query = f"""
            UPDATE {table_name}
            SET 칼로리 = (SELECT 칼로리 FROM food_data WHERE food_data.음식명 = {table_name}.음식명),
                탄수화물 = (SELECT 탄수화물 FROM food_data WHERE food_data.음식명 = {table_name}.음식명),
                단백질 = (SELECT 단백질 FROM food_data WHERE food_data.음식명 = {table_name}.음식명),
                지방 = (SELECT 지방 FROM food_data WHERE food_data.음식명 = {table_name}.음식명),
                콜레스테롤 = (SELECT 콜레스테롤 FROM food_data WHERE food_data.음식명 = {table_name}.음식명),
                식이섬유 = (SELECT 식이섬유 FROM food_data WHERE food_data.음식명 = {table_name}.음식명),
                나트륨 = (SELECT 나트륨 FROM food_data WHERE food_data.음식명 = {table_name}.음식명)
            WHERE EXISTS (
                SELECT 1 FROM food_data 
                WHERE food_data.음식명 = {table_name}.음식명 
                AND (
                    food_data.칼로리 != {table_name}.칼로리 OR
                    food_data.탄수화물 != {table_name}.탄수화물 OR
                    food_data.단백질 != {table_name}.단백질 OR
                    food_data.지방 != {table_name}.지방 OR
                    food_data.콜레스테롤 != {table_name}.콜레스테롤 OR
                    food_data.식이섬유 != {table_name}.식이섬유 OR
                    food_data.나트륨 != {table_name}.나트륨
                )
            )
        """
        cursor.execute(query)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error updating table {table_name}: {e}")


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
    # 아침, 점심, 저녁 테이블을 최신화
    auto_update_table('breakfast')
    auto_update_table('lunch')
    auto_update_table('dinner')

    # 최신화된 데이터를 가져오기
    breakfast_data = get_table_data('breakfast')
    lunch_data = get_table_data('lunch')
    dinner_data = get_table_data('dinner')

    # 최신화된 데이터를 템플릿에 전달
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

# 아침 메뉴 관리 페이지 (음식명 & 칼로리 검색)
@app.route('/breakfast', methods=['GET', 'POST'])
def breakfast():
    food_data = get_food_data()  # 기본 데이터 로드
    error_message = None

    if request.method == 'POST':
        # 클라이언트에서 요청받은 데이터
        keyword = request.form.get('keyword', '').strip()
        calorie_limit = request.form.get('calorieLimit', type=float)

        if not keyword and calorie_limit is None:  # 조건이 없을 경우
            error_message = "검색 조건을 입력해주세요."
        else:
            # 음식명과 칼로리 제한으로 검색
            food_data = search_foods(keyword, calorie_limit)
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

# 점심 메뉴 관리 페이지 (음식명 & 칼로리)
@app.route('/lunch', methods=['GET', 'POST'])
def lunch():
    food_data = get_food_data()
    lunch_data = get_table_data('lunch')  # lunch 테이블 데이터 가져오기
    error_message = None

    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip()
        calorie_limit = request.form.get('calorieLimit', type=float)

        if not keyword and calorie_limit is None:
            error_message = "검색 조건을 입력해주세요."
        else:
            food_data = search_foods(keyword, calorie_limit)
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

# 저녁 메뉴 관리 페이지 (음식명 & 칼로리)
@app.route('/dinner', methods=['GET', 'POST'])
def dinner():
    food_data = get_food_data()
    dinner_data = get_table_data('dinner')  # dinner 테이블 데이터 가져오기
    error_message = None

    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip()
        calorie_limit = request.form.get('calorieLimit', type=float)

        if not keyword and calorie_limit is None:
            error_message = "검색 조건을 입력해주세요."
        else:
            food_data = search_foods(keyword, calorie_limit)
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
        # 빈 데이터일 경우 0으로 대체
        food_name = request.form.get('food_name')
        calories = float(request.form.get('calories') or 0)
        carbs = float(request.form.get('carbs') or 0)
        protein = float(request.form.get('protein') or 0)
        fat = float(request.form.get('fat') or 0)
        cholesterol = float(request.form.get('cholesterol') or 0)
        fiber = float(request.form.get('fiber') or 0)
        sodium = float(request.form.get('sodium') or 0)

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