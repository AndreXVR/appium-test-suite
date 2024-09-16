import re

def bounds_to_coordinates(bounds):
    pattern = re.compile(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]')
    result =  pattern.search(bounds)
    return {}
    