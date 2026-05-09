from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from Dao.class_ import create_class, get_classes, get_class, put_class, delete_class
# from Scheme import class_ as ClassScheme
from Scheme.class_ import class_1#文件夹.文件名 加入 类
router_class = APIRouter()


@router_class.post("/classes1",summary='创建班级')
# def create_class_api(class_data: ClassScheme, db: Session = Depends(get_db)):
def create_class_api(class_data: class_1, db: Session = Depends(get_db)):
    """创建班级"""

    result = create_class(
        db=db ,#db 必须放第一个参数
        class_name=class_data.class_name,
        start_time=class_data.start_time,
        teacher_id=class_data.teacher_id,
        head_teacher_id=class_data.head_teacher_id

        )
    if result is False:
        raise HTTPException(status_code=400, detail="班级创建失败")
    return {"code": 200,
            "message": "班级创建成功",
            "data": {
                "class_id": result.class_id if hasattr(result, 'class_id') else None,
                "class_name": result.class_name if hasattr(result, 'class_name') else None
            }}




@router_class.get("/classes2",summary='获取班级列表')
def get_classes_api(db: Session = Depends(get_db)):
    """获取班级列表"""

    classes = get_classes(db)
    if classes is False:#调用的返回值只有一个对象和False两种
        raise HTTPException(status_code=400, detail="获取班级列表失败")
    return {"code": 200,
            "message": "获取班级列表成功",
            "data": classes}



@router_class.get("/classes3/{class_id}",summary='获取班级信息')
def get_class_api(class_id: int, db: Session = Depends(get_db)):
    """获取单个班级详情"""

    class_info = get_class(db, class_id)
    if class_info is False:#调用的返回值只有一个对象和False两种
        raise HTTPException(status_code=404, detail="班级不存在")
    return {"code": 200,
            "message": f"获取{class_id}班级信息",
            "data": class_info}



@router_class.put("/classes4/{class_id}",summary='更新班级信息')
# def update_class_api(class_id: int, class_data: ClassScheme, db: Session = Depends(get_db)):
def update_class_api(class_id: int, class_data: class_1, db: Session = Depends(get_db)):
    """更新班级信息"""

    class_info = get_class(db, class_id)
    if not class_info:
        raise HTTPException(status_code=404, detail="班级不存在")

    update_data = class_data.model_dump(exclude_unset=True)
    result = put_class(db, class_id, update_data)

    if result is False:#调用的返回值只有True和False两种
        raise HTTPException(status_code=400, detail="班级更新失败")
    return {"code": 200,
            "message": "班级更新成功",
            "data":result}




@router_class.delete("/classes5/{class_id}",summary='删除班级信息')
def delete_class_api(class_id: int, db: Session = Depends(get_db)):
    """删除班级（逻辑删除）"""

    result = delete_class(db, class_id)
    if result is False:#调用的返回值只有True和False两种
        raise HTTPException(status_code=404, detail="班级不存在")
    return {"code": 200,
            "message": "班级删除成功",
            "data":None}

