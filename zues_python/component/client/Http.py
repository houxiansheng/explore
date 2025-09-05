import asyncio
import sys
import traceback
from typing import (
    Callable,
    Optional,
    Union, AsyncGenerator,
)

import aiohttp


class Http:
    _session = None

    @classmethod
    async def get_session(cls):
        if cls._session is None or cls._session.closed:
            cls._session = aiohttp.ClientSession()
        return cls._session

    def _get(self, session, option):
        timeout = (
            option["timeout"] / 1000
            if isinstance(option["timeout"], Union[int, float])
            else 0
        )
        return session.get(
            option["url"],
            params=option["args"],
            timeout=timeout,
            headers=option["headers"],
        )

    def _post(self, session, option):
        timeout = 0 if option["timeout"] == 0 else option["timeout"] / 1000
        if option.get("is_body",False):
            return session.post(
                option["url"],
                json=option["args"],  # 这里改成 json=
                timeout=timeout,
                headers=option["headers"],
            )
        else:
            return session.post(
                option["url"],
                data=option["args"],
                timeout=timeout,
                headers=option["headers"],
            )

    # 流式输出
    def _sse(self):
        pass

    def defineOptions(
            self,
            url: str = None,
            headers: Optional[list] = None,
            method: str = "GET",
            timeout: Optional[list] = None,
            args: Union[str, list] = None,
            tryTimes: int = 1,
            callbackFun: Callable = None,
    ):
        return {
            "url": url,
            "headers": headers,
            "method": method,
            "timeout": timeout,
            "args": args,
            "tryTimes": tryTimes,
            "callbackFun": callbackFun,
        }

    async def s_curl(self, Optional: dict = None) -> tuple[int, dict, str]:
        # 确认url，超时时间
        method = Optional["method"].lower()
        Optional["headers"] = Optional["headers"] if "headers" in Optional else {}
        content = None
        headers = None
        status = 0
        session = await self.get_session()

        while Optional["tryTimes"] > 0:
            try:
                Optional["tryTimes"] -= 1
                request_func = self._post if method == "post" else self._get
                async with request_func(session, Optional) as resp:
                    status = resp.status
                    p_headers = resp.headers
                    headers = dict(p_headers.items())
                    content_type = p_headers.get("content-type", "").lower()
                    if "text/event-stream" not in content_type:
                        content = await resp.text(errors="ignore")
                        return status, headers, content
                    else:
                        if status == 200:
                            encoding = resp.charset or "utf-8"
                            async for chunk in resp.content.iter_chunked(1024):
                                decoded_chunk = chunk.decode(encoding, errors="ignore")
                                if "callbackFun" in Optional and callable(Optional["callbackFun"]):
                                    Optional["callbackFun"](status, headers, decoded_chunk)
                                return status, headers, decoded_chunk
                        else:
                            return status, headers, f"Error with status {status}"
            except (asyncio.TimeoutError, aiohttp.ClientError) as e:
                await asyncio.sleep(0.05)  # 简单的退避策略
                content = f"s_curl 请求失败,url:{Optional.get('url')},timeout:{Optional.get('timeout')}"
            except ValueError as e:
                traceback.print_exc()
                break
        return status, headers, content
