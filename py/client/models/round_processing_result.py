from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


import attr

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Union





T = TypeVar("T", bound="RoundProcessingResult")

@attr.s(auto_attribs=True)
class RoundProcessingResult:
    """Информация о раунде

    Attributes:
        error_message (Union[Unset, str]): Описание ошибки обработки раунда
        status (Union[Unset, str]): Статус раунда
        total_time (Union[Unset, int]): Итоговое время раунда
        total_length (Union[Unset, int]): Итоговое пройденное расстояние
    """

    error_message: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    total_time: Union[Unset, int] = UNSET
    total_length: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        error_message = self.error_message
        status = self.status
        total_time = self.total_time
        total_length = self.total_length

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if status is not UNSET:
            field_dict["status"] = status
        if total_time is not UNSET:
            field_dict["total_time"] = total_time
        if total_length is not UNSET:
            field_dict["total_length"] = total_length

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        error_message = d.pop("error_message", UNSET)

        status = d.pop("status", UNSET)

        total_time = d.pop("total_time", UNSET)

        total_length = d.pop("total_length", UNSET)

        round_processing_result = cls(
            error_message=error_message,
            status=status,
            total_time=total_time,
            total_length=total_length,
        )

        round_processing_result.additional_properties = d
        return round_processing_result

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
