import datetime as dt
import pandas as pd

class IndexModel:
    def __init__(self) -> None:
        self.stock_prices_file_path = "./data_sources/stock_prices.csv"
        self.index_level_results = pd.DataFrame({'Date': [], 'index_level': []})

    def calc_index_level(self, start_date: dt.date, end_date: dt.date) -> None:
        stock_prices = pd.read_csv(self.stock_prices_file_path)
        stock_prices['Date'] = pd.to_datetime(stock_prices['Date'], dayfirst=True).dt.date
        stock_prices = stock_prices.set_index('Date')

        month_end_dates = pd.Series(pd.date_range(start=start_date - pd.tseries.offsets.DateOffset(days=1), end=end_date, freq='M'))
        month_end_dates = month_end_dates.dt.date

        for i in range(len(month_end_dates) - 1):
            task_start_date = month_end_dates.loc[i]
            task_end_date = month_end_dates.loc[i + 1]
            task_index_level_results = self.calc_index_level_subtask(stock_prices, task_start_date, task_end_date)
            self.index_level_results = pd.concat([self.index_level_results, task_index_level_results])



    def export_values(self, file_name: str) -> None:
        adjustment_factor = 100 / self.index_level_results.iloc[0,1]
        self.index_level_results.index_level = self.index_level_results.index_level.multiply(adjustment_factor)
        print(self.index_level_results)
        self.index_level_results.to_csv(file_name, index=False)
    

    def calc_index_level_subtask(self, stock_prices: pd.DataFrame, task_start_date: dt.date, task_end_date: dt.date) -> pd.DataFrame:
        task_stock_prices = stock_prices.loc[(stock_prices.index >= task_start_date) & (stock_prices.index <= task_end_date)]
        task_stock_prices = task_stock_prices.sort_values(by=task_stock_prices.index[0], axis=1, ascending=False)

        task_stock_prices = task_stock_prices.iloc[1:, 0:3]
        task_stock_prices = task_stock_prices.mul([0.5, 0.25, 0.25])    

        task_index_level_results = pd.DataFrame({'index_level': task_stock_prices.iloc[:, 0] + task_stock_prices.iloc[:, 1] + task_stock_prices.iloc[:, 2]})
        task_index_level_results.reset_index(inplace=True)
        #print(task_index_level_results)

        return task_index_level_results



