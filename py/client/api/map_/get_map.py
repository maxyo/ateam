from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ...client import Client
from ...types import Response
from ... import errors

from ...models.map_ import Map
from typing import cast
from typing import Dict



def _get_kwargs(
    map_id: str = 'faf7ef78-41b3-4a36-8423-688a61929c08',
    *,
    client: Client,

) -> Dict[str, Any]:
    url = "{}/json/map/{map_id}.json".format(
        client.base_url,map_id=map_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    

    

    return {
	    "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, Map]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Map.from_dict(response.json())



        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, Map]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    map_id: str = 'faf7ef78-41b3-4a36-8423-688a61929c08',
    *,
    client: Client,

) -> Response[Union[Any, Map]]:
    """Получение данных детей, подарков и снежных зон.

    Args:
        map_id (str):  Default: 'faf7ef78-41b3-4a36-8423-688a61929c08'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Map]]
    """


    kwargs = _get_kwargs(
        map_id=map_id,
client=client,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    map_id: str = 'faf7ef78-41b3-4a36-8423-688a61929c08',
    *,
    client: Client,

) -> Optional[Union[Any, Map]]:
    """Получение данных детей, подарков и снежных зон.

    Args:
        map_id (str):  Default: 'faf7ef78-41b3-4a36-8423-688a61929c08'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Map]]
    """


    return sync_detailed(
        map_id=map_id,
client=client,

    ).parsed

async def asyncio_detailed(
    map_id: str = 'faf7ef78-41b3-4a36-8423-688a61929c08',
    *,
    client: Client,

) -> Response[Union[Any, Map]]:
    """Получение данных детей, подарков и снежных зон.

    Args:
        map_id (str):  Default: 'faf7ef78-41b3-4a36-8423-688a61929c08'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Map]]
    """


    kwargs = _get_kwargs(
        map_id=map_id,
client=client,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(client=client, response=response)

async def asyncio(
    map_id: str = 'faf7ef78-41b3-4a36-8423-688a61929c08',
    *,
    client: Client,

) -> Optional[Union[Any, Map]]:
    """Получение данных детей, подарков и снежных зон.

    Args:
        map_id (str):  Default: 'faf7ef78-41b3-4a36-8423-688a61929c08'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Map]]
    """


    return (await asyncio_detailed(
        map_id=map_id,
client=client,

    )).parsed

