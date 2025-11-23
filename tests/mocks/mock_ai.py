"""AI客户端测试桩"""
class MockAIClient:
    def __init__(self):
        self.call_count = 0
    
    def generate_response(self, user_input, context, scenario):
        self.call_count += 1
        return f"模拟AI回复: {user_input}"