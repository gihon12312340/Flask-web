# 使用 Python 官方映像作為基礎映像
FROM python:3.7


# 複製應用程式文件到容器中
COPY . /app/


# 設置工作目錄
WORKDIR /app


# 安裝 Flask 和相關套件，包含 pymysql
RUN pip install Flask pymysql
RUN pip install email_validator
RUN pip install cryptography
RUN pip install -r requirements.txt



# 運行 Flask 應用程式
CMD ["python", "run.py"]
