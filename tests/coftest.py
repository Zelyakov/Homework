from pathlib import Path
import sys

# Добавляем корень репозитория в sys.path, чтобы можно было импортировать пакет src
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

