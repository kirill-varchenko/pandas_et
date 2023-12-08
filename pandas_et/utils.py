import pandas as pd

from .extract import read
from .models import Schema
from .transform import apply_tranforms


def process_file(file: str, schema: Schema) -> pd.DataFrame:
    """Read file and apply transformations"""
    df = read(file, schema.read)
    return apply_tranforms(df, schema.transforms)
