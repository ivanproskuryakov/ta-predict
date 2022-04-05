class Estimator:
    def trades_diff_total(self, trades: []):
        total = 0

        for trade in trades:
            total = total + (trade['sell'] - trade['buy'])

        return total
