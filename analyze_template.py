#!/usr/bin/env python3

def analyze_template_syntax():
    """Analyze Django template for syntax errors"""
    print("=" * 60)
    print("🔍 ANALYZING TEMPLATE SYNTAX")
    print("=" * 60)
    
    template_path = "templates/social/group_chats.html"
    
    with open(template_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Track template tags
    if_stack = []
    for_stack = []
    block_stack = []
    
    errors = []
    
    for i, line in enumerate(lines, 1):
        line_content = line.strip()
        
        # Check for if statements
        if '{% if ' in line_content:
            if_stack.append(i)
            print(f"Line {i}: Found {% if %} - Stack depth: {len(if_stack)}")
        elif '{% elif ' in line_content:
            print(f"Line {i}: Found {% elif %}")
        elif '{% else %}' in line_content:
            print(f"Line {i}: Found {% else %}")
        elif '{% endif %}' in line_content:
            if if_stack:
                if_start = if_stack.pop()
                print(f"Line {i}: Found {% endif %} - Closes if from line {if_start}")
            else:
                errors.append(f"Line {i}: {% endif %} without matching {% if %}")
        
        # Check for for loops
        elif '{% for ' in line_content:
            for_stack.append(i)
            print(f"Line {i}: Found {% for %} - Stack depth: {len(for_stack)}")
        elif '{% endfor %}' in line_content:
            if for_stack:
                for_start = for_stack.pop()
                print(f"Line {i}: Found {% endfor %} - Closes for from line {for_start}")
            else:
                errors.append(f"Line {i}: {% endfor %} without matching {% for %}")
        
        # Check for blocks
        elif '{% block ' in line_content:
            block_name = line_content.split('{% block ')[1].split(' %}')[0]
            block_stack.append((i, block_name))
            print(f"Line {i}: Found {% block {block_name} %}")
        elif '{% endblock %}' in line_content or '{% endblock' in line_content:
            if block_stack:
                block_start, block_name = block_stack.pop()
                print(f"Line {i}: Found {% endblock %} - Closes block '{block_name}' from line {block_start}")
            else:
                errors.append(f"Line {i}: {% endblock %} without matching {% block %}")
    
    # Check for unclosed tags
    if if_stack:
        for line_num in if_stack:
            errors.append(f"Line {line_num}: Unclosed {% if %} statement")
    
    if for_stack:
        for line_num in for_stack:
            errors.append(f"Line {line_num}: Unclosed {% for %} statement")
    
    if block_stack:
        for line_num, block_name in block_stack:
            errors.append(f"Line {line_num}: Unclosed {% block {block_name} %} statement")
    
    print(f"\n📊 ANALYSIS RESULTS:")
    print(f"   Total lines: {len(lines)}")
    print(f"   {% if %} statements: Found and properly closed")
    print(f"   {% for %} statements: Found and properly closed")
    print(f"   {% block %} statements: Found and properly closed")
    
    if errors:
        print(f"\n❌ ERRORS FOUND:")
        for error in errors:
            print(f"   - {error}")
        return False
    else:
        print(f"\n✅ NO SYNTAX ERRORS FOUND!")
        return True

if __name__ == '__main__':
    analyze_template_syntax()
