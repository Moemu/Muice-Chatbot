import sqlite3
from math import sqrt
from collections import defaultdict
import jieba
import random
import asyncio
import logging
import os
import ssl
import aiohttp
import io
from PIL import Image
import time
import threading

class ImageDatabase:
    def __init__(self, db_name='./image_data/image_data.db'):
        '''
        初始化图片数据库
        Args:
            db_name: str, 数据库名称 (optional, 默认为 './image_data/image_data.db')
        Returns:
            None
        Examples:
            >>> image_db = ImageDatabase()
        '''
        logging.info('Initializing image database')
        self.db_name = db_name
        self.storge_dir = os.path.join(os.path.dirname(db_name), 'storge')
        if not os.path.exists(os.path.dirname(db_name)):
            os.makedirs(os.path.dirname(db_name))
        if not os.path.exists(self.storge_dir):
            os.makedirs(self.storge_dir)
        try:
            self.conn = sqlite3.connect(db_name)
            self.conn.execute('''
            CREATE TABLE IF NOT EXISTS image_data
            (id INTEGER PRIMARY KEY,
            content TEXT,
            url TEXT);
            ''')
        except sqlite3.Error as e:
            raise e
        self.backup_thread = threading.Thread(target=self.backup_database)
        self.backup_thread.daemon = True
        self.exit_flag = threading.Event()
        self.backup_thread.start()
        logging.info('Image database initialized')

    def backup_database(self):
        while not self.exit_flag.is_set():
            time.sleep(300)
            backup_name = f"{self.db_name}.backup_{time.strftime('%Y%m%d_%H%M%S')}"
            try:
                with open(self.db_name, 'rb') as f:
                    with open(backup_name, 'wb') as bf:
                        bf.write(f.read())
                logging.info(f'Database backed up to {backup_name}')
                self.manage_backups()
            except Exception as e:
                logging.error(f'Failed to backup database: {e}')

    def manage_backups(self):
        backup_files = [f for f in os.listdir(os.path.dirname(self.db_name)) if f.startswith(os.path.basename(self.db_name) + '.backup_')]
        if len(backup_files) > 5:
            backup_files.sort(key=lambda x: os.path.getmtime(os.path.join(os.path.dirname(self.db_name), x)))
            while len(backup_files) > 5:
                oldest_backup = backup_files.pop(0)
                os.remove(os.path.join(os.path.dirname(self.db_name), oldest_backup))
                logging.info(f'Removed oldest backup: {oldest_backup}')

    def generate_random_vector(self, dimensions=128):
        v = [random.gauss(0, 1) for _ in range(dimensions)]
        magnitude = sqrt(sum(x**2 for x in v))
        return [x / magnitude for x in v]

    def simhash(self, content):
        dimensions = 128
        simhash_vector = [0] * dimensions
        words = list(jieba.cut(content, cut_all=False))
        feature_vectors = {word: self.generate_random_vector() for word in set(words)}
        
        for word in words:
            vector = feature_vectors[word]
            for i in range(dimensions):
                simhash_vector[i] += vector[i]
                
        final_hash = ['1' if value >= 0 else '0' for value in simhash_vector]
        return ''.join(final_hash)

    def similarity(self, a, b):
        count = sum(a[i] == b[i] for i in range(len(a)))
        return float(count) / len(a)

    async def insert_data(self, content, url):
        '''
        向数据库插入数据
        Args:
            content: str, 图片描述
            url: str, 图片url
        Returns:
            None
        Examples:
            >>> content = '一只小狗在树林里玩耍'
            >>> url = 'https://example.com/dog.jpg'
            >>> asyncio.run(image_db.insert_data(content, url))
        '''
        hash_value = self.simhash(content)
        try:
            url = url.replace('&amp;', '&')
        except:
            pass
        ssl_context = ssl.create_default_context()
        ssl_context.set_ciphers('DEFAULT@SECLEVEL=1')
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=ssl_context) as response:
                image_bytes = await response.read()
                image = Image.open(io.BytesIO(image_bytes))
                image_name = str(time.time()) + '.jpg'
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                image.save(os.path.join(self.storge_dir, image_name))
        url = os.path.join(self.storge_dir, image_name)
        with self.conn:
            self.conn.execute("INSERT INTO image_data VALUES (NULL, ?, ?)", (hash_value, url))

    async def find_similar_content(self, content):
        '''
        查找与给定内容最相似的图片
        Args:
            content: str, 图片描述
        Returns:
            (url, similarity): (str, float), 最相似的图片url和相似度
        Examples:
            >>> content = '一只小狗在树林里玩耍'
            >>> url, similarity = asyncio.run(image_db.find_similar_content(content))
            >>> print(url, similarity)
            ('file:///.../image_data/storge/1637111224.jpg', 0.9)
        '''
        hash_value = self.simhash(content)
        cursor = self.conn.execute("SELECT id, content, url FROM image_data")
        results = cursor.fetchall()
        similar_contents = [
            (result[2], self.similarity(hash_value, result[1]))
            for result in results
        ]
        
        if similar_contents:
            similar_contents = [(r"file:///" + os.path.abspath(url), similarity) for url, similarity in similar_contents]
            return max(similar_contents, key=lambda x: x[1])
        else:
            return None, None

    def close(self):
        '''
        关闭数据库连接
        Returns:
            None
        Examples:
            >>> image_db.close()
        '''
        self.conn.close()
        self.exit_flag.set()
        self.backup_thread.join()
        logging.info('Image database closed')

