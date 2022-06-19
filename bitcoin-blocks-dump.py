import os
import json

from datetime import datetime
from blockchain_parser.blockchain import Blockchain
from src.parameters import DB_BITCOIN

db_index = f'{DB_BITCOIN}index'
collection = []
start_at = datetime.now()
blockchain = Blockchain(os.path.expanduser(db_index))

for block in blockchain.get_ordered_blocks(os.path.expanduser(db_index), 0):
    collection.append([
        block.hash,
        block.header.timestamp.timestamp()
    ])
    diff = datetime.now() - start_at
    print(f'{block.hash} {block.header.timestamp}  {len(collection)} {diff.seconds}')

diff = datetime.now() - start_at

print(f' --> {len(collection)} {diff.seconds}')

text = json.dumps(collection)

file = open('dat/bitcoin_blocks.json', 'w')
file.write(text)
file.close()
