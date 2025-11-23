import requests
import json
from config import DEEPSEEK_API_KEY, ENABLE_LLM, DEBUG_MODE, AI_MODEL, AI_TEMPERATURE, AI_MAX_TOKENS, AI_BASE_URL

class AIClient:
    def __init__(self):
        if ENABLE_LLM and DEEPSEEK_API_KEY and DEEPSEEK_API_KEY != '你的-deepseek-api-key':
            self.api_key = DEEPSEEK_API_KEY
            self.enabled = True
            if DEBUG_MODE:
                print("DeepSeek AI客户端已初始化，使用模型:", AI_MODEL)
        else:
            self.enabled = False
            if DEBUG_MODE:
                print("DeepSeek AI客户端未启用，请检查API密钥和开关设置")
            
    def generate_response(self, user_input, context, scenario):
        """调用DeepSeek API生成智能回复"""
        if not self.enabled:
            return None
        
        # 构建系统提示词
        system_prompt = self._build_system_prompt(scenario)
        
        # 构建对话消息
        messages = self._build_messages(system_prompt, context, user_input)
        
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            
            data = {
                'model': AI_MODEL,
                'messages': messages,
                'temperature': AI_TEMPERATURE,
                'max_tokens': AI_MAX_TOKENS,
                'stream': False
            }
            
            response = requests.post(
                f'{AI_BASE_URL}/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                return ai_response.strip()
            else:
                if DEBUG_MODE:
                    print(f"DeepSeek API调用失败: {response.status_code}")
                return None
                
        except Exception as e:
            if DEBUG_MODE:
                print(f"DeepSeek调用异常: {e}")
            return None
    
    def _build_system_prompt(self, scenario):
        """构建系统提示词"""
        scenario_prompts = {
            'ecommerce': '''你是一个专业的电商客服助手。请根据用户问题提供准确、友好的帮助。
主要处理：商品咨询、订单查询、物流跟踪、退换货、优惠活动等问题。
回复要求：专业、耐心、解决问题导向，适当使用表情符号增强亲和力。保持回复简洁，在50字以内。''',
            
            'tech_support': '''你是一个专业的技术支持工程师。请帮助用户解决技术问题。
主要处理：软件安装、系统错误、使用指导、故障排除、功能咨询等技术问题。
回复要求：专业、准确、分步骤指导，避免技术 jargon，确保用户能理解。保持回复简洁实用。''',
            
            'hotel': '''你是一个专业的酒店预订客服。请协助用户完成酒店相关服务。
主要处理：房间预订、价格咨询、取消政策、设施服务、入住问题等。
回复要求：热情、专业、详细，突出酒店优势和服务特色。回复要友好且有帮助。'''
        }
        
        return scenario_prompts.get(scenario, '你是一个专业的客服助手，请用友好、专业的方式回答用户问题，保持回复简洁明了。')
    
    def _build_messages(self, system_prompt, context, user_input):
        """构建消息格式"""
        messages = [
            {'role': 'system', 'content': system_prompt}
        ]
        
        # 添加上下文对话（最近3轮）
        if context:
            recent_context = context[-6:]  # 最近6条消息（3轮对话）
            for msg in recent_context:
                if msg.startswith('用户:'):
                    messages.append({'role': 'user', 'content': msg[3:].strip()})
                elif msg.startswith('助手:'):
                    messages.append({'role': 'assistant', 'content': msg[3:].strip()})
        
        # 添加当前用户输入
        messages.append({'role': 'user', 'content': user_input})
        
        return messages