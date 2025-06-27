#!/usr/bin/env python3
import os, json, argparse
from bs4 import BeautifulSoup
from tqdm import tqdm

LEVELS = {
    '#89171A': 'Critical',
    '#CC0000': 'High',
    '#F5770F': 'Medium',
    '#00705C': 'Low'
}

def parse_vuln_counts(path: str):
    """Парсит файл и возвращает словарь с количеством уязвимостей по уровням."""
    with open(path, 'rb') as f:
        soup = BeautifulSoup(f, 'lxml')

    stats = {}
    table = soup.select_one('table.statTable')
    if not table:
        return stats

    rows = table.find_all('tr')
    for row in rows:
        tds = row.find_all('td')
        if len(tds) >= 2:
            color_div = tds[0].find('div')
            if color_div:
                style = color_div.get('style', '')
                for color, level in LEVELS.items():
                    if color in style:
                        count = tds[1].get_text(strip=True)
                        stats[level] = int(count) if count.isdigit() else 0
    return stats

def walk_reports(input_dir: str, output: str):
    results = {}
    html_files = [f for f in os.listdir(input_dir)
                  if f.lower().endswith('.html') and os.path.isfile(os.path.join(input_dir, f))]
    try:
        for fname in tqdm(html_files, desc='Parsing stats', unit='file'):
            fpath = os.path.join(input_dir, fname)
            stats = parse_vuln_counts(fpath)
            results[fname] = stats
    except KeyboardInterrupt:
        print('\n[!] Прервано пользователем, выводим уже обработанные файлы…')

    if output == 'json':
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for report, stat in results.items():
            print(f'\nФайл: {report}')
            if stat:
                for level in ['Critical', 'High', 'Medium', 'Low']:
                    print(f'  {level}: {stat.get(level, 0)}')
            else:
                print('  Не удалось найти таблицу статистики или уровни уязвимостей.')

if __name__ == '__main__':
    argp = argparse.ArgumentParser()
    argp.add_argument('--dir', default='.', help='Директория с HTML-отчетами (по умолчанию текущая).')
    argp.add_argument('--output', choices=['json', 'console'], default='console',
                      help='Формат вывода: json, console (по умолчанию console).')
    args = argp.parse_args()
    walk_reports(args.dir, args.output)
