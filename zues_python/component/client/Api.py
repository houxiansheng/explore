from typing import (
    Callable,
    Optional,
    Union,
)

from .Http import Http
from ..auth import Auth
from ..config import Config
from ..decorator import record_costtime
from ..singleton import Singleton


class Api(Singleton):
    __map = {"http": Http, "https": Http}

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
            # 'method': method,
            "timeout": timeout,
            "args": args,
            "tryTimes": tryTimes,
            "callbackFun": callbackFun,
        }

    @record_costtime
    async def s_curl(self, Optional: dict = None) -> str:
        urlKey = Optional["urlKey"] or ""
        config = self._config[urlKey].copy() if urlKey in self._config else {}
        client = self.__parseProtocol(config["url"] or "")
        if client == None:
            return None
        client = client()
        # 签名信息
        if "auth" in config and config["auth"] == True:
            if config.get("tauth"):
                authConf = config.get("tauth")
            else:
                authConf = Config().get("tauth")
            tuid = authConf.get("uid", None)
            tauth_file = authConf.get("tauth_file", None)
            if tuid is None or tauth_file is None:
                raise Exception("tauth config error")
            source, sign = Auth.sign(
                tauth_file,
                tuid,
            )
            if sign != None:
                Optional.setdefault("headers", {})["Authorization"] = sign
                Optional["source"] = source
                del config["auth"]
        del Optional["urlKey"]
        config = config | Optional
        ret = await client.s_curl(config)
        return ret

    def __parseProtocol(self, url):
        if url == "":
            return None
        urls = url.split("://")
        protocol = urls[0] or ""
        if protocol in self.__map:
            return self.__map[protocol]
        return None
