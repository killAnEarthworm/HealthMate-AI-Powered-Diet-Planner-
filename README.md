healthoney项目用户手册

# 软件功能说明

Healthoney是一款基于AIGC的智能健康管理平台，专为糖尿病患者提供个性化的饮食与运动计划，旨在提高生活质量。主要功能包括体重趋势预测、健康数据分析、食物热量查询和个性化饮食计划，帮助用户实现科学的健康管理。

# 环境搭建

## 开发环境

|     |     |
| --- | --- |
| **类型** | **工具与环境** |
| 开发工具 | PyCharm, MySQL Workbench |
| 技术运用 | 程序框架：Flask |
| 运行环境 | Windows |
| 数 据 库 | MySQL 8.0 |
| 相关组件 | Fastgpt，Bootstrap, u-charts |

## 组件描述

1\. Fastgpt：开源大语言模型应用框架，用于自然语言处理和生成，为用户提供智能的饮食和运动建议。

2\. Bootstrap：前端框架，提供响应式设计和样式组件，帮助快速构建美观的用户界面。

3\. u-charts：图表库，用于数据可视化，展示用户的健康数据、趋势和分析结果，增强用户理解和互动体验。

# Healthoney 项目结构

## 项目结构

```
healthoney/
├── blueprints/                          # 蓝图模块目录
│   ├── data_board_personal_center/      # 数据看板与个人中心功能
│   ├── generate_plan/                   # 饮食运动计划生成功能
│   ├── health_report_weight_prediction/ # 健康报告与体重预测功能
│   └── nutrition_storage_login/         # 营养成分库与用户登录功能
├── static/                              # 静态资源文件
│   ├── assets/                          # u-charts 组件资源
│   ├── bootstrap/                       # Bootstrap 框架文件
│   ├── bootstrap-icons/                 # Bootstrap 图标库
│   ├── css/                             # 自定义样式文件
│   ├── images/                          # 图片资源
│   └── js/                              # JavaScript 脚本文件
├── templates/                           # 模板文件目录
│   ├── components/                      # 可复用组件（如导航栏）
│   ├── data_board/                      # 数据看板模板
│   ├── generate_plan/                   # 计划生成模板
│   ├── health_report/                   # 健康报告模板
│   ├── login/                           # 登录注册模板
│   ├── nutrition_storage/               # 营养成分库模板
│   ├── personal_center/                 # 个人中心模板
│   └── weight_prediction/               # 体重预测模板
├── app.py                               # Flask 应用主入口
├── database.py                          # 数据库连接管理
├── healthoney.sql                       # 数据库结构文件
└── models.py                            # 数据模型定义
```

## 核心文件说明

| 文件/目录 | 说明 |
|-----------|------|
| `app.py` | Flask 应用主入口，负责应用初始化、配置和蓝图注册 |
| `database.py` | 数据库连接管理模块 |
| `healthoney.sql` | 数据库结构定义及初始数据文件 |
| `models.py` | 数据模型定义，包含所有数据结构与数据库交互逻辑 |
| `blueprints/` | 应用功能模块（使用 Flask 蓝图实现模块化） |
| `static/` | 所有静态资源文件（CSS、JS、图片等） |
| `templates/` | HTML 模板文件，按功能模块组织 |

## 功能模块

### 蓝图模块
- **数据看板与个人中心** (`blueprints/data_board_personal_center`)
- **计划生成** (`blueprints/generate_plan`) - 饮食与运动计划生成
- **健康报告与预测** (`blueprints/health_report_weight_prediction`) - 健康分析与体重预测
- **营养库与认证** (`blueprints/nutrition_storage_login`) - 食物营养成分与用户登录

### 模板模块
- **基础模板** (`templates/base.html`) - 包含导航栏的基础模板
- **数据看板** (`templates/data_board/`) - 生理指标、饮食与运动数据可视化
- **计划生成** (`templates/generate_plan/`) - 个性化计划展示与调整界面
- **健康报告** (`templates/health_report/`) - 健康分析与统计信息展示
- **用户认证** (`templates/login/`) - 登录与注册界面
- **营养库** (`templates/nutrition_storage/`) - 食物营养信息查询
- **个人中心** (`templates/personal_center/`) - 用户档案与设置管理
- **体重预测** (`templates/weight_prediction/`) - 体重趋势预测与分析


## 源代码与数据导入

将项目healthoney导入PyCharm中,启动app.py即可运行。

# 运行环境安装与配置

## 系统部署图

本项目无需系统部署图，因此该部分内容省略。

## 系统要求

内存需求：最大20MB。

## 安装包及数据清单

安装包：healthoney文件夹

数据库：healthoney.sql

1.  导入数据库文件
2.  部署项目到PyCharm。

## 系统安装与配置

将项目healthoney导入PyCharm中,启动app.py即可运行。

# 用户操作说明

## 系统组成

