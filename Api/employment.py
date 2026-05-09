from fastapi import APIRouter, Depends,HTTPException,Form
from datetime import date
from database import get_db
from Dao import employment as employment_dao  # 改名解决冲突
from Scheme import respon,employment as employment_scheme  # 改名解决冲突
from Model.table import Student,Class
router_employment = APIRouter()


# 增加学生就业状态
@router_employment.post('/employment1',
                        response_model=employment_scheme.EmploymentOut,#employment.改为employment_scheme.从中导入
                        summary='增加学生就业状态')
def  create_employment_api(
    student_id: int=Form(...),
    student_name: str=Form(...),
    class_id: int=Form(...),
    class_name: str=Form(...),
    open_time: date=Form(...),
    offer_time: date=Form(...),
    company: str=Form(...),
    salary: int=Form(...),
    db =Depends(get_db),
):
    try:
        if salary < 0:
            return respon.fail(msg="工资不能为负数", code=400)
        if offer_time < open_time:
            return respon.fail(msg="录用时间不能早于开通时间", code=400)

        # 检查学生是否存在
        student = db.query(Student).filter(Student.student_id == student_id).first()
        if not student:
            return respon.fail(msg="该学生不存在，无法添加就业信息", code=400)
        #班级存在校验
        class_obj = db.query(Class).filter(Class.class_id == class_id).first()
        if not class_obj:
            return respon.fail(msg=f"班级 {class_id} 不存在", code=400)
        new_emp = employment_dao.create_employment(db=db,
                                                  student_id = student_id,
                                                  student_name = student_name,
                                                  class_id = class_id,
                                                  class_name = class_name,
                                                  open_time = open_time,
                                                  offer_time = offer_time,
                                                  company = company,
                                                  salary = salary)
        return {"code": 200,
                "message": "就业信息创建成功",
                "data": {
                    "employment_id": new_emp.employment_id,
                    "student_name": new_emp.student_name,
                    "company": new_emp.company
                }}
    except HTTPException as e:
        raise e
    except Exception as e:
        # 打印完整错误栈，终端会显示真实原因
        import traceback
        traceback.print_exc()
        db.rollback()
        raise HTTPException(status_code=500, detail=f"服务器错误: {str(e)}")

# 学生编号、公司名字、工资范围查询学生就业信息

@router_employment.get('/employment2',summary='查询学生就业信息')#查询用get，原来post改为get
def get_employment_by_student_id_api(db =Depends(get_db),
                                 student_id: int = None,
                                 company: str = None,
                                 min_salary: int = None,
                                 max_salary: int = None
                                 ):
    try:
        if min_salary is not None and max_salary is not None:
            if min_salary > max_salary:
                respon.fail("最低工资不能大于最高工资", 400)
        employment_list= employment_dao.get_employment_by_student_id(db,
                                                    student_id=student_id,
                                                    company=company,
                                                    min_salary=min_salary,
                                                    max_salary=max_salary)
        if not employment_list:
            respon.fail("未查询到符合条件的就业信息", 404)
        return employment_list#返回真实列表，不是返回 list 关键字
    except Exception as e:
        db.rollback()#数据库异常回滚
        respon.fail(str(e), 500)


# 逻辑删除就业信息
@router_employment.delete('/employment3/{employment_id}',summary='删除就业信息')
def delete_employment_api(employment_id :int,
                      db =Depends(get_db)):
    try:
        res = employment_dao.delete_employment(db,employment_id=employment_id)
        if not res:
            respon.fail('无该学员就业信息,删除失败', 404)
        return {"code": 200,
                "message": '删除信息成功',
                "data":employment_id}
    except Exception as e:
        db.rollback()
        respon.fail(str(e), 500)

# 查找冗余
@router_employment.get('/employment4',summary='查找冗余信息')
def get_employment_detail_api(employment_id:int,db=Depends(get_db)):
    try:
        res = employment_dao.get_employment_detail(db,employment_id=employment_id)
        if not res:
            respon.fail('无该学员就业信息', 404)#描述改为无该学员冗余较好
        return {"code": 200,
                "message": '信息查询成功',
                "data": res}
    except Exception as e:
        respon.fail(str(e), 500)







