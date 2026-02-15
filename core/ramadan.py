from datetime import date

# Approximate Ramadan ranges (Gregorian) for upcoming years.
RAMADAN_RANGES = [
    (date(2025, 2, 28), date(2025, 3, 29)),
    (date(2026, 2, 17), date(2026, 3, 18)),
    (date(2027, 2, 7), date(2027, 3, 8)),
    (date(2028, 1, 27), date(2028, 2, 25)),
    (date(2029, 1, 15), date(2029, 2, 13)),
    (date(2030, 1, 5), date(2030, 2, 3)),
]


def is_ramadan(check_date):
    return any(start <= check_date <= end for start, end in RAMADAN_RANGES)
