# DSL Agent 配置
import os

# DeepSeek API配置
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', '你的-deepseek-api-key')

# 功能开关
ENABLE_LLM = True  # 开启LLM功能
ENABLE_EMOTION = False  # 暂时关闭情感分析
DEBUG_MODE = True  # 开启调试信息

# AI模型配置
AI_MODEL = 'deepseek-chat'  # DeepSeek模型
AI_TEMPERATURE = 0.7
AI_MAX_TOKENS = 2000
AI_BASE_URL = 'https://api.deepseek.com/v1'  # DeepSeek API地址