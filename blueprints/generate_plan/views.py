from flask import Blueprint, render_template, request, jsonify, session, current_app
from models import User, UserProfile, PhysiologicalIndicators, HealthAnalysisReport, DietExercisePlan, FoodNutritionInfo
from blueprints.generate_plan.common import OutputParser, extract_meal_plan
from database import db
import requests

generate_plan_bp = Blueprint('generate_plan', __name__, template_folder='templates')


@generate_plan_bp.route('/generate_plan')
def generate_plan():
    user_id = session.get('user_id')  # 从会话中获取当前用户的 ID
    user = User.query.get(user_id)  # 根据用户 ID 查询用户
    diet_plan = (DietExercisePlan.query
                 .filter_by(user_id=user_id)
                 .order_by(DietExercisePlan.generated_at.desc())
                 .first())
    breakfast = OutputParser.extract_struct(diet_plan.breakfast_details, dict)
    lunch = OutputParser.extract_struct(diet_plan.lunch_details, dict)
    dinner = OutputParser.extract_struct(diet_plan.dinner_details, dict)
    snack = OutputParser.extract_struct(diet_plan.snacks_details, dict)
    addition_options = OutputParser.extract_struct(diet_plan.addition_options, dict)
    all_dishes = {}
    all_dishes.update(breakfast)
    all_dishes.update(lunch)
    all_dishes.update(dinner)
    all_dishes.update(snack)
    all_dishes.update(addition_options)

    menu_data = {
        "menu": {
            "breakfast": breakfast,
            "lunch": lunch,
            "dinner": dinner,
            "snack": snack
        },
        "options": all_dishes
    }

    # 计算营养总和
    nutrition_sum = calculate_nutrition_sum(menu_data.get("menu"))

    # 构建 nutrition_data
    nutrition_data = {
        "categories": ["维生素A", "胡萝卜素", "视黄醇单量", "维生素B1", "维生素B2", "烟酸", "维生素C", "维生素E",
                       "胆固醇", "钾", "钠", "钙", "镁", '铁', '锰', '锌', '铜', '磷', "硒"],
        "series": [
            {
                "name": "目标值",
                "data": [900, 3000, 900, 1.2, 1.3, 16, 90, 15, 300, 4700, 2300, 1000, 420, 18, 2.3, 11, 0.9, 700, 55]
            },
            {
                "name": "完成量",
                "data": [nutrition_sum.get("维生素A", 0), nutrition_sum.get("胡萝卜素", 0),
                         nutrition_sum.get("视黄醇单量", 0),
                         nutrition_sum.get("维生素B1", 0), nutrition_sum.get("维生素B2", 0),
                         nutrition_sum.get("烟酸", 0),
                         nutrition_sum.get("维生素C", 0), nutrition_sum.get("维生素E", 0),
                         nutrition_sum.get("胆固醇", 0),
                         nutrition_sum.get("钾", 0), nutrition_sum.get("钠", 0), nutrition_sum.get("钙", 0),
                         nutrition_sum.get("镁", 0), nutrition_sum.get("铁", 0), nutrition_sum.get("锰", 0),
                         nutrition_sum.get("锌", 0), nutrition_sum.get("铜", 0), nutrition_sum.get("磷", 0),
                         nutrition_sum.get("硒", 0)]
            }
        ]
    }

    calorie_data = {
        "categories": [{"value": 0.2, "color": "#1890ff"}, {"value": 0.8, "color": "#2fc25b"},
                       {"value": 1, "color": "#f04864"}],
        "series": [
            {
                "name": "完成率",
                "data": nutrition_sum.get("卡路里", 0) / diet_plan.daily_caloric_intake
            }
        ]
    }
    # 计算营养成分百分比
    nutrient_percentages = {
        "热量": int((nutrition_sum.get("卡路里", 0) / diet_plan.daily_caloric_intake) * 100),
        "碳水化合物": int((nutrition_sum.get("碳水化合物", 0) / diet_plan.carbohydrate_intake) * 100),
        "蛋白质": int((nutrition_sum.get("蛋白质", 0) / diet_plan.protein_intake) * 100),
        "脂肪": int((nutrition_sum.get("脂肪", 0) / diet_plan.fat_intake) * 100),
        "膳食纤维": int((nutrition_sum.get("膳食纤维", 0) / diet_plan.dietary_fibre_intake) * 100)
    }

    return render_template('generate_plan/generate_plan.html', nutrition_data=nutrition_data, calorie_data=calorie_data,
                           calorie=nutrition_sum.get("卡路里", 0), menu_data=menu_data, user=user, diet_plan=diet_plan,
                           all_dishes=all_dishes, nutrient_percentages=nutrient_percentages)


