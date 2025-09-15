import ast
import contextlib
import json
import re
from typing import List, Tuple, Union


def extract_meal_plan(data: str) -> dict:
    # 使用正则表达式匹配提取 JSON 部分
    json_pattern = r'```json\n(.*?)\n```'
    match = re.search(json_pattern, data, re.DOTALL)

    if match:
        json_text = match.group(1)
        # 将字符串中的转义字符处理为有效的 JSON
        json_text = json_text.replace('\\', '')

        # 添加大括号包裹，使其成为一个完整的 JSON 对象
        json_text = '{' + json_text + '}'

        # 将 JSON 字符串解析为字典
        return json.loads(json_text)

    raise ValueError("No valid JSON found in the input data.")


class OutputParser:
    @classmethod
    def parse_blocks(cls, text: str):
        # 首先根据"##"将文本分割成不同的block
        blocks = text.split("##")

        # 创建一个字典，用于存储每个block的标题和内容
        block_dict = {}

        # 遍历所有的block
        for block in blocks:
            # 如果block不为空，则继续处理
            if block.strip() != "":
                # 将block的标题和内容分开，并分别去掉前后的空白字符
                block_title, block_content = block.split("\n", 1)
                # LLM可能出错，在这里做一下修正
                if block_title[-1] == ":":
                    block_title = block_title[:-1]
                block_dict[block_title.strip()] = block_content.strip()

        return block_dict

    @classmethod
    def parse_code(cls, text: str, lang: str = "") -> str:
        pattern = rf"```{lang}.*?\s+(.*?)```"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            code = match.group(1)
        else:
            raise Exception
        return code

    @classmethod
    def parse_str(cls, text: str):
        text = text.split("=")[-1]
        text = text.strip().strip("'").strip('"')
        return text

    @classmethod
    def parse_file_list(cls, text: str) -> list[str]:
        # Regular expression pattern to find the tasks list.
        pattern = r"\s*(.*=.*)?(\[.*\])"

        # Extract tasks list string using regex.
        match = re.search(pattern, text, re.DOTALL)
        if match:
            tasks_list_str = match.group(2)

            # Convert string representation of list to a Python list using ast.literal_eval.
            tasks = ast.literal_eval(tasks_list_str)
        else:
            tasks = text.split("\n")
        return tasks

    @staticmethod
    def parse_python_code(text: str) -> str:
        for pattern in (r"(.*?```python.*?\s+)?(?P<code>.*)(```.*?)", r"(.*?```python.*?\s+)?(?P<code>.*)"):
            match = re.search(pattern, text, re.DOTALL)
            if not match:
                continue
            code = match.group("code")
            if not code:
                continue
            with contextlib.suppress(Exception):
                ast.parse(code)
                return code
        raise ValueError("Invalid python code")

    @classmethod
    def parse_data(cls, data):
        block_dict = cls.parse_blocks(data)
        parsed_data = {}
        for block, content in block_dict.items():
            # 尝试去除code标记
            try:
                content = cls.parse_code(text=content)
            except Exception:
                # 尝试解析list
                try:
                    content = cls.parse_file_list(text=content)
                except Exception:
                    pass
            parsed_data[block] = content
        return parsed_data

    @staticmethod
    def extract_content(text, tag="CONTENT"):
        # Use regular expression to extract content between [CONTENT] and [/CONTENT]
        extracted_content = re.search(rf"\[{tag}\](.*?)\[/{tag}\]", text, re.DOTALL)

        if extracted_content:
            return extracted_content.group(1).strip()
        else:
            raise ValueError(f"Could not find content between [{tag}] and [/{tag}]")

    @classmethod
    def extract_struct(cls, text: str, data_type: Union[type(list), type(dict)]) -> Union[list, dict]:
        # Find the first "{" and the last "}"
        start_index = text.find("{")
        end_index = text.rfind("}")

        if start_index != -1 and end_index != -1:
            # Extract the structure part
            structure_text = text[start_index: end_index + 1]

            # Remove any surrounding whitespace and ensure it's valid JSON
            structure_text = structure_text.strip()

            try:
                # Attempt to convert the text to a Python data type using ast.literal_eval
                result = ast.literal_eval(structure_text)

                # Ensure the result matches the specified data type
                if isinstance(result, (list, dict)):
                    return result

                raise ValueError(f"The extracted structure is not a {data_type}.")
            except (ValueError, SyntaxError) as e:
                raise Exception(f"Error while extracting and parsing the {data_type}: {e}")
        else:
            return [] if data_type is list else {}
