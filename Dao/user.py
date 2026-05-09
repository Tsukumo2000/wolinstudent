from sqlalchemy.orm import Session, sessionmaker
from Model.table import User
from fastapi import Query, HTTPException

# 从用户表中查对应的信息

def get_user(db: Session,
             usernames:str =Query(...),
             passwords:int =Query(...)):
    user = db.query(User).filter(User.username==usernames,User.password==passwords).first()
    return user

# 增加用户
def create_user(db: Session,
                 usernames:str ,
                 passwords:int ,
                 role_id :int = 1 ,ge=1,le=5):
    user = db.query(User).filter(User.username == usernames,User.user_is_deleted==0).first()
    if user:
        respon.fail("用户名已存在", 400)
    new_user = User(username =usernames,
                    password =passwords,
                    role_id =role_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return True


# 删除用户
def delete_user(db: Session,
                username: str):
    user = db.query(User).filter(User.username == username, User.user_is_deleted == 0).first()
    if not user:
        respon.fail("用户名不存在,无法删除", 400)
    user.user_is_deleted = 1
    db.commit()
    return True

#修改用户
def update_user(db:Session,
                   user_id : int,
                   username:str,password:int,role_id:int=1):
    user = db.query(User).filter(User.user_id ==user_id,User.user_is_deleted ==0).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail={"code": 400, "message": "用户不存在"}
        )
    user.username = username
    user.password = password
    user.role_id = role_id
    db.commit()
    db.refresh(user)
    return True

