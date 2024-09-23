from pathlib import Path


def validate_csv(path) -> bool:
    if not any(path.glob("*.csv")):
        return False
    return True


def validate_codeql(path) -> bool:
    if not any(path.glob("*.sarif")):
        return False
    return True


# these may be removed if later clojure and coccinelle inputs still only contains csv files

# def validate_clojure(path) -> bool:
#     if not any(path.glob('*.csv')):
#         return False
#     return True

# def validate_coccinelle(path) -> bool:
#     if not any(path.glob('*.csv')):
#         return False
#     return True

### CHANGE
# add more functions here if more tools is coming
