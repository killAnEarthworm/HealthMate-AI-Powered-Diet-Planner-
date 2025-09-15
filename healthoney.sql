DROP DATABASE IF EXISTS healthoney;

CREATE DATABASE healthoney;
USE healthoney;

/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2024/9/13 10:51:38                           */
/*==============================================================*/

drop table if exists diet_exercise_plans;

drop table if exists food_categories;

drop table if exists food_nutrition_info;

drop table if exists health_analysis_report;

drop table if exists user_profile;

drop table if exists users;

drop table if exists weight_predictions;

/*==============================================================*/
/* Table: diet_exercise_plans                                   */
/*==============================================================*/
create table diet_exercise_plans
(
   plan_id              int not null auto_increment,
   user_id              int not null,
   generated_at         timestamp DEFAULT CURRENT_TIMESTAMP,
   daily_caloric_intake DECIMAL(6, 2),
   protein_intake       DECIMAL(5, 2),
   fat_intake           DECIMAL(5, 2),
   carbohydrate_intake  DECIMAL(5, 2),
   dietary_fibre_intake DECIMAL(5, 2),
   breakfast_details    text not null,
   lunch_details        text not null,
   dinner_details       text not null,
   snacks_details       text,
   addition_options     text,
   exercise_type        varchar(255),
   exercise_duration    int,
   feedback             text,
   vitamin_a            DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '维生素A',
   carotene             DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '胡萝卜素',
   retinol              DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '视黄醇单量',
   vitamin_b1           DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '维生素B1',
   vitamin_b2           DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '维生素B2',
   niacin               DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '烟酸',
   vitamin_c            DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '维生素C',
   vitamin_e            DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '维生素E',
   cholesterol          DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '胆固醇',
   potassium            DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '钾',
   sodium               DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '钠',
   calcium              DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '钙',
   magnesium            DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '镁',
   iron                 DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '铁',
   manganese            DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '锰',
   zinc                 DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '锌',
   copper               DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '铜',
   phosphorus           DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '磷',
   selenium             DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '硒',
   primary key (plan_id)
);

INSERT INTO diet_exercise_plans (plan_id, user_id, daily_caloric_intake, protein_intake, fat_intake, carbohydrate_intake, breakfast_details, lunch_details, dinner_details, snacks_details, exercise_type, exercise_duration, feedback) VALUES
(1, 1, 2500.00, 75.00, 60.00, 300.00, '豆浆、全麦面包、鸡蛋', '清蒸鱼、炒青菜、米饭', '烤鸡胸肉、沙拉', '苹果、坚果', '跑步', 30, '感觉很好，有活力'),
(2, 2, 2000.00, 65.00, 50.00, 250.00, '燕麦粥、水果', '豆腐、蒸南瓜、糙米饭', '烤鱼、凉拌黄瓜', '香蕉、酸奶', '瑜伽', 45, '放松，压力减少'),
(3, 3, 2200.00, 70.00, 55.00, 275.00, '小米粥、蔬菜包', '红烧牛肉、炒菠菜、杂粮饭', '清蒸虾、凉拌海带', '橙子、杏仁', '游泳', 60, '体力有所提升'),
(4, 4, 2800.00, 80.00, 70.00, 350.00, '牛奶、全麦吐司、鸡蛋', '烤鸡腿、炒西兰花、糙米饭', '烤三文鱼、蔬菜沙拉', '葡萄、核桃', '力量训练', 45, '肌肉更紧实'),
(5, 5, 2100.00, 65.00, 55.00, 265.00, '豆浆、煎饼果子', '红烧肉、炒生菜、米饭', '清蒸鱼、凉拌豆腐', '梨、瓜子', '快走', 40, '心情愉悦，睡眠质量提高'),
(6, 6, 2300.00, 70.00, 60.00, 290.00, '酸奶、全麦面包、水果', '番茄炒蛋、炒青菜、糙米饭', '烤鸡胸肉、凉拌木耳', '苹果、腰果', '舞蹈', 50, '舞蹈技巧有所提升'),
(7, 7, 1900.00, 60.00, 45.00, 240.00, '绿豆粥、包子', '宫保鸡丁、炒空心菜、杂粮饭', '清蒸鱼、凉拌黄瓜', '香蕉、杏仁', '太极', 30, '身心平衡，感觉良好'),
(8, 8, 2400.00, 75.00, 65.00, 310.00, '牛奶、全麦面包、鸡蛋', '红烧鱼、炒青菜、糙米饭', '烤牛排、蔬菜沙拉', '橙子、核桃', '自行车', 60, '耐力有所提升'),
(9, 9, 2200.00, 65.00, 50.00, 275.00, '豆浆、煎饼果子、水果', '番茄炒蛋、炒生菜、米饭', '清蒸虾、凉拌海带', '葡萄、瓜子', '慢跑', 45, '体力有所提升，心情愉悦'),
(10, 10, 2600.00, 80.00, 70.00, 330.00, '酸奶、全麦吐司、鸡蛋', '烤鸡腿、炒西兰花、糙米饭', '烤三文鱼、蔬菜沙拉', '苹果、腰果', '爬山', 90, '体力和耐力都有所提升');

