import os
import sys
from interpreter.dsl_parser import parse_script
from interpreter.script_engine import ScriptEngine
from nlp.intent_recognizer import IntentRecognizer

class ScenarioManager:
    def __init__(self):
        self.scenarios = {}
        self.load_scenarios()
    
    def load_scenarios(self):
        """加载所有业务场景脚本"""
        scripts_dir = "scripts"
        for filename in os.listdir(scripts_dir):
            if filename.endswith(".dsl"):
                scenario_name = filename.replace(".dsl", "")
                with open(os.path.join(scripts_dir, filename), 'r', encoding='utf-8') as f:
                    script_content = f.read()
                parsed_script = parse_script(script_content)
                self.scenarios[scenario_name] = {
                    'name': scenario_name,
                    'script': parsed_script,
                    'description': self._get_scenario_description(scenario_name)
                }
    
    def _get_scenario_description(self, scenario_name):
        """获取场景描述"""
        descriptions = {
            'ecommerce': '电商客服',
            'tech_support': '技术支持', 
            'hotel': '酒店预订'
        }
        return descriptions.get(scenario_name, scenario_name)
    
    def list_scenarios(self):
        """列出所有可用场景"""
        return self.scenarios
    
    def get_scenario(self, name):
        """获取指定场景"""
        return self.scenarios.get(name)

def main():
    # 初始化组件
    recognizer = IntentRecognizer()
    engine = ScriptEngine()
    scenario_manager = ScenarioManager()
    
    # 显示场景选择
    print("=== 多业务场景智能客服系统 ===")
    print("请选择业务场景：")
    scenarios = scenario_manager.list_scenarios()
    
    scenario_list = list(scenarios.items())
    for i, (key, scenario) in enumerate(scenario_list, 1):
        print(f"{i}. {scenario['description']}")
    
    # 场景选择
    while True:
        try:
            choice = input(f"\n请输入场景编号 (1-{len(scenarios)}): ")
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(scenarios):
                selected_key, selected_scenario = scenario_list[choice_idx]
                engine.load_script(selected_scenario['script'])
                engine.set_scenario(selected_scenario['description'])  # 设置AI场景
                current_scenario = selected_scenario['description']
                print(f"\n已切换到: {current_scenario}")
                break
            else:
                print("无效的选择，请重新输入")
        except (ValueError, IndexError):
            print("请输入有效数字")
    
    # 对话循环
    print("\n智能客服助手已启动，输入'退出'结束对话，输入'切换'更换场景")
    print("=" * 50)
    
    while True:
        user_input = input("\n用户: ").strip()
        
        if user_input == '退出':
            print("感谢使用，再见！")
            break
        elif user_input == '切换':
            # 切换场景
            print("\n请选择新的业务场景：")
            scenario_list = list(scenarios.items())
            for i, (key, scenario) in enumerate(scenario_list, 1):
                print(f"{i}. {scenario['description']}")
            
            while True:
                try:
                    choice = input(f"\n请输入场景编号 (1-{len(scenarios)}): ")
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(scenarios):
                        selected_key, selected_scenario = scenario_list[choice_idx]
                        engine.load_script(selected_scenario['script'])
                        engine.set_scenario(selected_scenario['description'])  # 设置AI场景
                        current_scenario = selected_scenario['description']
                        print(f"\n已切换到: {current_scenario}")
                        break
                    else:
                        print("无效的选择，请重新输入")
                except (ValueError, IndexError):
                    print("请输入有效数字")
            continue
        
        if not user_input:
            print("助手: 您好，请问有什么可以帮您？")
            continue
            
        # 识别意图
        intent = recognizer.recognize_intent(user_input)
        
        # 执行脚本生成回复
        response = engine.execute(user_input, intent)
        
        # 输出回复
        print(f"助手: {response}")

if __name__ == "__main__":
    main()