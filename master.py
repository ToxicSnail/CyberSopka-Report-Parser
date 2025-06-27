#!/usr/bin/env python3
import json, argparse

def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def build_master(counts_json, cpe_json):
    counts = load_json(counts_json)
    cpes = load_json(cpe_json)
    master = {}

    all_keys = set(counts.keys()).union(cpes.keys())
    for report in all_keys:
        report_cpes = sorted(set(cpes.get(report, [])))
        test_str = f"Необходимо обновить следующее ПО: {', '.join(report_cpes)}" if report_cpes else "Необходимо обновить следующее ПО: отсутствует"
        master[report] = {
            "danger level": counts.get(report, {}),
            "cpe": report_cpes,
            "test text": test_str
        }
    return master

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Сборка master_file.json с полем test.')
    parser.add_argument('counts_json', help='Файл с данными о количестве уязвимостей (count_vuln.json)')
    parser.add_argument('cpe_json', help='Файл с данными о CPE (output.json)')
    parser.add_argument('-o', '--output', default='master_file.json', help='Имя итогового JSON (по умолчанию master_file.json)')
    args = parser.parse_args()

    master_data = build_master(args.counts_json, args.cpe_json)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(master_data, f, ensure_ascii=False, indent=2)

    print(f"[+] Итоговый файл сохранен: {args.output}")