Healthoney——基于AIGC的糖尿病健康管理平台主要由以下七大模块组成：

(1) 数据看板模块：记录用户每日生理指标，展示生理指标和健康状态的可视化数据。

(2) 健康分析报告模块：定期生成健康报告，分析用户的体重变化、饮食习惯和运动数据。

(3) 体重趋势预测模块：基于用户历史数据，利用机器学习技术预测未来体重变化趋势。

(4) 生成计划模块：根据用户信息自动生成个性化的饮食和运动计划，并支持历史计划的调整。

(5) 食物营养成分库模块：提供食物热量和营养成分查询，帮助用户了解食物信息，合理规划饮食。

(6) 个人中心模块：允许用户管理个人信息，包括档案编辑、密码修改和退出登录。

(7) 用户管理模块：用户注册、登录。

## 数据看板模块

### 数据展示功能

功能描述：数据展示功能用于实时展示用户的生理指标、饮食记录和运动情况。用户可以通过可视化图表直观了解自己的健康状态。

![dashboard.png](https://img.remit.ee/api/file/BQACAgUAAyEGAASHRsPbAAEB7opoyAPMTuokRo4zhdTFP08wrEMMkgADJwAC84pBVnLnpC765W-4NgQ.png)

### 录入用户生理指标功能

功能描述：该功能允许用户录入和更新自己的生理指标，如体重、血糖、血压等。这些数据将用于后续的健康分析和报告生成。

使用流程：

1.  点击“录入每日生理指标”
2.  输入要修改的生理指标，点击提交，数据更新成功。
![dashboard_insert.png](https://img.remit.ee/api/file/BQACAgUAAyEGAASHRsPbAAEB7q5oyAQ6YR8KG5PyI8M7DheWvzWwkAACJCcAAvOKQVYkqC5A-NEqyzYE.png)

## 生成计划模块
功能描述：自动获取已录入的生理指标构建提示词，生成定制化的饮食计划，可输入饮食偏好。
![diet_generate.png](https://img.remit.ee/api/file/BQACAgUAAyEGAASHRsPbAAEB7udoyATkacNELExhhWtynC4qHyBVLwACXScAAvOKQVZ96-vRavjKGjYE.png)

生成的计划可编辑，左侧可视化面板会自动计算当前计划的营养成分摄入状况
![diet.png](https://img.remit.ee/api/file/BQACAgUAAyEGAASHRsPbAAEB7sZoyASGVfYaZCzS2wzVBB7YrwhbxgACPCcAAvOKQVa_BuDfMFeCizYE.png)



## 食物营养成分库模块

### 食物营养成分查询功能

#### 功能描述：该功能允许用户通过选择食品和数量，直接计算出该食物所含的各类营养物质，并以数据形式呈现给用户。

使用流程：

1.点击输入框，选中自己想要查询的食物种类，再选择想要查询的食物名称，输入具体数量。

2.点击“查询”按钮，查询成功，数据显示在页面上。

![database.png](https://img.remit.ee/api/file/BQACAgUAAyEGAASHRsPbAAEB7yFoyAWXcdndtFqT0HJjXYrMNQW-EQACmScAAvOKQVZncrjKIr9MgjYE.png)
## 个人中心模块

### 用户档案管理功能

功能描述：用户档案管理功能允许用户查看和更新个人信息，包括姓名、联系方式和其他健康相关信息。

使用流程：

1.  点击用户档案
2.  输入要修改的信息，点击保存，数据更新完成。

![personal.png](https://img.remit.ee/api/file/BQACAgUAAyEGAASHRsPbAAEB7yxoyAW8KqSWMOXmfwJqqMNEMLNoTQACpScAAvOKQVasBzt-QAzQLzYE.png)
### 修改密码功能

#### 功能描述：用户可以通过此功能修改账户密码

使用流程：

1.  点击修改密码
2.  输入旧密码、新密码、再输入一次新密码，点击修改，修改成功

#### 

### 退出登录功能

#### 功能描述：该功能允许用户安全退出账户，确保个人信息的安全性。

使用流程：

1.  点击退出登录，点击确定，返回登录界面

## 用户管理模块

### 登录功能

#### 功能描述：该功能可以让用户通过已经注册过的账号进行登录。

使用流程：

1.  在输入框中输入邮箱账号和对应的密码。

1.  点击“登陆按钮”，成功登陆，进入数据看板。

![login.png](https://img.remit.ee/api/file/BQACAgUAAyEGAASHRsPbAAEB7zloyAXlA9ZCr8Ta9WK-xlY9XtfD7wACsicAAvOKQVbpEj7j5vY-MTYE.png)

### 注册功能

#### 功能描述：还未注册过的用户通过该功能进行邮箱注册。

使用流程：

1.  输入用户未注册的邮箱和密码，点击“发送验证码”按钮。

1.  输入QQ邮箱中收到的验证码，并点击“注册”按钮。注册成功后跳转至登录页面。
