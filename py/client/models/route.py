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
    from ..models.move import Move

T = TypeVar("T", bound="Route")


@attr.s(auto_attribs=True)
class Route:
    """
    Attributes:
        map_id (Union[Unset, str]): Идентификатор карты
        moves (Union[Unset, List['Move']]): Массив объектов с координатами, в которые будет совершаться перемещение
            Example: [{'x': 30, 'y': 60}, {'x': 120, 'y': 60}, {'x': 45, 'y': 150}, {'x': 0, 'y': 0}].
        stack_of_bags (Union[Unset, List[List[List[int]]]]): Массив с сумками подарков, при заходе в точку 0,0 (учитывая
            старт) берётся последний элемент Example: [[1, 2, 3], [4, 5, 6]].
    """

    map_id: Union[Unset, str] = UNSET
    moves: Union[Unset, List['Move']] = UNSET
    stack_of_bags: Union[Unset, List[List[List[int]]]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.move import Move
        map_id = self.map_id
        moves: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.moves, Unset):
            moves = []
            for moves_item_data in self.moves:
                moves_item = moves_item_data.to_dict()

                moves.append(moves_item)

        stack_of_bags: Union[Unset, List[List[List[int]]]] = UNSET
        if not isinstance(self.stack_of_bags, Unset):
            stack_of_bags = []
            for stack_of_bags_item_data in self.stack_of_bags:
                stack_of_bags_item = []
                for componentsschemas_gift_bag_item_data in stack_of_bags_item_data:
                    componentsschemas_gift_bag_item = componentsschemas_gift_bag_item_data

                    stack_of_bags_item.append(componentsschemas_gift_bag_item)

                stack_of_bags.append(stack_of_bags_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if map_id is not UNSET:
            field_dict["mapID"] = map_id
        if moves is not UNSET:
            field_dict["moves"] = moves
        if stack_of_bags is not UNSET:
            field_dict["stackOfBags"] = stack_of_bags

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.move import Move
        d = src_dict.copy()
        map_id = d.pop("mapID", UNSET)

        moves = []
        _moves = d.pop("moves", UNSET)
        for moves_item_data in (_moves or []):
            moves_item = Move.from_dict(moves_item_data)

            moves.append(moves_item)

        stack_of_bags = []
        _stack_of_bags = d.pop("stackOfBags", UNSET)
        for stack_of_bags_item_data in (_stack_of_bags or []):
            stack_of_bags_item = []
            _stack_of_bags_item = stack_of_bags_item_data
            for componentsschemas_gift_bag_item_data in (_stack_of_bags_item):
                componentsschemas_gift_bag_item = cast(List[int], componentsschemas_gift_bag_item_data)

                stack_of_bags_item.append(componentsschemas_gift_bag_item)

            stack_of_bags.append(stack_of_bags_item)

        route = cls(
            map_id=map_id,
            moves=moves,
            stack_of_bags=stack_of_bags,
        )

        route.additional_properties = d
        return route

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
