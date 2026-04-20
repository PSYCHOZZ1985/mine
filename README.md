# Python Settings CLI

Минимальный CLI-инструмент, который загружает настройки из JSON-конфига,
проверяет обязательные поля и формирует человекочитаемый текстовый отчёт.

Приложение умеет:

- запускаться с конфигом по умолчанию;
- принимать путь к конфигу через `--config`;
- проверять конфиг через `--validate-config`;
- показывать загруженный конфиг через `--show-config`;
- сохранять итоговый отчёт в файл через `--output`;
- понятно сообщать об ошибках файла, JSON и обязательных полей.

## Структура

- `src/main.py` — точка входа приложения.
- `tests/test_smoke.py` — тесты загрузки конфига, ошибок и CLI-режимов.
- `docs/structure.md` — краткое описание структуры проекта.
- `config/settings.example.json` — пример конфигурации.

## Обычный запуск

```bash
python src/main.py
```

Если аргументы не переданы, приложение читает `config/settings.example.json` и
печатает отчёт в консоль.

## Запуск с другим конфигом

```bash
python src/main.py --config path/to/settings.json
```

## Проверка конфига

```bash
python src/main.py --validate-config
```

Или с явным путём:

```bash
python src/main.py --config path/to/settings.json --validate-config
```

## Просмотр конфига

```bash
python src/main.py --show-config
```

## Сохранение отчёта в файл

```bash
python src/main.py --output report.txt
```

С другим конфигом:

```bash
python src/main.py --config path/to/settings.json --output report.txt
```

Если файл нельзя записать, приложение выведет понятную ошибку без traceback.

## Конфиг

Пример файла `config/settings.example.json`:

```json
{
  "app_name": "starter-project",
  "debug": true,
  "log_level": "INFO"
}
```

Обязательные поля:

- `app_name` — имя приложения в выводимом сообщении.
- `debug` — включает или выключает debug-режим.
- `log_level` — уровень логирования, например `INFO`, `DEBUG` или `WARNING`.

Если файл отсутствует, JSON поврежден, обязательного поля нет или отчёт нельзя
сохранить, приложение выведет понятную ошибку без traceback.

## Тесты

```bash
python -m unittest discover -s tests
```
