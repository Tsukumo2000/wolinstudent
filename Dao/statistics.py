from sqlalchemy.orm import Session
from Model.table import Student,Class,Score,Employment
from sqlalchemy import func, case, text
from datetime import datetime

###基本信息统计
#查询30岁以上的学员信息（查询任意年龄)
# 查询年龄大于指定值的学生
def get_students_over_age(db: Session, age: int,page :int =1,size :int =10):
    skip = (page - 1) * size  # 跳过多少条
    take = size  # 取多少条
    res = (db.query(Student).filter(Student.age > age,       # 这里用传进来的参数
                                     Student.student_is_deleted == 0 ).order_by
                                   (Student.student_id).offset(skip).limit
                                   (take).all()) # 逻辑删除过滤
    return res
#select * from Student
#where Student.age > age


# 统计每个班级的⼈数以及男⽣⼥⽣的⼈数
def get_students_count_gender(db: Session):
    stats = db.query(   Class.class_id.label("班级编号"),
                        func.count(Student.student_id).label("总人数"),
                        # 统计男生
                        func.sum(case([(Student.gender == "男", 1)], else_=0)).label("男生人数"),
                        # 统计女生
                        func.sum(case([(Student.gender == "女", 1)], else_=0)).label("女生人数")
                        ).join(Student, Class.class_id == Student.class_id  # 班级表 关联 学生表
                        ).filter(Student.student_is_deleted == 0  # 只统计未删除的学生
                        ).group_by(Class.class_id).all()  # 按班级分组
    return stats

# select class_id  班级编号,COUNT(*)  总人数,
#     SUM(gender = '男')  男生人数,SUM(gender = '女')  女生人数
# FROM table_student
# WHERE student_is_deleted = 0
# GROUP BY class_id
# ORDER BY class_id;


###成绩统计
#查询每次考试成绩都在80分以上的学⽣的编号，姓名和成绩(查询任意分数以上的同学)
def get_students_all_scores_above(db: Session, min_score: float):
    # 按学生分组，算出每个学生的最低分
    res  = db.query(Student.student_id,Student.student_name,func.min(Score.score).label("最低分")  # 求最低分
    ).join(Score).filter(
        Student.student_is_deleted == 0,Score.score_is_deleted == 0
    ).group_by(Student.student_id, Student.student_name
    ).having(func.min(Score.score) >= min_score).all()  # 最低分都达标 = 全部达标
    return res

# select s.student_id,s.student_name,sc.score
# FROM student JOIN score sc
# ON s.student_id = sc.student_id
# WHERE AND s.student_id IN (select student_id
#                               FROM score
#                               WHERE score_is_deleted = 0
#                               GROUP BY student_id
#                               HAVING MIN(score) >= 80)
# ORDER BY s.student_id;

#查询有两次以上不及格的学⽣的姓名，班级（自定义不及格次数）
def get_students_fail_ge_times(db: Session, fail_times: int):
    student_ids = (db.query(Student.student_id).join
           (Score,Student.student_id == Score.student_id).join
           (Class,Student.class_id == Class.class_id)
            .filter(Score.score < 60,Student.student_is_deleted == 0,Score.score_is_deleted == 0
            ).group_by(Student.student_id,Class.class_id
            ).having(func.count(Score.score_id) >= fail_times  # 自定义次数
            ).subquery())

    res = (db.query(
        Student.student_name.label("学生姓名"),
        Class.class_id.label("班级编号"),
        Score.score.label("不及格分数"),
        Score.exam_order.label("考次")
        ).join(Score, Student.student_id == Score.student_id
        ).join(Class, Student.class_id == Class.class_id
        ).filter(Student.student_id.in_(student_ids),  # 只查符合条件的学生
        Score.score < 60,Student.student_is_deleted == 0,Score.score_is_deleted == 0).all())
    return res

# select s.student_name  学生姓名,s.class_id  班级编号,sc.score  不及格成绩
# FROM table_student s
# JOIN table_score sc ON s.student_id = sc.student_id
# WHERE sc.score < 60  AND s.student_id IN (
#                                              select student_id
#                                              FROM table_score
#                                              WHERE score < 60 AND score_is_deleted = 0
#                                              GROUP BY student_id
#                                              HAVING COUNT(*) >= 2  -- 这里 2 可以改成任意次数);

# 统计每次考试每个班级的平均分，按照从⾼到低排序
def get_class_avg_per_exam(db: Session):
    res = (db.query(Class.class_id.label("班级编号"),Score.exam_order.label("考核序次"),
            func.avg(Score.score).label("平均分")).join
            (Student, Student.student_id == Score.student_id).join
            (Class, Class.class_id == Student.class_id).filter
                (Score.score_is_deleted == 0,
                Student.student_is_deleted == 0,
                Class.class_is_deleted == 0
                ).group_by(
                    Class.class_id,
                            Score.exam_order
                          ).order_by(func.avg(Score.score).desc()).all())
    return res


# select sc.exam_order  考试次数, s.class_id  班级,AVG(sc.score)  平均分
# FROM score sc
# JOIN student s ON sc.student_id = s.student_id
# GROUP BY sc.exam_order,s.class_id
# ORDER BY   平均分 DESC;



# 统计就业薪资最⾼的前五名学⽣的姓名，班级和就业时间，就业公司
def get_students_top5_salary(db: Session):
    res = db.query(Employment).order_by(Employment.salary.desc()).limit(5).all()
    List=[]
    for i in res:
        dict = {}
        dict['student_name']=i.student_name
        dict["class_id"] = i.class_id
        dict["offer_time"] = i.offer_time
        dict["company"] = i.company
        List.append(dict)
    res=List
    return res

# 统计每个学⽣的就业时⻓（offer下发时间-就业开放时间）
def get_students_per_job_time(db: Session):
    res = db.query(Employment).order_by(Employment.salary.desc()).limit(5).all()
    List=[]
    List2=[]
    for i in res:
        dict = {}
        dict['student_name']=i.student_name
        dict["job_time"] = (i.offer_time-i.open_time)/ 86400
        # dict["job_time"] = func.timestampdiff(text("DAY"), i.open_time,i.offer_time)
        List.append(dict)
    res=List
    return res


# 统计每个班级的平均就业时⻓（只统计进⼊就业阶段的学⽣，也就是有就业开放时间）
def get_class_per_job_time(db: Session):
    res = db.query(
        Employment.class_id,
        func.avg(
            func.timestampdiff(text("DAY"), Employment.open_time, Employment.offer_time)
        ).label("avg_job_time")
    ).group_by(Employment.class_id).all()
    return res