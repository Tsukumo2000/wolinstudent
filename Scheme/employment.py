from pydantic import BaseModel,Field
from datetime import datetime

class Employment(BaseModel):
    """ 就业信息 - 数据校验 """
    student_id: int =Field(ge=0,description='学生编号')  # 学生编号，主键
    student_name:str=Field(description='学生姓名')  # 姓名
    class_id: int =Field(description='班级') # 班级，
    class_name:str=Field(description='班级名称')
    open_time:datetime|None =Field(None,description='就业开放时间')  #就业开放时间
    offer_time:datetime|None =Field(None,description='offer下发时间')  #offer下发时间
    company:str|None =Field(None,max_length=64,description='就业公司') #就业公司
    salary:float|None = Field(ge=0,description='工资')

class EmploymentOut(BaseModel):
    code: int = 200
    msg: str = "操作成功"
    student_id: int
    student_name: str
