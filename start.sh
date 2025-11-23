#!/bin/bash

# 自动启动脚本
cd "$(dirname "$0")"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖（如果还没有）
pip install dashscope requests > /dev/null 2>&1

# 运行程序
echo "启动DSL Agent系统..."
python main.py