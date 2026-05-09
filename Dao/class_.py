from sqlalchemy.orm import Session
from datetime import date
from Model.table import Class,Teacher

# 创建班级
def create_class(
    db: Session,
    class_name:str,#班级名称
    start_time: date,#开课时间
    teacher_id: int,#授课老师
    head_teacher_id: int#班主任
):
    try:
        a = db.query(Class).filter(Class.teacher_id==teacher_id,Class.head_teacher_id==head_teacher_id,Class.class_is_deleted==0).first()
        #校验班级表：班级老师,班主任是否存在
        if a :
            #存在则返回
            return False


        #校验老师表：老师班主任是否存在
        #Teather.teacher_id 包含Class.head_teacher_id
        b = db.query(Teacher).filter(Teacher.teacher_is_deleted==0,Teacher.teacher_id == teacher_id).first()
        if b is None:#判断创建的班级是否不存在且老师这个人也存在，满足条件则添加新班级
            return False
        new_class = Class(
            class_name=class_name,
            start_time=start_time,
            teacher_id=teacher_id,
            head_teacher_id=head_teacher_id,
            class_is_deleted=0
            )

        db.add(new_class)
        db.commit()
        db.refresh(new_class)
        return True


    except Exception as e:
        print(f'Dao.class_创建班级: {e}')
        db.rollback()#添加回滚
        return False#添加返回值


# 查询班级列表
def get_classes(db: Session):
    try:
        return db.query(Class).filter(Class.class_is_deleted == 0).all()
    except Exception as e:
        print(f'Dao.class_查询班级: {e}')
        return False

# 查询单个班级详情
def get_class(db: Session, class_id: int):
    try:
        a = db.query(Class).filter(
            Class.class_id == class_id,
            Class.class_is_deleted == 0
        ).first()
        if a is not None:#判断对象a是否为空
            return a #不为空，则输出对象
        return False
    except Exception as e:
        print(f'Dao.class_查询单个班级: {e}')
        return False

# 更新班级信息
def put_class(db: Session, class_id: int, class_info: dict):
    try:
        data_class = db.query(Class).filter(Class.class_id == class_id,
                                            Class.class_is_deleted == 0).first()
        #通过class_id 查询到对应班级信息给一个对象
        if data_class:#若对象不为空
            if "class_name" in class_info:#如果键在字典中则，通过键修改值
                data_class.class_name = class_info.get("class_name")
            if "start_time" in class_info:
                data_class.start_time = class_info.get("start_time")
            if "teacher_id" in class_info:
                data_class.teacher_id = class_info.get("teacher_id")
            if "head_teacher_id" in class_info:
                data_class.head_teacher_id = class_info.get("head_teacher_id")

            db.commit()#修改完后统一提交
            db.refresh(data_class)
            return True #返回
        return False
    except Exception as e:
        print(f'Dao.class_更新班级信息: {e}')
        db.rollback()#回滚
        return False

# 逻辑删除班级
def delete_class(db: Session, class_id: int):
    try:
        data_class = db.query(Class).filter(Class.class_id == class_id,
                                            Class.class_is_deleted == 0).first()
        if data_class:
            data_class.class_is_deleted = 1
            db.commit()
            db.refresh(data_class)
            return True
        return False
    except Exception as e:
        print(f'Dao.class_逻辑删除班级: {e}')
        db.rollback()  # 添加回滚
        return False  # 添加返回值