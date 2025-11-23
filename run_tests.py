#!/usr/bin/env python3
"""
DSL Agent 主测试脚本
运行完整的测试套件
"""

import unittest
import sys
import os
import json
from datetime import datetime

def print_banner():
    """打印测试横幅"""
    print("=" * 60)
    print("      DSL Agent 测试套件")
    print("=" * 60)

def load_test_config():
    """加载测试配置"""
    config = {
        'test_mode': True,
        'report_path': 'test_reports',
        'include_integration': True
    }
    return config

def run_unit_tests():
    """运行单元测试"""
    print("\n🔧 运行单元测试...")
    
    loader = unittest.TestLoader()
    start_dir = 'tests/unit'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def run_integration_tests():
    """运行集成测试"""
    print("\n🔗 运行集成测试...")
    
    loader = unittest.TestLoader()
    start_dir = 'tests/integration' 
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

def generate_test_report(success):
    """生成测试报告"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'success': success,
        'test_suites': ['unit', 'integration'],
        'summary': '所有测试已完成' if success else '部分测试失败'
    }
    
    # 确保报告目录存在
    os.makedirs('test_reports', exist_ok=True)
    
    report_file = f"test_reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 测试报告已生成: {report_file}")
    return report_file

def main():
    """主测试函数"""
    print_banner()
    
    # 加载配置
    config = load_test_config()
    
    # 设置测试模式
    os.environ['TEST_MODE'] = 'true'
    
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python 版本: {sys.version}")
    
    # 运行测试
    unit_success = run_unit_tests()
    integration_success = run_integration_tests() if config['include_integration'] else True
    
    overall_success = unit_success and integration_success
    
    # 生成报告
    report_file = generate_test_report(overall_success)
    
    # 输出结果
    print("\n" + "=" * 60)
    if overall_success:
        print("所有测试通过！")
    else:
        print("部分测试失败，请检查详细信息")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    return 0 if overall_success else 1

if __name__ == '__main__':
    sys.exit(main())