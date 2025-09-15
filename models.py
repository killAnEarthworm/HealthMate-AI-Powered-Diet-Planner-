from database import db
from sqlalchemy import Enum
from datetime import datetime


# 定义 User 模型
class User(db.Model):
    __tablename__ = 'users'  # 指定表名
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_profile_id = db.Column(db.Integer)
    username = db.Column(db.String(50), unique=True, nullable=False)
    passwd = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True)
    gender = db.Column(Enum('male', 'female', 'other'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, onupdate=datetime.utcnow)
    date_of_birth = db.Column(db.Date, nullable=False)

    diet_exercise_plans = db.relationship('DietExercisePlan', backref='user', lazy=True)
    health_analysis_report = db.relationship('HealthAnalysisReport', backref='user', lazy=True)
    weight_predictions = db.relationship('WeightPrediction', backref='user', lazy=True)
    # 与UserProfile建立一对多关系
    user_profile = db.relationship('UserProfile', backref='user', uselist=False, lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class DietExercisePlan(db.Model):
    __tablename__ = 'diet_exercise_plans'

    plan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    generated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    daily_caloric_intake = db.Column(db.DECIMAL(6, 2))  # 卡路里推荐摄入量
    protein_intake = db.Column(db.DECIMAL(5, 2))
    fat_intake = db.Column(db.DECIMAL(5, 2))
    carbohydrate_intake = db.Column(db.DECIMAL(5, 2))
    dietary_fibre_intake = db.Column(db.DECIMAL(5, 2))
    breakfast_details = db.Column(db.Text, nullable=False)
    lunch_details = db.Column(db.Text, nullable=False)
    dinner_details = db.Column(db.Text, nullable=False)
    snacks_details = db.Column(db.Text)
    addition_options = db.Column(db.Text)
    exercise_type = db.Column(db.String(255))
    exercise_duration = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    vitamin_a = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    carotene = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    retinol = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    vitamin_b1 = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    vitamin_b2 = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    niacin = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    vitamin_c = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    vitamin_e = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    cholesterol = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    potassium = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    sodium = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    calcium = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    magnesium = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    iron = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    manganese = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    zinc = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    copper = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    phosphorus = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    selenium = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')

    def __repr__(self):
        return f'<DietExercisePlan {self.plan_id} for User {self.user_id}>'


class FoodCategory(db.Model):
    __tablename__ = 'food_categories'

    category_id = db.Column(db.String(16), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.SmallInteger, nullable=False, server_default='0')
    icon = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                           onupdate=db.func.current_timestamp())

    # 与FoodNutritionInfo建立一对多关系
    food_nutrition_infos = db.relationship('FoodNutritionInfo', backref='food_category', lazy=True)

    def __repr__(self):
        return f'<FoodCategory {self.category_id}: {self.name}>'


class FoodNutritionInfo(db.Model):
    __tablename__ = 'food_nutrition_info'

    food_id = db.Column(db.String(16), primary_key=True)
    category_id = db.Column(db.String(16), db.ForeignKey('food_categories.category_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='100.00')
    kcal = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    protein = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    fat = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    carbon_water = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    carbohydrates = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    dietary_fiber = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    vitamin_a = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    carotene = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    retinol = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    vitamin_b1 = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    vitamin_b2 = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    niacin = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    vitamin_c = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    vitamin_e = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    cholesterol = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    potassium = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    sodium = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    calcium = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    magnesium = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    iron = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    manganese = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    zinc = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    copper = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    phosphorus = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    selenium = db.Column(db.DECIMAL(10, 2), nullable=False, server_default='0.00')
    deleted = db.Column(db.Boolean, nullable=False, server_default='0')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f'<FoodNutritionInfo {self.food_id}: {self.name}>'


# 定义 HealthAnalysisReport 模型
class HealthAnalysisReport(db.Model):
    __tablename__ = 'health_analysis_report'

    report_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    generated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    body_type = db.Column(db.String(255), nullable=False)
    population_category = db.Column(db.String(255), nullable=False)
    physical_activity_level = db.Column(db.String(255))
    tags = db.Column(db.String(255), nullable=False)
    daily_calorie_expenditure = db.Column(db.DECIMAL(6, 2), nullable=False)  # 每日卡路里消耗量
    health_status = db.Column(db.Text, nullable=False)
    risk_factors = db.Column(db.Text)
    health_risks = db.Column(db.Text)

    def __repr__(self):
        return f'<HealthAnalysisReport {self.report_id} for User {self.user_id}>'


# 定义 UserProfile 模型
class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    user_profile_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, unique=True)  # 确保 user_id 唯一
    dietary_preference = db.Column(db.String(255))
    exercise_preference = db.Column(db.String(255))
    medical_history = db.Column(db.Text)
    allergies = db.Column(db.String(255))
    smoking_status = db.Column(Enum('never', 'former', 'current'))
    alcohol_consumption = db.Column(Enum('none', 'low', 'moderate', 'high'))
    medications = db.Column(db.Text)
    height = db.Column(db.DECIMAL(5, 2))
    weight = db.Column(db.DECIMAL(5, 2))
    bmi = db.Column(db.DECIMAL(5, 2))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.TIMESTAMP, onupdate=db.func.current_timestamp())
    chronic_conditions = db.Column(db.Text)

    def __repr__(self):
        return f'<UserProfile {self.user_profile_id} for User {self.user_id}>'


# 定义 WeightPrediction 模型
class WeightPrediction(db.Model):
    __tablename__ = 'weight_predictions'

    prediction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    prediction_date = db.Column(db.Date, nullable=False)
    current_weight = db.Column(db.DECIMAL(5, 2), nullable=False)
    predicted_weight = db.Column(db.DECIMAL(5, 2), nullable=False)
    predicted_bmi = db.Column(db.DECIMAL(5, 2))
    weight_trend = db.Column(Enum('increase', 'decrease', 'stable'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f'<WeightPrediction {self.prediction_id} for User {self.user_id}>'


class PhysiologicalIndicators(db.Model):
    __tablename__ = 'physiological_indicators'
    indicator_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    measurement_date = db.Column(db.Date, nullable=False)
    blood_pressure_sys = db.Column(db.DECIMAL(5, 2), nullable=False)
    blood_pressure_dia = db.Column(db.DECIMAL(5, 2), nullable=False)
    random_blood_glucose = db.Column(db.DECIMAL(5, 2), nullable=False)  # mmol/L
    glycated_hemoglobin = db.Column(db.DECIMAL(5, 2), nullable=False)  # %
    uric_acid = db.Column(db.DECIMAL(6, 2), nullable=False)  # 血尿酸
    oxygen_saturation = db.Column(db.DECIMAL(5, 2), nullable=False)  # 血饱和度
    total_cholesterol = db.Column(db.DECIMAL(6, 2), nullable=False)  # mmol/L
    triglycerides = db.Column(db.DECIMAL(6, 2), nullable=False)  # mmol/L
    hdl_cholesterol = db.Column(db.DECIMAL(6, 2), nullable=False)  # mmol/L
    ldl_cholesterol = db.Column(db.DECIMAL(6, 2), nullable=False)  # mmol/L
    height = db.Column(db.DECIMAL(5, 2), nullable=True)  # cm
    weight = db.Column(db.DECIMAL(5, 2), nullable=True)  # kg
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f'<PhysiologicalIndicators {self.id} for User {self.user_id}>'
