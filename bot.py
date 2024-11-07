from ape import Contract, chain
from ape.api import BlockAPI
from typing import Annotated
from taskiq import Context, TaskiqDepends
from rich import print as rich_print
from silverback import SilverbackBot, StateSnapshot

bot = SilverbackBot()

BTC_USD = Contract("0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c")
"""Chanklink BTC/USD price-aggregator contract."""


@bot.on_startup()
def bot_startup(startup_state: StateSnapshot):
    round_data = BTC_USD.latestRoundData()
    show_answer(round_data.answer, "Startup")


@bot.on_(chain.blocks)
def exec_block(block: BlockAPI, context: Annotated[Context, TaskiqDepends()]):
    # TODO: Remove once AnswerUpdated works?
    round_data = BTC_USD.latestRoundData()
    show_answer(round_data.answer, "New Block")


@bot.on_(BTC_USD.AnswerUpdated)
def exec_AnswerUpdated(log):
    # TODO: Why doesn't this event fire?
    show_answer(log.current, "AnswerUpdated")


def show_answer(answer: int, trigger: str):
    price_in_usd = answer / (10**8)
    if price_in_usd > 100000:
        rich_print(
            f"🎉🎉🎉 ({trigger}) BTC/USD price has exceeded 100K: "
            f"${price_in_usd:,.2f} 🎉🎉🎉"
        )
    else:
        rich_print(
            f"({trigger}) BTC/USD price: ${price_in_usd:,.2f}. "
            "Waiting for over $100K..."
        )
