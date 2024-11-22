from ape import Contract
from rich import print as rich_print
from silverback import SilverbackBot, StateSnapshot

bot = SilverbackBot()

BTC_USD_PRICE_FEED = Contract("0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c")


@bot.on_startup()
def bot_startup(startup_state: StateSnapshot):
    round_data = BTC_USD_PRICE_FEED.latestRoundData()
    show_answer(round_data.answer, "Startup")


@bot.on_(BTC_USD_PRICE_FEED.AnswerUpdated)
def exec_AnswerUpdated(log):
    show_answer(log.current, "AnswerUpdated")


@bot.on_(BTC_USD_PRICE_FEED.NewRound)
def exec_NewRound(log):
    round_data = BTC_USD_PRICE_FEED.latestRoundData()
    show_answer(round_data.answer, "New Round")


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
