import json


class Reader:
    threshold = 0
    items = []

    def append(self, item: float):
        l = len(self.items) - 1
        self.items[l][1].append(item)

    def volume_taken(self, totals: []):
        r = 0

        if totals["volume"]:
            r = (totals["volume_taker"] / totals["volume"]) * 100

        return r

    def is_last_hour(self, last_hour: int, hour):
        h = hour

        if hour == 0:
            h = 24

        diff = abs(last_hour - h)

        return diff == 4

    def read(self, asset: str, interval: str):
        with open(f'out_klines/{asset}_{interval}.json') as f:
            data = f.read()
            collection = json.loads(data)
            f.close()

        total = len(collection)
        first = collection[0]
        is_positive = float(first['avg_percentage']) >= 0
        self.items.append([is_positive, []])

        for i in range(1, total):
            item = collection[i]
            item_previous = collection[i - 1]
            is_positive = float(item['avg_percentage']) >= 0
            is_positive_previous = float(item_previous['avg_percentage']) >= 0

            if is_positive_previous != is_positive:
                self.items.append([is_positive, []])

            self.append(item)

        return self.items
