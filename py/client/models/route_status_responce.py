from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List

import attr

from ..types import UNSET, Unset

from typing import cast
from typing import Dict
from typing import Union
from typing import Optional
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.round_processing_result import RoundProcessingResult

T = TypeVar("T", bound="RouteStatusResponce")


@attr.s(auto_attribs=True)
class RouteStatusResponce:
    """
    Attributes:
        success (Union[Unset, bool]): Показатель успешности запроса
        error (Union[Unset, None, str]): Сообщение с описанием ошибки
        data (Union[Unset, None, RoundProcessingResult]): Информация о раунде
    """

    success: Union[Unset, bool] = UNSET
    error: Union[Unset, None, str] = UNSET
    data: Union[Unset, None, 'RoundProcessingResult'] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.round_processing_result import RoundProcessingResult
        success = self.success
        error = self.error
        data: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict() if self.data else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if success is not UNSET:
            field_dict["success"] = success
        if error is not UNSET:
            field_dict["error"] = error
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.round_processing_result import RoundProcessingResult
        d = src_dict.copy()
        success = d.pop("success", UNSET)

        error = d.pop("error", UNSET)

        _data = d.pop("data", UNSET)
        data: Union[Unset, None, RoundProcessingResult]
        if _data is None:
            data = None
        elif isinstance(_data, Unset):
            data = UNSET
        else:
            data = RoundProcessingResult.from_dict(_data)

        route_status_responce = cls(
            success=success,
            error=error,
            data=data,
        )

        route_status_responce.additional_properties = d
        return route_status_responce

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
