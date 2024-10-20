# Example of converting strings to integers and handling exceptions.
def convert_to_int(s):
    try:
        return int(s)
    except ValueError:
        return None
