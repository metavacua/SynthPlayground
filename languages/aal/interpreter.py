def interpret(aal_data):
    """
    Interprets a parsed AAL data structure.
    """
    for doc in aal_data:
        if "protocol_id" not in doc:
            raise ValueError("Missing 'protocol_id' in AAL data.")
        if "rules" not in doc:
            raise ValueError("Missing 'rules' in AAL data.")
    return True
