from trading_api_wrappers import SURBTC

class ExchangeClient(object):
    def __init__(self):
        pass

    @staticmethod
    def get_quote(orderbook, quote_max_accumulated):
        results = []
        for operation_type in ('bids', 'asks'):
            quoted_accumulated = 0
            base_accumulated = 0
            for entry in orderbook[operation_type]:
                quote_expent = entry[0] * entry[1]
                if quote_max_accumulated > quoted_accumulated + quote_expent:
                    quoted_accumulated += quote_expent
                    base_accumulated += entry[0]
                else:
                    remaining_quote = quote_max_accumulated - quoted_accumulated
                    quoted_accumulated += remaining_quote
                    base_accumulated += remaining_quote/entry[1]
                    break
            if quoted_accumulated != quote_max_accumulated:
                results.append(None)
            else:
                results.append(quoted_accumulated/base_accumulated)
        return results


class SurbtcClient(ExchangeClient):
    client = SURBTC.Public()

    @staticmethod
    def get_pair_mapping(base, quote):
        return base + '-' + quote

    @staticmethod
    def standarize_orderbook(raw_orderbook):
        orderbook = {}
        orderbook['bids'] = sorted(
            [(entry.amount, entry.price) for entry in raw_orderbook.bids],
            key=lambda x: x[1], reverse=True
        )
        orderbook['asks'] = sorted(
            [(entry.amount, entry.price) for entry in raw_orderbook.asks],
            key=lambda x: x[1], reverse=False
        )
        return orderbook

    def get_orderbook(self, base, quote):
        market = self.get_pair_mapping(base, quote)
        orderbook = self.client.order_book(market)
        return self.standarize_orderbook(orderbook)
