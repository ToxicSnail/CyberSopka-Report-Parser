from bs4 import BeautifulSoup
import pandas as pd
import os

files_list_path = "files.txt"

with open(files_list_path, "r", encoding="utf-8") as f:
    html_files = [line.strip() for line in f.readlines()]

for html_file in html_files:
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

        data = []

        rows = soup.find_all("tr")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 0:
                identifier = cols[0].text.strip() if len(cols) > 0 else ""
                risk_level = cols[1].find("div").text.strip() if len(cols) > 1 and cols[1].find("div") else ""
                description = cols[2].text.strip() if len(cols) > 2 else ""
                resource = cols[3].text.strip() if len(cols) > 3 and "fileslist" in cols[3].get("class", []) else ""

                data.append([identifier, risk_level, description, resource])

        df = pd.DataFrame(data, columns=["Идентификатор уязвимости", "Уровень опасности", "Описание", "Ресурс уязвимости"])

        critical_vulnerabilities = df[df["Уровень опасности"] == "Критический"]
        high_vulnerabilities = df[df["Уровень опасности"] == "Высокий"]

        combined_vulnerabilities = pd.concat([critical_vulnerabilities, high_vulnerabilities])

        if not combined_vulnerabilities.empty:
            output_file = f"{os.path.splitext(html_file)[0]}_critical_and_high_vulnerabilities.xlsx"
            combined_vulnerabilities.to_excel(output_file, index=False)
            print(f"Найдено {len(combined_vulnerabilities)} критических и высоких уязвимостей в файле {html_file}. Результаты сохранены в файл: {output_file}")
        
    else:
        print(f"Файл {html_file} не найден.")
