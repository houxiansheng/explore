# from ..libs import aioredis
import hashlib
from typing import Union, Optional

import redis.asyncio as aioredis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry

from ..decorator import check_args
from ..decorator import record_costtime
from ..hash import Hash
from ..singleton import Singleton


# 管道实例
class Pipe:
    def __init__(self, connectionPool, transaction=True):
        self.__cmds = []  # 修复点：改为实例变量
        self.__transaction = transaction
        self.__conn = connectionPool

    def exec(self, cmd, *args):
        self.__cmds.append([cmd, *args])

    async def commit(self):
        async with self.__conn.client() as conn:
            async with conn.pipeline(transaction=self.__transaction) as pipe_obj:
                for v in self.__cmds:
                    if hasattr(pipe_obj, v[0]):
                        method = getattr(pipe_obj, v[0])
                        method(*v[1:])
                    else:
                        raise AttributeError(f"对象 {conn} 没有可调用属性 {v[0]}")
                result = await pipe_obj.execute()
                # 每次commit后重置cmds
                self.__cmds = []
                return result
        return None


class redis_cli:

    def __init__(
            self,
            url: str = None,
            db: Union[str, int, float] = 0,
            socket_timeout: Optional[float] = None,
            socket_connect_timeout: Optional[float] = None,
    ):
        self.__pipe = None
        self.url = url
        self.__conn = aioredis.from_url(
            url,
            db=db,
            socket_timeout=socket_timeout,
            retry=Retry(ExponentialBackoff(cap=10, base=1), 3),  # 最多重试3次
            health_check_interval=30,  # 每隔 30 秒自动 PING 保活
        )

    @record_costtime
    async def exec(self, cmd: str = None, *args):
        async with self.__conn.client() as conn:
            if hasattr(conn, cmd):
                return await getattr(conn, cmd)(*args)
            else:
                raise AttributeError(f"对象{conn}没有可调用属性{cmd}")

    def multi(self, transaction=False):
        return Pipe(self.__conn, transaction)


class Redis(Singleton):
    __pool_ = {}
    _config = {}

    def __init__(self, options: dict = {}):
        pass

    # 检验配置信息是否存在
    def _init_config(
            self,
            busKey: str = None,
            hashKey: str = None,
            hashNo: int = 0,
            db: Union[str, int, float] = 0,
    ):
        config = {}
        if busKey in self._config:
            config = self._config[busKey]
        if not config:
            raise AttributeError(f"redis对象实例化key，暂未发现配置信息")
        if hashKey is None:
            if hashNo < 0 or hashNo >= len(config):
                raise AttributeError(
                    f"redis对象实例化hashNo：{hashNo}，暂未发现配置信息"
                )
        else:
            hashNo = Hash.crc32(hashKey, len(config))
        m = hashlib.md5()
        m.update((busKey + str(hashNo) + str(db)).encode())
        return m.hexdigest(), hashNo, config[hashNo]

    # 初始化参数
    def setConfig(self, config: dict = {}):
        self._config = config

    # 获取实例
    @check_args
    def getConnect(
            self,
            busKey: str = None,
            hashKey: str = None,
            hashNo: int = 0,
            db: Union[str, int, float] = 0,
            socket_timeout: Optional[float] = None,
            socket_connect_timeout: Optional[float] = None,
    ) -> redis_cli:
        uuid, hashNo, config = self._init_config(busKey, hashKey, hashNo)
        if uuid in self.__pool_:
            return self.__pool_[uuid]
        self.__pool_[uuid] = redis_cli(
            url="redis://" + config["host"] + ":" + str(config["port"]),
            db=db,
            socket_timeout=socket_timeout,
        )
        return self.__pool_[uuid]
