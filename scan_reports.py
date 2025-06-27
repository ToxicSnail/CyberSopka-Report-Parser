#!/usr/bin/env python3
import os, json, argparse
from bs4 import BeautifulSoup
from tqdm import tqdm

CRIT_BG = '#89171A'
HIGH_BG = '#CC0000'
TXT_OUT = 'parsed_results.txt'

def parse_cpe_for_crit_high(path: str):
    """Парсит один HTML-отчет, возвращает set CPE для критических/высоких уязвимостей."""
    with open(path, 'rb') as f:
        soup = BeautifulSoup(f, 'lxml')

    cpe = set()
    table = soup.select_one('table.vulnerabilitiesTbl')
    if not table:
        return cpe

    rows = table.find_all('tr')
    i = 0
    while i < len(rows):
        if rows[i].find('td', class_='bdu'):
            risk_div = rows[i].select_one('td.risk div')
            if risk_div:
                bg = risk_div.get('style', '')
                if CRIT_BG in bg or HIGH_BG in bg:
                    j = i + 1
                    while j < len(rows) and not rows[j].find('td', class_='bdu'):
                        prod = rows[j].find('td', class_='fileslist', colspan='2')
                        if prod:
                            for word in prod.get_text('\n').split():
                                if word.startswith('cpe:/'):
                                    cpe.add(word.strip())
                        j += 1
                    i = j
                    continue
        i += 1
    return cpe

def walk_reports(input_dir: str, output: str):
    """Обходит директорию, парсит HTML-отчеты и выводит результат."""
    results = {}
    html_files = [f for f in os.listdir(input_dir)
                  if f.lower().endswith('.html') and os.path.isfile(os.path.join(input_dir, f))]
    try:
        for fname in tqdm(html_files, desc='Parsing reports', unit='file'):
            fpath = os.path.join(input_dir, fname)
            results[fname] = sorted(parse_cpe_for_crit_high(fpath))
    except KeyboardInterrupt:
        print('\n[!] Прервано пользователем, выводим уже обработанные файлы…')

    if output == 'json':
        print(json.dumps(results, ensure_ascii=False, indent=2))
    elif output == 'txt':
        with open(TXT_OUT, 'w', encoding='utf-8') as fp:
            for rep, cpes in results.items():
                fp.write(f'Файл: {rep}\n')
                fp.writelines(f'  {c}\n' for c in cpes) if cpes else fp.write('  — нет CPE\n')
                fp.write('\n')
        print(f'[+] Записано в {TXT_OUT}')
    else:
        for rep, cpes in results.items():
            print(f'\nФайл: {rep}')
            print('\n'.join(f'  {c}' for c in cpes) or '  — нет CPE')

if __name__ == '__main__':
    argp = argparse.ArgumentParser()
    argp.add_argument('--dir', default='.', help='Директория с HTML-отчетами (по умолчанию текущая).')
    argp.add_argument('--output', choices=['json', 'console', 'txt'], default='console',
                      help='Формат вывода: json, console, txt (по умолчанию console).')
    args = argp.parse_args()
    walk_reports(args.dir, args.output)
