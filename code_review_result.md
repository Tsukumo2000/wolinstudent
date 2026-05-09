# 代码审查结果报告

> 生成时间：2026-05-08
> 审查范围：main.py, database.py, Api/, Dao/, Model/, Scheme/, 前端HTML

---

## 问题清单

---

### 【Bug-001】Api/teacher.py — update_teacher 冗余调用

- **文件**: `Api/teacher.py`
- **行号**: 第 88-97 行
- **严重程度**: 🔴 高
- **问题描述**: `update_teacher_api` 中对 `teacher.update_teacher()` 调用了两次，第二次是冗余的。

**修改前的代码**:
```python
# --- 第 88-97 行 ---
    try:
        ...
        teacher.update_teacher(db, teacher_id, update_dict)          # ← 第 90 行：第一次调用（冗余）
        res = teacher.update_teacher(db=db,                         # ← 第 93 行：第二次调用
                                     teacher_id =teacher_id,
                                     update_dict =update_dict)
        return {"code": 200,
                "message": "老师信息修改成功",
                "data": {"teacher_id": teacher_id}}
```

**修改后的代码**:
```python
# --- 第 88-97 行（删除第 90 行） ---
    try:
        ...
        # 【BUG-001 修复】删除冗余的第一次调用，只保留一次
        res = teacher.update_teacher(db=db,                          # ← 保留此行
                                     teacher_id =teacher_id,
                                     update_dict =update_dict)
        return {"code": 200,
                "message": "老师信息修改成功",
                "data": {"teacher_id": teacher_id}}
```

**具体更改**: 删除第 90 行 `teacher.update_teacher(db, teacher_id, update_dict)`

---

### 【Bug-002】Dao/user.py — delete_user 逻辑删除字段名不一致

- **文件**: `Dao/user.py`
- **行号**: 第 33 行
- **严重程度**: 🔴 高
- **问题描述**: `delete_user` 中使用 `user.is_deleted = 1`，但 User 模型定义的字段是 `user_is_deleted`，导致逻辑删除无效。

**修改前的代码**:
```python
# --- 第 30-35 行 ---
def delete_user(db: Session,
                username: str):
    user = db.query(User).filter(User.username == username, User.user_is_deleted == 0).first()
    if not user:
        respon.fail("用户名不存在,无法删除", 400)
    user.is_deleted = 1          # ← 第 33 行：错误字段名（应为 user_is_deleted）
    db.commit()
    return True
```

**修改后的代码**:
```python
# --- 第 30-35 行 ---
def delete_user(db: Session,
                username: str):
    user = db.query(User).filter(User.username == username, User.user_is_deleted == 0).first()
    if not user:
        respon.fail("用户名不存在,无法删除", 400)
    user.user_is_deleted = 1     # 【BUG-002 修复】修正字段名为 user_is_deleted
    db.commit()
    return True
```

**具体更改**: 第 33 行 `user.is_deleted = 1` → `user.user_is_deleted = 1`

---

### 【Bug-003】Api/score.py — get_all_score 重复调用

- **文件**: `Api/score.py`
- **行号**: 第 95-98 行
- **严重程度**: 🟡 中
- **问题描述**: `get_all_score` 函数被连续调用两次，造成数据库查询浪费。

**修改前的代码**:
```python
# --- 第 95-100 行 ---
    try:
        result = get_all_score(class_id=class_id,db=db)           # ← 第 96 行：第一次调用（冗余）
        all_score, avg_score = get_all_score(class_id=class_id,db=db)  # ← 第 97 行：第二次调用
        if not result:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": 400,
                    "message": '成绩删除失败'})
```

**修改后的代码**:
```python
# --- 第 95-100 行 ---
    try:
        # 【BUG-003 修复】删除第一次冗余调用，直接使用第二次调用的结果
        all_score, avg_score = get_all_score(class_id=class_id,db=db)  # ← 保留并赋值
        if not all_score:
            raise HTTPException(
                status_code=400,
                detail={
                    "code": 400,
                    "message": '成绩删除失败'})
```

**具体更改**: 删除第 96 行的冗余调用，保留第 97 行并直接使用其结果

---

### 【Bug-004】Dao/user.py — update_user 缺失导入 HTTPException

