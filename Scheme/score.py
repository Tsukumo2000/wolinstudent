from pydantic import BaseModel, Field

class Score(BaseModel):
    score_id : int =Field(ge=1,description="成绩id")
    class_id : int =Field(...,ge=1,description="班级id")
    student_id : int =Field(...,ge=1,description="学生id")
    exam_order : int =Field(...,ge=1,description="考核序次")
    score : float=Field(...,ge=0,le=100,description="考试分数")

class ScoreCreate(BaseModel):
    student_id: int = Field(..., ge=1, description="学生ID")
    exam_order: int = Field(..., ge=1, description="考核序次")
    score: float = Field(..., ge=0, le=100, description="成绩 0~100")
    class_id: int = Field(..., ge=1, description="班级ID")

class ScoreOut(BaseModel):
    student_id: int = Field(..., ge=1, description="学生ID")
    exam_order: int = Field(..., ge=1, description="考核序次")
    score: float = Field(..., ge=0, le=100, description="成绩 0~100")


