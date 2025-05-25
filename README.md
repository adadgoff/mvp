# MVP ДЗ 3

## Автор

Дадыков Артемий

## Лицензия

MIT License

## Эмоции

Хороший факультатив, узнал новое: `streamlit`.

## Запуск на Unix

Необходим установленный `python`.

```zsh
# Настройка виртуального окружения.
python3 -m venv .venv
source .venv/bin/activate

# Установка зависимостей.
pip install uv
uv sync

# Запуск.
cd pets && fastapi run
```
