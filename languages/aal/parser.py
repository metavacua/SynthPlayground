import yaml

def parse(aal_file):
    """
    Parses an AAL file and returns a list of Python dictionaries.
    """
    with open(aal_file, 'r') as f:
        return list(yaml.safe_load_all(f))
