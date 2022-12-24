from typing import Any, Dict, Type, TypeVar, Tuple, Optional, BinaryIO, TextIO, TYPE_CHECKING

from typing import List


import attr

from ..types import UNSET, Unset

from typing import cast
from typing import Dict
from typing import Union
from typing import cast, List
from ..types import UNSET, Unset

if TYPE_CHECKING:
  from ..models.snow_area import SnowArea
  from ..models.child import Child
  from ..models.gift import Gift




T = TypeVar("T", bound="Map")

@attr.s(auto_attribs=True)
class Map:
    """
    Attributes:
        gifts (Union[Unset, List['Gift']]):
        snow_areas (Union[Unset, List['SnowArea']]):
        children (Union[Unset, List['Child']]):
    """

    gifts: Union[Unset, List['Gift']] = UNSET
    snow_areas: Union[Unset, List['SnowArea']] = UNSET
    children: Union[Unset, List['Child']] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        from ..models.snow_area import SnowArea
        from ..models.child import Child
        from ..models.gift import Gift
        gifts: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.gifts, Unset):
            gifts = []
            for gifts_item_data in self.gifts:
                gifts_item = gifts_item_data.to_dict()

                gifts.append(gifts_item)




        snow_areas: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.snow_areas, Unset):
            snow_areas = []
            for snow_areas_item_data in self.snow_areas:
                snow_areas_item = snow_areas_item_data.to_dict()

                snow_areas.append(snow_areas_item)




        children: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.children, Unset):
            children = []
            for children_item_data in self.children:
                children_item = children_item_data.to_dict()

                children.append(children_item)





        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if gifts is not UNSET:
            field_dict["gifts"] = gifts
        if snow_areas is not UNSET:
            field_dict["snowAreas"] = snow_areas
        if children is not UNSET:
            field_dict["children"] = children

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.snow_area import SnowArea
        from ..models.child import Child
        from ..models.gift import Gift
        d = src_dict.copy()
        gifts = []
        _gifts = d.pop("gifts", UNSET)
        for gifts_item_data in (_gifts or []):
            gifts_item = Gift.from_dict(gifts_item_data)



            gifts.append(gifts_item)


        snow_areas = []
        _snow_areas = d.pop("snowAreas", UNSET)
        for snow_areas_item_data in (_snow_areas or []):
            snow_areas_item = SnowArea.from_dict(snow_areas_item_data)



            snow_areas.append(snow_areas_item)


        children = []
        _children = d.pop("children", UNSET)
        for children_item_data in (_children or []):
            children_item = Child.from_dict(children_item_data)



            children.append(children_item)


        map_ = cls(
            gifts=gifts,
            snow_areas=snow_areas,
            children=children,
        )

        map_.additional_properties = d
        return map_

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
