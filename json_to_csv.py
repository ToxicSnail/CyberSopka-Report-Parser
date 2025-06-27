#!/usr/bin/env python3
import json, argparse, csv

def json_to_csv(master_json, output_csv):
    with open(master_json, encoding='utf-8') as f:
        data = json.load(f)
    
    with open(output_csv, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['Report', 'Critical', 'High', 'Medium', 'Low', 'CPEs', 'Test']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for report, details in data.items():
            counts = details.get('counts', {})
            cpes = details.get('cpe', [])
            writer.writerow({
                'Report': report,
                'Critical': counts.get('Critical', 0),
                'High': counts.get('High', 0),
                'Medium': counts.get('Medium', 0),
                'Low': counts.get('Low', 0),
                'CPEs': ', '.join(cpes)
            })

    print(f"[+] CSV-файл сохранен: {output_csv}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Конвертирует master_file.json в таблицу CSV.')
    parser.add_argument('master_json', help='Путь к master_file.json')
    parser.add_argument('-o', '--output', default='master_table.csv', help='Имя итогового CSV (по умолчанию master_table.csv)')
    args = parser.parse_args()
    json_to_csv(args.master_json, args.output)
