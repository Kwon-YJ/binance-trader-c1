import os
from .utils import nan_to_zero
from .basic_backtester import BasicBacktester
from tqdm import tqdm
import gc


CONFIG = {
    "report_prefix": "v001",
    "detail_report": False,
    "position_side": "longshort",
    "entry_ratio": 0.2,
    # "commission": {"entry": 0.0004, "exit": 0.0002, "spread": 0.0004},
    "commission": {"entry": 0, "exit": 0, "spread": 0},
    "min_holding_minutes": 1,
    "max_holding_minutes": 30,
    "compound_interest": True,
    "order_criterion": "capital",
    "possible_in_debt": True,
    "exit_if_achieved": True,
    "achieve_ratio": 1,
    "achieved_with_commission": False,
    "max_n_updated": 0,
    "positive_entry_threshold": 8,
    "negative_entry_threshold": 8,
    "exit_threshold": "auto",
    "positive_probability_threshold": 8,
    "negative_probability_threshold": 8,
    "adjust_prediction": False,
}


class BacktesterV1(BasicBacktester):
    def __init__(
        self,
        base_currency,
        dataset_dir,
        exp_dir,
        report_prefix=CONFIG["report_prefix"],
        detail_report=CONFIG["detail_report"],
        position_side=CONFIG["position_side"],
        entry_ratio=CONFIG["entry_ratio"],
        commission=CONFIG["commission"],
        min_holding_minutes=CONFIG["min_holding_minutes"],
        max_holding_minutes=CONFIG["max_holding_minutes"],
        compound_interest=CONFIG["compound_interest"],
        order_criterion=CONFIG["order_criterion"],
        possible_in_debt=CONFIG["possible_in_debt"],
        exit_if_achieved=CONFIG["exit_if_achieved"],
        achieve_ratio=CONFIG["achieve_ratio"],
        achieved_with_commission=CONFIG["achieved_with_commission"],
        max_n_updated=CONFIG["max_n_updated"],
        positive_entry_threshold=CONFIG["positive_entry_threshold"],
        negative_entry_threshold=CONFIG["negative_entry_threshold"],
        exit_threshold=CONFIG["exit_threshold"],
        positive_probability_threshold=CONFIG["positive_probability_threshold"],
        negative_probability_threshold=CONFIG["negative_probability_threshold"],
        adjust_prediction=CONFIG["adjust_prediction"],
    ):
        super().__init__(
            base_currency=base_currency,
            dataset_dir=dataset_dir,
            exp_dir=exp_dir,
            report_prefix=report_prefix,
            detail_report=detail_report,
            position_side=position_side,
            entry_ratio=CONFIG["entry_ratio"],
            commission=CONFIG["commission"],
            min_holding_minutes=min_holding_minutes,
            max_holding_minutes=max_holding_minutes,
            compound_interest=compound_interest,
            order_criterion=order_criterion,
            possible_in_debt=possible_in_debt,
            exit_if_achieved=exit_if_achieved,
            achieve_ratio=achieve_ratio,
            achieved_with_commission=achieved_with_commission,
            max_n_updated=max_n_updated,
            positive_entry_threshold=positive_entry_threshold,
            negative_entry_threshold=negative_entry_threshold,
            exit_threshold=exit_threshold,
            positive_probability_threshold=positive_probability_threshold,
            negative_probability_threshold=negative_probability_threshold,
            adjust_prediction=adjust_prediction,
        )

    def run(self, display=True):

        self.build()
        self.initialize()

        for now in tqdm(self.index):
            # Step1: Prepare pricing and signal
            pricing = self.historical_data_dict["pricing"].loc[now]
            predictions = self.historical_data_dict["predictions"].loc[now]
            probabilities = self.historical_data_dict["probabilities"].loc[now]

            # Set assets which has signals
            positive_assets = self.tradable_coins[
                (predictions >= self.positive_entry_bins)
                & (probabilities >= self.positive_probability_bins)
            ]
            negative_assets = self.tradable_coins[
                (predictions <= self.negative_entry_bins)
                & (probabilities >= self.negative_probability_bins)
            ]

            # Debug: Print current state
            # print(f"\nTime: {now}")
            # print(f"Number of positions: {len(self.positions)}")
            # print(f"Number of trade returns: {len(self.historical_trade_returns)}")
            # if len(self.positions) > 0:
            #     print("Current positions:")
            #     for pos in self.positions:
            #         print(f"  {pos.asset} ({pos.side})")

            # Exit
            self.handle_exit(
                positive_assets=positive_assets,
                negative_assets=negative_assets,
                pricing=pricing,
                now=now,
            )

            # Debug: Print state after exit
            # print(f"Number of positions after exit: {len(self.positions)}")
            # print(f"Number of trade returns after exit: {len(self.historical_trade_returns)}")

            # Compute how much use cache
            if self.compound_interest is False:
                cache_to_order = self.entry_ratio
            else:
                if self.order_criterion == "cache":
                    if self.cache > 0:
                        cache_to_order = nan_to_zero(
                            value=(self.cache * self.entry_ratio)
                        )
                    else:
                        cache_to_order = 0

                elif self.order_criterion == "capital":
                    # Entry with capital base
                    cache_to_order = nan_to_zero(
                        value=(
                            self.compute_capital(pricing=pricing, now=now)
                            * self.entry_ratio
                        )
                    )

            # Entry
            self.handle_entry(
                predictions=predictions,
                cache_to_order=cache_to_order,
                positive_assets=positive_assets,
                negative_assets=negative_assets,
                pricing=pricing,
                now=now,
            )

            # To report
            self.report(value=self.cache, target="historical_caches", now=now)
            self.report(
                value=self.compute_capital(pricing=pricing, now=now),
                target="historical_capitals",
                now=now,
            )
            self.report(value=self.positions, target="historical_positions", now=now)


        report = self.generate_report()



        


        self.store_report(report=report)

        if display is True:
            self.display_metrics()
            self.display_report(report=report)

        # Remove historical data dict to reduce memory usage
        del self.historical_data_dict
        gc.collect()


if __name__ == "__main__":
    import fire

    fire.Fire(BacktesterV1)
