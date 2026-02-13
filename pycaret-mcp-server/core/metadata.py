import os
import pandas as pd
from chardet import detect
from .config import MAX_FILE_SIZE
from .data_types import get_descriptive_type
from .validation import validate_file_path
from .error_handling import ErrorType, handle_exception, log_and_return_error

def read_metadata(file_path: str) -> dict:
    try:
        val = validate_file_path(file_path)
        if not val['valid']: return log_and_return_error(ErrorType.INVALID_FILE_PATH, val['error'])
        
        file_size = os.path.getsize(file_path)
        if file_size > MAX_FILE_SIZE: return log_and_return_error(ErrorType.FILE_TOO_LARGE, "File too large")

        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.csv':
            with open(file_path, 'rb') as f:
                raw = f.read(10000)
                enc = detect(raw)['encoding'] or 'utf-8'
            df = pd.read_csv(file_path, encoding=enc, nrows=100)
            rows = sum(1 for _ in open(file_path, 'r', encoding=enc)) - 1
            type_name = "csv"
        elif ext in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path, nrows=100)
            rows = "Unknown (Excel)"
            type_name = "excel"
        else:
            return log_and_return_error(ErrorType.UNSUPPORTED_FILE_TYPE, "Unsupported extension")

        cols = []
        for col in df.columns:
            cols.append({
                "name": str(col),
                "type": get_descriptive_type(df[col]),
                "examples": df[col].dropna().head(3).tolist()
            })

        return {
            "status": "SUCCESS",
            "file_info": {"type": type_name, "size_kb": round(file_size/1024, 2)},
            "data": {"rows": rows, "columns": cols}
        }
    except Exception as e:
        return handle_exception(e, ErrorType.DATA_ERROR, "Metadata extraction failed")