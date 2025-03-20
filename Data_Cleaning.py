def clean_numeric_value(value):
    """Convert values like '2k' to integers (2000)"""
    if isinstance(value, str):
        # Handle 'k' suffix (thousands)
        if value.lower().endswith('k'):
            try:
                return int(float(value[:-1]) * 1000)
            except ValueError:
                return 0
        # Handle other potential formats
        try:
            return int(value)
        except ValueError:
            return 0
    return value