/*==============================================================*/
/* Table: food_categories                                       */
/*==============================================================*/
create table food_categories
(
   category_id          varchar(16) not null,
   name                 varchar(255) not null,
   description          text,
   status               tinyint DEFAULT 0 not NULL,
   icon                 varchar(255) not null,
   created_at           timestamp DEFAULT CURRENT_TIMESTAMP,
   updated_at           timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   primary key (category_id)
);

INSERT INTO food_categories (category_id, name, description, status, icon, created_at, updated_at)
VALUES
('0100', '乳制品和蛋制品', '', 0, 'food/0100.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('0200', '调味品类', '', 0, 'food/0200.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('0300', '婴儿食品', '', 0, 'food/0300.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('0400', '油脂', '', 0, 'food/0400.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('0500', '家禽产品', '', 0, 'food/0500.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('0600', '汤、酱汁和肉汁', '', 0, 'food/0600.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('0700', '香肠和午餐肉', '', 0, 'food/0700.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('0800', '谷物早餐', '', 0, 'food/0800.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('0900', '水果和果汁', '', 0, 'food/0900.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('1000', '猪肉制品', '', 0, 'food/1000.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('1100', '蔬菜及蔬菜制品', '', 0, 'food/1100.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('1200', '坚果和种子产品', '', 0, 'food/1200.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('1300', '牛肉产品', '', 0, 'food/1300.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('1400', '饮料', '', 0, 'food/1400.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('1500', '鳍鱼和贝类产品', '', 0, 'food/1500.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('1600', '豆类及豆类制品', '', 0, 'food/1600.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('1700', '羔羊肉、小牛肉和野味产品', '', 0, 'food/1700.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('1800', '烘焙制品', '', 0, 'food/1800.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('1900', '甜品', '', 0, 'food/1900.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('2000', '谷物和意大利面', '', 0, 'food/2000.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('2100', '速食', '', 0, 'food/2100.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('2200', '饭菜、主菜和配菜', '', 0, 'food/2200.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('2500', '点心', '', 0, 'food/2500.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('3500', '美洲印第安人/阿拉斯加土著食物', '', 0, 'food/3500.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07'),
('3600', '餐厅食品', '', 0, 'food/3600.png', '2020-09-02 16:48:07', '2020-09-02 16:48:07');

/*==============================================================*/
/* Table: food_nutrition_info                                   */
/*==============================================================*/
create table food_nutrition_info
(
   food_id              varchar(16) not null COMMENT '唯一id',
   category_id          varchar(16) not null COMMENT '外键，关联食物类别',
   name                 varchar(255) not null COMMENT '食物名称',
   quantity             DECIMAL(10, 2) not NULL DEFAULT 100.00 COMMENT '数量，默认值为100',
   kcal                 DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '卡路里',
   protein              DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '蛋白质（克）',
   fat                  DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '脂肪（克）',
   carbon_water         DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '碳水',
   carbohydrates        DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '碳水化合物（克）',
   dietary_fiber        DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '膳食纤维（克）',
   vitamin_a            DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '维生素A',
   carotene             DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '胡萝卜素',
   retinol              DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '视黄醇单量',
   vitamin_b1           DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '维生素B1',
   vitamin_b2           DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '维生素B2',
   niacin               DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '烟酸',
   vitamin_c            DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '维生素C',
   vitamin_e            DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '维生素E',
   cholesterol          DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '胆固醇',
   potassium            DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '钾',
   sodium               DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '钠',
   calcium              DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '钙',
   magnesium            DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '镁',
   iron                 DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '铁',
   manganese            DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '锰',
   zinc                 DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '锌',
   copper               DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '铜',
   phosphorus           DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '磷',
   selenium             DECIMAL(10, 2) not NULL DEFAULT 0.00 COMMENT '硒',
   deleted              tinyint(1) not NULL DEFAULT 0 COMMENT '逻辑删除标志，0: 未删除，1: 已删除',
   created_at           timestamp DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
,
   primary key (food_id)
);



/*==============================================================*/
/* Table: health_analysis_report                                */
/*==============================================================*/
create table health_analysis_report
(
   report_id            int not null auto_increment,
   user_id              int not null,
   generated_at         timestamp DEFAULT CURRENT_TIMESTAMP,
   body_type            ENUM('underweight', 'normal', 'overweight', 'obese')
                         not null,
   population_category  ENUM('chiled', 'adult', 'old')
                         not null,
   physical_activity_level ENUM('sedentary', 'light', 'moderate', 'active'),
   daily_calorie_expenditure DECIMAL(6, 2)
                              not null,
   health_status        text not null,
   risk_factors         text,
   health_risks         text,
   primary key (report_id)
);

    INSERT INTO health_analysis_report (report_id, user_id, body_type, population_category, physical_activity_level, daily_calorie_expenditure, health_status, risk_factors, health_risks) VALUES
(1, 1, 'normal', 'adult', 'active', 2800.00, '良好，建议保持', '无', '无'),
(2, 2, 'overweight', 'adult', 'sedentary', 2000.00, '超重，建议增加运动', '高血压风险', '心血管疾病风险'),
(3, 3, 'normal', 'adult', 'moderate', 2500.00, '良好，建议保持', '无', '无'),
(4, 4, 'underweight', 'adult', 'light', 1800.00, '体重偏低，建议增加营养摄入', '营养不良风险', '免疫力下降风险'),
(5, 5, 'obese', 'adult', 'sedentary', 2200.00, '肥胖，建议控制饮食和增加运动', '糖尿病风险', '心血管疾病风险'),
(6, 6, 'normal', 'adult', 'active', 3000.00, '良好，建议保持', '无', '无'),
(7, 7, 'overweight', 'adult', 'light', 2200.00, '超重，建议增加运动', '高胆固醇风险', '心血管疾病风险'),
(8, 8, 'normal', 'adult', 'moderate', 2600.00, '良好，建议保持', '无', '无'),
(9, 9, 'underweight', 'adult', 'light', 1700.00, '体重偏低，建议增加营养摄入', '营养不良风险', '免疫力下降风险'),
(10, 10, 'obese', 'adult', 'sedentary', 2100.00, '肥胖，建议控制饮食和增加运动', '糖尿病风险', '心血管疾病风险');

/*==============================================================*/
/* Table: user_profile                                          */
/*==============================================================*/
create table user_profile
(
   user_profile_id      int not null,
   user_id              int,
   dietary_preference   varchar(255),
   exercise_preference  varchar(255),
   medical_history      text,
   allergies            varchar(255),
   smoking_status ENUM('never', 'former', 'current'),
   alcohol_consumption  ENUM('none', 'low', 'moderate', 'high'),
   medications          text,
   height               DECIMAL(5, 2),
   weight               DECIMAL(5, 2),
   bmi                  DECIMAL(5, 2),
   created_at           timestamp DEFAULT CURRENT_TIMESTAMP,
   updated_at           timestamp ON UPDATE CURRENT_TIMESTAMP,
   chronic_conditions   text,
   primary key (user_profile_id)
);

INSERT INTO user_profile (user_profile_id, user_id, dietary_preference, exercise_preference, medical_history, allergies, smoking_status, alcohol_consumption, medications, height, weight, bmi, chronic_conditions) VALUES
(1, 1, '素食', '跑步', '无', '无', 'never', 'none', '无', 175.00, 70.00, 22.86, '无'),
(2, 2, '无特殊要求', '游泳', '无', '无', 'former', 'low', '无', 165.00, 55.00, 20.20, '无'),
(3, 3, '低盐', '瑜伽', '无', '无', 'current', 'moderate', '无', 168.00, 60.00, 21.30, '无'),
(4, 4, '高蛋白', '健身', '无', '无', 'never', 'high', '无', 180.00, 80.00, 24.69, '无'),
(5, 5, '低脂', '篮球', '无', '无', 'former', 'none', '无', 175.00, 65.00, 21.39, '无'),
(6, 6, '无特殊要求', '舞蹈', '无', '无', 'current', 'low', '无', 160.00, 50.00, 19.50, '无'),
(7, 7, '全素', '太极', '无', '无', 'never', 'moderate', '无', 170.00, 68.00, 23.50, '无'),
(8, 8, '低糖', '散步', '无', '无', 'former', 'high', '无', 172.00, 72.00, 24.38, '无'),
(9, 9, '无特殊要求', '骑自行车', '无', '无', 'current', 'none', '无', 164.00, 58.00, 21.52, '无'),
(10, 10, '高蛋白', '登山', '无', '无', 'never', 'low', '无', 178.00, 75.00, 23.67, '无');

/*==============================================================*/
/* Table: users                                                 */
/*==============================================================*/
create table users
(
   user_id              int not null AUTO_INCREMENT,
   user_profile_id      int,
   username             varchar(50) not NULL UNIQUE,
   passwd               varchar(16) not null ,
   email                varchar(100) not NULL UNIQUE,
   phone_number         varchar(20) UNIQUE,
   gender               ENUM('male', 'female', 'other') not null,
   created_at           timestamp DEFAULT CURRENT_TIMESTAMP,
   updated_at           timestamp ON UPDATE CURRENT_TIMESTAMP,
   date_of_birth        date not null,
   primary key (user_id)
);
INSERT INTO users (user_id, user_profile_id, username, passwd, email, phone_number, gender, date_of_birth) VALUES
(1, 1, '张三','123456','john.doe@example.com', '1234567890', 'male', '1990-01-15'),
(2, 2, '李四','123456', 'jane.doe@example.com', '0987654321', 'female', '1992-05-22'),
(3, 3, '小周','123456', 'alice.smith@example.com', '1122334455', 'female', '1985-08-30'),
(4, 4, '老刘','123456', 'bob.jones@example.com', '6655443322', 'male', '1988-11-12'),
(5, 5, '守法网民','123456', 'charlie.brown@example.com', '7733224466', 'male', '1993-02-28'),
(6, 6, '啃你脑壳我啃啃啃','123456', 'diana.prince@example.com', '8822114488', 'female', '1982-07-19'),
(7, 7, '再坚持一分钟','123456', 'eli.ot@example.com', '5566778899', 'other', '1975-04-05'),
(8, 8, '踩死一只蚯蚓','123456', 'frank.underwood@example.com', '3322114488', 'male', '1978-09-21'),
(9, 9, '你好','123456', 'grace.hopper@example.com', '7744332211', 'female', '1980-12-09'),
(10, 10, '愣住','123456', 'hank.marvin@example.com', '5544332211', 'male', '1983-03-27');
/*==============================================================*/
/* Table: weight_predictions                                    */
/*==============================================================*/
create table weight_predictions
(
   predicttion_id       int not null,
   user_id              int,
   predicttion_date     date not null,
   current_weight       decimal(5,2) not null,
   predicted_weight     decimal(5,2) not null,
   predicted_bmi        decimal(5,2),
   weight_trend         ENUM('increase', 'decrease', 'stable') not null,
   created_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   primary key (predicttion_id)
);

/*==============================================================*/
/* Table: physiological_indicators                              */
/*==============================================================*/
CREATE TABLE physiological_indicators
(
    indicator_id                INT NOT NULL AUTO_INCREMENT,
    user_id                     INT NOT NULL,
    measurement_date            DATE NOT NULL,
    blood_pressure_sys          DECIMAL(5, 2),  -- 收缩压
    blood_pressure_dia          DECIMAL(5, 2),  -- 舒张压
    random_blood_glucose        DECIMAL(5, 2),  -- 随机血糖，单位 mmol/L
    glycated_hemoglobin         DECIMAL(5, 2),  -- 糖氧化血红蛋白 (%)
    uric_acid                   DECIMAL(5, 2),  -- 血尿酸
    oxygen_saturation           DECIMAL(5, 2),  -- 血饱和度 (%)
    total_cholesterol           DECIMAL(5, 2),  -- 总胆固醇，单位 mmol/L
    triglycerides               DECIMAL(5, 2),  -- 甘油三酯，单位 mmol/L
    hdl_cholesterol             DECIMAL(5, 2),  -- 高密度脂蛋白胆固醇，单位 mmol/L
    ldl_cholesterol             DECIMAL(5, 2),  -- 低密度脂蛋白胆固醇，单位 mmol/L
    created_at                  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at                  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (indicator_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE
);

ALTER TABLE physiological_indicators
ADD COLUMN height DECIMAL(5, 2),  -- 身高，单位为米
ADD COLUMN weight DECIMAL(5, 2);  -- 体重，单位为千克

INSERT INTO physiological_indicators (user_id, measurement_date, blood_pressure_sys, blood_pressure_dia, random_blood_glucose, glycated_hemoglobin, uric_acid, oxygen_saturation, total_cholesterol, triglycerides, hdl_cholesterol, ldl_cholesterol ,weight) VALUES
(1, '2024-09-01', 120.00, 80.00, 5.5, 5.0, 300.00, 98.00, 4.5, 1.2, 1.3, 2.5, 78),
(1, '2024-09-23', 180.00, 90.00, 9.5, 5.0, 410.00, 98.00, 4.5, 1.2, 4.3, 2.5, 78),
(2, '2024-09-02', 130.00, 85.00, 6.0, 5.4, 320.00, 97.00, 5.0, 1.5, 1.0, 3.0, 78),
(3, '2024-09-03', 125.00, 82.00, 5.8, 5.2, 280.00, 96.00, 4.0, 1.1, 1.5, 2.0, 78),
(4, '2024-09-04', 140.00, 90.00, 7.5, 6.0, 350.00, 95.00, 6.0, 1.8, 1.2, 4.0, 78),
(5, '2024-09-05', 110.00, 70.00, 5.0, 4.8, 290.00, 99.00, 3.5, 0.9, 1.8, 1.5, 78),
(6, '2024-09-06', 135.00, 87.00, 6.8, 5.5, 310.00, 94.00, 5.5, 1.4, 1.1, 3.5, 78),
(7, '2024-09-07', 118.00, 76.00, 4.9, 4.6, 270.00, 100.00, 3.8, 1.0, 1.6, 2.2, 78),
(8, '2024-09-08', 145.00, 92.00, 7.0, 6.3, 360.00, 93.00, 6.5, 2.0, 1.0, 4.5, 78),
(9, '2024-09-09', 115.00, 75.00, 5.3, 5.1, 300.00, 98.00, 4.1, 1.3, 1.4, 2.8, 78),
(10, '2024-09-10', 125.00, 80.00, 5.6, 5.2, 290.00, 97.00, 4.3, 1.2, 1.5, 2.1, 78);



alter table diet_exercise_plans add constraint FK_Reference_5 foreign key (user_id)
      references users (user_id) on delete restrict on update restrict;

      
alter table food_nutrition_info add constraint FK_Reference_7 foreign key (category_id)
      references food_categories (category_id) on delete restrict on update restrict;

alter table health_analysis_report add constraint FK_Reference_6 foreign key (user_id)
      references users (user_id) on delete restrict on update restrict;

alter table user_profile add constraint FK_Reference_4 foreign key (user_id)
      references users (user_id) on delete restrict on update restrict;

alter table users add constraint FK_Reference_3 foreign key (user_profile_id)
      references user_profile (user_profile_id) on delete restrict on update restrict;

alter table weight_predictions add constraint FK_Reference_1 foreign key (user_id)
      references users (user_id) on delete restrict on update restrict;



SHOW TABLES ;

SELECT * FROM diet_exercise_plans;


