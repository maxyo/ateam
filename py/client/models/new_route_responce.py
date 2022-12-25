from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List

import attr

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Optional
from typing import Union

T = TypeVar("T", bound="NewRouteResponce")


@attr.s(auto_attribs=True)
class NewRouteResponce:
    """
    Attributes:
        success (Union[Unset, bool]): Показатель успешности запроса
        error (Union[Unset, None, str]): Сообщение с описанием ошибки
        round_id (Union[Unset, None, str]): ID созданного раунда
    """

    success: Union[Unset, bool] = UNSET
    error: Union[Unset, None, str] = UNSET
    round_id: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        success = self.success
        error = self.error
        round_id = self.round_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if success is not UNSET:
            field_dict["success"] = success
        if error is not UNSET:
            field_dict["error"] = error
        if round_id is not UNSET:
            field_dict["roundId"] = round_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        success = d.pop("success", UNSET)

        error = d.pop("error", UNSET)

        round_id = d.pop("roundId", UNSET)

        new_route_responce = cls(
            success=success,
            error=error,
            round_id=round_id,
        )

        new_route_responce.additional_properties = d
        return new_route_responce

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
