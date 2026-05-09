import os
from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
from Api.user import router_users
from Api.employment import router_employment
from Api.statistics import router_statistic
from Api.teacher import router_teacher
from Api.score import router_score
from Api.class_ import router_class
from Api.student import router_student
from Api.user import router_users

load_dotenv()

app = FastAPI()
app.include_router(router_users,prefix='/user',tags=['用户登录'])
app.include_router(router_employment,prefix='/employment',tags=['就业管理'])
app.include_router(router_statistic,prefix='/statistic',tags=['统计分析'])
app.include_router(router_teacher,prefix='/teacher',tags=['教师管理'])
app.include_router(router_score,prefix='/score',tags=['成绩管理'])
app.include_router(router_class,prefix='/class',tags=['班级管理'])
app.include_router(router_student,prefix='/student',tags=['学生管理'])




if __name__ == '__main__':
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "8886"))
    uvicorn.run('main:app', host=host, port=port, reload=True)