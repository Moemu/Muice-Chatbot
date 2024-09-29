import csv
import os
import shutil
from llm.faiss_memory import FAISSMemory
from alive_progress import alive_bar
import time

def load_memories_from_csv(file_path: str, memory_instance: FAISSMemory, total_lines: int):
    """
    从指定路径加载.csv文件，并将每一对(input, output)作为记忆插入到memory_instance中。
    
    :param file_path: .csv文件的路径
    :param memory_instance: FAISSMemory类的实例
    :param total_lines: 文件总行数
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        with alive_bar(total_lines, spinner="classic", stats='({rate}, eta:{eta})') as bar:
            lines_processed = 0
            for line in file:
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    input_part, output_part = parts
                    memory_instance.insert_memory({"input": input_part}, {"output": output_part})
                lines_processed += 1
                if lines_processed % 100 == 0:
                    # 每100行执行一次检查和备份
                    print(f"Processed {lines_processed} lines, testing memory...")
                    memory.save_all_data()
                    try:
                        tmp = memory_instance.search_memory({"input": "xxx"})
                        print("Result:", tmp)
                    except Exception as e:
                        print(f"Error while searching: {e}")
                        print("数据库可能损坏，请检查csv文件并重新导入数据。")
                        raise e
                    print("Memory test passed.")
                bar()  # 更新进度条


memory = FAISSMemory(model_path="./model/distiluse-base-multilingual-cased-v1",db_path="./memory/faiss_index.faiss",top_k=1)

# 导入.csv文件
file_path = input("请输入.csv文件的路径：").strip()

if not os.path.exists(file_path):  # 检查文件是否存在
    print("文件不存在！")
    exit()

if not file_path.endswith('.csv'):  # 检查文件格式
    print("文件格式错误！")
    exit()

# 获取文件总行数
with open(file_path, 'r', encoding='utf-8') as file:
    total_lines = sum(1 for _ in file)

# 加载并显示进度条
load_memories_from_csv(file_path, memory, total_lines)
memory.save_all_data()