# 查询食物营养成分的函数
def get_nutrition_data(dish_data):
    # 初始化营养成分字典
    nutrition_sum = {
        "卡路里": 0, "蛋白质": 0, "膳食纤维": 0, "脂肪": 0, "碳水化合物": 0, "维生素A": 0, "胡萝卜素": 0,
        "视黄醇单量": 0, "维生素B1": 0, "维生素B2": 0, "烟酸": 0, "维生素C": 0,
        "维生素E": 0, "胆固醇": 0, "钾": 0, "钠": 0, "钙": 0, "镁": 0, '铁': 0, '锰': 0, '锌': 0, '铜': 0, '磷': 0,
        "硒": 0
    }

    # 遍历 dish_data 中的每个食材及其用量
    for ingredient, quantity in dish_data.items():
        # 查询数据库，获取食材的营养成分
        food_info = FoodNutritionInfo.query.filter(FoodNutritionInfo.name.like(f'%{ingredient}%')).first()

        if food_info:
            # 计算每种营养成分的总量
            nutrition_sum["卡路里"] += food_info.kcal * quantity / 100
            nutrition_sum["蛋白质"] += food_info.protein * quantity / 100
            nutrition_sum["膳食纤维"] += food_info.vitamin_a * quantity / 100
            nutrition_sum["脂肪"] += food_info.fat * quantity / 100
            nutrition_sum["碳水化合物"] += food_info.carbohydrates * quantity / 100
            nutrition_sum["维生素A"] += food_info.vitamin_a * quantity / 100
            nutrition_sum["胡萝卜素"] += food_info.carotene * quantity / 100
            nutrition_sum["视黄醇单量"] += food_info.retinol * quantity / 100
            nutrition_sum["维生素B1"] += food_info.vitamin_b1 * quantity / 100
            nutrition_sum["维生素B2"] += food_info.vitamin_b2 * quantity / 100
            nutrition_sum["烟酸"] += food_info.niacin * quantity / 100
            nutrition_sum["维生素C"] += food_info.vitamin_c * quantity / 100
            nutrition_sum["维生素E"] += food_info.vitamin_e * quantity / 100
            nutrition_sum["胆固醇"] += food_info.cholesterol * quantity / 100
            nutrition_sum["钾"] += food_info.potassium * quantity / 100
            nutrition_sum["钠"] += food_info.sodium * quantity / 100
            nutrition_sum["钙"] += food_info.calcium * quantity / 100
            nutrition_sum["镁"] += food_info.magnesium * quantity / 100
            nutrition_sum["铁"] += food_info.iron * quantity / 100
            nutrition_sum["锰"] += food_info.manganese * quantity / 100
            nutrition_sum["锌"] += food_info.zinc * quantity / 100
            nutrition_sum["铜"] += food_info.copper * quantity / 100
            nutrition_sum["磷"] += food_info.phosphorus * quantity / 100
            nutrition_sum["硒"] += food_info.selenium * quantity / 100

    return nutrition_sum


# 计算营养总和的函数
def calculate_nutrition_sum(menu_data):
    nutrition_sum = {
        "卡路里": 0, "蛋白质": 0, "膳食纤维": 0, "脂肪": 0, "碳水化合物": 0, "维生素A": 0, "胡萝卜素": 0,
        "视黄醇单量": 0, "维生素B1": 0, "维生素B2": 0, "烟酸": 0, "维生素C": 0,
        "维生素E": 0,
        "胆固醇": 0, "钾": 0, "钠": 0, "钙": 0, "镁": 0, '铁': 0, '锰': 0, '锌': 0, '铜': 0, '磷': 0, "硒": 0
    }

    for meal, dishes in menu_data.items():
        for dish, ingredients in dishes.items():
            nutrition_data = get_nutrition_data(ingredients)
            for nutrient, value in nutrition_data.items():
                nutrition_sum[nutrient] += value

    return nutrition_sum


