import pymysql
import time
import redis


class analysis_insert():
    def run(self):
        # 连接 MySQL 数据库
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

        today_start = int(
            time.mktime(
                time.strptime(time.strftime("%Y-%m-%d 00:00:00", time.localtime(time.time())), "%Y-%m-%d %H:%M:%S")))
        # 连接 MySQL 数据库
        conn1 = pymysql.connect(host='wbsearch3.doris.data.sina.com.cn', port=9036, user='wbsearch_r',
                                passwd='s38eydhrhD',
                                db='wbsearch', charset='utf8')
        doris_map = ['ts', 'ip', 'value']
        # log_cursor = open("/tmp/fhxb.log", 'w')
        for kpi_key in kapi_list.keys():
            if kpi_key.find('nodes') > 0 or kpi_key.find('5xx') > 0 or kpi_key.find('4xx') > 0 or kpi_key.find(
                    'mapi') > 0 or kpi_key.find('history') > 0:
                continue
            data_kpi_key = 'makerbot.data.' + kpi_key
            data_collect_interval = kapi_list[kpi_key]['collect_interval']
            sum_list = {}
            for day in range(2, 10):
                pre_time = today_start - day * 86400
                for ts in range(142):
                    sql_start = pre_time + (ts - 1) * 600
                    sql_end = pre_time + (ts) * 600
                    sql = 'select ' + ','.join(
                        doris_map) + ' from ods_wb_search_makerbot_kpi where kpi_cachekey="' + data_kpi_key + '" and ts>=' + (
                                  '%d' % sql_start) + ' and ts<' + ('%d' % sql_end);
                    # print(sql)
                    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sql_end)))
                    cursor1 = conn1.cursor()
                    cursor1.execute(sql)
                    # 获取所有结果
                    results1 = cursor1.fetchall()
                    for result in results1:
                        metric_ts = int((result[0] + 8 * 3600) % 86400)
                        metric_ts = metric_ts - (metric_ts % data_collect_interval)
                        metric_ts_str = "%d" % metric_ts
                        metric_val = int(float(result[2]) * 100)
                        if metric_val <= 0:
                            continue;
                        if metric_ts_str not in sum_list:
                            sum_list[metric_ts_str] = {
                                'num': 0,
                                'val': 0
                            }
                            # log_cursor.write(("%d" % day) + '--' + metric_ts_str + "\n")
                        sum_list[metric_ts_str]['num'] += 1
                        sum_list[metric_ts_str]['val'] += metric_val
            for metric_key in sum_list.keys():
                avg = int(sum_list[metric_key]['val'] / sum_list[metric_key]['num'])
                sum_list[metric_key]['avg'] = avg
            self.analysis_insert(data_kpi_key, sum_list)

    def analysis_insert(self, cache_key, avg_list):
        now_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        # 连接 MySQL 数据库
        conn = pymysql.connect(host='10.41.41.33', user='root', passwd='123123', db='falcon', charset='utf8')
        rredis = redis.Redis(host='10.41.41.33', port=6379, db=15, decode_responses=True)
        # 获取数据库游标
        cursor = conn.cursor()
        # 执行 SQL 语句
        cursor.execute('SELECT id,ts,avg FROM dcenter_metric_analisys where cache_key="' + cache_key + '"')
        results = cursor.fetchall()
        exist_map = {}
        for result in results:
            ts_tmp = "%d" % result[1]
            exist_map[ts_tmp] = result
        rredis.delete("analysis_" + cache_key)
        for metric_key in avg_list.keys():
            rredis_pipe = rredis.pipeline()
            if metric_key not in exist_map:
                sql = 'INSERT INTO dcenter_metric_analisys (cache_key, ts, avg,ip,created_at,updated_at) VALUES ("' + cache_key + '",' + metric_key + ',' + (
                        "%d" % avg_list[metric_key]['avg']) + ',"' + now_date + '","' + now_date + '")'
            else:
                sql = 'update dcenter_metric_analisys set avg=' + (
                        "%d" % avg_list[metric_key]['avg']) + ',updated_at="' + now_date + '" where id=' + (
                              "%d" % exist_map[metric_key][0])

            # rredis_pipe.zadd("analysis_" + cache_key, {metric_key: ("%d" % avg_list[metric_key]['avg'])});
            # rredis_pipe.ZREMRANGEBYSCORE("analysis_" + cache_key, int(metric_key), int(metric_key))
            rredis_pipe.zadd("analysis_" + cache_key,
                             {str(metric_key) + '_' + str(avg_list[metric_key]['avg']): int(metric_key)});
            rredis_pipe.execute()
            cursor.execute(sql)
            conn.commit()

        cursor.close()
        conn.close()
