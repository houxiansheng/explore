from logging.handlers import QueueListener, QueueHandler

import multiprocessing


class LogQueue:
    def start_listener(self, global_log_queue):
        # 由于多个tag只有一个queue所以只需要一个listener
        fh = []
        queue = None
        for item in global_log_queue.values():
            fh.append(item["handler"])
            if queue is None:
                queue = item["queue"]
            # 创建 QueueListener
        if queue is not None:
            ql = QueueListener(queue, *fh)
            ql.start()
