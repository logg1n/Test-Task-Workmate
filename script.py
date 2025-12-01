import csv
import re

from table import Table


def analysis_of_developer_performance(files, *callbacks, keys=None):

    pattern = re.compile(r"^-?\d+(?:\.\d+)?$")

    table = None

    for file in files:
        with open(file, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)

            valid_keys = [k for k in (keys or []) if k in headers]

            if table is None:
                table = Table(valid_keys)

            indexes = [headers.index(v) for v in valid_keys]

            for row in reader:
                if valid_keys:
                    values = [
                        float(v) if pattern.match(v) else v
                        for v in (row[i] for i in indexes)
                    ]
                    table.add_row(values)

    if table is None:
        return None

    result = table
    for c in callbacks or ():
        result = c(result)

    return result
