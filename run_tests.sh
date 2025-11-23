#!/bin/bash

# DSL Agent 测试运行脚本

echo "=== 启动 DSL Agent 测试套件 ==="

# 设置环境
export PYTHONPATH=$PYTHONPATH:$(pwd)
export TEST_MODE=true

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 创建测试报告目录
mkdir -p test_reports

# 检查 Python 命令
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}❌ 未找到 Python 命令！${NC}"
    exit 1
fi

echo -e "${YELLOW}使用 Python 命令: $PYTHON_CMD${NC}"
echo -e "${YELLOW}运行 Python 测试套件...${NC}"

# 运行测试
$PYTHON_CMD run_tests.py

TEST_RESULT=$?

# 输出结果
if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}测试通过！${NC}"
else
    echo -e "${RED}测试失败！${NC}"
fi

echo "=== 测试完成 ==="
exit $TEST_RESULT