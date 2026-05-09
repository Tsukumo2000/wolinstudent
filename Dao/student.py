
#学生方法模块
from sqlalchemy.orm import Session
#导包：引入会话方法(需要会话为我们运输数据)
from Model.table import Student,Role,Class,Employment
#导入表模块
from sqlalchemy import Date



#学生增加方法（返回bool值，表示成功或者失败）
def create_student(db:Session,student_name:str,
                   gender:str,age:int,
                   class_id:int,native_place:str,
                   school:str,major:str,
                   education:str,admission_time:Date,
                   graduation_time:Date,counselor_id:int,
                   role_id:int,student_is_deleted:int=0
                   ):

    # 根据学生id查询学生，若存在返回False，若不存在则返回True
    try:
        role_id_1 = db.query(Role).filter(Role.role_id==role_id,Role.role_is_deleted == 0).first()
        if role_id_1 is None:# 角色不存在 → 不能创建
            return False
        class_id_1 = db.query(Class).filter(Class.class_id==class_id,Class.class_is_deleted == 0).first()
        if class_id_1 is None:
            return False


        #若存在则返回一个对象（为True）

        #逻辑判断

            #接入传入的新属性，创建一个新的学生对象
        new_student =Student(
                   student_name = student_name,
                   gender = gender , age = age,
                   class_id = class_id , native_place = native_place,
                   school = school , major = major,
                   education = education , admission_time = admission_time,
                   graduation_time = graduation_time , counselor_id = counselor_id,
                   student_is_deleted = student_is_deleted , role_id = role_id
                                )
        db.add(new_student)#添加对象
        db.commit()#提交对象
        db.refresh(new_student)#刷新数据库
        return True

    except Exception as a:
        print(f'学生增加方法异常：{a}')#开发人员观察异常
        db.rollback()
        return False




#学生删除方法（返回bool值，表示成功或者失败）
def delete_stundent(db: Session, student_id: int):
    try:
        student_id_2 = db.query(Student).filter(Student.student_id == student_id , Student.student_is_deleted == 0).first()
        #判断是否在表中有这个人
        if student_id_2 is not None:
            # 逻辑删除
            student_id_2.student_is_deleted = 1
            #将标记修改为一，使其查不到
            db.commit()
            db.refresh(student_id_2)
            return True
        return False
    except Exception as a:
        print(f'学生删除方法异常：{a}')#开发人员观察异常
        db.rollback()
        return False


#学生修改方法（返回bool值，表示成功或者失败）
def update_student(db:Session,student_id:int ,**kwargs):
    try:
        #根据学生id查询学生
        student_id_2 = db.query(Student).filter(Student.student_id == student_id , Student.student_is_deleted == 0).first()
        if student_id_2 is not None:

             #for key,value in kwargs.items():
                  #.items()获取字典键值对
                  #student_id_2.key = value
                  #此方法会重新添加一个键为：key，值为：value的新字段，并不会在原键上修改值

             db.query(Student).filter(Student.student_is_deleted == 0 , Student.student_id==student_id).update(kwargs)
             #update({...})里面必须是字典,必须加 filter()，否则 全表更新,必须 db.commit() 才会真正保存
             db.commit()
             db.refresh(student_id_2)
             return True
             #循环结束统一提交

        return False
    except Exception as a:
        print(f'学生修改方法异常:{a}')#开发人员观察异常
        db.rollback()
        return False



#学生查询方法
#1.查询单条（返回对象）
def get_student_by_id(db:Session,student_id:int):
    try:
        student_id_1 = db.query(Student).filter(Student.student_id == student_id , Student.student_is_deleted == 0).first()
        # 若存在则返回一个对象（为True）
        if student_id_1 is not None:
            return student_id_1
        else:
            return False
    except Exception as a:
        print(f'查询单条方法异常：{a}')#开发人员观察异常
        db.rollback()
        return False



