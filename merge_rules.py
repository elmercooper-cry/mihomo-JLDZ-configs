import os
from pathlib import Path

def load_yaml_files(directory):
    rules_with_comments = []
    for ext in ("*.yaml", "*.yml", "*.txt"):
        for file_path in Path(directory).glob(ext):
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                current_comment = []
                rules = []
                in_payload = False
                for line in lines:
                    stripped = line.strip()
                    # 跳过空行
                    if not stripped:
                        continue
                    # 检查 payload 层级
                    if stripped.lower().startswith("payload:"):
                        in_payload = True
                        continue
                    # 只处理 payload 下的内容（如果有 payload）
                    if in_payload and not (stripped.startswith('-') or stripped.startswith('#')):
                        continue
                    if stripped.startswith('#'):
                        current_comment.append(stripped)
                    elif stripped.startswith('- DOMAIN-SUFFIX'):
                        rules.append({'rule': stripped, 'comment': current_comment[:]})
                        current_comment = []
                if rules:
                    rules_with_comments.append({
                        'file': file_path.name,
                        'rules': rules
                    })
    return rules_with_comments

def merge_rules(rules_with_comments):
    seen = set()
    merged_rules = []
    for file_data in rules_with_comments:
        merged_rules.append(f"# Rules from {file_data['file']}")
        for rule_data in file_data['rules']:
            rule = rule_data['rule']
            if rule not in seen:
                seen.add(rule)
                merged_rules.extend(rule_data['comment'])
                merged_rules.append(rule)
        merged_rules.append("")
    return merged_rules

def save_merged_yaml(rules, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Merged Sensitive Websites List for Mihomo\n")
        f.write("rules:\n")
        for line in rules:
            f.write(f"  {line}\n")

def main():
    config_dir = "configs"
    output_file = "sensitive-websites.yaml"
    rules_with_comments = load_yaml_files(config_dir)
    merged_rules = merge_rules(rules_with_comments)
    save_merged_yaml(merged_rules, output_file)
    print(f"Merged {len([r for r in merged_rules if r.startswith('-')])} unique rules into {output_file}")

if __name__ == "__main__":
    main()
