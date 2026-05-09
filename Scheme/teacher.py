from pydantic import BaseModel, Field
from typing import Optional, Literal, List

class Teacher(BaseModel):
    teacher_id : int =Field(max_length=5,description="教师编号，长度不超过5位数")
    teacher_name : str =Field(...,max_length=32,description="教师姓名，长度不超过32字符")
    gender : Literal["男", "女"] | None = Field(None, description="性别")
    phone : str =Field(...,max_length=18,pattern='^1[3-9]\d{9}$',description="教师手机号，必须符合手机号码")
    classes: Optional[List[str]] = Field(None, description="带班列表，例如：['1001', '1002']")
    role_id : int = Field(...,ge=1,le=5,description="职位id，必须是1-5中的一个")


