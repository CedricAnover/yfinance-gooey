from gooey import Gooey, GooeyParser
import yfinance as yf

def get_ohlcv_df(ticker, start_date, end_date, timeframe="1d"):
    symbol = yf.Ticker(ticker)

    # Note: In Gooey, the Dates are given as strings with format (YYYY-MM-DD).

    df_ohlcv = symbol.history(period="1mo", interval=timeframe,
                              start=start_date, end=end_date, prepost=False, actions=False,
                              auto_adjust=True, back_adjust=False, repair=False, keepna=False,
                              proxy=None, rounding=False, timeout=10,
                              debug=True, raise_errors=False)
    return df_ohlcv

# The program basically just a data collection (data entry) for the user inputs/arguments.
@Gooey(program_name="Yahoo Finance Data Downloader")
def main():
    parser = GooeyParser(description="Get Yahoo Finance Ticker Data.")
    # main_parser = parser.add_subparsers(required=True)

    parser.add_argument("Ticker", widget="TextField", help="Type a valid yahoo finance ticker")

    parser.add_argument("StartDate", widget="DateChooser", help="Select the Start Date")
    parser.add_argument("EndDate", widget="DateChooser", help="Select the End Date")

    parser.add_argument("--Timeframe", widget="Dropdown", help="Select the Timeframe",
                        default="1d",
                        choices=["1m","2m","5m","15m","30m","60m","90m","1h","1d","5d","1wk","1mo","3mo"]
                        )

    parser.add_argument("FileExtension", widget="Dropdown", help="Select the File Extension for export (csv/xlsx)", choices=[".csv", ".xlsx"])

    parser.add_argument("Directory", widget="DirChooser", help="Write the directory for export")

    return parser.parse_args()

if __name__ == "__main__":
    args = main()

    # Get the OHLCV Date
    df = get_ohlcv_df(args.Ticker, args.StartDate, args.EndDate, timeframe=args.Timeframe)
    df.index = df.index.date # Use only date

    # Export the DataFrame to the supplied directory with filename and extension.
    if args.FileExtension == ".csv":
        df.to_csv(fr'{args.Directory}\{args.Ticker}{args.FileExtension}')
    if args.FileExtension == ".xlsx":
        df.to_excel(fr'{args.Directory}\{args.Ticker}{args.FileExtension}')