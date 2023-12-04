"""
Describe strategy
"""
from multiprocessing import Value
import backtrader as bt
import arrow
from typing import Optional
from libs.strategy import loader
import pandas
import pandas_ta as ta


#from libs.strategy import strategy as strat

# logger = log.setup_custom_logger('pairtrading1a', settings.STRTLOG)

strat = loader.strategy


class Strategy(strat.Strategy):
    """description"""

    params = (
        ('take_profit', 1),
        ('trailing_stop', 1),
        ('timeout', 100),
        ('stop_loss', 1),
        ('rsi_period', 14),
        ('long_entry', 55),
        ('long_exit', 45),
        ('short_entry', 45),
        ('short_exit', 55),
        ('pre_load_bars', 30),
        ('feeds', 2)
    )

    next_open: arrow.Arrow

    def local_init(self):
        """description"""
        self.verbose = False
        self.order_cmd = "spread"
        if self.p.timeout:
            self.p.timeout = self.datas[1].bar_size_minutes * self.p.timeout
        if self.p.long_exit >= self.p.long_entry:
            self.cerebro.runstop()
        if self.p.short_exit <= self.p.short_entry:
            self.cerebro.runstop()

    def local_next(self):
        """ description """
        if self.entry_signal[0]:
            if self.curtime[0] >= self.next_open:
                self.open_pos(0)
                self.crossed_lower = False
                self.crossed_upper = False

    def set_indicators_df(self):
        if not self.indicators_df.empty:
            if self.indicators_df.index[-1] == self.datas[1].index[-1]:
                return
        self.indicators_df = self.data[['close', 'high', 'low']].copy()
        self.indicators_df['vi_pos'], self.indicators_df['vi_neg'] = ta.trend.vortex(self.indicators_df['high'], self.indicators_df['low'], self.indicators_df['close'], length=self.p.vi_period)
        self._set_signals()
        self.indicators_df = self.indicators_df.dropna()

    def _set_signals(self):
        self.indicators_df['long_entry'] = False
        self.indicators_df['long_exit'] = False
        self.indicators_df['short_entry'] = False
        self.indicators_df['short_exit'] = False

        long_entry_cond = (self.indicators_df['vi_pos'] > self.indicators_df['vi_neg']) & (self.indicators_df['vi_pos'].shift(1) <= self.indicators_df['vi_neg'].shift(1))
        long_exit_cond = self.indicators_df['vi_pos'] < self.indicators_df['vi_neg']
        short_entry_cond = (self.indicators_df['vi_neg'] > self.indicators_df['vi_pos']) & (self.indicators_df['vi_neg'].shift(1) <= self.indicators_df['vi_pos'].shift(1))
        short_exit_cond = self.indicators_df['vi_neg'] < self.indicators_df['vi_pos']

        self.indicators_df.loc[long_entry_cond, 'long_entry'] = True
        self.indicators_df.loc[long_exit_cond, 'long_exit'] = True
        self.indicators_df.loc[short_entry_cond, 'short_entry'] = True
        self.indicators_df.loc[short_exit_cond, 'short_exit'] = True


    def set_indicators(self):
        try:
            long_entry = self.indicators_df.loc[self.curtime[1].format('YYYY-MM-DD HH:mm:ss'), 'long_entry']
        except KeyError:
            long_entry = None
        try:
            short_entry = self.indicators_df.loc[self.curtime[1].format('YYYY-MM-DD HH:mm:ss'), 'short_entry']
        except KeyError:
            short_entry = None
        try:
            long_exit = self.indicators_df.loc[self.curtime[1].format('YYYY-MM-DD HH:mm:ss'), 'long_exit']
        except KeyError:
            long_exit = None
        try:
            short_exit = self.indicators_df.loc[self.curtime[1].format('YYYY-MM-DD HH:mm:ss'), 'short_exit']
        except KeyError:
            short_exit = None
        self.set_indicator('long_entry', long_entry)
        self.set_indicator('short_entry', short_entry)
        self.set_indicator('long_exit', long_exit)
        self.set_indicator('short_exit', short_exit)

    def local_nextstart(self):
        """ Only runs once, before local_next"""
        self.next_open = self.curtime[0]

    def get_entry_signal(self):
        """
        blah
        """
        try:
            if self.curtime[0] >= self.next_open:
                self.entry_signal[0] = ""
                if self.indicators.long_entry:
                    self.entry_signal[0] = "Buy"
                elif self.indicators.short_entry:
                    self.entry_signal[0] = "Sell"
        except KeyError:
            pass

    def risk_management(self):
        """
        Handle risk management for the strategy.
        This function checks for stop loss and take profit conditions,
        and closes the position if either of them are met.

        only works when there is a position, runs every tick
        """
        # Check for stop loss
        res = self.check_exit()
        if not res:
            if self.pos[0] < 0 and self.indicators.short_exit:
                res = self.close_position(feed=0, reason="strategy")
            elif self.pos[0] > 0 and self.indicators.long_exit:
                res = self.close_position(feed=0, reason="strategy")
        if res:
            self.next_open = self.time_to_next_bar(feed=1)
            self.entry_signal[0] = ""
            time_difference = (self.next_open.timestamp() - self.curtime[0].timestamp())
            if time_difference <= 60:  # less than 60 seconds
                self.next_open = self.next_open.shift(minutes=self.datas[1].bar_size_minutes)
            self.crossed_lower = False
            self.crossed_upper = False

    def event_in(self) -> Optional[arrow.Arrow]:
        """
        Find the date of the next buy or sell signal based on the current time.
        """
        curtime = pandas.to_datetime(self.next_open.format('YYYY-MM-DD HH:mm:ss'))

        # Filter based on conditions and time
        mask = ((self.indicators_df['long_entry'] == True) | (self.indicators_df['short_entry'] == True)) \
                & (self.indicators_df.index >= curtime)

        filtered_df = self.indicators_df[mask]

        # Check if the filtered dataframe has any rows
        if not filtered_df.empty:
            return arrow.get(str(filtered_df.index[0]))
        # If the function hasn't returned by this point, simply return None

    def event_out(self) -> Optional[arrow.Arrow]:
        """
        take profit and stop_loss are automatic
        """
        curtime = pandas.to_datetime(self.curtime[1].format('YYYY-MM-DD HH:mm:ss'))

        # Check the position before proceeding
        if self.pos[0] < 0:
            # Filter based on conditions and time for short exit
            mask = (self.indicators_df['short_exit'] == True) & (self.indicators_df.index >= curtime)
        else:
            # Filter based on conditions and time for long exit
            mask = (self.indicators_df['long_exit'] == True) & (self.indicators_df.index >= curtime)

        filtered_df = self.indicators_df[mask]

        # Check if the filtered dataframe has any rows
        if not filtered_df.empty:
            return arrow.get(str(filtered_df.index[0]))