- **文件**: `Dao/user.py`
- **行号**: 第 1 行（导入区）、第 43 行（使用处）
- **严重程度**: 🟡 中
- **问题描述**: `update_user` 函数中使用了 `HTTPException`，但文件头部未导入，会导致运行时错误。

**修改前的代码**:
```python
# --- 第 1-5 行（文件头部） ---
from sqlalchemy.orm import Session, sessionmaker
from Model.table import User
from fastapi import Query
# 缺少：from fastapi import HTTPException

# --- 第 40-48 行（update_user 函数） ---
def update_user(db:Session,
                   user_id : int,
                   username:str,password:int,role_id:int=1):
    user = db.query(User).filter(User.user_id ==user_id,User.user_is_deleted ==0).first()
    if not user:
        raise HTTPException(           # ← 第 43 行：使用了未导入的 HTTPException
            status_code=400,
            detail={"code": 400, "message": "用户不存在"}
        )
```

**修改后的代码**:
```python
# --- 第 1-6 行（文件头部） ---
from sqlalchemy.orm import Session, sessionmaker
from Model.table import User
from fastapi import Query
from fastapi import HTTPException      # 【BUG-004 修复】添加 HTTPException 导入

# --- 第 41-49 行（update_user 函数） ---
def update_user(db:Session,
                   user_id : int,
                   username:str,password:int,role_id:int=1):
    user = db.query(User).filter(User.user_id ==user_id,User.user_is_deleted ==0).first()
    if not user:
        raise HTTPException(           # ← 现在可以正常使用
            status_code=400,
            detail={"code": 400, "message": "用户不存在"}
        )
```

**具体更改**:
1. 在第 4 行后添加 `from fastapi import HTTPException`

---

### 【Bug-005】Api/employment.py — employment4 返回结构不一致

- **文件**: `Api/employment.py`
- **行号**: 第 97-103 行
- **严重程度**: 🟡 中
- **问题描述**: `employment4` 接口返回时将整个 `res`（字典）嵌套在 `data` 中，与其他接口返回格式不一致。

**修改前的代码**:
```python
# --- 第 95-104 行 ---
@router_employment.get('/employment4',summary='查找冗余信息')
def get_employment_detail_api(employment_id:int,db=Depends(get_db)):
    try:
        res = employment_dao.get_employment_detail(db,employment_id=employment_id)
        if not res:
            respon.fail('无该学员就业信息', 404)
        return {"code": 200,
                "message": '信息查询成功',
                "data": res}          # ← 第 101 行：res 是字典 {employment, student_name, class_name}
    except Exception as e:
        respon.fail(str(e), 500)
```

**修改后的代码**:
```python
# --- 第 95-104 行 ---
@router_employment.get('/employment4',summary='查找冗余信息')
def get_employment_detail_api(employment_id:int,db=Depends(get_db)):
    try:
        res = employment_dao.get_employment_detail(db,employment_id=employment_id)
        if not res:
            respon.fail('无该学员就业信息', 404)
        # 【BUG-005 修复】展平返回结构，直接取 employment 对象返回
        return {"code": 200,
                "message": '信息查询成功',
                "data": res.get("employment") if res else None}  # ← 返回 employment 对象
    except Exception as e:
        respon.fail(str(e), 500)
```

**具体更改**: 第 101 行 `data: res` → `data: res.get("employment") if res else None`

---

### 【Bug-006】Scheme/respon.py — 函数名拼写错误

- **文件**: `Scheme/respon.py`
- **行号**: 第 18 行
- **严重程度**: 🟢 低
- **问题描述**: 函数名 `sucess_list` 拼写错误（少了一个 c），应为 `success_list`。

**修改前的代码**:
```python
# --- 第 18-24 行 ---
def sucess_list(list,code :int =200, msg : str ="查询成功",page :int =1,size :int =10):  # ← 第 18 行：拼写错误
    raise HTTPException(status_code =code,
                        detail ={"code" :code,
                                 "message" :msg,
                                 "data" : {"list" :list,
                                           "page" :page,
                                           "size" :size}})
```

