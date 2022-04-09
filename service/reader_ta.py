import json


class ReaderTA:
    def read(self, asset: str, interval: str):
        with open(f'out_klines/{asset}_{interval}.json') as f:
            data = f.read()
            collection = json.loads(data)
            f.close()

        items = []
        total = len(collection)

        for i in range(0, total):
            item = collection[i]
            items.append(item)

        return items
