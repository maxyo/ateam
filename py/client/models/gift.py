from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


import attr

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union





T = TypeVar("T", bound="Gift")

@attr.s(auto_attribs=True)
class Gift:
    """
    Attributes:
        id (Union[Unset, int]): Идентификатор подарка Example: 10.
        weight (Union[Unset, int]): Вес подарка, кг Example: 4.
        volume (Union[Unset, int]): Объем подарка, дм.куб. Example: 12.
    """

    id: Union[Unset, int] = UNSET
    weight: Union[Unset, int] = UNSET
    volume: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        weight = self.weight
        volume = self.volume

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if id is not UNSET:
            field_dict["id"] = id
        if weight is not UNSET:
            field_dict["weight"] = weight
        if volume is not UNSET:
            field_dict["volume"] = volume

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        weight = d.pop("weight", UNSET)

        volume = d.pop("volume", UNSET)

        gift = cls(
            id=id,
            weight=weight,
            volume=volume,
        )

        gift.additional_properties = d
        return gift

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
