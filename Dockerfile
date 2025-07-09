# FROM python:3.9-slim


# WORKDIR /app

# # 複製完整專案內容（包含 requirements.txt）
# COPY . .

# # 安裝相依套件
# RUN pip install --no-cache-dir -r requirements.txt

# # 確保模型檔存在於對應路徑（可省略這行，因為上面已經 COPY . .）
# # COPY models/lid.176.bin /app/models/lid.176.bin

# EXPOSE 8080
# CMD ["python", "app.py"]


FROM python:3.9-slim

# # 安裝 fastText 所需的編譯工具
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     g++ \
#     && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 複製專案檔案
COPY . .
# COPY models/lid.176.bin /app/models/lid.176.bin
# 安裝 Python 相依套件
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["python", "app.py"]
