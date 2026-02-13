import os

def validate_file_path(file_path: str) -> dict:
    if not file_path:
        return {"valid": False, "error": "File path is required"}
    if not os.path.exists(file_path):
        return {"valid": False, "error": f"File not found: {file_path}"}
    return {"valid": True}

def validate_pandas_code(code: str) -> dict:
    if not code or len(code.strip()) < 5:
        return {"valid": False, "error": "Code is too short or empty"}
    return {"valid": True}