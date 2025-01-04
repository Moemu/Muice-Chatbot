import os
import re
import faiss
import pickle
import logging
import time
from sentence_transformers import SentenceTransformer
from typing import Dict, Any
from langchain.memory import VectorStoreRetrieverMemory
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS


def save_index(index, path):
    faiss.write_index(index, path)

def load_index(path, embedding_size):
    return faiss.read_index(path)

class FAISSMemory():
    model_path: str = "./model/distiluse-base-multilingual-cased-v1"
    db_path: str = "./memory/faiss_index.faiss"
    top_k: int = 1

    def __init__(self, model_path: str = "./model/distiluse-base-multilingual-cased-v1", db_path: str = "./memory/faiss_index.faiss", top_k: int = 1):
        self.model_path = model_path
        self.db_path = db_path
        self.top_k = top_k
        logging.info(f"Loading FAISS memory with model {self.model_path} and database {self.db_path}")
        self.model = SentenceTransformer(self.model_path)
        embedding_size = self.model.get_sentence_embedding_dimension()
        logging.info(f"Embedding size: {embedding_size}")
        if not os.path.exists(os.path.dirname(db_path)):
            os.makedirs(os.path.dirname(db_path))
        if not os.path.exists(self.db_path):
            index = faiss.IndexFlatL2(embedding_size)
            save_index(index, self.db_path)
        self.index = load_index(self.db_path, embedding_size)
        self.docstore = self.load_docstore()
        self.index_to_docstore_id = self.load_index_to_docstore_id()

        assert isinstance(self.docstore, InMemoryDocstore), "Docstore must be an instance of InMemoryDocstore"
        assert isinstance(self.index_to_docstore_id, dict), "Index to docstore ID mapping must be a dictionary"

        vectorstore = FAISS(self.embedding_function, self.index, self.docstore, self.index_to_docstore_id)
        retriever = vectorstore.as_retriever(search_kwargs=dict(k=self.top_k))
        self.memory = VectorStoreRetrieverMemory(retriever=retriever)

        logging.info(f"FAISS memory loaded with {self.index.ntotal} vectors")

    def embedding_function(self, texts):
        if texts is None:
            raise ValueError("Input texts cannot be None")
        return self.model.encode(texts)

    def load_docstore(self):
        docstore_path = self.db_path + ".docstore"
        if os.path.exists(docstore_path):
            with open(docstore_path, 'rb') as f:
                docstore = pickle.load(f)
                assert isinstance(docstore, dict), "Docstore must be a dictionary"
            return InMemoryDocstore(docstore)
        else:
            return InMemoryDocstore({})
        
    def save_docstore(self):
        docstore_path = self.db_path + ".docstore"
        with open(docstore_path, 'wb') as f:
            assert isinstance(self.docstore._dict, dict), "Docstore must be a dictionary"
            pickle.dump(self.docstore._dict, f)
    
    def load_index_to_docstore_id(self):
        index_mapping_path = self.db_path + ".mapping"
        if os.path.exists(index_mapping_path):
            with open(index_mapping_path, 'rb') as f:
                index_to_docstore_id = pickle.load(f)
            return index_to_docstore_id
        else:
            return {}
    
    def save_index_to_docstore_id(self):
        index_mapping_path = self.db_path + ".mapping"
        with open(index_mapping_path, 'wb') as f:
            assert isinstance(self.index_to_docstore_id, dict), "Index to docstore ID mapping must be a dictionary"
            pickle.dump(self.index_to_docstore_id, f)

    def search_memory(self, inputs: Dict[str, Any]) -> Any:
        start_time = time.time()
        message = inputs.get('input')
        memory_results = self.memory.load_memory_variables({"prompt": message})
        end_time = time.time()
        logging.info(f"Memory search used: {end_time - start_time} seconds")

        if not memory_results:
            return {"input": ["", ""], "output": ["", ""]}
        
        history = memory_results.get("history", "")

        if not history:
            return {"input": ["", ""], "output": ["", ""]}

        # 使用正则表达式来匹配所有的input和output对
        # 处理最后一项可能没有 \n 的情况
        pattern = r'input: (.*?)\noutput: (.*?)(?:\n|$)'
        matches = re.findall(pattern, history)

        if not matches:
            return {"input": ["", ""], "output": ["", ""]}

        # 取最后两条记录
        last_two_inputs = []
        last_two_outputs = []

        # 从后往前遍历，取最后两条记录
        for i in range(-1, -3, -1):
            try:
                last_two_inputs.insert(0, matches[i][0].strip())
                last_two_outputs.insert(0, matches[i][1].strip())
            except IndexError:
                break

        # 如果不足两条，则用空字符串填充
        while len(last_two_inputs) < 2:
            last_two_inputs.insert(0, "")
        while len(last_two_outputs) < 2:
            last_two_outputs.insert(0, "")

        return {
            "input": last_two_inputs,
            "output": last_two_outputs
        }
    
    def insert_memory(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        input_message = inputs.get('input')
        output_message = outputs.get('output')
        logging.info(f"Inserting memory: {input_message} -> {output_message}")
        self.memory.save_context({"input": input_message}, {"output": output_message})

        # 保存索引和文档数据
        self.save_all_data()
    
    def save_all_data(self):
        self.save_docstore()
        self.save_index_to_docstore_id()
        save_index(self.index, self.db_path)