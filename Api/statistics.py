from fastapi import APIRouter,Depends,Query
from database import get_db
from Dao import statistics
from Scheme import respon
from sqlalchemy.orm import Session

router_statistic = APIRouter()

# 查询年龄大于指定值的学生

@router_statistic.get('/statistic1',summary='年龄大于指定值的学生')
def get_students_over_age_api(age: int= Query(...,ge=1,le=100, description="年龄"),
                              page: int = Query(ge=1, description="分页查询页数"),
                              size: int = Query(ge=1, description="分页查询每页数据数"),
                              db: Session = Depends(get_db)):
    try:
        student_list = statistics.get_students_over_age(age =age,db = db)
        if not student_list:
            respon.fail('不存在符合条件的学生',404)
        skip = (page-1)*size
        lst = student_list[skip : skip + size]
        return {"code": 200,
                "message": '查询学生信息成功',
                "data": {"list": lst,
                         "page": page,
                         "size": size}}
    except Exception as e:
        respon.fail(str(e), 500)

# 统计每个班级的⼈数以及男⽣⼥⽣的⼈数

@router_statistic.get('/statistic2',summary='统计每个班级的⼈数以及男⽣⼥⽣的⼈数')
def get_students_count_gender_api(db = Depends(get_db)):
    try:
        stats = statistics.get_students_count_gender(db =db)
        if not stats:
            respon.fail('没有学生信息',404)
        return {"code": 200,
                "message": '查询信息成功',
                "data": stats}
    except Exception as e:
        respon.fail(str(e), 500)

###成绩统计
# 查询每次考试成绩都在80分以上的学⽣的编号，姓名和成绩(查询任意分数以上的同学)

@router_statistic.get('/statistic3',summary='统计每次考试成绩都在x分以上学生信息')
def get_students_all_scores_above_api(min_score: float,db = Depends(get_db)):
    try:
        stats = statistics.get_students_all_scores_above(db =db,min_score =min_score)
        if not stats:
            respon.fail('没有学生信息', 404)
        return {"code": 200,
                "message": '查询信息成功',
                "data": stats}
    except Exception as e:
        respon.fail(str(e), 500)

# 查询有两次以上不及格的学⽣的姓名，班级和不及格成绩（自定义不及格次数）

@router_statistic.get('/statistic4',summary='统计几次以上不及格的学⽣的姓名，班级和不及格成绩')
def get_students_fail_ge_times_api(fail_times: int,db = Depends(get_db)):
    try:
        stats = statistics.get_students_fail_ge_times(db =db,fail_times=fail_times)
        if not stats:
            respon.fail('没有学生信息', 404)
        return {"code": 200,
                "message": '查询信息成功',
                "data": stats}
    except Exception as e:
        respon.fail(str(e), 500)

# 统计每次考试每个班级的平均分，按照从⾼到低排序

@router_statistic.get('/statistic5',summary='每次考试每个班级的平均分')
def get_class_avg_per_exam_api(db = Depends(get_db)):
    try:
        stats = statistics.get_class_avg_per_exam(db =db)
        if not stats:
            respon.fail('没有学生信息', 404)
        return {"code": 200,
                "message": '查询信息成功',
                "data": stats}
    except Exception as e:
        respon.fail(str(e), 500)

# 统计就业薪资最⾼的前五名学⽣的姓名，班级和就业时间，就业公司
@router_statistic.get('/statistic6',summary='就业薪资最⾼的前五名')
def get_students_top5_salary_api(db = Depends(get_db)):
    try:
        stats = statistics.get_students_top5_salary(db =db)
        if not stats:
            respon.fail('没有学生信息', 404)
        return {"code": 200,
                "message": '查询信息成功',
                "data": stats}
    except Exception as e:
        respon.fail(str(e), 500)

# 统计每个学⽣的就业时⻓（offer下发时间-就业开放时间）
@router_statistic.get('/statistic7',summary='每个学⽣的就业时⻓')
def get_students_per_job_time_api(db = Depends(get_db)):
    try:
        stats = statistics.get_students_per_job_time(db =db)
        if not stats:
            respon.fail('没有学生信息', 404)
        return {"code": 200,
                "message": '查询信息成功',
                "data": stats}
    except Exception as e:
        respon.fail(str(e), 500)

# 统计每个班级的平均就业时⻓（只统计进⼊就业阶段的学⽣，也就是有就业开放时间）
@router_statistic.get('/statistic8',summary='每个班级的平均就业时⻓')
def get_class_per_job_time_api(db = Depends(get_db)):
    try:
        stats = statistics.get_class_per_job_time(db =db)
        if not stats:
            respon.fail('没有学生信息', 404)
        return {"code": 200,
                "message": '查询信息成功',
                "data": stats}
    except Exception as e:
        respon.fail(str(e), 500)
