from pydantic import BaseModel, Field

class User(BaseModel):
    username : str =Field(...,max_length=12,description="用户名最大长度为12")
    password : str =Field(...,max_length=12,description="密码最大长度为12")
    role_id: int = Field(..., ge=1, le=5, description="职位id，必须是1-5中的一个")