#2.(统计)查询列表（多条学生信息）（返回列表对象）
def get_student_list(db:Session,page:int=1,size:int=10):
    '''
    (统计)查询列表（多条学生信息）
    :param db: 会话
    :param page: 页码
    :param size: 每页条数（长度）
    :return: True/False
    '''
    try:
        list1=db.query(Student).filter(Student.student_is_deleted == 0).order_by(Student.student_id).offset((page-1)*size).limit(size).all()
        #.offset(n) 是：跳过前面 n 条数据，从第 n+1 条开始取
        #因为我们是从多少页取，则是跳过：（前n-1页乘以每页条数），又因为索引从零开始：则(page-1)*size不用加壹
        #limit(n):取N条
        return list1

    except Exception as a:
        print(f'查询列表异常:{a}')#开发人员观察异常
        db.rollback()
        return False

#3.多关键词查询
def get_student_More(db:Session,**kwargs):
    '''
    多关键词查询
    :return:True/False
    '''
    try :
        #遍历传入的不定长参数（字典），并判断是否含有student_id,若有则按照student_id查询
        for k,v in kwargs.items():#遍历你传进来的所有查询条件
            a = db.query(Student).filter(Student.student_id == v , Student.student_is_deleted == 0).first()
            #遍历传入的值，与数据库表的student_id
            if k=='student_id' and a:
                return a
        else:
            #最初设想：将传入的kwargs字典的每一个键值对遍历出来，
            #        并再将数据库表的每一行数据转成字典，并以元素的形式存入列表a：[{},{}]
            # 遍历列表a，  再将kwargs字典遍历出的每一个键值对，都判断一遍是否全在a[n](元素)中
            #但实现繁杂，转而思考是否可以判断一个字典是否可以在另一个字典的内：
            #即一个字典包含另一个字典
            #通过查询资料发现一个方法： a.items() <= b.items()：判断dict_a 是 dict_b 的子集（键 + 值都包含）

            b = db.query(Student).filter(Student.student_is_deleted == 0).all()#获取表数据，转换为一个对象：该语句输出的是：一个列表，里面装着 N 个 Student 类的实例对象（ORM 对象）
                                       #b = [<Student 1号对象>,<Student 2号对象>,<Student 3号对象>]
                                       #可遍历，不可直接通过索引取值

            # #通过列表表达式，将每行转字典，组成列表
            # result = [stu.dict() for stu in b]
            #此处stu.dict()该方法只有Pydantic 模型或FastAPI 序列化模型才有，项目为 SQLAlchemy ORM 模型 不可用
            #则用__dict__: 所有对象自带的字典！Python 内部会把对象的所有属性全部存在一个内置字典里，用 __dict__ 就能拿出来
            result = []
            for stu in b:
                d = stu.__dict__.copy()#.copy（）作用：防止不小心改到原对象，安全规范写法
                d.pop("_sa_instance_state", None)#通过__dict__拿出来的原始内置字典会自带"_sa_instance_state": <something>
                                                 #这个键值对，通过pop（删指定的键，键不存在返回此默认值）删除清理
                if kwargs.items() <= d.items() :#判断 kwargs 是 字典d 的子集（键 + 值都包含）
                    result.append(d)#将清理干净的d（字典）作为元素加入列表

            return result#将查询出的满足条件的字典以列表的元素输出

    except Exception as a:
        print(f'多关键词查询异常：{a}')#开发人员观察异常
        db.rollback()
        return False
# hasattr(对象, "属性名字符串"):判断对象有没有这个属性
# 判断一个对象，是否包含某个属性 / 字段:返回：True / False
# getattr(对象, "属性名字符串"):从对象里取出这个属性
# 根据字符串，动态获取对象的属性 / 字段:动态生成查询条件;返回：True / False
 # 遍历你传的所有查询条件
    # 先检查
    # Student
    # 表里有没有这个字段
    # 有字段 → 动态生成查询条件

# 两个字典之间：可以用 all(k in b for k in a) 或 a.items() <= b.items()
#  a.items() <= b.items()：判断dict_a 是 dict_b 的子集（键 + 值都包含）
