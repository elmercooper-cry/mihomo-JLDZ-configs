import os
import yaml
from pathlib import Path

def load_yaml_files(directory):
    rules_with_comments = []
    for file_path in Path(directory).glob("*.[yaml|txt]"):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            current_comment = []
            rules = []
            for line in lines:
                line = line.strip()
                if line.startswith('#'):
                    current_comment.append(line)
                elif line.startswith('- DOMAIN-SUFFIX'):
                    rules.append({'rule': line, 'comment': current_comment[:]})
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
        # Add a comment indicating the source file
        merged_rules.append(f"# Rules from {file_data['file']}")
        for rule_data in file_data['rules']:
            rule = rule_data['rule']
            if rule not in seen:
                seen.add(rule)
                # Include any preceding comments for this rule
                merged_rules.extend(rule_data['comment'])
                merged_rules.append(rule)
        # Add a blank line after each file's rules for readability
        merged_rules.append("")
    return merged_rules

def save_merged_yaml(rules, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Merged Sensitive Websites List for Mihomo\n")
        f.write("rules:\n")
        for line in rules:
            f.write(f"  {line}\n")

def main():
    config_dir = "configs"  # Adjust this to the directory containing your YAML/TXT files
    output_file = "sensitive-websites.yaml"
    
    # Load all rules with comments
    rules_with_comments = load_yaml_files(config_dir)
    
    # Merge rules
    merged_rules = merge_rules(rules_with_comments)
    
    # Save merged rules
    save_merged_yaml(merged_rules, output_file)
    
    print(f"Merged {len([r for r in merged_rules if r.startswith('-')])} unique rules into {output_file}")

if __name__ == "__main__":
    main()
