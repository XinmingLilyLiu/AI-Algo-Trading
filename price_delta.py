import csv
import os
import sys

def tryread(name):
    try:
        with open(name, "r") as csvfile:
            return [r for r in csv.reader(csvfile)]
    except:
        print(f"Could not read file: {name}")
        exit(-1)

def conv_row(row, conv_dict):
    new_row = row
    for i in conv_dict: new_row[i] = conv_dict[i](new_row[i])
    return new_row

def conv(data, conv_dict):
    return map(lambda r: conv_row(r, conv_dict), data)

def price_delta(data, date_col_n="history_day_date",
                open_col_n="history_day_open",
                close_col_n="history_day_close"):
    if data is None or len(data) == 0:
        raise ValueError("Data empty")
    
    cols = data[0]

    if not set([date_col_n, open_col_n, close_col_n]).issubset(set(cols)):
        raise ValueError("Data has incorrect columns")

    date_col = cols.index(date_col_n)
    open_col, close_col = cols.index(open_col_n), cols.index(close_col_n)

    data = list(conv(data[1:], {open_col: float, close_col: float}))

    calc_data = [date_col_n, "intra", "delta_pc"]
    for i in range(len(data) - 1):
        r_now, r_next = data[i], data[i + 1]
        pc_intra = (r_now[close_col] - r_now[open_col]) / r_now[open_col]
        pc_before = (r_next[open_col] - r_now[close_col]) / r_now[close_col]

        calc_data.append([r_now[date_col], 1, pc_intra])
        calc_data.append([r_next[date_col], 0, pc_before])

    r_last = data[-1]
    pc_intra_last = (r_last[close_col] - r_last[open_col]) / r_last[open_col]
    calc_data.append([r_last[date_col], 1, pc_intra_last])

    return calc_data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: price_delta.py [data.csv]", file=sys.stderr)
        exit(1)

    data = tryread(sys.argv[1])

    calc_data = None

    try:
        calc_data = price_delta(data)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        exit(1)

    if not calc_data is None:
        writer = csv.writer(sys.stdout)
        writer.writerow(["history_day_date", "intra", "delta_pc"])
        for r in calc_data: writer.writerow(r)
