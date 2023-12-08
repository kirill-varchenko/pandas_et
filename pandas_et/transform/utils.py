from functools import reduce

import pandas as pd

from .impls import TRANSFORMS
from .models import TransformAnnotation


def apply_tranform(df: pd.DataFrame, transform: TransformAnnotation) -> pd.DataFrame:
    """Apply transform"""
    transform_params = transform.model_dump()
    transform_name = transform_params.pop("op")
    fn = TRANSFORMS[transform_name]
    return fn(df, **transform_params)


def apply_tranforms(
    df: pd.DataFrame, transforms: list[TransformAnnotation]
) -> pd.DataFrame:
    """Apply sequence of transforms"""
    return reduce(lambda cum, new: apply_tranform(cum, new), transforms, df)
