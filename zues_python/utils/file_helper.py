from langchain.chains.llm import LLMChain
import re


class FileHelper:
    def file_get_content(filename):
        try:
            # 使用with语句打开文件，这样可以确保文件最后会被正确关闭
            with open(
                filename, "r", encoding="utf-8"
            ) as fp:  # 'r' 表示读取模式，'utf-8' 是编码方式
                content = fp.read()  # 读取文件全部内容
            return content
        except FileNotFoundError:
            # 如果文件不存在，则返回空字符串（或者你可以根据需要抛出异常）
            return ""
        except Exception as e:
            # 捕获其他可能的异常（例如权限问题），并返回空字符串或进行其他处理
            # 这里简单返回空字符串，但通常更好的做法是记录错误或抛出异常
            print(f"An error occurred: {e}")
            return ""

    def file_put_contents(filename, content, mode="a+"):
        try:
            with open(filename, mode) as fp:
                n = fp.write(content)
                # 在'a+'模式下，文件指针在文件末尾，不需要额外的操作
                # 但如果需要确保文件内容被写入（尤其是在某些系统或配置下），可以调用fp.flush()
                # 注意：在with语句中，文件会在离开with块时自动关闭，因此不需要显式调用fp.close()
                return n
        except Exception as e:
            print(f"写入文件时发生错误: {e}")
        return None

    def parse_ini_file(filename):
        section_pattern = r"^\s*\[([^\[\]]+)\]\s*$"
        keyvalue_pattern = (
            r'^\s*([\w_\.]+)\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s"\'#]+))\s*(#.*)?$'
        )
        data = {}
        section = "default"

        with open(filename, "r", encoding="utf-8") as fp:
            for line in fp:
                line = line.strip()
                if not line or line.startswith(";") or line.startswith("#"):
                    continue  # 忽略空行和注释行

                m = re.match(section_pattern, line)
                if m:
                    section = m.group(1)
                if section not in data:
                    data[section] = {}
                    continue

                m = re.match(keyvalue_pattern, line)
                if m:
                    key = m.group(1)
                    value = next(
                        (x for x in m.groups()[1:] if x), ""
                    )  # 提取第一个非空值
                    if value.isdigit():  # 尝试将值转换为整数
                        value = int(value)
                    elif value.lower() in ("true", "yes", "on", "1"):
                        value = True
                    elif value.lower() in ("false", "no", "off", "0"):
                        value = False

                data[section][key] = value

        return data
