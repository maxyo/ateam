from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List

import attr

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union

T = TypeVar("T", bound="SnowArea")


@attr.s(auto_attribs=True)
class SnowArea:
    """
    Attributes:
        r (Union[Unset, int]): Радиус окружности, описывающей снежную зону Example: 10.
        x (Union[Unset, int]): Координата X центра окружности, описывающей снежную зону Example: 100.
        y (Union[Unset, int]): Координата Y центра окружности, описывающей снежную зону Example: 250.
    """

    r: Union[Unset, int] = UNSET
    x: Union[Unset, int] = UNSET
    y: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        r = self.r
        x = self.x
        y = self.y

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if r is not UNSET:
            field_dict["r"] = r
        if x is not UNSET:
            field_dict["x"] = x
        if y is not UNSET:
            field_dict["y"] = y

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        r = d.pop("r", UNSET)

        x = d.pop("x", UNSET)

        y = d.pop("y", UNSET)

        snow_area = cls(
            r=r,
            x=x,
            y=y,
        )

        snow_area.additional_properties = d
        return snow_area

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
