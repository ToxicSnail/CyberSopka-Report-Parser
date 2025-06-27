#!/usr/bin/env python3
import json, argparse

def analyze_unique_cpes(json_file):
    with open(json_file, encoding='utf-8') as f:
        data = json.load(f)
    unique_cpes = set()
    for cpe_list in data.values():
        unique_cpes.update(cpe_list)
    return sorted(unique_cpes)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Анализатор уникальных CPE из JSON-отчета.')
    parser.add_argument('jsonfile', help='Путь к JSON-файлу с результатами парсинга.')
    args = parser.parse_args()

    uniques = analyze_unique_cpes(args.jsonfile)
    print('[+] Уникальные CPE (всего: {}):'.format(len(uniques)))
    for cpe in uniques:
        print(cpe)
