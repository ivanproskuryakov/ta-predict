import json


class Reader:
    threshold = 0
    items = []

    def append(self, item: float):
        l = len(self.items) - 1
        self.items[l][1].append(item)

    def read(self, asset: str, interval: str):
        with open(f'out_klines/{asset}_{interval}.json') as f:
            data = f.read()
            collection = json.loads(data)
            f.close()

        total = len(collection)

        item_first = collection[0]
        is_positive = float(item_first['avg_percentage']) >= 0
        self.items.append([is_positive, []])

        # ---------

        for i in range(1, total):
            item = collection[i]
            item_previous = collection[i - 1]
            is_positive = float(item['avg_percentage']) >= 0
            is_positive_previous = float(item_previous['avg_percentage']) >= 0

            if is_positive_previous != is_positive:
                self.items.append([is_positive, []])

            self.append(item)

        return self.items
