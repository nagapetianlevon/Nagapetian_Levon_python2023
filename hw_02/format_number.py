def format_number(value: float) -> str:

    int, frac= f"{value:,.3f}".split('.')
    formatted = f"{int.replace(',', ' ')} .{frac}"

    return f'{formatted:*^30}'


print(format_number((100)))
print(format_number((123488482390.28174)))