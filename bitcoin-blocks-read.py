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
    print(block)
    print(block.header)
    print(len(block.transactions))
    exit()