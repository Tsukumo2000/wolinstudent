from pydantic import BaseModel, Field
from datetime import date

class class_1(BaseModel):

    class_name : str = Field(min_length=0,max_length=30,description="班级名字")
    start_time : date=Field(...,description="开班时间:日期格式")
    head_teacher_id : int =Field(...,description="班主任ID")
    teacher_id : int =Field(...,description="授课老师ID")
