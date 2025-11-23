def parse_script(script_content):
    """
    解析DSL脚本内容
    """
    rules = []
    fallback = "抱歉，我不理解您的问题"
    
    lines = script_content.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        if line.startswith('WHEN'):
            # 解析规则: WHEN "关键词" THEN RESPONSE "回复内容"
            parts = line.split('THEN RESPONSE')
            if len(parts) == 2:
                trigger = parts[0].replace('WHEN', '').strip().strip('"')
                response = parts[1].strip().strip('"')
                rules.append({
                    'trigger': trigger,
                    'response': response
                })
                
        elif line.startswith('FALLBACK'):
            # 解析默认回复
            fallback = line.replace('FALLBACK', '').strip().strip('"')
            
    return {
        'rules': rules,
        'fallback': fallback
    }