import json
from datetime import datetime
import numpy as np

with open('out_bitcoin/blocks.json') as f:
    data = f.read()
    collection = json.loads(data)
    f.close()

total = 0

for i in range(1, len(collection)):
    p = collection[i - 1]
    c = collection[i]
    diff = datetime.utcfromtimestamp(c[1]) - datetime.utcfromtimestamp(p[1])
    minutes = np.round(diff.total_seconds() / 60, 0)

    if minutes > 120:
        total = total + 1
        print(c[0], datetime.utcfromtimestamp(c[1]).date(), minutes)

print(f'total: {total}')