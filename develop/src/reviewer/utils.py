from itertools import product
from collections import OrderedDict


def grid(params):
    def _handle_value(value):
        return list(value) if type(value) == list or type(value) == tuple else [value]

    params = OrderedDict(
        [(key, _handle_value(value=params[key])) for key in sorted(list(params.keys()))]
    )

    keys = list(params.keys())
    for values in product(*list(params.values())):
        param = dict(zip(keys, values))
        yield param






import pandas as pd


def nan_to_zero(value):
    if str(value) in ("nan", "None"):
        return 0

    return value


def load_parquet(path):
    return pd.read_parquet(path)


class Position:
    def __init__(
        self,
        asset,
        side,
        qty,
        entry_price,
        prediction,
        entry_at,
        n_updated=0,
        is_exited=False,
    ):
        self.asset = asset
        self.side = side
        self.qty = qty
        self.entry_price = entry_price
        self.prediction = prediction
        self.entry_at = entry_at
        self.n_updated = n_updated
        self.is_exited = is_exited

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __repr__(self):
        return f"Position(asset={self.asset}, side={self.side}, qty={self.qty}, entry_price={self.entry_price:.4f}, n_updated={self.n_updated}, is_exited={str(self.is_exited)})"

    def __str__(self):
        return self.__repr__()
