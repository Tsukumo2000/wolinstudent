import json

from fastapi import APIRouter, Query, Depends, HTTPException,Form

from database import get_db
from Dao import teacher
from Scheme import respon

router_teacher = APIRouter()


@router_teacher.get('/teacher1',summary='查询所有老师信息')
def get_teacher_all_api(db=Depends(get_db),
                     page :int=Query(ge=1,description="分页查询页数"),
                     size :int=Query(ge=1,description="分页查询每页数据数")):
    try:
        teacher_list, total = teacher.get_teacher_all(db, page, size)
        if not teacher_list:
            return {"code": 404,
                    "message": '超出查询数量',
                    "data": {"total": total,
                             "page": page,
                             "size": size}}
        return {"code": 200,
                "message": '查询老师信息成功',
                "data": {"list": teacher_list,
                         "total": total,
                         "page": page,
                         "size": size}}
    except Exception as e:
        respon.fail(str(e),500)



@router_teacher.post('/teacher2',summary='查询老师信息')
def get_teacher_message_api(fieldname:str =Form(description="所在字段"),
                        keyword :str =Form(description="关键字"),
                        page :int =Form(1,ge=1,description="分页查询页数"),
                        size :int =Form(10,ge=1,description="分页查询每页数据数"),
                        db=Depends(get_db)):
    try:
        teacher_fieldname = ['teacher_id', 'teacher_name', 'gender', 'phone', 'classes', 'role_id']
        if fieldname not in teacher_fieldname:
            respon.fail("输入信息不在表字段内,仅支持：'teacher_id','teacher_name','gender','phone','classes','role_id'",
                        400)
        keyword = keyword.strip()
        if not keyword:
            respon.fail("关键字不能为空", 400)

        teacher_list = teacher.get_teacher_message(db=db,
                                                   fieldname=fieldname,
                                                   keyword=keyword,
                                                   page=page,
                                                   size=size)
        # if not teacher_list:
        #     respon.fail("无符合条件的老师信息", 404)
        return {"code": 200,
                "message": '查询老师信息成功',
                "data": {"list": teacher_list,
                         "page": page,
                         "size": size}}
    except Exception as e:
        msg = str(e)
        if msg not in ["无老师信息", "关键字不能为空","输入信息不在表字段内,仅支持：'teacher_id','teacher_name','gender','phone','classes','role_id'"]:
            respon.fail(str(e), 400)
        respon.fail(str(e), 500)



@router_teacher.post('/teacher3',summary='修改老师信息')
def update_teacher_api(teacher_id : int= Form(...,ge=1,description='老师id必填'),
                       teacher_name: str = Form(None,description='老师姓名选填'),
                       gender: str = Form(None,description='老师性别选填'),
                       phone: str = Form(None,description='老师电话选填'),
                       classes: str = Form(None,description='老师班级选填'),
                       role_id: int = Form(None,description='老师职位选填'),
                       db =Depends(get_db)):
    try:
        update_dict = {}
        if teacher_name and teacher_name.strip() != "" and teacher_name != "string":
            update_dict["teacher_name"] = teacher_name
        if gender and gender.strip() != "" and gender != "string":
            update_dict["gender"] = gender
        if phone and phone.strip() != "" and phone != "string":
            update_dict["phone"] = phone
        if classes and classes.strip() != "" and classes != "string":
            update_dict["classes"] = classes
        if role_id is not None and role_id != 0:
            update_dict["role_id"] = role_id
        if not update_dict:
            respon.fail("更新内容不能为空", 400)
        res = teacher.update_teacher(db=db,
                                     teacher_id =teacher_id,
                                     update_dict =update_dict)
        return {"code": 200,
                "message": "老师信息修改成功",
                "data": {"teacher_id": teacher_id}}
    except Exception as e:
        msg =str(e)
        if "老师不存在" in msg:
            respon.fail(msg, 404)
        respon.fail(msg, 500)


@router_teacher.delete('/teacher4',summary='逻辑删除老师信息')
def delete_teacher_api(teacher_id : int =Form(...,ge=1,description="老师ID"),
                       db =Depends(get_db)):
    try:
        res = teacher.delete_teacher(db = db,
                                     teacher_id =teacher_id)
        return {"code": 200,
                "message": '删除老师信息成功',
                "data": {"teacher_id": teacher_id}}
    except Exception as e:
        db.rollback()
        respon.fail(str(e), 500)


@router_teacher.post('/teacher5',summary='增加老师')
def create_teacher_api(teacher_name: str =Form(...,description="老师姓名"),
                       gender: str =Form(...,description="老师性别"),
                       phone: str =Form(...,description="老师电话"),
                       classes: str =Form(...,description="所带班级"),
                       role_id: int =Form(...,ge=1,le=5,description="老师职级"),
                       db =Depends(get_db)):
    try:
        res = teacher.create_teacher(db = db,
                                     teacher_name=teacher_name,
                                     gender=gender, phone=phone,
                                     classes=classes,
                                     role_id=role_id)
        if not res:
            return {"code": 404,
                    "message": "老师已存在,新增失败" }
        return {"code": 200,
                "message": '增加老师信息成功',
                "data": {"teacher_name": teacher_name}}

    except Exception as e:
        db.rollback()
        respon.fail(str(e), 500)





