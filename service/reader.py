from yachalk import chalk
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

        # overall = ''
        negative = []
        positive = []
        total = len(collection)

        for i in range(1, total):
            time = collection[i]['time_open']
            item = collection[i]
            item_previous = collection[i - 1]

            percentage = float(item['avg_percentage'])
            percentage_previous = float(item_previous['avg_percentage'])
            # volume = float(item['volume'])
            # volume_taker = int(item['volume_taker'])
            # volume_maker = int(item['volume_maker'])
            # trades = int(item['trades'])
            change = f'{percentage:.1f}'

            if percentage > self.threshold:
                if percentage_previous < 0:
                    positive.append([])
                change = chalk.green(f'{percentage:.1f}')
                self.append(positive, item)

            if percentage < self.threshold:
                if percentage_previous > 0:
                    negative.append([])
                change = chalk.red(f'{percentage:.1f}')
                self.append(negative, item)

            # overall += f'{change} '

        return [
            negative,
            positive
        ]
