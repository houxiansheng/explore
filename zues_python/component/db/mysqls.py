#!/usr/bin/env python
# -*- coding:utf-8 -*-
from databases import Database


class MysqlPool:
    __conns = {}
    _config = {}

    def setConfig(self, config: dict):
        self._config = config

    def getConnect(self, busKey: str):
        if busKey in self.__conns:
            return self.__conns[busKey]
        cfg = self._config.get(busKey)
        if not cfg:
            raise ValueError(f"数据库配置未找到，key={busKey}")

        url = (
            f"mysql+asyncmy://{cfg['user']}:{cfg['password']}@"
            f"{cfg['host']}:{cfg['port']}/{cfg['db']}?charset={cfg.get('charset', 'utf8mb4')}"
        )
        db = Database(url)
        self.__conns[busKey] = db
        return db


async def query_version():
    db = mysql_pool.getConnect("database_growth_s")
    await db.connect()
    version_row = await db.fetch_one("SELECT VERSION();")
    await db.disconnect()
    print("MySQL版本:", dict(version_row))
    print("数据库版本号:", version_row["VERSION()"])


if __name__ == "__main__":
    import asyncio

    # 初始化全局连接池管理实例
    mysql_pool = MysqlPool()
    mysql_pool.setConfig({
        "database_growth_s": {
            'host': 's4458i.eos.grid.sina.com.cn',
            'port': 4458,
            'user': 'growth_r',
            'password': 'BTk8OzgdMPnjw75a',
            'db': 'growth_s_weibo_com',
            "charset": "utf8mb4"
        }
    })
    asyncio.run(query_version())
