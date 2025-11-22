# 1、交易引擎
from vnpy.app.cta_strategy import (
    CtaEngine,
    CtaStrategy,
    BarGenerator,
    ArrayManager,
)

# 创建交易引擎实例
engine = CtaEngine()

# 添加策略
class MyStrategy(CtaStrategy):
    author = "Your Name"

    # 策略初始化函数
    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager()

    # 数据处理函数
    def on_bar(self, bar):
        self.am.update_bar(bar)
        if not self.am.inited:
            return

        # 这里编写策略逻辑
        pass

# 添加策略实例
engine.add_strategy(MyStrategy, {"name": "MyStrategy", "vt_symbol": "ETHUSDT", "setting": {}})

# 2、数据管理
from vnpy.app.data_manager import DriverManager

# 创建数据管理器实例
manager = DriverManager()

# 加载历史数据
data = manager.load_history_data("ETHUSDT", "1min", start_time="2023-01-01 00:00:00", end_time="2023-01-31 23:59:59")

# 打印数据
print(data.head())

# 3、风险控制
from vnpy.app.risk_manager import RiskManager

# 创建风险管理器实例
risk_manager = RiskManager()

# 设置风险参数
risk_manager.set_position_limit("ETHUSDT", 10)  # 设置ETHUSDT的最大持仓为10手
risk_manager.set_order_limit("ETHUSDT", 5)     # 设置ETHUSDT的最大挂单数为5

# 检查订单是否通过风险控制
order = risk_manager.check_order("ETHUSDT", "BUY", 1, 1000)
if order:
    print("订单通过风险控制")
else:
    print("订单未通过风险控制")


# 4、事件驱动

from vnpy.event import Event, EventEngine

# 创建事件引擎实例
event_engine = EventEngine()

# 定义事件处理函数
def on_order(event: Event):
    print(f"收到订单事件：{event}")

# 注册事件处理函数
event_engine.register(on_order, "ORDER")

# 触发事件
event_engine.put(Event("ORDER", {"data": "订单数据"}))

# 5、日志管理
from vnpy.trader.utility import LogEngine

# 创建日志引擎实例
log_engine = LogEngine()

# 设置日志级别
log_engine.set_level("INFO")

# 输出日志
log_engine.info("这是一条信息日志")
log_engine.error("这是一条错误日志")

# 6、回测框架

from vnpy.app.cta_strategy import CtaBacktestingMode
from vnpy.app.cta_strategy.backtesting import BacktestingEngine

# 创建回测引擎实例
engine = BacktestingEngine()

# 设置回测参数
engine.set_parameters(mode=CtaBacktestingMode, interval="1min", start_time="2023-01-01 00:00:00", end_time="2023-01-31 23:59:59")

# 添加策略
engine.add_strategy(MyStrategy, {"name": "MyStrategy", "vt_symbol": "ETHUSDT", "setting": {}})

# 运行回测
engine.run_backtesting()

# 输出回测结果
print(engine.get_result())

# vnpy的高级功能
# 事件驱动引擎
#vnpy`` 使用事件驱动模型，使得交易处理更加高效。以下是一个简单的事件处理示例：
from vnpy.event import Event, EventEngine

# 创建事件引擎
engine = EventEngine()

# 定义事件处理函数
def on_bar(event: Event):
    print(f"Received bar data: {event.data}")

# 注册事件处理函数
engine.register(on_bar, Event.BAR)

# 模拟发送事件
engine.put_event(Event(Event.BAR, "2021-01-01 10:00:00"))

# 启动事件引擎
engine.start()

# 多交易所支持
#vnpy`` 支持多个交易所，使得用户可以在一个平台管理多个交易所的账户。以下是如何添加一个交易所的示例：
from vnpy.app.cta_strategy import CtaEngine
from vnpy.gateway.bitfinex import BitfinexGateway

# 创建策略引擎
engine = CtaEngine()

# 添加Bitfinex交易所
engine.add_gateway(BitfinexGateway)

# 配置交易所连接信息
engine.set_gateway_config("Bitfinex", {"key": "your_api_key", "secret": "your_api_secret"})

# 策略管理
#vnpy`` 提供了强大的策略管理功能，支持策略的创建、加载和运行。以下是一个简单的策略示例：

from vnpy.app.cta_strategy import CtaTemplate, BarGenerator, ArrayManager

class MyStrategy(CtaTemplate):
    author = "Your Name"

    # 策略参数
    parameter = 10

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager()

    def on_init(self):
        self.write_log("策略初始化")
        self.load_bar(10)

    def on_bar(self, bar):
        self.am.update_bar(bar)
        if not self.am.inited:
            return

        # 策略逻辑
        if self.am.cross_over(self(parameter)):
            self.buy(bar.close_price, 1)
        elif self.am.cross_below(self(parameter)):
            self.sell(bar.close_price, 1)

