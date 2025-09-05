from ctypes import cdll
import os, time, base64, hmac, hashlib, json
from urllib.parse import quote

wb_header = None
wb_header_time = 0


class Auth:
    @staticmethod
    def sign(fileName, uid):
        # 超过5s 并且 wb_header不为空则重新获取
        global wb_header, wb_header_time
        if time.time() - wb_header_time < 5 and not wb_header is None:
            return uid, wb_header
        # 判断fileName是否存在
        if not os.path.exists(fileName):
            return None
        # 读取fileName内容，jsondecode，获取到密钥，计算签名
        token = ""
        with open(fileName, "r") as f:
            token = f.read(2048)
        token = json.loads(token)
        # 如果conent是dict结构，则获取key
        if (
            isinstance(token, dict)
            and "tauth_token" in token
            and "tauth_token_secret" in token
        ):
            if uid:
                param = f"uid={uid}"
                sign = base64.b64encode(
                    hmac.new(
                        token["tauth_token_secret"].encode(),
                        param.encode(),
                        hashlib.sha1,
                    ).digest()
                ).decode()
                wb_header = f'TAuth2 token="{quote(token["tauth_token"])}",param="{quote(param)}",sign="{quote(sign)}"'
            else:
                wb_header = f'TAuth2 token="{token["tauth_token"]}"'
            wb_header_time = time.time()
        else:
            wb_header = None
        return uid, wb_header
