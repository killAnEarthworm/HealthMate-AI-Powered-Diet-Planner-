import random
from datetime import datetime
from _decimal import Decimal
from flask import Blueprint, render_template, redirect, url_for, request, session, flash, jsonify
from models import User
from flask_mail import Message
from database import db
from models import FoodNutritionInfo, FoodCategory
from unicodedata import decimal

nutrition_storage_login_bp = Blueprint('nutrition_storage_login', __name__, template_folder='../templates')


@nutrition_storage_login_bp.route('/calculate', methods=['GET', 'POST'])
def calculate():
    data = request.form  # 获取表单数据
    food_name = data.get('food_name')  # 获取食品名称
    quantity2 = data.get('quantity2')  # 获取数量

    print(f"Received food_name: {food_name}, quantity: {quantity2}")  # Debug output

    # 校验数量
    try:
        quantity2 = Decimal(quantity2)  # 转换为 Decimal
    except (ValueError, TypeError):
        return jsonify({"error": "无效的数量格式"}), 400

    # 查询数据库中的食物数据
    food = FoodNutritionInfo.query.filter_by(name=food_name).first()

    # 校验食品名称和数量
    if not food_name or quantity2 <= 0:
        return jsonify({"error": "食物名称或数量不能为空且数量必须大于0"}), 400

    if not food:
        return jsonify({"error": "食物未找到"}), 404

    # 计算每项营养成分按比例的值
    # nutrient_value为每100g食品所含的营养成分
    def calculate_value(nutrient_value, quantity2):
        nutrient_value = Decimal(nutrient_value)
        return (nutrient_value * quantity2) / 100

    nutrition_result = {
        "kcal": calculate_value(food.kcal, quantity2),
        "protein": calculate_value(food.protein, quantity2),
        "fat": calculate_value(food.fat, quantity2),
        "carbohydrates": calculate_value(food.carbohydrates, quantity2),
        "dietary_fiber": calculate_value(food.dietary_fiber, quantity2),
        "carotene": calculate_value(food.carotene, quantity2),
        "retinol": calculate_value(food.retinol, quantity2),
        "vitamin_b1": calculate_value(food.vitamin_b1, quantity2),
        "vitamin_b2": calculate_value(food.vitamin_b2, quantity2),
        "niacin": calculate_value(food.niacin, quantity2),
        "vitamin_c": calculate_value(food.vitamin_c, quantity2),
        "vitamin_e": calculate_value(food.vitamin_e, quantity2),
        "vitamin_a": calculate_value(food.vitamin_a, quantity2),
        "cholesterol": calculate_value(food.cholesterol, quantity2),
        "potassium": calculate_value(food.potassium, quantity2),
        "sodium": calculate_value(food.sodium, quantity2),
        "magnesium": calculate_value(food.magnesium, quantity2),
        "iron": calculate_value(food.iron, quantity2),
        "manganese": calculate_value(food.manganese, quantity2),
        "zinc": calculate_value(food.zinc, quantity2),
        "copper": calculate_value(food.copper, quantity2),
        "phosphorus": calculate_value(food.phosphorus, quantity2),
        "selenium": calculate_value(food.selenium, quantity2),


        # 添加其他所需的营养成分计算
    }

    return jsonify(nutrition_result)


@nutrition_storage_login_bp.route('/nutrition_storage/foods/<category_id>', methods=['GET', 'POST'])
def get_foods(category_id):
    foods = FoodNutritionInfo.query.filter_by(category_id=category_id).all()
    print(f'Category ID: {category_id}, Foods: {foods}')

    food_list = [{'id': food.food_id, 'name': food.name} for food in foods]
    print(food_list)
    return jsonify(food_list)


@nutrition_storage_login_bp.route('/nutrition_storage', methods=['GET', 'POST'])
def nutrition_storage():
    categories = FoodCategory.query.all()  # 获取所有食品种类
    return render_template('nutrition_storage/nutrition_storage.html', categories=categories)  # 使用完整的端点名称


@nutrition_storage_login_bp.route('/', methods=['GET', 'POST'])
def login():
    login_failed = False
    if request.method == 'POST':
        # 获取表单数据
        email = request.form['email']
        passwd = request.form['passwd']

        user = User.query.filter_by(email=email).first()

        if user and user.passwd == passwd:
            # 如果用户存在且密码匹配，将用户信息存入 session 并重定向到首页
            session['user_id'] = user.user_id
            flash('登录成功', 'success')
            return redirect(url_for('data_board_personal_center.data_board'))  # 跳转到主页
        else:
            # 匹配失败，显示错误信息并重定向回登录页面
            login_failed = True  # 登录失败标志

    return render_template('login/login.html', login_failed=login_failed)


@nutrition_storage_login_bp.route('/logout')
def logout():
    return redirect(url_for('nutrition_storage_login.login'))  # 使用完整的端点名称


@nutrition_storage_login_bp.route('/enroll', methods=['GET', 'POST'])
def enroll():
    if request.method == 'POST':
        email = request.form['email']
        passwd = request.form['passwd']
        captcha = request.form.get('captcha')  # 获取用户输入的验证码

        # 检查邮箱是否已存在
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("该邮箱已注册", "error")
            return redirect(url_for('nutrition_storage_login.enroll'))

        # 验证验证码是否正确
        saved_captcha = session.get('captcha')  # 获取之前生成的验证码
        if saved_captcha is None or saved_captcha != captcha:
            flash("验证码错误", "error")
            return redirect(url_for('nutrition_storage_login.enroll'))

        # 邮箱不存在且验证码正确，保存用户信息到数据库
        new_user = User(
            email=email,
            passwd=passwd,
            username=email,
            gender="other",
            date_of_birth=datetime(2000, 1, 1),
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            print(f"用户 {email} 保存成功")
            flash("注册成功，请登录！", "success")
            return redirect(url_for('nutrition_storage_login.login'))
        except Exception as e:
            db.session.rollback()  # 回滚事务
            print(f"注册失败: {str(e)}")  # 打印异常
            flash(f"注册失败: {str(e)}", "error")
            return redirect(url_for('nutrition_storage_login.enroll'))

    return render_template('login/enroll.html')


@nutrition_storage_login_bp.route('/mail_test', methods=['GET', 'POST'])
def mail_test():
    try:
        from app import mail2  # 延迟导入，避免循环导入问题

        # 获取用户输入的邮箱
        email = request.form['email']  # 假设前端表单中输入了用户的邮箱

        # 生成随机的六位数验证码
        captcha = str(random.randint(100000, 999999))  # 生成 100000 到 999999 之间的随机数

        # 保存验证码到 session 中，使用邮箱作为键
        session['captcha'] = captcha

        # recipients 是接收人，是一个数组，可以给多人同时发送邮件
        message = Message(subject="验证码",
                          recipients=[email],  # 替换为你的测试邮件地址
                          body=f"您的验证码是：{captcha}")
        mail2.send(message)
        return "邮件发送成功"
    except Exception as e:
        return f"邮件发送失败: {str(e)}"
