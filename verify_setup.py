#!/usr/bin/env python3
"""
Project structure verification script.
Checks that all necessary files are in place.
"""
import os
from pathlib import Path

def check_structure():
    """Verify project structure."""
    
    base_dir = Path(__file__).parent
    
    required_files = [
        # Python files
        "app/__init__.py",
        "app/main.py",
        "app/models.py",
        "app/schemas.py",
        "app/database.py",
        "app/llm.py",
        
        # Frontend files
        "app/templates/index.html",
        "app/static/styles.css",
        "app/static/app.js",
        
        # Configuration
        "requirements.txt",
        ".gitignore",
        ".env.example",
        
        # Documentation
        "README.md",
        "AI_NOTES.md",
        "PROMPTS_USED.md",
        "ABOUTME.md",
        "QUICKSTART.md",
        
        # Scripts
        "run.py",
    ]
    
    print("Checking project structure...\n")
    
    missing = []
    for file_path in required_files:
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} (MISSING)")
            missing.append(file_path)
    
    print("\n" + "="*50)
    
    if not missing:
        print("✓ All required files present!")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set OPENAI_API_KEY environment variable")
        print("3. Run: python run.py")
        print("4. Open: http://localhost:8000")
        return True
    else:
        print(f"✗ Missing {len(missing)} file(s)")
        return False

def check_python_syntax():
    """Check Python files for syntax errors."""
    import py_compile
    
    base_dir = Path(__file__).parent
    python_files = [
        "app/main.py",
        "app/models.py",
        "app/schemas.py",
        "app/database.py",
        "app/llm.py",
        "run.py",
    ]
    
    print("\n" + "="*50)
    print("Checking Python syntax...\n")
    
    errors = []
    for file_path in python_files:
        full_path = base_dir / file_path
        try:
            py_compile.compile(str(full_path), doraise=True)
            print(f"✓ {file_path}")
        except py_compile.PyCompileError as e:
            print(f"✗ {file_path}: {e}")
            errors.append(file_path)
    
    print("\n" + "="*50)
    
    if not errors:
        print("✓ All Python files have valid syntax!")
        return True
    else:
        print(f"✗ {len(errors)} file(s) have syntax errors")
        return False

if __name__ == "__main__":
    structure_ok = check_structure()
    syntax_ok = check_python_syntax()
    
    if structure_ok and syntax_ok:
        print("\n" + "="*50)
        print("PROJECT READY!")
        print("="*50)
        exit(0)
    else:
        exit(1)
