from datetime import datetime


def make_time_batches(from_date: str, to_date: str, fmt: str = "%d/%m/%Y"):
    start_dt = datetime.strptime(from_date, fmt)
    end_dt = datetime.strptime(to_date, fmt)
    if start_dt > end_dt:
        raise ValueError("Start date must be before end date")

    time_from = int(start_dt.timestamp())

    time_to = int(end_dt.timestamp())
    step = 15 * 86400
    batches = []

    cur_start = time_from
    while cur_start <= time_to:
        cur_end = min(cur_start + step, time_to)
        batches.append((cur_start, cur_end))
        cur_start = cur_end + 1

    return batches , time_from , time_to

