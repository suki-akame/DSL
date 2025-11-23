#!/usr/bin/env python3
"""简单测试脚本"""
import unittest
import json
import os
import sys

def run_tests():
    # 加载测试数据
    try:
        with open('tests/data/test_cases.json') as f:
            test_data = json.load(f)
        print("测试数据:", test_data['test_cases'][0])
    except FileNotFoundError:
        print("测试数据文件未找到，使用默认数据")
        test_data = {"test_cases": [{"input": "hello", "expected_intent": "问候"}]}
    
    # 添加项目根目录到Python路径
    sys.path.insert(0, os.getcwd())
    
    # 运行测试
    print("运行单元测试...")
    loader = unittest.TestLoader()
    start_dir = 'tests/unit'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print(f"\n测试结果: {'通过' if result.wasSuccessful() else '失败'}")
    return result.wasSuccessful()

if __name__ == '__main__':
    print("启动简单测试框架...")
    success = run_tests()
    exit(0 if success else 1)