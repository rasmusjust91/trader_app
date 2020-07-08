import yfinance as yf
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

if __name__ == "__main__":
    danske_bank = yf.download(
        'DANSKE.CO',
        start='2019-01-01',
        end='2019-12-31',
        progress=False,
        interval='15m'
    )

    print(
        danske_bank
    )
