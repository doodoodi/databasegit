from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 초기 메뉴 데이터
menu_data = {
    "breakfast": ["두부", "닭가슴살", "무김치"],
    "lunch": [],
    "dinner": []
}

# 메인 경로에서 food_web_startpage.html 렌더링
@app.route('/')
def home():
    return render_template('food_web_startpage.html')

# siksa.html에서 메뉴 데이터 렌더링
@app.route('/siksa')
def siksa():
    return render_template('siksa.html', menu_data=menu_data)

# /add_menu 경로로 데이터 추가 요청 처리
@app.route('/add_menu', methods=['POST'])
def add_menu():
    meal_type = request.form.get('meal_type')  # "breakfast", "lunch", or "dinner"
    menu_item = request.form.get('menu_item')  # 메뉴 이름
    if meal_type and menu_item:
        menu_data[meal_type].append(menu_item)  # 해당 식사에 메뉴 추가
    return redirect(url_for('siksa'))  # 변경된 데이터를 보여주는 siksa.html로 리다이렉트

# 개별 메뉴 관리 페이지
@app.route('/breakfast')
def breakfast():
    return render_template('breakfast.html', meal_type="breakfast")

@app.route('/lunch')
def lunch():
    return render_template('lunch.html', meal_type="lunch")

@app.route('/dinner')
def dinner():
    return render_template('dinner.html', meal_type="dinner")


if __name__ == '__main__':
    app.run(debug=True)
