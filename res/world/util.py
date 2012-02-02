"""utility functions for the world scripts"""

def img(*parts):
    """Process a sequence of string parts and return an image filename.
    
    If parts is tested false, return an empty string. If parts has only
    one element, return that element. Otherwise, return a string of
    each part joined by '-' (hyphen) characters.
    """
    if not parts:
        return ''
    if len(parts) == 1:
        return parts[0]
    return '-'.join(parts)
