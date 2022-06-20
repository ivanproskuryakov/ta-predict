import os
import json

from datetime import datetime
from blockchain_parser.blockchain import Blockchain

DB_BITCOIN = '/home/ivan/.bitcoin/blocks'
DB_BITCOIN_INDEX = '/home/ivan/.bitcoin/blocks/index'

collection = []
start_at = datetime.now()
blockchain = Blockchain(DB_BITCOIN)

for block in blockchain.get_ordered_blocks(os.path.expanduser(DB_BITCOIN_INDEX), 0):
    # print(block)
    # print(block.header)
    # exit()
    collection.append([
        block.hash,
        block.header.timestamp.timestamp()
    ])
    diff = datetime.now() - start_at
    print(f'{block.hash} {block.header.timestamp}  {len(collection)} {diff.seconds}')

diff = datetime.now() - start_at

print(f' --> {len(collection)} {diff.seconds}')

text = json.dumps(collection)

file = open('data/bitcoin_blocks.json', 'w')
file.write(text)
file.close()
