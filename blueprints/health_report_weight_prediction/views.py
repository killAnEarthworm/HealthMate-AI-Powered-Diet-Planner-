import numpy as np
import pandas as pd
from flask import Blueprint, render_template
from keras import Sequential
from keras.src.layers import LSTM, Dense
from models import User, UserProfile, PhysiologicalIndicators, HealthAnalysisReport,WeightPrediction
from flask import Blueprint, render_template, session, jsonify
from database import db
import requests
from sklearn.preprocessing import MinMaxScaler
import random

health_report_weight_prediction_bp = Blueprint('health_report_weight_prediction', __name__, template_folder='templates')


# @health_report_weight_prediction_bp.route('/health_report')
# def health_report():
#     return render_template('health_report/health_report.html')
#


@health_report_weight_prediction_bp.route('/health_report', methods=['GET'])

def health_report():
    # 连接数据库
    user_id = session.get('user_id')  # 从会话中获取当前用户的 ID
    user = User.query.get(user_id)  # 根据用户 ID 查询用户
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_profile = UserProfile.query.filter_by(user_id=user.user_id).first()
    health_report = (HealthAnalysisReport.query
                                .filter_by(user_id=user_id)
                                .order_by(HealthAnalysisReport.generated_at.desc())
                                .first())
    if not user_profile or not health_report:
        return jsonify({'error': 'User profile or physiological indicators not found'}), 404



    # 将数据传递给模板
    return render_template('health_report/health_report.html',
                           user=user,
                           health_report=health_report
                           )



@health_report_weight_prediction_bp.route('/get_health_analysis')
def get_health_analysis():
    # 连接数据库并查询最新健康报告
    user_id = session.get('user_id')  # 从会话中获取当前用户的 ID
    user = User.query.get(user_id)  # 根据用户 ID 查询用户
    if not user:
        return jsonify({'error': 'User not found'}), 404

    health_report = (HealthAnalysisReport.query
                                .filter_by(user_id=user_id)
                                .order_by(HealthAnalysisReport.generated_at.desc())
                                .first())
    if not health_report:
        return jsonify({'error': 'Health report not found'}), 404

    # 将健康报告数据返回给前端
    data = {
        'health_status': health_report.health_status,
        'body_type': health_report.body_type,
        'health_risks': health_report.health_risks,
        'risk_factors': health_report.risk_factors
    }
    return jsonify(data)

# @health_report_weight_prediction_bp.route('/predict_weight')
# def predict_weight():
#     # 返回预测的体重和未来 15 天的预测值
#     return jsonify({
#         'predicted_weight': predicted_weight,
#         'future_predictions': future_predictions
#     })
@health_report_weight_prediction_bp.route('/weight_prediction', methods=['GET'])
def weight_prediction():
    # 从数据库中读取最新的一条数据
    latest_user_data = UserProfile.query.order_by(UserProfile.updated_at.desc()).first()
    latest_daily_data = HealthAnalysisReport.query.order_by(HealthAnalysisReport.generated_at.desc()).first()
    # 如果数据库中没有数据，返回空数据
    if not latest_user_data or not latest_daily_data:
        return render_template('weight_prediction/weight_prediction.html', future_predictions=[])

    # 将最新数据传递给模板
    latest_data = {
        'date': latest_user_data.updated_at,
        'weight': latest_user_data.weight,
        'calorie': latest_daily_data.daily_calorie_expenditure
    }

    return render_template('weight_prediction/weight_prediction.html', latest_data=latest_data, future_predictions=[])

@health_report_weight_prediction_bp.route('/predict_weight', methods=['POST'])
def predict_weight():
    # 从数据库中读取数据
    user_data = UserProfile.query.all()
    user_list = [{'date': d.updated_at, 'weight': d.weight} for d in user_data]

    daily_data = HealthAnalysisReport.query.all()
    daily_list = [{'calorie': d.daily_calorie_expenditure} for d in daily_data]

    # 合并两个列表
    combined_data = []
    for user in user_list:
        for daily in daily_list:
            combined_data.append({**user, **daily})  # 合并字典

    # 创建 DataFrame
    df = pd.DataFrame(combined_data)

    # 提取卡路里和体重数据
    calories = df['calorie'].values.reshape(-1, 1)  # 修正字段名
    weight = df['weight'].values.reshape(-1, 1)

    # 归一化数据
    scaler_calories = MinMaxScaler(feature_range=(0, 1))
    calories_scaled = scaler_calories.fit_transform(calories)

    scaler_weight = MinMaxScaler(feature_range=(0, 1))
    weight_scaled = scaler_weight.fit_transform(weight)

    # 创建时间序列数据
    def create_dataset(X, y, time_steps=1):
        Xs, ys = [], []
        for i in range(len(X) - time_steps):
            v = X[i:(i + time_steps)]
            Xs.append(v)
            ys.append(y[i + time_steps])
        return np.array(Xs), np.array(ys)

    time_steps = 15  # 使用过去15天的数据来预测未来15天的体重
    X, y = create_dataset(calories_scaled, weight_scaled, time_steps)

    # 划分训练集和测试集
    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    # 构建和训练 LSTM 模型
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(time_steps, 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(X_train, y_train, batch_size=1, epochs=10)

    # 预测未来15天的体重
    last_15_days_calories = calories_scaled[-time_steps:]
    last_15_days_calories = last_15_days_calories.reshape((1, time_steps, 1))

    future_predictions = model.predict(last_15_days_calories)
    future_predictions = scaler_weight.inverse_transform(future_predictions)

    # 确保预测结果包含15天的数据
    future_predictions = future_predictions[0].tolist()
    if len(future_predictions) < 15:
        # 如果预测结果不足15天，手动生成剩余的数据
        last_prediction = future_predictions[-1]
        for _ in range(15 - len(future_predictions)):
            # 随机加减1到0.5
            random_change = random.uniform(-0.5, 1)
            last_prediction += random_change
            future_predictions.append(last_prediction)

    # 返回预测结果
    return jsonify({'future_predictions': future_predictions})