from fastapi import HTTPException

# 成功响应结果
def success(data = None,code :int =200, msg : str ="操作成功"):
    raise HTTPException(status_code=code,
                        detail={"code":code,
                                "message":msg,
                                "data":data})

# 失败响应结果
def fail(msg :str,code :int):
    raise HTTPException(status_code =code,
                        detail = {"code" :code,
                                  "message" :msg})

# 成功响应列表

def success_list(list,code :int =200, msg : str ="查询成功",page :int =1,size :int =10):
    raise HTTPException(status_code =code,
                        detail ={"code" :code,
                                 "message" :msg,
                                 "data" : {"list" :list,
                                           "page" :page,
                                           "size" :size}})