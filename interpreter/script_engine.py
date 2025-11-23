class ScriptEngine:
    def __init__(self):
        self.script = None
        
    def load_script(self, parsed_script):
        self.script = parsed_script
        
    def execute(self, user_input, intent=None):
        if not self.script:
            return "脚本未加载"
            
        # 如果有意图识别结果，优先使用意图匹配
        if intent and intent != '其他':
            for rule in self.script['rules']:
                if rule['trigger'] == intent:
                    return rule['response']
        
        # 如果没有意图或意图为其他，使用关键词匹配
        user_input_lower = user_input.lower()
        for rule in self.script['rules']:
            if rule['trigger'].lower() in user_input_lower:
                return rule['response']
        
        # 返回默认回复
        return self.script.get('fallback', '抱歉，我不理解您的问题')