# 加载策略
engine.add_strategy(MyStrategy, {"vt_symbol": "BTC/USDT", "setting": {"parameter": 20}})

# 风险控制
#vnpy`` 提供了完善的风险控制功能，包括资金管理、止损和止盈等。以下是一个简单的风险控制示例：

from vnpy.app.cta_strategy import CtaTemplate

class MyStrategy(CtaTemplate):
    # 策略参数
    max_position = 10  # 最大持仓

    def on_order(self, order):
        if order.status == Status.ALL特拉DED:
            if order.direction == Direction.LONG:
                self.position += order.volume
            elif order.direction == Direction.SHORT:
                self.position -= order.volume

            # 检查是否超过最大持仓
            if abs(self.position) > self.max_position:
                self.write_log("超过最大持仓，平仓操作")
                self.close_all()

    def on_stop_order(self, stop_order):
        # 处理止损订单
        if stop_order.status == Status.ALL特拉DED:
            self.write_log("止损订单触发，平仓操作")
            self.close_all()

# 数据存储
#vnpy`` 支持将历史数据存储到数据库中，方便后续分析和回测。以下是如何将数据存储到数据库的示例：

from vnpy.app.data_manager importDataManager

# 创建数据管理器
manager = DataManager()

# 添加数据到数据库
manager.save_data("tick_data", tick_data)
manager.save_data("bar_data", bar_data)

# 查询数据
data = manager.load_data("tick_data", start_time="2021-01-01", end_time="2021-01-02")

# 多语言支持
#vnpy`` 支持多种编程语言，包括 Python、C++ 和 Java 等。以下是一个使用 C++ 扩展的示例：
#include < vnpy/vnpy.hpp>
'''
class MyExtension : public Extension {
public:
    MyExtension() : Extension("MyExtension") {}

    void on_init() override {
        // 初始化代码
    }

    void on_bar(Bar& bar) override {
        // 处理K线数据
    }
};

extern "C" Extension* create_extension() {
    return new MyExtension();
}

'''
# 量化交易平台
# 通过整合以上高级功能，vnpy 可以构建一个完整的量化交易平台，以下是一个简单的交易流程示例
from vnpy.app.cta_strategy import CtaEngine
from vnpy.app.data_manager import DataManager
from vnpy.gateway.bitfinex import BitfinexGateway

# 创建策略引擎
cta_engine = CtaEngine()
# 创建数据管理器
data_manager = DataManager()

# 添加交易所
cta_engine.add_gateway(BitfinexGateway)
# 配置交易所连接信息
cta_engine.set_gateway_config("Bitfinex", {"key": "your_api_key", "secret": "your_api_secret"})

# 加载策略
cta_engine.add_strategy(MyStrategy, {"vt_symbol": "BTC/USDT", "setting": {"parameter": 20}})

# 数据存储
data_manager.save_data("tick_data", tick_data)
data_manager.save_data("bar_data", bar_data)

# 启动策略引擎
cta_engine.start()


# vnpy的实际应用场景
# 量化交易策略开发
# 在量化交易中，vnpy 提供了一套完整的框架，便于开发、测试和部署交易策略。以下是一个简单的双均线策略示例：

from vnpy.app.cta_strategy import (
    CtaTemplate,
    BarGenerator,
    ArrayManager,
    TickData,
    BarData,
    TradeData,
    OrderData
)

class DoubleMaStrategy(CtaTemplate):
    author = "AI"

    ma_short = 5
    ma_long = 10
    fixed_size = 1

    parameters = ["ma_short", "ma_long", "fixed_size"]
    variables = []

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager()

    def on_init(self):
        self.write_log("策略初始化")
        self.load_bar(10)

    def on_start(self):
        self.write_log("策略启动")
        self.put_event()

    def on_stop(self):
        self.write_log("策略停止")
        self.put_event()

    def on_tick(self, tick: TickData):
        self.bg.update_tick(tick)

    def on_bar(self, bar: BarData):
        self.am.update_bar(bar)
        if not self.am.inited:
            return

        short_ma = self.am.sma(self.ma_short, array=True)
        long_ma = self.am.sma(self.ma_long, array=True)

        if short_ma[-1] > long_ma[-1] and short_ma[-2] <= long_ma[-2]:
            self.buy(bar.close_price, self.fixed_size)
        elif short_ma[-1] < long_ma[-1] and short_ma[-2] >= long_ma[-2]:
            self.sell(bar.close_price, self.fixed_size)

