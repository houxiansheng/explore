import asyncio
# from component.client.Http import Http as http_test
from component.db.redis import Redis as redis1
from component.db.mcq import Mcq as mcq1
import sys
import os
import traceback
from datetime import datetime
import random
from component.manager import Manager


async def callbacl(status, headers, msg):
    print(msg)
    count = 1000
    rerrrrr = redis1()
    now1 = datetime.datetime()
    milliseconds1 = int(now1.timestamp() * 1000)
    while count > 0:
        count -= 1
        aa = await rerrrrr.exec('c')
    now2 = datetime.datetime()
    milliseconds2 = int(now2.timestamp() * 1000)
    print(milliseconds2 - milliseconds1)


async def www():
    count = 1000
    rerrrrr = redis1()
    now1 = datetime.now()
    milliseconds1 = int(now1.timestamp() * 1000)
    while count > 0:
        count -= 1
        # aa=await redis1().getInstance(1234).exec('get','hxb12345')
        if count % 100 == 0:
            print(count)
        try:
            mmm = mcq1.getInstance(1233)
            await mmm.set('hxbhxbttttt', '1234')
            # await mmm.set('hxbhxbttttt','12345')
            # await mmm.set('hxbhxbttttt','12346')
            # await mmm.set('hxbhxbttttt','12347')
            # rs = await mmm.set('hxbhxbttttt','12348')
            rs = await mmm.get('hxbhxbttttt')
            # rr = redis1().getInstance(1234)
            # pipe = rr.multi(False);
            # pipe.exec('set','hxb12345',1)
            # pipe.exec('set','hxb12345',2)
            # pipe.exec('get','hxb12345')
            # rs = await pipe.commit()
            # print(rs)
        except ValueError as e:
            print(f"捕获到1111异常: {e}")
            print(e)
            print(e)
            print(e)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            for filename, line_number, function_name, text in traceback.extract_tb(exc_traceback):
                print(f'异常发生在文件{filename}，行号{line_number}')
    # print(aa)
    # print(aa)
    # print(aa)
    # print(aa)
    now2 = datetime.now()
    milliseconds2 = int(now2.timestamp() * 1000)
    print(f'耗时情况:{milliseconds2 - milliseconds1}')


async def tt():
    try:
        # await www()
        # await www()
        # await www()
        tasks = []
        tasks.append(www())
        tasks.append(www())
        tasks.append(www())
        tasks.append(www())
        tasks.append(www())
        tasks.append(www())
        tasks.append(www())
        tasks.append(www())
        tasks.append(www())
        tasks.append(www())
        tasks.append(www())
        tasks.append(www())
        tasks.append(www())
        # task_set = asyncio.gather(asyncio.create_task(www()))  # 将每个任务都放入任务列表
        # task_set = asyncio.gather(asyncio.create_task(www()))  # 将每个任务都放入任务列表
        # task_set = asyncio.gather(asyncio.create_task(www()))  # 将每个任务都放入任务列表
        # task_set = asyncio.gather(asyncio.create_task(www()))  # 将每个任务都放入任务列表
        # task_set = asyncio.gather(asyncio.create_task(www()))  # 将每个任务都放入任务列表
        # task_set = asyncio.gather(asyncio.create_task(www()))  # 将每个任务都放入任务列表
        # task_set = asyncio.gather(asyncio.create_task(www()))  # 将每个任务都放入任务列表
        # task_set = asyncio.gather(asyncio.create_task(www()))  # 将每个任务都放入任务列表
        # task_set = asyncio.gather(asyncio.create_task(www()))  # 将每个任务都放入任务列表
        # task_set = asyncio.gather(asyncio.create_task(www()))  # 将每个任务都放入任务列表
        # task_set = asyncio.gather(asyncio.create_task(www()))  # 将每个任务都放入任务列表
        # task_set = asyncio.gather(asyncio.create_task(www()))  # 将每个任务都放入任务列表
        # task_set = asyncio.gather(asyncio.create_task(www()))  # 将每个任务都放入任务列表
        # task_set = asyncio.gather(asyncio.create_task(www()))  # 将每个任务都放入任务列表
        task_set = asyncio.gather(*tasks)  # 将每个任务都放入任务列表
        await task_set
        # 获取当前时间的毫秒数
        print('开始休息')
        await  asyncio.sleep(20)
    # print(123424)
    # http_test11 = http_test()
    # print(123424)
    # sss = await http_test11.s_curl(http_test11.defineOptions(
    # 	# url = 'http://admin.ai.s.weibo.com/api/llm/analysis_demo_result.json?query=%E4%B8%AD%E5%8C%BB%E5%85%BB%E7%94%9F',
    # 	# url = 'http://admin.ai.s.weibo.com/api/llm/analysis_demo_result.json?query=%E4%B8%AD%E5%8C%BB%E5%85%BB%E7%94%9F&content_type=loop',
    # 	url = 'http://admin.ai.s.weibo.com/api/llm/analysis_demo_result.json?query=%E4%B8%AD%E5%8C%BB%E5%85%BB%E7%94%9F',
    # 	args = [],
    # 	timeout = 0,
    # 	callbackFun = callbacl
    # )
    # )
    # for a in sss:
    # 	print(a)

    except ValueError as e:
        print(f"捕获到1111异常: {e}")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        for filename, line_number, function_name, text in traceback.extract_tb(exc_traceback):
            print(f'异常发生在文件{filename}，行号{line_number}')


async def cccc():
    Manager().setConfPath('/data1/apache2/htdocs/hxb-mproxy/zues_conf')
    # res = await (Manager().getInstance(instance='redis').getConnect(busKey='llm', hashKey="1234").exec('get','hxb'))
    res = await Manager().getInstance(instance='redis').getConnect(busKey='llm', hashNo=2).exec('get', 'hxb')
    res = await Manager().getInstance(instance='mcq').getConnect(busKey='llm').get('hxbhxbttttt')
    print(res.decode())
    print(res.decode())
    print(res.decode())
    print(res.decode())


if __name__ == "__main__":
    asyncio.run(cccc())
