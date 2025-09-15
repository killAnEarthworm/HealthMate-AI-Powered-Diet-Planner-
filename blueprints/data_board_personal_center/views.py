from flask import session, Blueprint, render_template, request, redirect, url_for, flash
from database import db
from datetime import datetime, timedelta
from models import User,UserProfile,PhysiologicalIndicators


data_board_personal_center_bp = Blueprint('data_board_personal_center', __name__, template_folder='../templates')


@data_board_personal_center_bp.route('/data_board', methods=['GET', 'POST'])
def data_board():
    user_id = session.get('user_id')  # 从会话中获取当前用户的 ID
    user = User.query.get(user_id)  # 根据用户 ID 查询用户

    # 获取用户最近的测量记录
    latest_record = PhysiologicalIndicators.query.filter_by(user_id=user.user_id).order_by(PhysiologicalIndicators.measurement_date.desc()).first()

    if request.method == 'POST':
        # 获取表单数据
        measurement_date = request.form.get('measurementDate')
        blood_pressure_sys = request.form.get('systolicPressure')
        blood_pressure_dia = request.form.get('diastolicPressure')
        random_blood_glucose = request.form.get('randomBloodSugar')
        glycated_hemoglobin = request.form.get('hba1c')
        uric_acid = request.form.get('bloodUricAcid')
        oxygen_saturation = request.form.get('bloodSaturation')
        total_cholesterol = request.form.get('totalCholesterol')
        triglycerides = request.form.get('triglycerides')
        hdl_cholesterol = request.form.get('hdlCholesterol')
        ldl_cholesterol = request.form.get('ldlCholesterol')
        height = request.form.get('height')  # 获取身高
        weight = request.form.get('weight')  # 获取体重

        # 创建新记录
        new_record = PhysiologicalIndicators(
            user_id=user.user_id,
            measurement_date=measurement_date,
            blood_pressure_sys=blood_pressure_sys,
            blood_pressure_dia=blood_pressure_dia,
            random_blood_glucose=random_blood_glucose,
            glycated_hemoglobin=glycated_hemoglobin,
            uric_acid=uric_acid,
            oxygen_saturation=oxygen_saturation,
            total_cholesterol=total_cholesterol,
            triglycerides=triglycerides,
            hdl_cholesterol=hdl_cholesterol,
            ldl_cholesterol=ldl_cholesterol,
            height=height,  # 添加身高
            weight=weight   # 添加体重
        )

        try:
            db.session.add(new_record)
            db.session.commit()  # 保存更改到数据库
            flash('数据已成功提交！')
        except Exception as e:
            db.session.rollback()  # 回滚会话
            flash(f'提交失败：{str(e)}')

        return redirect(url_for('data_board_personal_center.data_board'))

    return render_template('data_board/data_board.html', latest_record=latest_record)


@data_board_personal_center_bp.route('/personal_center/user_profile', methods=['GET', 'POST'])
def user_profile():
    user_id = session.get('user_id')  # 从会话中获取当前用户的 ID
    user = User.query.get(user_id)  # 根据用户 ID 查询用户
    user_profile = UserProfile.query.filter_by(user_id=user.user_id).first() or UserProfile()  # 确保获取到 UserProfile
    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('username', user.username)
        email = request.form.get('email', user.email)
        phone = request.form.get('phone', user.phone_number)
        gender = request.form.get('gender', user.gender)
        birthdate = request.form.get('birthdate', user.date_of_birth)
        # 验证必填字段
        if not username or not email:
            flash('用户名和邮箱不能为空！')
            return redirect(url_for('data_board_personal_center.user_profile'))
        # 更新数据库
        user = User.query.first()  # 假设使用Flask-Login
        user.username = username
        user.email = email
        user.phone_number = phone
        user.gender = gender
        user.date_of_birth = birthdate

        # 获取身体数据和健康状况
        height = request.form.get('heightRange', user_profile.height)
        weight = request.form.get('weightRange', user_profile.weight)
        bmi = request.form.get('bmi', user_profile.bmi)
        allergies = request.form.get('allergies', user_profile.allergies)
        medical_history = request.form.get('medicalHistory', user_profile.medical_history)
        chronic_conditions = request.form.get('chronicConditions', user_profile.chronic_conditions)
        current_medications = request.form.get('currentMedications', user_profile.medications)

        # 更新或创建用户档案
        user_profile = UserProfile.query.filter_by(user_id=user.user_id).first()
        if user_profile is None:
            user_profile = UserProfile(user_id=user.user_id)

        user_profile.height = height
        user_profile.weight = weight
        user_profile.bmi = bmi
        user_profile.allergies = allergies
        user_profile.medical_history = medical_history
        user_profile.chronic_conditions = chronic_conditions
        user_profile.medications = current_medications

        if not user_profile.user_id:
            user_profile.user_id = user.user_id

        # 获取生活习惯和偏好
        dietary_preference = request.form.get('dietaryPreference', user_profile.dietary_preference)
        exercise_preference = request.form.get('exercisePreference', user_profile.exercise_preference)
        smoking_status = request.form.get('smokingStatus', user_profile.smoking_status)
        alcohol_consumption = request.form.get('alcoholConsumption', user_profile.alcohol_consumption)

        # 更新用户档案
        user_profile.dietary_preference = dietary_preference
        user_profile.exercise_preference = exercise_preference
        user_profile.smoking_status = smoking_status
        user_profile.alcohol_consumption = alcohol_consumption

        try:
            db.session.commit()  # 保存更改到数据库
            flash('信息已更新！')

            # 查询并打印更新后的用户信息
            updated_user = User.query.first()
            print(f'Updated User: {updated_user.username}, {updated_user.email}')
        except Exception as e:
            db.session.rollback()  # 回滚会话
            flash(f'更新失败：{str(e)}')

        return redirect(url_for('data_board_personal_center.user_profile'))

    return render_template('personal_center/user_profile.html', user=user, user_profile=user_profile)


