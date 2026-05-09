from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class Student(BaseModel):
    """学生 - 数据校验"""
    student_name: str=Field(max_length=32,description= '姓名')  # 姓名
    gender: Literal["男","女"]|None = Field(None,description= '性别')  # 性别
    age: int|None = Field(ge=1,le=100,description='年龄')  # 年龄
    class_id: int=Field(description='班级编号')  # 班级编号，外键
    native_place:str|None =Field(None,max_length=64)  #籍贯
    school:str|None =Field(None,max_length=64) # 毕业学校
    major:str|None =Field(None,max_length=64)  # 专业
    education:str|None =Field(None,max_length=32) # 学历
    admission_time:datetime|None =Field(None,description='入学时间') #入学时间
    graduation_time:datetime|None =Field(None,description='毕业时间')  #毕业时间
    counselor_id:int=Field(description='顾问编号') # 顾问编号，外键
