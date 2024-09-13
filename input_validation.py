from pathlib import Path

def validate_CQL(path) -> bool:
    if not any(path.glob('*.sarif')):
        return False
    return True

def validate_CLJ(path) -> bool:
    if not any(path.glob('*.csv')):
        return False
    return True

def validate_CNL(path) -> bool:
    if not any(path.glob('*.csv')):
        return False
    return True

### CHANGE
# add more functions here if more tools is coming