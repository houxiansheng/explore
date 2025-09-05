import sys

import pymysql

import redis
import datetime, time
import pickle, re, json, logging, numpy

logger = logging.getLogger()
handler = logging.FileHandler('logfile.log')
logger.addHandler(handler)
metric_lasttime = 120


class analysis_debug():
    def run(self):
        print("我是456789")
        ts = int(time.time())
        # print(ts)
        metrics = self.getMetrics()
        # print(metrics)
        online_metrics = self.getOnlineMetrics(metrics)
        # print(online_metrics)
        avg_metrics = self.getAvgMetrics(metrics)
        self.diffMetrics(metrics, avg_metrics, online_metrics)

    def getMetrics(self):
        conn = pymysql.connect(host='10.41.41.33', user='root', passwd='123123', db='falcon', charset='utf8')

        # 获取数据库游标
        cursor = conn.cursor()

        map = ['cache_key', 'collect_interval']
        # 执行 SQL 语句
        cursor.execute('SELECT ' + ','.join(map) + ' FROM dcenter_metric')

        # 获取所有结果
        results = cursor.fetchall()
        # 打印查询结果
        kapi_list = {}
        for row in results:
            kapi_list[row[0]] = {
                map[0]: row[0],
                map[1]: row[1]
            }
        # 关闭游标和连接
        cursor.close()
        conn.close()
        return kapi_list

    def diffMetrics(self, metrics, avg_metrics, online_metrics):
        today_start = int(
            time.mktime(
                time.strptime(time.strftime("%Y-%m-%d 00:00:00", time.localtime(time.time())), "%Y-%m-%d %H:%M:%S")))
        now = int(time.time())
        now_sec = now - today_start
        # print(today_start, now_sec)
        # sys.exit()
        for metric in metrics:
            if metric in avg_metrics and metric in online_metrics:
                # print(metric)
                # print(avg_metrics[metric])
                # print(online_metrics[metric])
                logger.error(metric)
                # 获取满足需要的数据
                logger.error(json.dumps(avg_metrics[metric]))
                logger.error(json.dumps(online_metrics[metric]))
                avg_keys = avg_metrics[metric].keys()
                online_keys = online_metrics[metric].keys()
                avg_nums = []
                online_nums = []
                trend_rate = 0;
                for key in avg_keys:
                    key_int = int(key)
                    if now_sec - metric_lasttime < key_int:
                        avg_nums.append(avg_metrics[metric][key]/100)
                for key in online_keys:
                    key_int = int(key)
                    if now - key_int < metric_lasttime:
                        online_nums.append(online_metrics[metric][key])
                # print("我是实时原来", online_metrics[metric])
                if sum(online_nums) > 0:
                    trend_rate = abs(1 - (numpy.mean(avg_nums) / numpy.mean(online_nums)))
                if trend_rate >= 0.2:
                    print(metric)
                    print("我是均值", avg_nums)
                    print("我是均值原来", avg_metrics[metric])
                    print("我是实时", online_nums)
                    print("我是实时原来", online_metrics[metric])
                    print("比率关系", trend_rate,numpy.mean(avg_nums),numpy.mean(online_nums))

    def getOnlineMetrics(self, cache_keys):
        rredis = redis.Redis(host='rs52004.hebe.grid.sina.com.cn', port=52004, db=0, decode_responses=True)
        rredis_pipe = rredis.pipeline()
        count = 0
        all_res = []
        for cache_key in cache_keys:
            # print('makerbot.data.' + cache_key)
            rredis_pipe.get('makerbot.data.' + cache_key);
            if count > 1:
                res = rredis_pipe.execute()
                all_res = all_res + res
                count = 0
            count = count + 1
        if count > 0:
            res = rredis_pipe.execute()
            all_res = all_res + res
        end_res = {}
        sub_index = 0
        for cache_key in cache_keys:
            tmp_res = all_res[sub_index]
            sub_index = sub_index + 1
            if cache_key.find('nodes') > 0 or cache_key.find('5xx') > 0 or cache_key.find('4xx') > 0 or cache_key.find(
                    'mapi') > 0 or cache_key.find('history') > 0 or cache_key.find('.capacity') > 0 or cache_key.find(
                'uery.zongsou.empty') > 0:
                continue
            if tmp_res != None:
                tmp_res_json = json.loads(tmp_res)
                if 'aggregate' in tmp_res_json['list']:
                    end_res[cache_key] = {}
                    for tmp_metric in tmp_res_json['list']['aggregate']:
                        end_res[cache_key][tmp_metric['timestamp']] = tmp_metric['value']
        return end_res

    def getAvgMetrics(self, cache_keys):
        rredis = redis.Redis(host='10.2.39.130', port=6379, db=15, decode_responses=True)
        rredis_pipe = rredis.pipeline()
        count = 0
        all_res = []
        now_ts = int(time.time())
        end = int((now_ts + 8 * 3600) % 86400)
        start = end - metric_lasttime
        for cache_key in cache_keys:
            print('analysis_makerbot.data.' + cache_key, start, end)
            rredis_pipe.zrangebyscore('analysis_makerbot.data.' + cache_key, start, end, withscores=True);
            if count > 30:
                res = rredis_pipe.execute()
                all_res = all_res + res
                count = 0
            count = count + 1
        if count > 0:
            res = rredis_pipe.execute()
            all_res = all_res + res
        end_res = {}
        sub_index = 0
        for cache_key in cache_keys:
            sub_index = sub_index + 1
            if cache_key.find('nodes') > 0 or cache_key.find('5xx') > 0 or cache_key.find('4xx') > 0 or cache_key.find(
                    'mapi') > 0 or cache_key.find('history') > 0:
                continue
            if sub_index < len(all_res):
                tmp_res = all_res[sub_index]
                if tmp_res != None and len(tmp_res) > 0:
                    tmp_dict = {}
                    for tmp_metric in tmp_res:
                        m_val = re.split('_', tmp_metric[0])
                        tmp_dict[int(m_val[0])] = int(m_val[1])
                    end_res[cache_key] = tmp_dict
        return end_res