@data_board_personal_center_bp.route('/personal_center/change_password', methods=['GET', 'POST'])
def change_password():
    user_id = session.get('user_id')  # 从会话中获取当前用户的 ID
    user = User.query.get(user_id)  # 根据用户 ID 查询用户
    if request.method == 'POST':
        old_password = request.form.get('inputOldPassword')
        new_password = request.form.get('inputNewPassword')
        confirm_password = request.form.get('inputConfirmPassword')

        # 调试信息
        print(f"Stored password: {user.passwd}")
        print(f"Input old password: {old_password}")

        # 检查旧密码是否正确
        if user.passwd != old_password:  # 直接比较明文密码
            flash('旧密码错误！')
            return redirect(url_for('data_board_personal_center.change_password'))

        # 检查新密码和确认密码是否一致
        if new_password != confirm_password:
            flash('新密码与确认密码不一致！')
            return redirect(url_for('data_board_personal_center.change_password'))

        # 更新密码
        user.passwd = new_password  # 直接存储明文密码

        try:
            db.session.commit()  # 保存更改到数据库
            flash('密码修改成功！')
        except Exception as e:
            db.session.rollback()  # 回滚会话
            flash(f'更新失败：{str(e)}')

        return redirect(url_for('data_board_personal_center.change_password'))

    return render_template('personal_center/change_password.html')




@data_board_personal_center_bp.route('/api/blood_pressure_data', methods=['GET'])
def blood_pressure_data():
    user_id = session.get('user_id')
    if user_id is None:
        return {"error": "用户未登录"}, 403

    # 获取今天的日期
    today = datetime.now().date()
    # 计算本周一和周日的日期
    start_of_week = today - timedelta(days=today.weekday())  # 本周一
    end_of_week = start_of_week + timedelta(days=6)  # 本周日

    # 查询指定日期范围内的血压数据
    records = PhysiologicalIndicators.query.filter(
        PhysiologicalIndicators.user_id == user_id,
        PhysiologicalIndicators.measurement_date >= start_of_week,
        PhysiologicalIndicators.measurement_date <= end_of_week
    ).order_by(PhysiologicalIndicators.measurement_date).all()

    # 生成本周日期列表
    week_dates = [(start_of_week + timedelta(days=i)).strftime("%m-%d") for i in range(7)]

    # 初始化数据字典
    blood_pressure_data = {
        "systolic": {date: None for date in week_dates},
        "diastolic": {date: None for date in week_dates}
    }

    # 填充数据
    for record in records:
        date_str = record.measurement_date.strftime("%m-%d")
        blood_pressure_data["systolic"][date_str] = float(record.blood_pressure_sys)
        blood_pressure_data["diastolic"][date_str] = float(record.blood_pressure_dia)

    # 格式化输出
    categories = week_dates
    systolic_pressure = [blood_pressure_data["systolic"][date] for date in week_dates]
    diastolic_pressure = [blood_pressure_data["diastolic"][date] for date in week_dates]

    series = [
        {"name": "伸缩压", "data": systolic_pressure},
        {"name": "舒张压", "data": diastolic_pressure}
    ]

    return {"categories": categories, "series": series}


@data_board_personal_center_bp.route('/api/blood_saturation_data', methods=['GET'])
def blood_saturation_data():
    user_id = session.get('user_id')
    if user_id is None:
        return {"error": "用户未登录"}, 403

    # 查询用户最新的血饱和度记录
    latest_record = PhysiologicalIndicators.query.filter_by(user_id=user_id).order_by(PhysiologicalIndicators.measurement_date.desc()).first()

    if latest_record is None:
        return {"error": "没有找到血饱和度数据"}, 404

    # 返回血饱和度数据
    series = [
        {
            "name": "血饱和度",
            "color": "#2fc25b",
            "data": float(latest_record.oxygen_saturation) / 100  # 将百分比转换为小数
        }
    ]

    return {"series": series}

