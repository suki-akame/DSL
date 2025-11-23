import os
import sys
sys.path.append(os.path.dirname(__file__))

from config import ENABLE_LLM

class ScriptEngine:
    def __init__(self):
        self.script = None
        self.current_scenario = "通用客服"
        self.ai_client = None
        self.conversation_history = []
        
        # 只有在需要时才初始化 AI 客户端
        if ENABLE_LLM:
            try:
                from ai_client import AIClient
                self.ai_client = AIClient()
            except ImportError:
                print("警告: 无法导入 AIClient，AI 功能将不可用")
                self.ai_client = None
        
    def load_script(self, parsed_script):
        self.script = parsed_script
        
    def set_scenario(self, scenario_name):
        """设置当前场景"""
        self.current_scenario = scenario_name
        
    def execute(self, user_input, intent=None):
        if not self.script:
            return "脚本未加载"
            
        # 记录用户输入
        self.conversation_history.append(f"用户: {user_input}")
        
        # 1. 优先使用意图匹配
        if intent and intent != '其他':
            for rule in self.script['rules']:
                if rule['trigger'] == intent:
                    response = rule['response']
                    self.conversation_history.append(f"助手: {response}")
                    return response
        
        # 2. 关键词匹配
        user_input_lower = user_input.lower()
        for rule in self.script['rules']:
            if rule['trigger'].lower() in user_input_lower:
                response = rule['response']
                self.conversation_history.append(f"助手: {response}")
                return response
        
        # 3. AI智能回复（当规则不匹配时）
        if self.ai_client and hasattr(self.ai_client, 'enabled') and self.ai_client.enabled:
            ai_response = self.ai_client.generate_response(
                user_input, 
                self.conversation_history,
                self.current_scenario
            )
            if ai_response:
                self.conversation_history.append(f"助手: {response}")
                return ai_response
        
        # 4. 默认回复
        fallback = self.script.get('fallback', '抱歉，我不理解您的问题，请换种方式描述或联系人工客服。')
        self.conversation_history.append(f"助手: {fallback}")
        
        # 限制对话历史长度
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-10:]
            
        return fallback