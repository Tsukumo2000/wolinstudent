import os
from fastapi import APIRouter, Query, Depends, HTTPException
from starlette.responses import RedirectResponse

from database import get_db, Session
from Dao.user import get_user, delete_user, update_user, create_user
from Scheme import respon

router_users =APIRouter()

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:8000")

@router_users.get('/')
def check_user(name:str ,
               password:int ,
               db=Depends(get_db)):
    user = get_user(db,name,password)
    if user.role.job=='管理员':
        return RedirectResponse(f"{FRONTEND_BASE_URL}/View/GuanLi_admin/GuanLi_admin.html")
    if user.role.job=='学生':
        return RedirectResponse(f"{FRONTEND_BASE_URL}/View/GuanLi_student/GuanLi_student.html")
    if user.role.job=='授课教师':
        return RedirectResponse(f"{FRONTEND_BASE_URL}/View/GuanLi_teacher/GuanLi_teacher.html")
    if user.role.job=='顾问':
        return RedirectResponse(f"{FRONTEND_BASE_URL}/View/GuanLi_consultant/GuanLi_consultant.html")
    if user.role.job=='班主任':
        return RedirectResponse(f"{FRONTEND_BASE_URL}/View/GuanLi_head/GuanLi_head.html")


    # if not user:
    #     respon.fail("用户不存在","401")
    # return {"code": 200, "msg": "登录成功", "role": user.role.job}

# {name}/{password}


@router_users.post('/user1',summary='增加用户')
def create_user_api(usernames:str ,
                     passwords:int ,
                     role_id :int ,
                     db =Depends(get_db)):
    try:
        result = create_user(db=db,
                             usernames =usernames,
                             passwords =passwords,
                             role_id =role_id)
        if not result:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": 400,
                    "message": '用户成绩录入失败'})
        return {"code": 200,
                "message": '用户录入成功',
                "data": {"usernames": usernames}}
    except Exception as e:
        db.rollback()
        msg = str(e)
        if msg != "用户名已存在":
            respon.fail(str(e), 400)
        respon.fail(str(e), 500)

@router_users.delete("/user2",summary='用户删除管理')
def delete_user_api(username: str,
                     db:Session = Depends(get_db)):
    try:
        result = delete_user(
            db=db,
            username = username)
        if not result:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": 400,
                    "message": '用户删除失败'})
        return {"code": 200,
                "message": '用户删除成功'}
    except Exception as e:
        db.rollback()
        msg = str(e)
        if msg != "该用户不存在，无法修改":
            respon.fail(str(e), 400)
        respon.fail(str(e), 500)


#修改用户
@router_users.put("/update", summary="用户修改")
def update_user_api(
        user_id: int,
        username: str,
        password: str,
        role_id: int = 1,
        db=Depends(get_db)
):
    try:
        update_user(
            db=db,
            user_id=user_id,
            username=username,
            password=password,
            role_id=role_id
        )
        return {
            "code": 200,
            "msg": "用户修改成功"
        }

    # 业务异常直接抛出
    except HTTPException:
        raise

    # 服务异常回滚
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={"code": 500, "message": f"服务器异常：{str(e)}"}
        )