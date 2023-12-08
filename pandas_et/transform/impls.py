from typing import Any, Callable, Concatenate, Literal, ParamSpec

import pandas as pd
from natsort import natsort_keygen

P = ParamSpec("P")

TransformFn = Callable[Concatenate[pd.DataFrame, P], pd.DataFrame]


def extract(
    df: pd.DataFrame, pattern: str, source: str, destination: str
) -> pd.DataFrame:
    df[destination] = df[source].str.extract(pattern, expand=False)
    return df


def rename(df: pd.DataFrame, mapping: dict[str, str]) -> pd.DataFrame:
    return df.rename(columns=mapping)


def convert(
    df: pd.DataFrame, dtype: str, source: str, destination: str | None
) -> pd.DataFrame:
    dest = destination or source
    df[dest] = df[source].astype(dtype)  # type: ignore
    return df


def drop_na(
    df: pd.DataFrame,
    axis: Literal["rows", "columns"] = "rows",
    how: Literal["any", "all"] = "any",
    columns: list[str] | None = None,
) -> pd.DataFrame:
    pd_axis = "index" if axis == "rows" else "columns"
    return df.dropna(axis=pd_axis, how=how, subset=columns)


def fill_na(
    df: pd.DataFrame, columns: list[str] | None = None, value: Any = ""
) -> pd.DataFrame:
    if columns is None:
        return df.fillna(value)
    for column in columns:
        df[column] = df[column].fillna(value)
    return df


def query(df: pd.DataFrame, expression: str) -> pd.DataFrame:
    return df.query(expression)


def reindex(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    return df.reindex(columns=columns)


def sort_(
    df: pd.DataFrame, by: str | list[str], ascending: bool = True, natsort: bool = False
) -> pd.DataFrame:
    key = natsort_keygen() if natsort else None
    return df.sort_values(by=by, ascending=ascending, key=key)


def concat(
    df: pd.DataFrame, columns: list[str], destination: str, sep: str = " "
) -> pd.DataFrame:
    if not columns:
        return df
    if len(columns) == 1:
        df[destination] = df[columns[0]]
        return df
    df[destination] = df[columns[0]].str.cat(others=df[columns[1:]], sep=sep, na_rep="")
    return df


def normalize_whitespaces(
    df: pd.DataFrame, columns: list[str] | None = None
) -> pd.DataFrame:
    """Strip and replace whitespace with a single space"""
    if columns is None:
        return df.fillna("").replace(r"\s+", " ", regex=True).applymap(str.strip)
    for column in columns:
        df[column] = (
            df[column].fillna("").replace(r"\s+", " ", regex=True).apply(str.strip)
        )
    return df


TRANSFORMS: dict[str, TransformFn] = {
    "extract": extract,
    "rename": rename,
    "convert": convert,
    "drop_na": drop_na,
    "fill_na": fill_na,
    "query": query,
    "reindex": reindex,
    "sort": sort_,
    "concat": concat,
    "normalize_whitespaces": normalize_whitespaces,
}