**修改后的代码**:
```python
# --- 第 18-24 行 ---
def success_list(list,code :int =200, msg : str ="查询成功",page :int =1,size :int =10):  # 【BUG-006 修复】修正拼写
    raise HTTPException(status_code =code,
                        detail ={"code" :code,
                                 "message" :msg,
                                 "data" : {"list" :list,
                                           "page" :page,
                                           "size" :size}})
```

**具体更改**: 第 18 行函数名 `sucess_list` → `success_list`

---

### 【Bug-007】Api/student.py — 注释掉的废弃代码需清理

- **文件**: `Api/student.py`
- **严重程度**: 🟡 中
- **问题描述**: 文件中存在大量注释掉的废弃代码（query_student、update_student_api 等），影响代码可读性。

**修改前的代码**:
```python
# --- 第 40-58 行（大量注释代码） ---
# @router_student.get("/query",summary='学生多关键词查询')
# def query_student(
#     student_id: int | None = None,
#     ...
# ):
#     ...
# @router_student.post("/student/more_query", summary="多关键词查询学生")
# def get_student_more_api(
#     ...
# ):
#     ...
# @router_student.put("/{student_id}",summary='学生更新')
# def update_student_api(student_id: int, condition:Dict[str,Any],db: Session = Depends(get_db)):
#     ...
```

**修改后的代码**:
```python
# --- 第 40-58 行（删除所有注释代码，保留有效代码） ---
@router_student.post("/student/more_query", summary="多关键词查询学生")
def get_student_more_api(
    condition: Dict[str, Any],
    db: Session = Depends(get_db)
):
    result = get_student_More(db=db, **condition)
    if result is False:
        raise HTTPException(status_code=500, detail="查询失败")
    return {
        "code": 200,
        "message": "查询成功",
        "data": result
    }
```

**具体更改**: 删除第 40-58 行所有注释代码，保留有效的 `get_student_more_api` 函数

---

### 【Bug-008】Api/employment.py — create_employment 返回值未统一

- **文件**: `Api/employment.py`
- **行号**: 第 44 行
- **严重程度**: 🟢 低
- **问题描述**: `create_employment_api` 直接返回 ORM 对象 `new_emp`，未包装为统一响应格式 `{"code": 200, "message": "...", "data": ...}`

**修改前的代码**:
```python
# --- 第 42-47 行 ---
        new_emp = employment_dao.create_employment(db=db,
                                                  ...
                                                  salary = salary)
        return new_emp            # ← 第 44 行：直接返回 ORM 对象
    except HTTPException as e:
        raise e
```

**修改后的代码**:
```python
# --- 第 42-47 行 ---
        new_emp = employment_dao.create_employment(db=db,
                                                    ...
                                                    salary = salary)
        # 【BUG-008 修复】包装为统一响应格式
        return {"code": 200,
                "message": "就业信息创建成功",
                "data": {
                    "employment_id": new_emp.employment_id,
                    "student_name": new_emp.student_name,
                    "company": new_emp.company
                }}
    except HTTPException as e:
        raise e
```

**具体更改**: 第 44 行 `return new_emp` → 包装为统一响应格式

---

### 【Bug-009】Dao/employment.py — get_employment_detail 返回格式不匹配

- **文件**: `Dao/employment.py`
- **行号**: 第 94-105 行
- **严重程度**: 🟡 中
- **问题描述**: `get_employment_detail` 返回包含嵌套字典结构，但调用方 Api 层只取 `res`，导致数据不匹配。

**修改前的代码**:
```python
# --- 第 94-107 行 ---
def get_employment_detail(db: Session, employment_id: int):
    emp = db.query(Employment).filter(
        Employment.employment_id == employment_id,
        Employment.employment_is_deleted == 0
    ).first()

    if not emp:
        return None

    student = db.query(Student).filter(...).first()
    class_obj = db.query(Class).filter(...).first()

    # 【问题】返回嵌套字典结构
    return {
        "employment": emp,           # ← 第 102 行：嵌套了 ORM 对象
        "student_name": student_name,
        "class_name": class_name
    }
```

