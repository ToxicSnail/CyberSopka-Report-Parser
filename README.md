# CyberSopka Report Parser

Скрипты для автоматического анализа отчетов сканирования уязвимостей: парсинг HTML-отчетов, сбор статистики, извлечение CPE, объединение результатов в итоговый master-файл.

## Структура проекта
- `scan_reports.py` — парсит HTML-отчеты, извлекает CPE для уязвимостей уровня Critical/High, формирует JSON с уникальными CPE для каждого отчета.

- `count_vulns.py` — собирает статистику по количеству уязвимостей (Critical, High, Medium, Low) из отчетов и сохраняет в JSON.

- `analyze_cpes.py` — анализирует JSON с CPE, собирает и выводит общий список уникальных CPE.

- `master.py` — объединяет результаты из count_vulns.json и output.json в итоговый master-файл с количеством уязвимостей, списком CPE и строкой с рекомендацией.

 ## Установка зависимостей
```bash
pip install beautifulsoup4 lxml tqdm
```

## Использование

### 1. Парсинг отчетов для получения CPE

Соберите уникальные CPE из всех HTML-файлов в директории:
```bash
python3 scan_reports.py --dir ./reports --output json > output.json
```

### 2. Подсчет количества уязвимостей по уровням

Соберите статистику по уровням уязвимостей для всех отчетов:
```bash
python3 count_vulns.py --dir ./reports --output json > count_vulns.json
```

### 3. Анализ всех CPE

Для проверки уникальных CPE во всех отчетах:
```bash
python3 analyze_cpes.py output.json
```

### 4. Сборка master-файла

Объедините количество уязвимостей и список CPE в итоговый master-файл:
```bash
python3 build_master.py count_vulns.json output.json -o master_file.json
```

### Итоговый master-файл
В master-файле для каждого отчета формируется структура:
```json
"some_report.html": {
  "counts": {
    "Critical": 24,
    "High": 229,
    "Medium": 99,
    "Low": 6
  },
  "cpe": [
    "cpe:/a:git_project:git",
    "cpe:/a:microsoft:excel:1991"
  ],
  "test": "Необходимо обновить следующее ПО: cpe:/a:git_project:git, cpe:/a:microsoft:excel:1991"
}
```

### 5. Преобразование master-файла в таблицу
Создайте CSV-таблицу с удобным представлением данных для Excel/Sheets/GSlides:
```bash
python3 json_to_csv.py master_file.json -o master_table.csv
```

## что можно улучшить?
Можно сделать каскадное автоматизированное выполнение с последующей прроверкой корректности.

## Лицензия?
Да сделал Горький Кирилл