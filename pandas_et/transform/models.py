from typing import Annotated, Any, Literal, Union

from pydantic import BaseModel, Field


class Extract(BaseModel):
    op: Literal["extract"] = "extract"
    pattern: str
    source: str
    destination: str


class Rename(BaseModel):
    op: Literal["rename"] = "rename"
    mapping: dict[str, str]


class Convert(BaseModel):
    op: Literal["convert"] = "convert"
    dtype: str
    source: str
    destination: str | None = None


class DropNA(BaseModel):
    op: Literal["drop_na"] = "drop_na"
    axis: Literal["rows", "columns"] = "rows"
    how: Literal["any", "all"] = "any"
    columns: list[str] | None = None


class FillNA(BaseModel):
    op: Literal["fill_na"] = "fill_na"
    columns: list[str] | None = None
    value: Any = ""


class Query(BaseModel):
    op: Literal["query"] = "query"
    expression: str


class Reindex(BaseModel):
    op: Literal["reindex"] = "reindex"
    columns: list[str]


class Sort(BaseModel):
    op: Literal["sort"] = "sort"
    by: str | list[str]
    ascending: bool = True
    natsort: bool = False


class Concat(BaseModel):
    op: Literal["concat"] = "concat"
    columns: list[str]
    destination: str
    sep: str = " "


class NormalizeWhitespaces(BaseModel):
    op: Literal["normalize_whitespaces"] = "normalize_whitespaces"
    columns: list[str] | None = None


TransformAnnotation = Annotated[
    Union[
        Extract,
        Rename,
        Convert,
        DropNA,
        FillNA,
        Query,
        Reindex,
        Sort,
        Concat,
        NormalizeWhitespaces,
    ],
    Field(discriminator="op"),
]