@data_board_personal_center_bp.route('/api/uric_acid_data', methods=['GET'])
def uric_acid_data():
    user_id = session.get('user_id')
    if user_id is None:
        return {"error": "用户未登录"}, 403

    # 获取今天的日期
    today = datetime.now().date()
    # 计算本周一和周日的日期
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # 查询指定日期范围内的血尿酸数据
    records = PhysiologicalIndicators.query.filter(
        PhysiologicalIndicators.user_id == user_id,
        PhysiologicalIndicators.measurement_date >= start_of_week,
        PhysiologicalIndicators.measurement_date <= end_of_week
    ).order_by(PhysiologicalIndicators.measurement_date).all()

    # 生成本周日期列表
    week_dates = [(start_of_week + timedelta(days=i)).strftime("%m-%d") for i in range(7)]

    # 初始化数据字典
    uric_acid_data = {date: None for date in week_dates}

    # 填充数据
    for record in records:
        date_str = record.measurement_date.strftime("%m-%d")
        uric_acid_data[date_str] = float(record.uric_acid)

    # 格式化数据
    categories = week_dates
    uric_acid_levels = [uric_acid_data[date] for date in week_dates]

    series = [
        {"name": "血尿酸水平", "data": uric_acid_levels}
    ]

    return {"categories": categories, "series": series}

@data_board_personal_center_bp.route('/api/blood_glucose_data', methods=['GET'])
def blood_glucose_data():
    user_id = session.get('user_id')
    if user_id is None:
        return {"error": "用户未登录"}, 403

    # 获取今天的日期
    today = datetime.now().date()
    # 计算本周一和周日的日期
    start_of_week = today - timedelta(days=today.weekday())  # 本周一
    end_of_week = start_of_week + timedelta(days=6)  # 本周日

    # 查询指定日期范围内的血糖数据
    records = PhysiologicalIndicators.query.filter(
        PhysiologicalIndicators.user_id == user_id,
        PhysiologicalIndicators.measurement_date >= start_of_week,
        PhysiologicalIndicators.measurement_date <= end_of_week
    ).order_by(PhysiologicalIndicators.measurement_date).all()

    # 生成本周日期列表
    week_dates = [(start_of_week + timedelta(days=i)).strftime("%m-%d") for i in range(7)]

    # 初始化数据字典
    blood_glucose_data = {
        "glucose": {date: None for date in week_dates},
        "hba1c": {date: None for date in week_dates}
    }

    # 填充数据
    for record in records:
        date_str = record.measurement_date.strftime("%m-%d")
        blood_glucose_data["glucose"][date_str] = float(record.random_blood_glucose)
        blood_glucose_data["hba1c"][date_str] = float(record.glycated_hemoglobin)

    # 格式化输出
    categories = week_dates
    glucose_levels = [blood_glucose_data["glucose"][date] for date in week_dates]
    hba1c_levels = [blood_glucose_data["hba1c"][date] for date in week_dates]

    series = [
        {"name": "血糖（mmol/L）", "type": "line", "color": "#0C847A", "data": glucose_levels},
        {"name": "糖氧化血红蛋白（%）", "index": 1, "type": "column", "data": hba1c_levels}
    ]

    return {"categories": categories, "series": series}

@data_board_personal_center_bp.route('/api/cholesterol_data', methods=['GET'])
def cholesterol_data():
    user_id = session.get('user_id')
    if user_id is None:
        return {"error": "用户未登录"}, 403

    # 获取今天的日期
    today = datetime.now().date()

    # 查询今天的血脂数据
    record = PhysiologicalIndicators.query.filter(
        PhysiologicalIndicators.user_id == user_id,
        PhysiologicalIndicators.measurement_date == today
    ).first()

    if not record:
        return {
            "categories": ["总胆固醇", "甘油三酯", "高密度脂蛋白胆固醇", "低密度脂蛋白胆固醇"],
            "series": [{
                "name": "今日指标",
                "data": [None, None, None, None]  # 如果没有数据，填充为 None
            }]
        }

    # 提取血脂数据
    cholesterol_data = [
        record.total_cholesterol,
        record.triglycerides,
        record.hdl_cholesterol,
        record.ldl_cholesterol
    ]

    # 格式化输出
    return {
        "categories": ["总胆固醇", "甘油三酯", "高密度脂蛋白胆固醇", "低密度脂蛋白胆固醇"],
        "series": [{
            "name": "今日指标",
            "data": cholesterol_data
        }]
    }
