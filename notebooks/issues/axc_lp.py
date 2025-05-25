from uniswappy import *
import pandas as pd
import numpy as np
from icecream import ic
from pydantic import BaseModel, ConfigDict
from dataclasses import dataclass
import traceback
from axc_lp import *

import matplotlib.pyplot as plt

@dataclass
class TokenScenario:
    user: str
    usdt_in: int
    reserve: int
    name0: str
    name1: str
    address0: str
    address1: str
    tick_spacing: any
    fee: any
    init_price: any

def plotme(df, title, annotation):
    plt.figure(figsize=(10,6))
    for key, grp in df.groupby('lower'):
        plt.plot(grp['swap'], grp['price'], label=key)

    plt.text(25000, 0.6, annotation )
    plt.legend(title=title)
    plt.xlabel('Tokens sold (TKN)')
    plt.ylabel('Swap price (USDT/TKN)')
    plt.show()

def get_tick(lp, x):
    if x == "min_tick":
        return UniV3Utils.getMinTick(lp.tickSpacing)
    elif x == "max_tick":
        return UniV3Utils.getMaxTick(lp.tickSpacing)
    return UniV3Helper().get_price_tick(lp, 0, x)

def setup_lp(tenv, pool_params):
    factory = UniswapFactory("ETH pool factory", "0x%d" )
    tkn0 = ERC20(tenv.name0, tenv.address0)
    tkn1 = ERC20(tenv.name1, tenv.address1)
    exchg_data = UniswapExchangeData(
        tkn0 = tkn0, tkn1 = tkn1,
        symbol="LP", 
        address="0x011", version="V3",
        tick_spacing = tenv.tick_spacing,
        fee=tenv.fee
    )
    lp = factory.deploy(exchg_data)
    lp.initialize(tenv.init_price)
    for pool_param in pool_params:
        AddLiquidity().apply(
            lp, tkn1, tenv.user, pool_param[0],
            get_tick(lp, pool_param[1]), 
            get_tick(lp, pool_param[2])
        )
#    lp.summary()
    return (lp, tkn0, tkn1)

def do_calc(tenv):
    results = []
    for lower in [0.95, 0.9, 0.8, 0.7, 0.5, 0.1, 0.000001]:
        for swap in np.geomspace(100, tenv.usdt_in, num=100):
            (lp, tkn0, tkn1) = setup_lp(tenv, [[
                tenv.reserve, lower, 1.0
            ]])
            try:
                out = Swap().apply(lp, tkn0, tenv.user, swap)
                results.append({
                    "lower": lower,
                    "swap": swap,
                    "out": out,
                    "price": float(out) / float(swap)
                })
            except AssertionError:
                pass
    return pd.DataFrame(results)

def do_calc1(tenv):
    results = []
    insurance_lower = 0.95
    insurance_upper = 0.98
    for frac_reserve in np.geomspace(0.0001, 0.99, num=10):
        for swap in np.geomspace(100, tenv.usdt_in, num=100):
            (lp, tkn0, tkn1) = setup_lp(
                tenv, [
                    [tenv.reserve * (1.0 - frac_reserve), "min_tick", 1.0],
                    [tenv.reserve * frac_reserve, insurance_lower, 1.0]
                ]
            )
            try:
                out = Swap().apply(lp, tkn0, tenv.user, swap)
                results.append({
                    "lower": frac_reserve * 100,
                    "swap": swap,
                    "out": out,
                    "price": float(out) / float(swap)
                })
            except AssertionError:
                pass
    return pd.DataFrame(results)

__all__ = ['plotme', 'do_calc', 'do_calc1', 'setup_lp', 'TokenScenario']