import os
from pathlib import Path

def print_tree(directory):
    print(f"\n📂 Inspecting: {directory}")
    if not directory.exists():
        print("   ❌ Folder not found!")
        return

    for root, dirs, files in os.walk(directory):
        level = root.replace(str(directory), '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f"{indent}📁 {os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            file_path = Path(root) / f
            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"{subindent}📄 {f} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    base_path = Path("../data/raw").resolve()
    print("="*60)
    print("DIGITAL GENOME DATA DIAGNOSTICS")
    print("="*60)
    print_tree(base_path)
    print("="*60)