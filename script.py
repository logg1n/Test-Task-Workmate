import csv
import re

from table import Table


def analysis_of_developer_performance(files, keys=None):
    pattern = re.compile(r"^-?\d+(?:\.\d+)?$")
    table = None

    for file in files:
        with open(file, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)

            if not keys:
                valid_keys = headers
            else:
                valid_keys = [k for k in keys if k in headers]

            if table is None:
                table = Table(valid_keys)

            indexes = [headers.index(v) for v in valid_keys]

            if not indexes:
                continue

            for row in reader:
                values = [
                    float(v) if pattern.match(v) else v
                    for v in (row[i] for i in indexes)
                ]
                table.add_row(values)

    return table
