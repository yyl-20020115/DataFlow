
import os
import json
import argparse
from pathlib import Path

def find_md_files(directory):
    """
    递归查找目录下所有的 .md 文件，排除隐藏目录
    """
    p = Path(directory)
    if not p.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    md_files = []
    for file_path in p.rglob("*.md"):
        # 排除隐藏文件夹中的文件
        if not any(part.startswith('.') for part in file_path.parts):
            md_files.append(file_path)
    return md_files

def process_md_file(file_path):
    """
    读取MD文件内容，返回清理后的文本
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # 去除首尾空白，保留内部格式
        return content.strip()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def convert_to_jsonl(md_files, output_file):
    """
    将MD文件列表转换为 {"text": "..."} 格式的JSONL文件
    """
    count = 0
    skipped = 0
    
    # 确保输出目录存在
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f_out:
        for md_path in md_files:
            text_content = process_md_file(md_path)
            
            if text_content:
                data_item = {
                    "text": text_content
                }
                # ensure_ascii=False 保证中文等非ASCII字符正常显示
                json_line = json.dumps(data_item, ensure_ascii=False)
                f_out.write(json_line + '\n')
                count += 1
            else:
                skipped += 1
                
    print(f"Conversion completed.")
    print(f"Successfully converted: {count} files")
    print(f"Skipped/Empty: {skipped} files")
    print(f"Output saved to: {os.path.abspath(output_file)}")

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown files to LLaMA-Factory compatible JSONL format.")
    parser.add_argument("--input_dir", type=str, default=".", help="Directory to search for .md files (default: current directory)")
    parser.add_argument("--output_file", type=str, default="train_data.jsonl", help="Output JSONL file name (default: train_data.jsonl)")
    
    args = parser.parse_args()
    
    input_dir = args.input_dir
    output_file = args.output_file
    
    print(f"Searching for .md files in: {os.path.abspath(input_dir)}")
    
    try:
        md_files = find_md_files(input_dir)
    except FileNotFoundError as e:
        print(e)
        return

    if not md_files:
        print("No markdown files found in the specified directory.")
        return
        
    print(f"Found {len(md_files)} markdown files. Starting conversion...")
    
    convert_to_jsonl(md_files, output_file)

if __name__ == "__main__":
    main()
