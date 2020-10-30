SET1 = dict(
    base_currency="USDT",
    position_side="longshort",
    exit_if_achieved=True,
    achieve_ratio=[1, 2, 5],
    achieved_with_commission=True,
    min_holding_minutes=[0, 10],
    max_holding_minutes=60,
    entry_ratio=0.1,
    commission={"entry": 0.0, "exit": 0.0},
    compound_interest=True,
    order_criterion="capital",
    max_n_updated=0,
    entry_qay_threshold=[8, 9],
    entry_qby_threshold=[8, 9],
    entry_qay_prob_threshold=[0, 0.2, 0.4],
    entry_qby_prob_threshold=[0, 0.2, 0.4],
    exit_q_threshold=[9],
)

SET2 = dict(
    base_currency="USDT",
    position_side="longshort",
    exit_if_achieved=True,
    achieve_ratio=[1, 2, 5],
    achieved_with_commission=True,
    min_holding_minutes=[0, 10],
    max_holding_minutes=60,
    entry_ratio=0.001,
    commission={"entry": 0.0, "exit": 0.0},
    compound_interest=True,
    order_criterion="capital",
    max_n_updated=None,
    entry_qay_threshold=[8, 9],
    entry_qby_threshold=[8, 9],
    entry_qay_prob_threshold=[0, 0.2, 0.4],
    entry_qby_prob_threshold=[0, 0.2, 0.4],
    exit_q_threshold=[9],
)

C_SET1 = dict(
    base_currency="USDT",
    position_side="longshort",
    exit_if_achieved=True,
    achieve_ratio=[1, 2, 5],
    achieved_with_commission=True,
    min_holding_minutes=[0, 10],
    max_holding_minutes=60,
    entry_ratio=0.1,
    commission={"entry": 0.0004, "exit": 0.0002},
    compound_interest=True,
    order_criterion="capital",
    max_n_updated=0,
    entry_qay_threshold=[8, 9],
    entry_qby_threshold=[8, 9],
    entry_qay_prob_threshold=[0, 0.2, 0.4],
    entry_qby_prob_threshold=[0, 0.2, 0.4],
    exit_q_threshold=[9],
)

C_SET2 = dict(
    base_currency="USDT",
    position_side="longshort",
    exit_if_achieved=True,
    achieve_ratio=[1, 2, 5],
    achieved_with_commission=True,
    min_holding_minutes=[0, 10],
    max_holding_minutes=60,
    entry_ratio=0.001,
    commission={"entry": 0.0004, "exit": 0.0002},
    compound_interest=True,
    order_criterion="capital",
    max_n_updated=None,
    entry_qay_threshold=[8, 9],
    entry_qby_threshold=[8, 9],
    entry_qay_prob_threshold=[0, 0.2, 0.4],
    entry_qby_prob_threshold=[0, 0.2, 0.4],
    exit_q_threshold=[9],
)
