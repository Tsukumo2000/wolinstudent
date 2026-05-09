#FROM python:3.11
#WORKDIR /app
#COPY requirements.txt .
#RUN pip install --no-cache-dir -r requirements.txt
#COPY . .
#EXPOSE 8000
#CMD ["uvicorn", "main:app","--host","0.0.0.0","--port","8000"]



#FROM python:3.11
#
#WORKDIR /app
#COPY requirements.txt .
#

#RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/
#RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
#
#COPY . .
#EXPOSE 8000
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


# 1. 基础镜像（官方Python轻量级镜像）
FROM python:3.11-slim

# 2. 设置工作目录
WORKDIR /app

# 3. 复制依赖文件并安装（利用Docker缓存，加速构建）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 复制项目代码
COPY . .

# 5. 暴露容器端口（FastAPI默认8000）
EXPOSE 8000

# 6. 启动命令（0.0.0.0允许外部访问容器）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


