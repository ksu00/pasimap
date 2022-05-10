

def is_ascii(
        s: str
        ) -> bool:
    try:
        s.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True
