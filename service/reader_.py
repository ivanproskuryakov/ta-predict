import json

class Reader:
    threshold = 0.1

    def append(self, collection: [], item: float):
        if len(collection) == 0:
            collection.append([])

        l = len(collection) - 1
        collection[l].append(item)

    def read(self, asset: str, interval: str):
        with open(f'out_klines/{asset}_{interval}.json') as f:
            data = f.read()
            collection = json.loads(data)
            f.close()

        negative = []
        positive = []
        total = len(collection)

        for i in range(1, total):
            item = collection[i]
            item_previous = collection[i - 1]
            percentage = float(item['avg_percentage'])
            percentage_previous = float(item_previous['avg_percentage'])

            if percentage > 0:
                if percentage_previous < 0:
                    positive.append([])
                self.append(positive, item)

            if percentage < 0:
                if percentage_previous > 0:
                    negative.append([])
                self.append(negative, item)


        return [
            negative,
            positive
        ]
