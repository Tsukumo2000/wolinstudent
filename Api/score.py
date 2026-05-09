from fastapi import APIRouter, Depends,Path,Query,HTTPException
from sqlalchemy.orm import Session

from database import get_db
from Dao.score import create_score, update_score, delete_score,get_score,get_all_score
from Scheme import respon

router_score = APIRouter(prefix="/scores", tags=["成绩管理"])



@router_score.post("/",summary='成绩录⼊与管理')
def create_score_api(student_id: int =Query(...,ge=1,description="学生ID"),
                     exam_order: int =Query(...,ge=1,description="考核次序"),
                     score: float =Query(...,ge=0,le=100,description="分数") ,
                     db =Depends(get_db)):

    try:
        result = create_score(
            db =db,
            student_id =student_id,
            exam_order =exam_order,
            score=score)
        if not result:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": 400,
                    "message": '成绩录入失败'})
        return {"code": 200,
                "message": '成绩录入成功',
                "data": {"student_id": student_id,
                         "score":score}}

    except Exception as e:
        db.rollback()
        msg =str(e)
        if msg not in ["学生不存在","班级不存在","该学生本次考试成绩已存在，不可重复添加"]:
            respon.fail(str(e), 400)
        respon.fail(str(e), 500)

# @router_score.post("/",summary='成绩录⼊与管理')
# def create_score_api(score_data: ScoreCreate,
#                      db =Depends(get_db)):
#
#     try:
#         result = create_score(db, score_data)
#         if not result:
#             raise HTTPException(
#                 status_code=400,
#                 detail={
#                     "code": 400,
#                     "message": '成绩录入失败'})
#         return {"code": 200,
#                 "message": '成绩录入成功',
#                 "data": {"data":score_data}}
#     except Exception as e:
#         db.rollback()
#         msg =str(e)
#         if msg not in ["学生不存在","班级不存在","学生不属于该班级"]:
#             respon.fail(str(e), 400)
#         respon.fail(str(e), 500)

@router_score.put("/",summary='成绩修改管理')
def update_score_api(student_id: int =Query(description="学生id"),
                     exam_order: int =Query(...,ge=1,description="考核次序"),
                     score: float =Query(...,ge=0,le=100,description="分数") ,
                     db =Depends(get_db)):
    try:
        result = update_score(
            db=db,
            student_id=student_id,
            exam_order=exam_order,
            score=score)

        if not result:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": 400,
                    "message": '成绩修改失败'})
        return {"code": 200,
                "message": '成绩录入成功',
                "data": {"student_id": student_id,
                         "score":score}}
    except Exception as e:
        db.rollback()
        msg = str(e)
        if msg not in ["学生不存在", "班级不存在","该学生此轮考试成绩不存在，无法修改","该学生此轮考试成绩与修改成绩相同，无需修改"]:
            respon.fail(str(e), 400)
        respon.fail(str(e), 500)

    

@router_score.delete("/",summary='成绩删除管理')
def delete_score_api(exam_order:int=Query(ge=0,description="考核次序"),
                     student_id:int=Query(ge=0,description="学生ID"),
                     db:Session = Depends(get_db)):
    try:
        result = delete_score(
            db=db,
            exam_order=exam_order,
            student_id=student_id)
        if not result:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": 400,
                    "message": '成绩删除失败'})
        return {"code": 200,
                "message": '成绩删除成功'}
    except Exception as e:
        db.rollback()
        msg = str(e)
        if msg not in ["学生不存在", "该成绩已删除，请勿重复删除","该学生此轮考试成绩不存在，无法删除"]:
            respon.fail(str(e), 400)
        respon.fail(str(e), 500)

@router_score.get("/student/{student_id}",summary='按照学生编号+考核次序查询成绩')
def get_score(student_id:int=Path(ge=0,description="学生ID"),
              exam_order:int=Query(ge=0,description="考核次序"),
              db:Session = Depends(get_db)):
    try:
        result = get_score(db=db,
                           exam_order =exam_order,
                           student_id =student_id)
        if not result:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": 400,
                    "message": '查询失败'})

    except Exception as e:
        db.rollback()
        msg = str(e)
        if msg not in ["学生不存在", "该学生成绩不存在"]:
            respon.fail(str(e), 400)
        respon.fail(str(e), 500)


@router_score.get('/',summary='按照班级查询所有成绩及平均分')
def get_all(class_id: int=Query(ge=0,description="学生班级ID"),
            db:Session = Depends(get_db)):
    try:
        all_score, avg_score = get_all_score(class_id=class_id,db=db)
        if not all_score:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": 400,
                    "message": '查询失败'})
        return {"code": 200,
                "message": '查询成功',
                "data": {"class_id": class_id,
                         "all_score": all_score,
                         "avg_score":avg_score}}
    except Exception as e:
        db.rollback()
        msg = str(e)
        if msg != "班级不存在":
            respon.fail(str(e), 400)
        respon.fail(str(e), 500)

