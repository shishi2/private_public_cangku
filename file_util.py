import os
import json
import glob
import pandas as pd

DEFAULT_KEYS = ["question", "human_answers", "chatgpt_answers"]

def ensure_file_exists(file_path):
	"""
	检查文件是否存在，不存在则创建对应目录和空文件，最后返回文件路径

	:param file_path: str, 文件路径
	:return: str, 文件路径
	"""
	dir_name = os.path.dirname(file_path)
	if dir_name and not os.path.exists(dir_name):
		os.makedirs(dir_name, exist_ok=True)
	if not os.path.exists(file_path):
		with open(file_path, 'w', encoding='utf-8'):
			pass
	return file_path


def read_jsonl(file_path, keys=DEFAULT_KEYS):
	"""
	读取jsonl文件 test_data_english

	:param file_path: str, 文件路径
	:param keys: [str], 每一行中的键
	:return: [[str]], 依照keys的顺序
	"""

	values_list = [[] for _ in keys]

	with open(file_path, "r", encoding="utf-8") as f:
		for line in f:
			data = json.loads(line)
			for i, key in enumerate(keys):
				value = data.get(key, "")
				if isinstance(value, list):	# [] -> str
					value = " ".join(str(v) if v is not None else "" for v in value) if value else ""
				elif not isinstance(value, str):	# num/None/dict/other -> ""
					value = ""
				values_list[i].append(value.strip())

	return values_list

def list_file_path(dir, file_type="jsonl"):
	"""
	读取路径下所有的jsonl文件

	:return: list[str], 该目录下所有jsonl文件的路径
	:raises FileNotFoundError: 目录不存在
	:param dir: str, 路径
	"""
	if not os.path.isdir:
		raise FileNotFoundError(f"目录不存在: {dir}")
	# return glob.glob(os.path.join(dir, f"*/*/*.{file_type}"))
	return glob.glob(os.path.join(dir, f"*.{file_type}"))




