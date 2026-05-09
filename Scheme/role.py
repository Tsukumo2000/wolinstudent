from pydantic import BaseModel, Field
from typing import Literal

class Role(BaseModel):
    role_id: int = Field(ge=1, le=5, description="职位id，必须是1-5中的一个")
    job : Literal['管理员','学生','授课教师','顾问','班主任'] = Field(None,description="性别")