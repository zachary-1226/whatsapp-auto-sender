# 1. 基础镜像：明确指定 Debian 12 (bookworm) 稳定版本以避免软件包冲突
FROM python:3.10-slim-bookworm

# 2. 设置全局工作目录
WORKDIR /app

# 设置环境变量，防止生成 pyc 文件和开启不带缓存的实时日志输出
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 5. 系统依赖：安装必要的工具
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    gnupg \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 现代 Chrome 安装方式：使用 Chrome 官方 apt 仓库
# 安装 google-chrome-stable 会自动安装 Chrome 所需的绝大部分底层依赖库（例如 libnss3, libxss1 等）
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 3. 拷贝当前目录下的所有文件到容器的 /app 目录下
COPY . /app

# 4. 依赖安装：根据项目的依赖文件写好安装命令，并清理安装缓存减小体积
RUN pip install --no-cache-dir pandas selenium webdriver_manager openpyxl

# 6. 启动命令：默认运行核心脚本
CMD ["python", "script.py"]