**修改后的代码**:
```python
# --- 第 94-107 行 ---
def get_employment_detail(db: Session, employment_id: int):
    emp = db.query(Employment).filter(
        Employment.employment_id == employment_id,
        Employment.employment_is_deleted == 0
    ).first()

    if not emp:
        return None

    student = db.query(Student).filter(...).first()
    class_obj = db.query(Class).filter(...).first()

    # 【BUG-009 修复】展平返回结构，直接返回必要字段
    return {
        "employment_id": emp.employment_id,
        "student_name": student_name,
        "class_name": class_name,
        "company": emp.company,
        "salary": emp.salary,
        "offer_time": emp.offer_time
    }
```

**具体更改**: 第 102-106 行，将嵌套的 `employment` ORM 对象展平为具体字段

---

### 【Bug-010】Api/class_.py — 返回值处理逻辑可读性差

- **文件**: `Api/class_.py`
- **行号**: 第 20-26 行
- **严重程度**: 🟢 低
- **问题描述**: `create_class_api` 在 result 为 False 时进入 return 分支不合理（应该抛异常），且返回格式可读性差。

**修改前的代码**:
```python
# --- 第 18-28 行 ---
@router_class.post("/classes1",summary='创建班级')
def create_class_api(class_data: class_1, db: Session = Depends(get_db)):
    result = create_class(db=db,
                          class_name=class_data.class_name,
                          start_time=class_data.start_time,
                          teacher_id=class_data.teacher_id,
                          head_teacher_id=class_data.head_teacher_id)
    if result is False:
        raise HTTPException(status_code=400, detail="班级创建失败")
    return {"code": 200,                      # ← 第 26 行：返回格式可读性差
            "message": "班级创建成功",
            "data": result}
```

**修改后的代码**:
```python
# --- 第 18-28 行 ---
@router_class.post("/classes1",summary='创建班级')
def create_class_api(class_data: class_1, db: Session = Depends(get_db)):
    result = create_class(db=db,
                          class_name=class_data.class_name,
                          start_time=class_data.start_time,
                          teacher_id=class_data.teacher_id,
                          head_teacher_id=class_data.head_teacher_id)
    if result is False:
        raise HTTPException(status_code=400, detail="班级创建失败")
    # 【BUG-010 修复】统一返回格式，明确返回班级ID
    return {"code": 200,
            "message": "班级创建成功",
            "data": {
                "class_id": result.class_id if hasattr(result, 'class_id') else None,
                "class_name": result.class_name if hasattr(result, 'class_name') else None
            }}
```

**具体更改**: 第 26-27 行优化返回格式，使用 `hasattr` 安全获取属性

---

## 修复记录表

| 条目ID | 文件 | 问题描述 | 状态 | 修复时间 | 备注 |
|--------|------|---------|------|---------|------|
| Bug-001 | Api/teacher.py | update_teacher 冗余调用 | ✅ 已修复 | 2026-05-08 | 删除第 90 行 |
| Bug-002 | Dao/user.py | delete_user 字段名不一致 | ✅ 已修复 | 2026-05-08 | `is_deleted` → `user_is_deleted` |
| Bug-003 | Api/score.py | get_all_score 重复调用 | ✅ 已修复 | 2026-05-08 | 删除第 96 行冗余调用 |
| Bug-004 | Dao/user.py | update_user 缺失导入 | ✅ 已修复 | 2026-05-08 | 添加 HTTPException 导入 |
| Bug-005 | Api/employment.py | employment4 返回结构不一致 | ✅ 已修复 | 2026-05-08 | 展平返回结构（配合 Bug-009） |
| Bug-006 | Scheme/respon.py | 函数名拼写错误 | ✅ 已修复 | 2026-05-08 | `sucess_list` → `success_list` |
| Bug-007 | Api/student.py | 注释代码需清理 | ✅ 已修复 | 2026-05-08 | 删除废弃注释代码（2处） |
| Bug-008 | Api/employment.py | create_employment 返回值未统一 | ✅ 已修复 | 2026-05-08 | 包装为统一响应格式 |
| Bug-009 | Dao/employment.py | get_employment_detail 返回格式 | ✅ 已修复 | 2026-05-08 | 展平返回结构（配合 Bug-005） |
| Bug-010 | Api/class_.py | 返回值不一致 | ✅ 已修复 | 2026-05-08 | 优化返回格式 |
