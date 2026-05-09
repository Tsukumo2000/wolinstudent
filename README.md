# 沃林学生管理系统 (Wolin Student Management System)

基于 FastAPI + SQLAlchemy + MySQL 构建的学生管理后台系统，提供 RESTful API 接口和前端管理页面。

## 项目架构

```
Project_04201/
├── main.py                 # 应用入口，FastAPI 实例与路由注册
├── database.py             # 数据库连接配置（SQLAlchemy + PyMySQL）
├── login.html              # 登录页面
├── Dockerfile              # Docker 部署配置
├── requirements.txt        # Python 依赖清单
├── .env                    # 环境变量配置
│
├── Model/                  # ORM 数据模型
│   └── table.py            # 数据库表映射（Student, Score, Employment, Class, Teacher, User, Role）
│
├── Scheme/                 # Pydantic 数据校验模型
│   ├── class_.py           # 班级校验
│   ├── employment.py       # 就业信息校验
│   ├── respon.py           # 统一响应格式
│   ├── role.py             # 角色校验
│   ├── score.py            # 成绩校验
│   ├── student.py          # 学生校验
│   ├── teacher.py          # 教师校验
│   └── user.py             # 用户校验
│
├── Dao/                    # 数据访问层（数据库操作）
│   ├── class_.py           # 班级 CRUD
│   ├── employment.py       # 就业信息 CRUD
│   ├── score.py            # 成绩 CRUD
│   ├── statistics.py       # 统计分析查询
│   ├── student.py          # 学生 CRUD
│   ├── teacher.py          # 教师 CRUD
│   └── user.py             # 用户 CRUD
│
├── Api/                    # API 路由层
│   ├── class_.py           # 班级管理接口
│   ├── employment.py       # 就业管理接口
│   ├── score.py            # 成绩管理接口
│   ├── statistics.py       # 统计分析接口
│   ├── student.py          # 学生管理接口
│   ├── teacher.py          # 教师管理接口
│   └── user.py             # 用户登录接口
│
└── View/                   # 前端 HTML 页面
    ├── GuanLi_admin/       # 管理员页面
    ├── GuanLi_consultant/  # 顾问页面
    ├── GuanLi_head/        # 班主任页面
    ├── GuanLi_student/     # 学生页面
    ├── GuanLi_teacher/     # 教师页面
    ├── employment/         # 就业管理页面
    └── statistic/          # 统计分析页面
```

## 技术栈

| 组件 | 技术 |
|------|------|
| 后端框架 | FastAPI 0.136.1 |
| ORM | SQLAlchemy 2.0.49 |
| 数据库 | MySQL (PyMySQL) |
| 数据校验 | Pydantic 2.13.4 |
| 服务器 | Uvicorn 0.46.0 |
| 前端 | 原生 HTML + CSS |
| 环境管理 | python-dotenv 1.2.2 |

## 快速开始

### 1. 环境准备

确保已安装 Python 3.10+ 和 MySQL 数据库。

### 2. 配置环境变量

在 `.env` 文件中配置数据库连接信息：

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=123456
DB_DATABASE=fastapi_project0420
API_HOST=127.0.0.1
API_PORT=8886
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 初始化数据库

确保 MySQL 中已创建 `fastapi_project0420` 数据库，表结构由 SQLAlchemy ORM 自动管理。

### 5. 启动服务

```bash
python main.py
```

服务启动后访问 `http://127.0.0.1:8886` 查看登录页面，API 文档访问 `http://127.0.0.1:8886/docs`。

## API 接口概览

| 前缀 | 标签 | 功能 |
|------|------|------|
| `/user` | 用户登录 | 用户认证、CRUD |
| `/employment` | 就业管理 | 就业信息增删查改 |
| `/statistic` | 统计分析 | 多维度数据统计 |
| `/teacher` | 教师管理 | 教师信息管理 |
| `/score` | 成绩管理 | 成绩录入与查询 |
| `/class` | 班级管理 | 班级信息管理 |
| `/student` | 学生管理 | 学生信息管理 |

## 数据模型

- **Student** - 学生信息（姓名、性别、年龄、班级、籍贯、学历等）
- **Score** - 成绩记录（学生、班级、考核序次、分数）
- **Employment** - 就业信息（公司、薪资、时间等）
- **Class** - 班级信息（名称、开课时间、授课老师、班主任）
- **Teacher** - 教师信息（姓名、性别、电话、角色权限）
- **User** - 系统用户（用户名、密码、角色）
- **Role** - 角色定义（管理员、学生、授课教师、顾问、班主任）

## 部署

使用 Docker 部署：

```bash
docker build -t student-management-system .
docker run -p 8000:8000 student-management-system
```
