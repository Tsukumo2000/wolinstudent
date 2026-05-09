from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import date
from sqlalchemy.orm import Session
from Scheme import respon
from  typing import  Dict,Any

from database import get_db
from Scheme.student import Student
from Dao.student import create_student, delete_stundent, update_student, get_student_by_id, get_student_list, get_student_More

router_student = APIRouter(tags=["学生管理"])

@router_student.post("/",summary='学生添加')
def create_student_api(student_name:str,
                     gender:str =Query(None),
                     age:int =Query(None),
                     class_id:int =Query(None),
                     native_place:str =Query(None),
                     school:str =Query(None),
                     major:str =Query(None),
                     education:str =Query(None),
                     admission_time:date =Query(None),
                     graduation_time:date =Query(None),
                     counselor_id:int =Query(None),
                     role_id:int =Query(None), db = Depends(get_db)):
    """创建学生"""
    try:

        result = create_student(
            # student_id=student_data.student_id,
            student_name=student_name,
            gender=gender,
            age=age,
            class_id=class_id,
            native_place=native_place,
            school=school,
            major=major,
            education=education,
            admission_time=admission_time,
            graduation_time=graduation_time,
            counselor_id=counselor_id,
            role_id=role_id,
            db=db
        )
        if result is False:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": 400,
                    "message": '学生创建失败（外键不存在/参数错误）'})
        return {"code": 200,
                "message": '学生创建成功',
                "data": {"student_name": student_name}}
    except Exception as e:
        db.rollback()
        msg =str(e)
        if msg not in ["学生不存在","班级不存在","学生不属于该班级"]:
            respon.fail(str(e), 400)
        respon.fail(str(e), 500)

@router_student.post("/student/more_query", summary="多关键词查询学生")
def get_student_more_api(
    condition: Dict[str, Any],  # 前端传查询条件：{"student_name":"张三","age":20}
    db: Session = Depends(get_db)
):
    # 直接调用你写的函数
    result = get_student_More(db=db, **condition)

    # 如果返回 False → 异常
    if result is False:
        raise HTTPException(status_code=500, detail="查询失败")

    return {
        "code": 200,
        "message": "查询成功",
        "data": result
    }
# [修复] /list 路由必须在 /{student_id} 之前，否则 /list 会被 /{student_id} 匹配
@router_student.get("/list",summary='查询学生列表')
def get_student_list_api(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    """获取学生列表"""
    students = get_student_list(db=db, page=page, size=size)
    if students is None:
        raise HTTPException(status_code=404, detail="学生列表为空")
    # get_student_list 返回的是列表，需要转换为字典列表
    result = []
    for s in students:

        result.append(s)
    return {"code": 200, "message": "获取成功", "data": result}

@router_student.get("/{student_id}",summary='单个学生查询')
def get_student(student_id: int, db: Session = Depends(get_db)):
    """获取单个学生"""
    student = get_student_by_id(db=db, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")
    d = student.__dict__.copy()
    d.pop("_sa_instance_state", None)
    return {"code": 200, "message": "获取成功", "data": d}

@router_student.put("/update_student/{update_student_id}", summary="更新学生信息")
def update_student_api(
    student_id: int,
    update_fields: Dict[str, Any],  # 前端传 {字段:值}
    db: Session = Depends(get_db)
):
    # 直接调用你写的 update_student
    result = update_student(
        db=db,
        student_id=student_id,
        ** update_fields  # 解包字典
    )

    if not result:
        raise HTTPException(status_code=404, detail="学生不存在或更新失败")

    return {
        "code": 200,
        "message": "更新成功",
        "data": None
    }
@router_student.delete("/{student_id}",summary='学生删除')
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """删除学生"""
    result = delete_stundent(db, student_id)
    if not result:
        raise HTTPException(status_code=404, detail="学生不存在")
    return {"code": 200, "message": "学生删除成功", "data": f"学号为{student_id}的学生已删除"}

