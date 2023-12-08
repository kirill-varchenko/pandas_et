import logging
import re
from pathlib import Path
from typing import Callable

import pandas as pd

from . import models

logger = logging.getLogger("pandas_et")


def _match_pattern(pattern: re.Pattern):
    def helper(col: str) -> bool:
        res = pattern.match(col) is not None
        if not res:
            logger.debug("Dropped by pattern matcher: %s", col)
        return res

    return helper


def _is_in_list(variants: list[str]):
    var_set = set(variants)

    def helper(col: str) -> bool:
        res = col in var_set
        if not res:
            logger.debug("Dropped by given list: %s", col)
        return res

    return helper


def _usecols(model: models.BaseRead) -> list[str] | Callable | None:
    """Make pandas usecols argument from the model."""
    return (
        _match_pattern(model.columns)
        if isinstance(model.columns, re.Pattern)
        else _is_in_list(model.columns)
        if isinstance(model.columns, list)
        else model.columns
    )


def _filter_sheet_names(
    sheet_names: list[str],
    condition: int | str | list[str] | re.Pattern | None,
) -> list[str]:
    """Filter list of sheetnames based on given spec."""
    if condition is None:
        return sheet_names
    if isinstance(condition, int):
        return [sheet_names[condition]]
    if isinstance(condition, str):
        if condition in sheet_names:
            return [condition]
        return []
    if isinstance(condition, list):
        return [sheet_name for sheet_name in sheet_names if sheet_name in condition]
    if isinstance(condition, re.Pattern):
        return [sheet_name for sheet_name in sheet_names if condition.match(sheet_name)]
    return []


def read_csv(file: str, model: models.ReadCSV) -> pd.DataFrame:
    """Read file as CSV."""
    df = pd.read_csv(file, sep=model.sep, usecols=_usecols(model), dtype=str)
    return df


def read_excel(file: str, model: models.ReadExcel) -> pd.DataFrame:
    """Read file as Excel."""
    excel = pd.ExcelFile(file)
    sheet_dfs = []
    logger.debug(
        "Loaded sheets: %s", ", ".join(repr(sheet) for sheet in excel.sheet_names)
    )
    for sheet_name in _filter_sheet_names(excel.sheet_names, model.sheets):  # type: ignore
        df = excel.parse(sheet_name, usecols=_usecols(model), dtype=str)
        if model.sheetname_column:
            df[model.sheetname_column] = sheet_name
        sheet_dfs.append(df)
    df = pd.concat(sheet_dfs, ignore_index=True)
    return df


def read(file: str, model: models.BaseRead) -> pd.DataFrame:
    """Read file based on read model."""
    if isinstance(model, models.ReadCSV):
        df = read_csv(file, model)
    elif isinstance(model, models.ReadExcel):
        df = read_excel(file, model)
    else:
        raise TypeError()
    if model.filename_column:
        df[model.filename_column] = Path(file).name
    return df
