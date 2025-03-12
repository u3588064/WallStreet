"""
市场工具模块，提供金融市场模拟所需的工具函数
"""

import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional


class MarketUtils:
    """金融市场工具类"""
    
    @staticmethod
    def generate_price_series(
        initial_price: float,
        days: int,
        volatility: float = 0.01,
        drift: float = 0.0001,
        random_seed: Optional[int] = None
    ) -> pd.Series:
        """
        生成价格时间序列（几何布朗运动）
        
        Args:
            initial_price: 初始价格
            days: 天数
            volatility: 波动率
            drift: 漂移率
            random_seed: 随机种子
            
        Returns:
            价格时间序列
        """
        if random_seed is not None:
            np.random.seed(random_seed)
            
        # 生成日期索引
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # 生成价格序列（几何布朗运动）
        returns = np.random.normal(drift, volatility, days) + 1
        price_series = initial_price * returns.cumprod()
        
        return pd.Series(price_series, index=date_range)
    
    @staticmethod
    def calculate_returns(prices: pd.Series) -> pd.Series:
        """
        计算收益率
        
        Args:
            prices: 价格序列
            
        Returns:
            收益率序列
        """
        return prices.pct_change().dropna()
    
    @staticmethod
    def calculate_volatility(returns: pd.Series, window: int = 20) -> pd.Series:
        """
        计算波动率
        
        Args:
            returns: 收益率序列
            window: 窗口大小
            
        Returns:
            波动率序列
        """
        return returns.rolling(window=window).std() * np.sqrt(252)  # 年化
    
    @staticmethod
    def calculate_sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        """
        计算夏普比率
        
        Args:
            returns: 收益率序列
            risk_free_rate: 无风险利率
            
        Returns:
            夏普比率
        """
        excess_returns = returns.mean() * 252 - risk_free_rate
        volatility = returns.std() * np.sqrt(252)
        return excess_returns / volatility if volatility != 0 else 0
    
    @staticmethod
    def simulate_market_shock(
        prices: pd.Series,
        shock_magnitude: float = -0.05,
        recovery_days: int = 30,
        recovery_strength: float = 0.7
    ) -> pd.Series:
        """
        模拟市场冲击
        
        Args:
            prices: 价格序列
            shock_magnitude: 冲击幅度
            recovery_days: 恢复天数
            recovery_strength: 恢复强度
            
        Returns:
            冲击后的价格序列
        """
        shocked_prices = prices.copy()
        
        # 应用冲击
        shock_day = prices.index[-1] - timedelta(days=recovery_days)
        shock_idx = prices.index.get_indexer([shock_day], method='nearest')[0]
        
        # 冲击当天价格变化
        shocked_prices.iloc[shock_idx] *= (1 + shock_magnitude)
        
        # 恢复期
        for i in range(shock_idx + 1, len(prices)):
            days_since_shock = i - shock_idx
            recovery_factor = min(1.0, days_since_shock / recovery_days * recovery_strength)
            remaining_shock = shock_magnitude * (1 - recovery_factor)
            shocked_prices.iloc[i] = prices.iloc[i] * (1 + remaining_shock)
            
        return shocked_prices
    
    @staticmethod
    def calculate_correlation_matrix(returns_dict: Dict[str, pd.Series]) -> pd.DataFrame:
        """
        计算相关性矩阵
        
        Args:
            returns_dict: 收益率字典，键为资产名称，值为收益率序列
            
        Returns:
            相关性矩阵
        """
        # 将所有收益率序列合并为一个DataFrame
        returns_df = pd.DataFrame(returns_dict)
        
        # 计算相关性矩阵
        return returns_df.corr()
    
    @staticmethod
    def simulate_trading_volume(
        price_series: pd.Series,
        base_volume: int = 1000000,
        price_sensitivity: float = 0.5,
        random_factor: float = 0.3
    ) -> pd.Series:
        """
        模拟交易量
        
        Args:
            price_series: 价格序列
            base_volume: 基础交易量
            price_sensitivity: 价格敏感度
            random_factor: 随机因子
            
        Returns:
            交易量序列
        """
        # 计算价格变化的绝对百分比
        price_changes = price_series.pct_change().abs().fillna(0)
        
        # 生成随机噪声
        noise = np.random.normal(1, random_factor, len(price_series))
        
        # 计算交易量
        volume = base_volume * (1 + price_changes * price_sensitivity) * noise
        
        return pd.Series(volume, index=price_series.index).round().astype(int)
    
    @staticmethod
    def generate_order_book(
        current_price: float,
        depth: int = 10,
        spread_percent: float = 0.1,
        volume_base: int = 100,
        price_step: float = 0.01
    ) -> Dict[str, List[Tuple[float, int]]]:
        """
        生成订单簿
        
        Args:
            current_price: 当前价格
            depth: 深度
            spread_percent: 买卖价差百分比
            volume_base: 基础交易量
            price_step: 价格步长
            
        Returns:
            订单簿，包含买单和卖单
        """
        half_spread = current_price * spread_percent / 200  # 半个价差
        
        # 生成买单
        bids = []
        bid_price = current_price - half_spread
        for i in range(depth):
            volume = int(volume_base * (1 - i * 0.05) * random.uniform(0.8, 1.2))
            bids.append((round(bid_price, 2), volume))
            bid_price -= price_step * random.uniform(0.8, 1.2)
            
        # 生成卖单
        asks = []
        ask_price = current_price + half_spread
        for i in range(depth):
            volume = int(volume_base * (1 - i * 0.05) * random.uniform(0.8, 1.2))
            asks.append((round(ask_price, 2), volume))
            ask_price += price_step * random.uniform(0.8, 1.2)
            
        return {
            "bids": bids,  # 买单 [(价格, 数量), ...]
            "asks": asks,  # 卖单 [(价格, 数量), ...]
        }
    
    @staticmethod
    def calculate_market_liquidity(order_book: Dict[str, List[Tuple[float, int]]]) -> float:
        """
        计算市场流动性
        
        Args:
            order_book: 订单簿
            
        Returns:
            市场流动性指标
        """
        bids = order_book["bids"]
        asks = order_book["asks"]
        
        # 计算买单和卖单的总量
        bid_volume = sum(vol for _, vol in bids)
        ask_volume = sum(vol for _, vol in asks)
        
        # 计算买卖价差
        best_bid = bids[0][0] if bids else 0
        best_ask = asks[0][0] if asks else float('inf')
        spread = best_ask - best_bid
        
        # 流动性指标 = 总量 / 价差
        if spread > 0:
            return (bid_volume + ask_volume) / spread
        return float('inf')  # 如果价差为0，流动性无限大
    
    @staticmethod
    def simulate_interest_rates(
        initial_rate: float = 0.02,
        days: int = 365,
        volatility: float = 0.0005,
        mean_reversion: float = 0.01,
        long_term_mean: float = 0.03,
        random_seed: Optional[int] = None
    ) -> pd.Series:
        """
        模拟利率（Vasicek模型）
        
        Args:
            initial_rate: 初始利率
            days: 天数
            volatility: 波动率
            mean_reversion: 均值回归速度
            long_term_mean: 长期均值
            random_seed: 随机种子
            
        Returns:
            利率时间序列
        """
        if random_seed is not None:
            np.random.seed(random_seed)
            
        # 生成日期索引
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Vasicek模型
        rates = [initial_rate]
        for _ in range(1, days):
            dr = mean_reversion * (long_term_mean - rates[-1]) + volatility * np.random.normal()
            new_rate = max(0.001, rates[-1] + dr)  # 确保利率为正
            rates.append(new_rate)
            
        return pd.Series(rates, index=date_range) 