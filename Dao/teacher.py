
from sqlalchemy.orm import Session
from Model.table import Teacher
from Scheme import respon


def get_teacher_all(db :Session,page :int =1,size :int =10):
    skip = (page - 1) * size
    total = db.query(Teacher).count()
    teacher_list = db.query(Teacher).filter(Teacher.teacher_is_deleted ==0).order_by(Teacher.teacher_id).limit(size).offset(skip).all()
    return teacher_list,total



def get_teacher_message(db :Session,
                        fieldname:str ,
                        keyword :str,
                        page :int =1,size :int =10):
    teacher_fieldname = ['teacher_id','teacher_name','gender','phone','classes','role_id']

    skip = (page - 1) * size
    column = getattr(Teacher, fieldname)
    total = db.query(Teacher).filter(Teacher.teacher_is_deleted == 0,
                                     column.like(f"%{keyword}%")).count()
    teacher_list = db.query(Teacher).filter(Teacher.teacher_is_deleted == 0,
                                            column.like(f"%{keyword}%")).order_by(Teacher.teacher_id).limit(size).offset(skip).all()
    if not teacher_list:
        respon.fail("无符合条件的老师信息", 404)
    return teacher_list ,total



def update_teacher(db:Session,
                   teacher_id : int,
                   update_dict : dict):
    teacher = db.query(Teacher).filter(Teacher.teacher_id ==teacher_id,
                                       Teacher.teacher_is_deleted ==0).first()
    if not teacher:
        respon.fail("该老师不存在", 404)
    if "teacher_name" in update_dict:
        teacher.teacher_name = update_dict["teacher_name"]
    if "gender" in update_dict:
        teacher.gender = update_dict["gender"]
    if "phone" in update_dict:
        teacher.phone = update_dict["phone"]
    if "classes" in update_dict:
        teacher.classes = update_dict["classes"]
    if "role_id" in update_dict:
        teacher.role_id = update_dict["role_id"]
    db.commit()
    db.refresh(teacher)
    return True


def delete_teacher(db: Session, teacher_id: int):
    teacher_id_2 = db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()
    if not teacher_id_2:
        respon.fail("该老师不存在", 404)
    if teacher_id_2.teacher_is_deleted == 1:
        respon.fail("该老师已被删除", 404)
    teacher_id_2.teacher_is_deleted = 1
    db.commit()
    db.refresh(teacher_id_2)
    return True



def create_teacher(db: Session,
                   teacher_name: str, gender: str,
                   phone: str,
                   classes: str,
                   role_id: int, teacher_is_deleted: int = 0
                   ):
    exist_teacher = db.query(Teacher).filter(Teacher.teacher_name == teacher_name,Teacher.teacher_is_deleted == 0).first()
    if exist_teacher:
        return False
    new_teacher = Teacher(
        teacher_name=teacher_name,
        gender=gender,
        phone=phone,
        classes=classes,
        role_id=role_id,
        teacher_is_deleted=teacher_is_deleted
    )

    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return True
