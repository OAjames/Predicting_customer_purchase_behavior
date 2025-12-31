from pathlib import Path


def setup_directories(base_path: str = "."):
    """
    This function scaffolds the entire project structure and
    creates required directories and files if they don't exist yet.
    """
    base = Path(base_path)

    # directories
    directories = [
        base / "data/raw",  
        base / "data/processed",  
        base / "notebooks",  
        base / "artifacts",
        base / "scripts",  
        base / "data/features",  
        base / "models",  
        base / "reports/figures", 
    ]

    # 2. Create directories and add .gitkeep
    for d in directories:
        d.mkdir(parents=True, exist_ok=True)
        (d / ".gitkeep").touch()

    # 3. Create essential project files
    files = {
        base
        / "requirements.txt": "pandas\nnumpy\nmatplotlib\nseaborn\nscikit-learn\nlightgbm\ntqdm\njupyter\nshap\n",
        base / "scripts/__init__.py": "",
        base / ".gitignore": "data/\n__pycache__/\n.ipynb_checkpoints/\n*.pkl\n.env",
    }

    for file_path, content in files.items():
        if not file_path.exists():
            with open(file_path, "w") as f:
                f.write(content)
            print(f"Created: {file_path}")

    print(f"Project structure initialized at: {base.resolve()}")


if __name__ == "__main__":
    setup_directories(".")


