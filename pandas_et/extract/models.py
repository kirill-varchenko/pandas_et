import re
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class BaseRead(BaseModel):
    type: Literal["csv", "excel"]
    columns: list[str] | re.Pattern | None = None
    filename_column: str | None = None


class ReadCSV(BaseRead):
    type: Literal["csv"] = "csv"
    sep: str = ","


class ReadExcel(BaseRead):
    type: Literal["excel"] = "excel"
    sheets: int | list[str] | re.Pattern | None = 0
    sheetname_column: str | None = None


ReadAnnotation = Annotated[ReadCSV | ReadExcel, Field(discriminator="type")]
