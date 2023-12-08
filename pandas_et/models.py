from pydantic import BaseModel

from .extract import ReadAnnotation
from .transform import TransformAnnotation


class Schema(BaseModel):
    read: ReadAnnotation
    transforms: list[TransformAnnotation] = []