@generate_plan_bp.route('/update-menu', methods=['POST'])
def update_menu():
    user_id = session.get('user_id')  # 从会话中获取当前用户的 ID
    diet_plan = (DietExercisePlan.query
                 .filter_by(user_id=user_id)
                 .order_by(DietExercisePlan.generated_at.desc())
                 .first())
    data = request.get_json()
    menu_data = data.get('menu', {})

    # 计算营养总和
    nutrition_sum = calculate_nutrition_sum(menu_data)

    # 构建 nutrition_data
    nutrition_data = {
        "categories": ["维生素A", "胡萝卜素", "视黄醇单量", "维生素B1", "维生素B2", "烟酸", "维生素C", "维生素E",
                       "胆固醇", "钾", "钠", "钙", "镁", '铁', '锰', '锌', '铜', '磷', "硒"],
        "series": [
            {
                "name": "目标值",
                "data": [900, 3000, 900, 1.2, 1.3, 16, 90, 15, 300, 4700, 2300, 1000, 420, 18, 2.3, 11, 0.9, 700, 55]
            },
            {
                "name": "完成量",
                "data": [nutrition_sum.get("维生素A", 0), nutrition_sum.get("胡萝卜素", 0),
                         nutrition_sum.get("视黄醇单量", 0),
                         nutrition_sum.get("维生素B1", 0), nutrition_sum.get("维生素B2", 0),
                         nutrition_sum.get("烟酸", 0),
                         nutrition_sum.get("维生素C", 0), nutrition_sum.get("维生素E", 0),
                         nutrition_sum.get("胆固醇", 0),
                         nutrition_sum.get("钾", 0), nutrition_sum.get("钠", 0), nutrition_sum.get("钙", 0),
                         nutrition_sum.get("镁", 0), nutrition_sum.get("铁", 0), nutrition_sum.get("锰", 0),
                         nutrition_sum.get("锌", 0), nutrition_sum.get("铜", 0), nutrition_sum.get("磷", 0),
                         nutrition_sum.get("硒", 0)]
            }
        ]
    }

    # 计算卡路里
    calorie = nutrition_sum.get("卡路里", 0)  # 这里假设卡路里是各项营养的总和

    # 构建 calorie_data
    calorie_data = {
        "categories": [{"value": 0.2, "color": "#1890ff"}, {"value": 0.8, "color": "#2fc25b"},
                       {"value": 1, "color": "#f04864"}],
        "series": [
            {
                "name": "完成率",
                "data": calorie / diet_plan.daily_caloric_intake  # 这里假设目标卡路里是 2000
            }
        ]
    }

    nutrient_percentages = {
        "热量": int((nutrition_sum.get("卡路里", 0) / diet_plan.daily_caloric_intake) * 100),
        "碳水化合物": int((nutrition_sum.get("碳水化合物", 0) / diet_plan.carbohydrate_intake) * 100),
        "蛋白质": int((nutrition_sum.get("蛋白质", 0) / diet_plan.protein_intake) * 100),
        "脂肪": int((nutrition_sum.get("脂肪", 0) / diet_plan.fat_intake) * 100),
        "膳食纤维": int((nutrition_sum.get("膳食纤维", 0) / diet_plan.dietary_fibre_intake) * 100)
    }

    return jsonify({
        "nutrition_data": nutrition_data,
        "calorie_data": calorie_data,
        "calorie": calorie,
        "nutrient_percentages": nutrient_percentages
    })


@generate_plan_bp.route('/save-menu', methods=['POST'])
def save_menu():
    data = request.get_json()
    menu = data.get("menu")
    generate_time = data.get("generate_time")
    user_id = session.get('user_id')  # 从会话中获取当前用户的 ID

    # 根据生成时间和用户 ID 筛选出符合条件的数据
    diet_plan = (DietExercisePlan.query
                 .filter_by(user_id=user_id)
                 .order_by(DietExercisePlan.generated_at.desc())
                 .first())

    if diet_plan:
        # 更新数据
        diet_plan.breakfast_details = str(menu.get("breakfast"))
        diet_plan.lunch_details = str(menu.get("lunch"))
        diet_plan.dinner_details = str(menu.get("dinner"))
        diet_plan.snacks_details = str(menu.get("snacks"))
        diet_plan.addition_options = str(menu.get("addition_options"))
    else:
        # 如果没有找到符合条件的数据，则创建新数据
        diet_plan = DietExercisePlan(
            user_id=user_id,
            breakfast_details=str(menu.get("breakfast")),
            lunch_details=str(menu.get("lunch")),
            dinner_details=str(menu.get("dinner")),
            snacks_details=str(menu.get("snacks")),
            addition_options=str(menu.get("addition_options")),
            generate_time=generate_time
        )
        db.session.add(diet_plan)

    # 提交更改
    db.session.commit()

    return jsonify({"status": "success", "message": "菜单已保存"})


