import json
import os

BASE = './db'

class Collection:
    def __init__(self,path) -> None:
        self.docs = []
        self.count = 0
        self.path=f'{BASE}/path'
        if not os.path.exists(self.path):
            os.mkdir(self.path)
    def insert(self, doc):
        with open(self.path+f'/{self.count}.json','w') as f:
            f.write(json.dumps(doc,indent=4))
    def get():
        pass
        