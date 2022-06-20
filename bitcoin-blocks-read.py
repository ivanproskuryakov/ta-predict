import os

from datetime import datetime
from blockchain_parser.blockchain import Blockchain, Block, get_block

DB_BITCOIN = '/home/ivan/.bitcoin/blocks'
DB_BITCOIN_INDEX = '/home/ivan/.bitcoin/blocks/index'

collection = []
start_at = datetime.now()
blockchain = Blockchain(DB_BITCOIN)

blocks = blockchain.get_ordered_blocks(
    os.path.expanduser(DB_BITCOIN_INDEX)
)

block = Block(get_block('/home/ivan/.bitcoin/blocks/blk00001.dat', 31300506), 124392)

for transaction in block.transactions:
    for t_inputs in transaction.inputs:
        print(t_inputs)
    for t_outputs in transaction.outputs:
        print(input)