@generate_plan_bp.route('/generate_plan/send_data', methods=['POST'])
def send_data():
    user_id = session.get('user_id')  # 从会话中获取当前用户的 ID
    user = User.query.get(user_id)  # 根据用户 ID 查询用户
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_profile = UserProfile.query.filter_by(user_id=user.user_id).first()
    physiological_indicators = (PhysiologicalIndicators.query
                                .filter_by(user_id=user_id)
                                .order_by(PhysiologicalIndicators.measurement_date.desc())
                                .first())
    if not user_profile or not physiological_indicators:
        return jsonify({'error': 'User profile or physiological indicators not found'}), 404

    # 获取前端传来的 want_eat 数据
    want_eat = request.form.get('want_eat')

    prompt = (f"user_id：{user_id};性别：{user.gender}；饮食偏好：{user_profile.dietary_preference}，{want_eat}；"
              f"年龄：{user.date_of_birth}，既往病史：{user_profile.medical_history}；过敏史：{user_profile.allergies}；"
              f"身高{user_profile.height}cm；体重：{physiological_indicators.weight}kg；bmi：{user_profile.bmi}；"
              f"血压收缩压：{physiological_indicators.blood_pressure_sys}；"
              f"血压舒张压：{physiological_indicators.blood_pressure_dia}；"
              f"随机血糖：{physiological_indicators.random_blood_glucose}mmol/L；"
              f"血尿酸：{physiological_indicators.uric_acid}微摩尔/升；"
              f"血氧饱和度：{physiological_indicators.oxygen_saturation}%；"
              f"总胆固醇：{physiological_indicators.total_cholesterol}mmol/L；"
              f"高密度脂蛋白胆固醇：{physiological_indicators.hdl_cholesterol}mmol/L；"
              f"低密度脂蛋白胆固醇：{physiological_indicators.ldl_cholesterol}mmol/L；")

    print("当前提示词："+prompt)

    # 从应用配置中获取API设置
    api_url = current_app.config.get('FASTGPT_API_URL')
    api_key = current_app.config.get('FASTGPT_API_KEY')

    # 调用大语言模型 API
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'stream': False,
        'detail': False,
        'messages': [
            {
                'content': prompt,
                'role': 'user'
            }
        ]
    }

    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        return jsonify({'success': 'Data processed successfully'}), 200
    else:
        return jsonify({'error': 'Failed to call the language model API'}), response.status_code


@generate_plan_bp.route('/getData', methods=['POST'])
def get_data():
    data = request.get_json()
    health_report = OutputParser.extract_struct(data.get("health_report"), dict)
    user_id = data.get('user_id')
    daily_calorie_expenditure = data.get("need_kcal")
    diet_plan = extract_meal_plan(data.get("plan"))
    nutrition_intake = OutputParser.extract_struct(data.get("nutrition_value"), dict)

    # 创建 HealthAnalysisReport 实例
    report = HealthAnalysisReport(
        user_id=user_id,
        body_type=health_report['body_type'],
        population_category=health_report['population_category'],
        health_status=health_report['health_status'],
        risk_factors=health_report['risk_factors'],
        health_risks=health_report['health_risks'],
        tags=health_report['tags'],
        daily_calorie_expenditure=daily_calorie_expenditure,
    )
    db.session.add(report)
    db.session.commit()

    diet_plan = DietExercisePlan(
        user_id=user_id,
        daily_caloric_intake=nutrition_intake['daily_calorie_expenditure'],
        breakfast_details=str(diet_plan['breakfast']),
        lunch_details=str(diet_plan['lunch']),
        dinner_details=str(diet_plan['dinner']),
        snacks_details=str(diet_plan['snack']),
        addition_options=str(diet_plan['addition_options']),
        protein_intake=nutrition_intake['protein_intake'],
        fat_intake=nutrition_intake['fat_intake'],
        carbohydrate_intake=nutrition_intake['carbohydrate_intake'],
        dietary_fibre_intake=nutrition_intake['dietary_fibre_intake']
    )

    # 添加到数据库
    db.session.add(diet_plan)
    db.session.commit()

    return data


# 从用户特征表中提取出每日所需卡路里，返回一个字典{"need_kcal":"num"}
@generate_plan_bp.route('/progressNum', methods=['POST'])
def progress_json():
    data = request.get_json()
    request_content = data.get("ai回复内容", "")
    result_dict = OutputParser.extract_struct(request_content, dict)

    return result_dict