# 风险管理
# vnpy 支持多种风险管理策略，包括止损、止盈等。以下是一个简单的止损策略示例：
class StopLossStrategy(CtaTemplate):
    author = "AI"

    stop_loss_threshold = 0.02  # 设置止损阈值

    parameters = ["stop_loss_threshold"]
    variables = ["trading_price"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.trading_price = 0

    def on_init(self):
        self.write_log("策略初始化")
        self.load_bar(10)

    def on_start(self):
        self.write_log("策略启动")
        self.put_event()

    def on_stop(self):
        self.write_log("策略停止")
        self.put_event()

    def on_tick(self, tick: TickData):
        if self.pos_long > 0:
            if tick.last_price < self.trading_price * (1 - self.stop_loss_threshold):
                self.sell(tick.last_price, abs(self.pos_long))
                self.write_log("触发止损，平仓")

# 套利交易
# vnpy 支持套利交易策略的开发，以下是一个简单的统计套利策略示例：
class StatisticalArbitrageStrategy(CtaTemplate):
    author = "AI"

    ma_window = 30
    hedge_ratio = 1.0

    parameters = ["ma_window", "hedge_ratio"]
    variables = []

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)

    def on_init(self):
        self.write_log("策略初始化")
        self.load_bar(10)

    def on_start(self):
        self.write_log("策略启动")
        self.put_event()

    def on_stop(self):
        self.write_log("策略停止")
        self.put_event()

    def on_bar(self, bar: BarData):
        # 假设有两个相关联的资产
        bar1 = self.get_bar("asset1")
        bar2 = self.get_bar("asset2")

        if bar1 and bar2:
            spread = bar1.close_price - bar2.close_price * self.hedge_ratio
            ma_spread = self.calculate_ma(spread, self.ma_window)

            if spread < ma_spread:
                self.buy("asset1", 1)
                self.sell("asset2", self.hedge_ratio)
            elif spread > ma_spread:
                self.sell("asset1", 1)
                self.buy("asset2", self.hedge_ratio)

# 账户管理
# vnpy 提供了账户管理功能，可以方便地查询和管理账户资产。以下是一个查询账户余额的示例：
class AccountManagementStrategy(CtaTemplate):
    author = "AI"

    def on_init(self):
        self.write_log("策略初始化")
        self.load_bar(10)

    def on_start(self):
        self.write_log("策略启动")
        self.put_event()

    def on_stop(self):
        self.write_log("策略停止")
        self.put_event()

    def on_tick(self, tick: TickData):
        account = self.account()
        balance = account.balance
        self.write_log(f"当前账户余额：{balance}")

# 回测与优化
# vnpy 支持策略的回测与优化，以下是一个简单的回测示例：

from vnpy.app.cta_strategy import CtaTemplate, BarGenerator, ArrayManager, TickData, BarData, TradeData, OrderData
from vnpy.app.cta_backtesting import CtaBacktestingEngine, OptimizationSetting


class MeanReversionStrategy(CtaTemplate):
    author = "AI"

    entry_threshold = 0.02
    exit_threshold = 0.02

    parameters = ["entry_threshold", "exit_threshold"]
    variables = []

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager()

    def on_bar(self, bar: BarData):
        self.am.update_bar(bar)
        if not self.am.inited:
            return

        if self.am.sma(20) < self.am.close[-1] * (1 - self.entry_threshold):
            self.buy(bar.close_price, 1)
        elif self.am.sma(20) > self.am.close[-1] * (1 + self.exit_threshold):
            self.sell(bar.close_price, 1)


# 创建回测引擎
engine = CtaBacktestingEngine()
engine.set_parameters
vt_symbol = "EURUSD", interval = "1m", start_date = "2021-01-01 00:00:00", end_date = "2022-01-01 00:00:00"
engine.add_strategy(MeanReversionStrategy, {"entry_threshold": 0.02, "exit_threshold": 0.02})

# 进行回测
engine.run_backtesting()

# 实盘交易
# vnpy 支持实盘交易，以下是一个简单的实盘交易示例：
from vnpy.app.cta_strategy import CtaTemplate, BarGenerator, ArrayManager, TickData, BarData, TradeData, OrderData
from vnpy.app.cta_trading import CtaTradingEngine


class RealTradingStrategy(CtaTemplate):
    author = "AI"

    ma_window = 20

    parameters = ["ma_window"]
    variables = []

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.bg = BarGenerator(self.on_bar)
        self.am = ArrayManager()

    def on_bar(self, bar: BarData):
        self.am.update_bar(bar)
        if not self.am.inited:
            return

        ma_price = self.am.sma(self.ma_window, array=True)[-1]
        if self.am.close[-1] > ma_price:
            self.buy(bar.close_price, 1)
        elif self.am.close[-1] < ma_price:
            self.sell(bar.close_price, 1)


# 创建交易引擎
engine = CtaTradingEngine()
engine.add_strategy(RealTradingStrategy, {"ma_window": 20})

# 启动交易
engine.start_trading()


