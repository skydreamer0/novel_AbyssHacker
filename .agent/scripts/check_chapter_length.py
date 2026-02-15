import os
import re

def count_chinese_chars(text):
    """
    Counts the number of Chinese characters and punctuation in the text.
    """
    # Unicode range for Chinese characters and punctuation
    # CJK Unified Ideographs: 4E00-9FFF
    # Chinese punctuation: 3000-303F, FF00-FFEF (Fullwidth forms including punctuation)
    # We'll use a regex to match these ranges.
    pattern = re.compile(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]')
    return len(pattern.findall(text))

def scan_chapters(directory):
    """
    Scans the directory for .md files and checks their word count.
    """
    under_limit_chapters = []
    
    print(f"{'Chapter File':<60} | {'Char Count':<10} | {'Status'}")
    print("-" * 85)

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md") and "chapter" in file.lower():
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    char_count = count_chinese_chars(content)
                    
                    status = "OK"
                    if char_count < 3000:
                        status = "SHORT"
                        under_limit_chapters.append((filepath, char_count))
                    
                    # Create a relative path for cleaner output
                    rel_path = os.path.relpath(filepath, directory)
                    print(f"{rel_path:<60} | {char_count:<10} | {status}")
                    
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

    print("-" * 85)
    if under_limit_chapters:
        print(f"\nFound {len(under_limit_chapters)} chapters under 3000 characters:")
        for path, count in under_limit_chapters:
             print(f"- {os.path.basename(path)}: {count} characters")
        # exit(1) # Optional: exit with error code if under limit
    else:
        print("\nAll chapters meet the 3000 character requirement.")

if __name__ == "__main__":
    # Assuming the script is run from the project root or we can point to the '稿件' directory relative to the script
    # The script is in .agent/scripts/
    # The '稿件' directory is in the project root.
    
    # Get the project root directory (2 levels up from this script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    manuscript_dir = os.path.join(project_root, "稿件")
    
    if os.path.exists(manuscript_dir):
        print(f"Scanning chapters in: {manuscript_dir}")
        scan_chapters(manuscript_dir)
    else:
        print(f"Directory not found: {manuscript_dir}")
