# Конфигурационное управление — практическая работа №2

**Группа:** ИКБО-60-25  
**Вариант:** 18

Инструмент строит и визуализирует граф зависимостей пакетов Rust (Cargo).
Информация о зависимостях получается напрямую по HTTP из API crates.io.
Готовые менеджеры пакетов и сторонние библиотеки для получения зависимостей
в программе не используются.

## Этап 1. Минимальный прототип с конфигурацией

Поддержаны параметры командной строки:

- `--package` — имя анализируемого пакета;
- `--repository` — URL реестра или путь к тестовому репозиторию;
- `--test-mode` — режим тестового репозитория;
- `--output` — имя PNG-файла;
- `--ascii-tree` — вывод ASCII-дерева;
- `--max-depth` — максимальная глубина анализа;
- `--load-order` — вывод порядка загрузки зависимостей.

Проверяются пустое имя пакета, корректность URL/пути, глубина анализа и
расширение выходного файла.

## Этап 2. Сбор данных

Используется формат пакетов Rust (Cargo). Программа обращается напрямую к
HTTP API crates.io, получает версии пакета и список его прямых зависимостей.
Для каждой зависимости выбирается подходящая неотозванная версия с учётом
распространённых SemVer-ограничений Cargo.

## Этап 3. Основные операции

Граф зависимостей строится алгоритмом BFS без рекурсии через очередь
`collections.deque`. Для каждого узла хранится глубина. Уже раскрытые узлы
попадают в множество `expanded`, поэтому циклические зависимости не приводят
к бесконечному обходу.

Тестовый репозиторий задаётся JSON-файлом:

```json
{
  "A": ["B", "C"],
  "B": ["D"],
  "C": ["D"],
  "D": []
}
```

В папке `tests/data` есть:
- `basic.json` — обычный граф;
- `cycle.json` — граф с циклом;
- `deep.json` — граф для проверки ограничения глубины.

## Этап 4. Порядок загрузки

Порядок загрузки строится так, чтобы зависимость располагалась раньше пакета,
который от неё зависит. Если граф содержит цикл, полный порядок невозможен:
программа выводит узлы, участвующие в циклической части.

Для сравнения со штатным инструментом Cargo можно использовать:

```bash
cargo tree -e normal --depth 3
```

Результаты могут отличаться, потому что Cargo учитывает Cargo.lock, features,
target-specific зависимости и полное разрешение версий, а эта работа
анализирует сведения реестра напрямую.

## Этап 5. Визуализация

Программа:
1. формирует Mermaid-представление графа;
2. сохраняет Mermaid-код в файл `.mmd`;
3. отправляет Mermaid-код на публичный HTTP-рендерер Kroki;
4. сохраняет результат в PNG;
5. при `--ascii-tree` выводит ASCII-представление дерева.

Для PNG нужен доступ в интернет.

## Запуск

```bash
chmod +x run.sh
./run.sh --package serde --max-depth 2 --output serde.png
```

Полный пример:

```bash
./run.sh \
  --package serde \
  --repository https://crates.io/api/v1 \
  --max-depth 2 \
  --ascii-tree \
  --load-order \
  --output serde.png
```

## Тестовый режим

```bash
./run.sh \
  --package A \
  --repository tests/data/basic.json \
  --test-mode \
  --max-depth 4 \
  --ascii-tree \
  --load-order \
  --output demo.png
```

## Три примера реальных пакетов

```bash
./run.sh --package serde --max-depth 2 --ascii-tree --output serde.png
./run.sh --package clap --max-depth 2 --ascii-tree --output clap.png
./run.sh --package rand --max-depth 2 --ascii-tree --output rand.png
```

Эти же команды находятся в `examples.sh`.

## Тесты

```bash
make test
```

или:

```bash
python3 -m unittest discover -s tests -v
```

Тесты проверяют:
- валидацию параметров;
- BFS;
- ограничение глубины;
- обработку циклов;
- порядок загрузки;
- SemVer;
- Mermaid.

## Структура репозитория

```text
.
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── graph.py
│   ├── main.py
│   ├── semver.py
│   ├── sources.py
│   └── visualize.py
├── tests/
│   ├── data/
│   │   ├── basic.json
│   │   ├── cycle.json
│   │   └── deep.json
│   ├── test_config.py
│   ├── test_graph.py
│   ├── test_semver.py
│   └── test_visualize.py
├── .gitignore
├── examples.sh
├── Makefile
├── README.md
└── run.sh
```

## История разработки

Каждый этап отражён отдельным Conventional/Scoped Commit:

```text
feat(cli): implement configurable prototype
feat(cargo): collect direct Cargo dependencies
feat(graph): build dependency graph with iterative BFS
feat(graph): add dependency load order
feat(visualization): add Mermaid ASCII and PNG output
```
