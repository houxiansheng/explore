import asyncio
import aiohttp
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    List,
    Mapping,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
    cast,
)


class Http():
    async def _get(self, option):
        async with aiohttp.ClientSession() as session:
            timeout = 0 if option['timeout'] == 0 else option['timeout'] / 1000
            async with session.get(option['url'], params=option['args'], timeout=timeout,
                                   headers=option['headers']) as resp:
                return resp.status, await resp.text()

    def _post(self):
        pass

    # 流式输出
    def _sse(self):
        pass

    def s_curl(
            self,
            header: Optional[list] = None,
            method: str = 'GET',
            timeout: Optional[list] = None,
            args: Union[str, list] = None,
            tryTimes: int = 1
    ):
        # 确认url，超时时间
        method = method.lower()
        if method == 'post':
            return self._post()
        else:
            return self._get()
