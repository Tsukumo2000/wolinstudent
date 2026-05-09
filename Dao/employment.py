from sqlalchemy.orm import Session
from datetime import date
from Model.table import Employment
from Model.table import Student
from Model.table import Class
# 记录学生就业状态
def create_employment(
    db: Session,
    student_id: int,# 学⽣编号
    student_name: str,# 学⽣姓名
    class_id: int,# 班级编号
    class_name:str,#班级名称  后加的
    open_time: date,# 就业开放时间
    offer_time: date,#offer下发时间
    company: str,#就业公司
    salary: int#就业薪资
):
    try:
        new_emp = Employment(
            student_id=student_id,
            student_name=student_name,
            class_id=class_id,
            class_name=class_name,
            open_time=open_time,
            offer_time=offer_time,
            company=company,
            salary=salary,
            employment_is_deleted=0
        )
        db.add(new_emp)
        db.commit()
        db.refresh(new_emp)
        return new_emp  # 返回创建的对象
    except Exception as e:
        db.rollback()  # 异常时回滚事务
        raise e  # 把异常抛给上层接口处理


# 学生编号、公司名字、工资范围查询学生就业信息
def get_employment_by_student_id(
    db: Session,
    student_id: int = None,
    company: str = None,
    min_salary: int = None,#最小薪资
    max_salary: int = None#最大薪资
):
    query = db.query(Employment).filter(Employment.employment_is_deleted == 0)

    if student_id:
        query = query.filter(Employment.student_id == student_id)
    if company:
        query = query.filter(Employment.company == company)
    if min_salary is not None:
        query = query.filter(Employment.salary >= min_salary)
    if max_salary is not None:
        query = query.filter(Employment.salary <= max_salary)

    return query.all()


# 查询单个学生就业信息
def get_employment(db: Session, employment_id: int):
    return db.query(Employment).filter(
        Employment.employment_id == employment_id,
        Employment.employment_is_deleted == 0# 只删除未删除的数据
    ).first()


# 修改就业信息
def put_employment(db: Session, employment_id: int, employment: dict):
    data_employment = db.query(Employment).filter(Employment.employment_id == employment_id,
                                                  Employment.employment_is_deleted == 0).first()
    if data_employment:
        if "company" in employment:
            data_employment.company = employment.get("company")
        if "salary" in employment:
            data_employment.salary = employment.get("salary")
        if "open_time" in employment:
            data_employment.open_time = employment.get("open_time")
        if "offer_time" in employment:
            data_employment.offer_time = employment.get("offer_time")

        db.commit()
        return True
    return False
# 逻辑删除就业信息
def delete_employment(db: Session, employment_id: int):
    data_employment = db.query(Employment).filter(Employment.employment_id == employment_id,
                                                  Employment.employment_is_deleted == 0).first()
    if data_employment:
        data_employment.employment_is_deleted = 1
        db.commit()
        return True
    return False
# 查询学⽣姓名(冗余)、学⽣班级(冗余)
def get_employment_detail(db: Session, employment_id: int):
    emp = db.query(Employment).filter(
        Employment.employment_id == employment_id,
        Employment.employment_is_deleted == 0
    ).first()
    
    if not emp:
        return None
        
    # 获取学生姓名
    student = db.query(Student).filter(Student.student_id == emp.student_id,
                                       Student.student_is_deleted == 0).first()
    student_name = student.student_name if student else None
    
    # 获取班级名称
    class_obj = db.query(Class).filter(Class.class_id == emp.class_id,
                                       Class.class_is_deleted == 0).first()
    class_name = class_obj.class_name if class_obj else None
    
    # 返回包含冗余字段的对象
    return {
        "employment_id": emp.employment_id,
        "student_name": student_name,
        "class_name": class_name,
        "company": emp.company,
        "salary": emp.salary,
        "offer_time": emp.offer_time
    }
