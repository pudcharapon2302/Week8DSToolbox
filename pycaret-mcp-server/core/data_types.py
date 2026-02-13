import pandas as pd

def get_descriptive_type(series: pd.Series) -> str:
    if pd.api.types.is_bool_dtype(series): return 'bool'
    if pd.api.types.is_datetime64_any_dtype(series): return 'datetime'
    if pd.api.types.is_numeric_dtype(series):
        if pd.api.types.is_integer_dtype(series): return 'int'
        return 'float'
    if pd.api.types.is_categorical_dtype(series) or pd.api.types.is_object_dtype(series):
        return 'string/category'
    return str(series.dtype)