from sqlalchemy.orm import Session
from sqlalchemy import func
from Model.table import Score
from Model.table import Student,Class
from Scheme import respon



def create_score(
    db: Session,
    student_id: int,
    exam_order: int,
    score: float
):

    student = db.query(Student).filter(Student.student_id == student_id,
                                       Student.student_is_deleted == 0).first()
    if not student:
        respon.fail("学生不存在", 400)

    class_id = student.class_id
    class_info = db.query(Class).filter(Class.class_id == class_id,
                                        Class.class_is_deleted == 0).first()
    if not class_info:
        respon.fail("班级不存在", 400)

    exist_score = db.query(Score).filter(Score.student_id == student_id,
                                         Score.exam_order == exam_order,
                                         Score.score_is_deleted == 0).first()
    if exist_score:
        respon.fail("该学生本次考试成绩已存在，不可重复添加", 400)

    # class_info = db.query(Class).filter(Class.class_id == class_id,Class.class_is_deleted == 0).first()
    # if not class_info:
    #     respon.fail("班级不存在", 400)
    #
    # if student.class_id != class_id:
    #     respon.fail("学生不属于该班级", 400)

    new_score = Score(
        student_id=student_id,
        exam_order=exam_order,
        score=score,
        class_id=class_id,
        score_is_deleted=0
    )
    db.add(new_score)
    db.commit()
    db.refresh(new_score)
    return True

# def create_score(
#         db: Session,
#         score_data: ScoreCreate
#     ):
#     student_id = score_data.student_id
#     class_id = score_data.class_id
#     exam_order = score_data.exam_order
#     score = score_data.score
#
#     student = db.query(Student).filter(Student.student_id == student_id, Student.student_is_deleted == 0).first()
#     if not student:
#         respon.fail("学生不存在", 400)
#     class_info = db.query(Class).filter(Class.class_id == class_id, Class.class_is_deleted == 0).first()
#     if not class_info:
#         respon.fail("班级不存在", 400)
#     if student.class_id != class_id:
#         respon.fail("学生不属于该班级", 400)
#
#     new_score = Score(
#         student_id=student_id,
#         exam_order=exam_order,
#         score=score,
#         class_id=class_id,
#         score_is_deleted=0
#     )
#     db.add(new_score)
#     db.commit()
#     return True




def update_score(
        db: Session,
        student_id: int,
        exam_order: int,
        score: float
):
    student = db.query(Student).filter(Student.student_id == student_id,
                                       Student.student_is_deleted == 0).first()
    if not student:
        respon.fail("学生不存在", 400)

    class_id = student.class_id
    class_info = db.query(Class).filter(Class.class_id == class_id,
                                        Class.class_is_deleted == 0).first()
    if not class_info:
        respon.fail("班级不存在", 400)

    score_record = db.query(Score).filter(Score.student_id == student_id,
                                          Score.exam_order == exam_order,
                                          Score.score_is_deleted == 0).first()
    if not score_record:
        respon.fail("该学生此轮考试成绩不存在，无法修改", 400)

    score_record = db.query(Score).filter(Score.student_id == student_id,
                                          Score.exam_order == exam_order,
                                          Score.score_is_deleted == 0,
                                          Score.score==score).first()
    if  score_record:
        respon.fail("该学生此轮考试成绩与修改成绩相同，无需修改", 400)

    # if student.class_id != class_id:
    #     respon.fail("学生不属于该班级", 400)

    score_record.score =score
    db.commit()
    db.refresh(score_record)
    return True


def delete_score(
    db: Session,
    student_id: int,
    exam_order: int):

    student = db.query(Student).filter(Student.student_id == student_id,
                                       Student.student_is_deleted == 0).first()
    if not student:
        respon.fail("学生不存在", 400)

    score_record = db.query(Score).filter(Score.student_id == student_id,
                                          Score.exam_order == exam_order).first()
    if not score_record:
        respon.fail("该学生此轮考试成绩不存在，无法删除", 400)
    if score_record.score_is_deleted == 1:
        respon.fail("该成绩已删除，请勿重复删除", 400)

    score_record.score_is_deleted =1
    db.commit()
    return True



def get_score(db: Session,
              student_id: int,
              exam_order: int):

    student = db.query(Student).filter(Student.student_id == student_id,
                                       Student.student_is_deleted == 0).first()
    if not student:
        respon.fail("学生不存在", 400)

    score_record = db.query(Score).filter(Score.student_id == student_id,
                                          Score.exam_order == exam_order,
                                          Score.score_is_deleted == 0).first()
    if not score_record:
        respon.fail("该学生成绩不存在", 400)

    score_record = db.query(Score).filter(Score.student_id == student_id,
                                          Score.is_deleted == 0).first()
    return score_record


def get_all_score(db: Session,
                  class_id: int):
    class_info = db.query(Class).filter(Class.class_id == class_id,
                                        Class.class_is_deleted == 0).first()
    if not class_info:
        respon.fail("班级不存在", 400)
    avg_score = db.query(Score.exam_order,func.avg(Score.score).label('avg_score')).join(Student).filter(Score.class_id ==class_id,
                                                                                                         Score.score_is_deleted == 0,
                                                                                                         Student.student_is_deleted ==0).group_by(Score.exam_order).all()
    all_score = db.query(Score).join(Student).filter(Score.class_id ==class_id,
                                                     Score.score_is_deleted == 0,
                                                     Student.student_is_deleted ==0).order_by(Score.exam_order, Score.student_id).all()
    return all_score,avg_score

    # all_score = db.query(Score).filter(Score.class_id == class_id,Score.is_deleted == 0).all()
    #
    # avg_score = (db.query(func.avg(Score.score)).filter(Score.class_id == class_id,Score.is_deleted == 0).scalar())
    # return all_score,avg_score


