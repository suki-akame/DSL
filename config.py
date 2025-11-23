# DSL Agent 配置
import os

# 通义千问API配置（可选）
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY', '')

# 功能开关
ENABLE_LLM = False  # 暂时关闭LLM，使用关键词匹配
ENABLE_EMOTION = False  # 暂时关闭情感分析
DEBUG_MODE = False  # 关闭调试信息