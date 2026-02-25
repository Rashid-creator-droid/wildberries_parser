from core.logger import Logger


class CurrencyConverter:

    @staticmethod
    def convert_rub_cop(price_cop: int) -> float:
        ruble = price_cop / 100
        Logger.debug(f"Конретация цены в рубли: {price_cop} -> {ruble}")
        return ruble
