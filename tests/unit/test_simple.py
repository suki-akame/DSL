import unittest
import sys
import os

# 修复导入路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from nlp.intent_recognizer import IntentRecognizer

# 直接定义测试桩，避免复杂导入
class MockAIClient:
    def __init__(self):
        self.call_count = 0
    
    def generate_response(self, user_input, context, scenario):
        self.call_count += 1
        return f"模拟AI回复: {user_input}"

class TestSimple(unittest.TestCase):
    def setUp(self):
        self.recognizer = IntentRecognizer()
        self.mock_ai = MockAIClient()
    
    def test_intent_hello(self):
        """测试问候意图识别 - TDD风格"""
        result = self.recognizer.recognize_intent("hello")
        self.assertEqual(result, "问候")
    
    def test_intent_refund(self):
        """测试退款意图识别"""
        result = self.recognizer.recognize_intent("我要退款")
        self.assertEqual(result, "退款")
    
    def test_mock_ai(self):
        """测试桩使用"""
        response = self.mock_ai.generate_response("test", [], "场景")
        self.assertIn("模拟AI回复", response)
        self.assertEqual(self.mock_ai.call_count, 1)

if __name__ == '__main__':
    unittest.main()