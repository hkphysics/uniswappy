#!/usr/bin/env python3

from uniswappy import *
import pandas as pd
import numpy as np
from icecream import ic
import traceback
from axc_lp import *

fee = UniV3Utils.FeeAmount.MEDIUM
tick_spacing = UniV3Utils.TICK_SPACINGS[fee]
init_price = UniV3Utils.encodePriceSqrt(1000,1000)

usdt_in = 10**6
tenv = TokenScenario(
    user = 'user',
    reserve = usdt_in * 0.2,
    name0 = "TKN",
    name1 = "USDT",
    address0 = "0x111",
    address1 = "0x09",   
    usdt_in = usdt_in,
    tick_spacing = tick_spacing,
    fee = fee,
    init_price = init_price
)

nsteps = 50
lp_prices = []
lp_liquidity = []

def do_sim(tenv, lp, tkn0, tkn1):
    # Set up liquidity pool
    frac_reserve = 0.05

    # Run simulation
    for i in range(1, nsteps):
        accounts = MockAddress().apply(500)
        select_tkn = EventSelectionModel().bi_select(0.5)
        rnd_add_amt = TokenDeltaModel(100000).delta()
        rnd_swap_amt = TokenDeltaModel(100000).delta()
        user_add = random.choice(accounts)
        user_swap = random.choice(accounts)
        try:
            out = Swap().apply(lp, tkn0 if select_tkn == 0 else tkn1, user_swap, rnd_swap_amt)
            lp_prices.append(lp.get_price(tkn0))
            lp_liquidity.append(lp.get_liquidity())
            lp.summary()
            print("*****", select_tkn, rnd_swap_amt, out, lp.get_price(tkn0))
        except AssertionError:
            print("Failed", select_tkn, rnd_swap_amt)
#            print(traceback.format_exc())
            pass

(lp, tkn0, tkn1) = setup_lp(
        tenv, [
            [tenv.reserve, 0.9, 1.0]
        ]
)
do_sim(tenv, lp, tkn0, tkn1)
