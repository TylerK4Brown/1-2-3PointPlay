## number_formatting.py
## Converts numeric values to cleaner UI-friendly representations when possible
## This probably didn't have to be its own module, but it is anyways

# Displays floating point values as integers if they are whole numbers, otherwise displays them as floats
def format_points(value):
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value