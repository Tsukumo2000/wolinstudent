from database import Base, engine
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship


# 学生表
class Student(Base):
    __tablename__ = "table_student"
    student_id = Column(Integer, primary_key=True, comment='学生编号',autoincrement=True)
    student_name = Column(String(32), nullable=False, comment='姓名')
    gender = Column(String(8), comment='性别')
    age = Column(Integer, comment='年龄')
    class_id = Column(Integer, ForeignKey("table_class.class_id"),nullable=False, comment='班级编号')
    native_place = Column(String(64), comment='籍贯')
    school = Column(String(64), comment='毕业院校')
    major = Column(String(64), comment='专业')
    education = Column(String(32), comment='学历')
    admission_time = Column(Date, comment='入学时间')
    graduation_time = Column(Date, comment='毕业时间')
    counselor_id = Column(Integer, comment='顾问编号')
    student_is_deleted = Column(Integer, default=0, comment='逻辑删除 0/1')
    role_id = Column(Integer,ForeignKey("role.role_id"), default=1, comment='角色ID')
    #关系
    class_info = relationship("Class", back_populates="students")
    scores = relationship("Score", back_populates="student")
    employments = relationship("Employment", back_populates="student")
    role = relationship("Role", back_populates="students")


# 成绩表
class Score(Base):
    __tablename__ = "table_score"
    score_id = Column(Integer, primary_key=True,autoincrement=True)
    class_id = Column(Integer,ForeignKey("table_class.class_id"), comment='班级编号')
    student_id = Column(Integer, ForeignKey("table_student.student_id"), comment='学生编号')
    exam_order = Column(Integer, nullable=False, comment='考核序次')
    score = Column(Float, comment='成绩')
    score_is_deleted = Column(Integer, default=0, comment='逻辑删除 0/1')
    #关系
    student = relationship("Student", back_populates="scores")

# 就业表
class Employment(Base):
    __tablename__ = "table_employment"
    employment_id = Column(Integer, primary_key=True,autoincrement=True)
    student_id = Column(Integer, ForeignKey("table_student.student_id"), comment='学生编号')
    student_name = Column(String(32), comment='姓名',nullable=False)
    class_id = Column(Integer, ForeignKey("table_class.class_id"), comment='班级编号')
    class_name = Column(String(30))
    open_time = Column(Date, comment='就业开放时间')
    offer_time = Column(Date, comment='offer下发时间')
    company = Column(String(64), comment='就业公司')
    salary = Column(Float, comment='就业薪资',nullable=False)
    employment_is_deleted = Column(Integer, default=0, comment='逻辑删除 0/1')
    #关系
    student = relationship("Student", back_populates="employments")
# 班级表
class Class(Base):
    __tablename__ = "table_class"
    class_id = Column(Integer, primary_key=True, comment='班级编号',autoincrement=True)
    class_name = Column(String(30))
    start_time = Column(Date, comment='开课时间')
    teacher_id = Column(Integer, ForeignKey("table_teacher.teacher_id"), comment='授课老师')
    head_teacher_id = Column(Integer, ForeignKey("table_teacher.teacher_id"), comment='班主任')
    class_is_deleted = Column(Integer, default=0, comment='逻辑删除 0/1')

    #关系
    students = relationship("Student", back_populates="class_info")
    teacher = relationship("Teacher", foreign_keys=[teacher_id], back_populates="teach_classes")
    head_teacher = relationship("Teacher", foreign_keys=[head_teacher_id], back_populates="head_classes")
# 教师表
class Teacher(Base):
    __tablename__ = "table_teacher"
    teacher_id = Column(Integer, primary_key=True, comment='教师编号',autoincrement=True)
    teacher_name = Column(String(32), comment='姓名',nullable=False)
    gender = Column(String(8), comment='性别')
    phone = Column(String(16), comment='电话')
    classes = Column(String(30), comment='带班列表')
    role_id = Column(Integer,ForeignKey("role.role_id"), comment='等级权限')
    teacher_is_deleted = Column(Integer, default=0, comment='逻辑删除 0/1')
    #关系
    role = relationship("Role",foreign_keys=[role_id], back_populates="teachers")
    teach_classes = relationship("Class", foreign_keys=[Class.teacher_id], back_populates="teacher")
    head_classes = relationship("Class", foreign_keys=[Class.head_teacher_id], back_populates="head_teacher")


# 用户表（你文档写 table_user，注意和学生表重名，我保留原名）
class User(Base):
    __tablename__ = "table_user"
    user_id = Column(Integer, primary_key=True, autoincrement=True,comment='用户编号')
    username = Column(String(30), comment='用户名',nullable=False)
    password = Column(String(30), comment='密码',nullable=False)
    role_id = Column(Integer, ForeignKey("role.role_id"),comment='角色ID')
    user_is_deleted = Column(Integer, default=0, comment='逻辑删除 0/1')
    #关系
    role = relationship("Role", back_populates="users")

# 身份表（角色表）
class Role(Base):
    __tablename__ = "role"

    role_id = Column(Integer, primary_key=True, comment='角色ID',autoincrement=True)
    job = Column(String(30), comment='角色名称',nullable=False)
    role_is_deleted = Column(Integer, default=0, comment='逻辑删除 0/1')
    #关系
    users = relationship("User", back_populates="role")
    teachers = relationship("Teacher", back_populates="role")
    students = relationship("Student", back_populates="role")