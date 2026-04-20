# Starter Python Settings App

Минимальное Python-приложение, которое загружает настройки из JSON-конфига и
печатает понятное сообщение о текущем режиме работы.

## Структура

- `src/main.py` — точка входа приложения.
- `tests/test_smoke.py` — тесты загрузки конфига и сборки сообщения.
- `docs/structure.md` — краткое описание структуры проекта.
- `config/settings.example.json` — пример конфигурации.

## Запуск

```bash
python src/main.py
```

Приложение читает `config/settings.example.json` и выводит сообщение на основе
полей `app_name`, `debug` и `log_level`.

## Конфиг

Пример файла `config/settings.example.json`:

```json
{
  "app_name": "starter-project",
  "debug": true,
  "log_level": "INFO"
}
```

Чтобы изменить поведение приложения, поменяйте значения:

- `app_name` — имя приложения в выводимом сообщении.
- `debug` — включает или выключает debug-режим.
- `log_level` — уровень логирования, например `INFO`, `DEBUG` или `WARNING`.

Если файл отсутствует или JSON поврежден, приложение выведет понятную ошибку
конфигурации без traceback.

## Тесты

```bash
python -m unittest discover -s tests
```
