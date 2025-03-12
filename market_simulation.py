"""
市场模拟核心逻辑模块，负责协调各金融主体之间的交互和市场运作
"""

import logging
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import autogen
from tqdm import tqdm

from config import (
    SIMULATION_PARAMS,
    MARKET_PARAMS,
    ASSET_CLASSES,
    REGULATORY_PARAMS,
    EVENT_PARAMS,
    FINANCIAL_ENTITIES,
)
from utils import FinancialAgent, MarketUtils


class MarketSimulation:
    """金融市场模拟类，负责协调各金融主体之间的交互和市场运作"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化金融市场模拟
        
        Args:
            config_path: 配置文件路径，如果为None则使用默认配置
        """
        self.logger = logging.getLogger("MarketSimulation")
        self.logger.setLevel(SIMULATION_PARAMS.get("log_level", "INFO"))
        
        # 设置随机种子
        random_seed = SIMULATION_PARAMS.get("random_seed", 42)
        random.seed(random_seed)
        np.random.seed(random_seed)
        
        # 初始化模拟参数
        self.simulation_days = SIMULATION_PARAMS.get("simulation_days", 252)
        self.current_day = 0
        self.start_date = datetime.strptime(
            SIMULATION_PARAMS.get("initial_date", "2023-01-01"),
            "%Y-%m-%d"
        )
        self.current_date = self.start_date
        
        # 初始化市场状态
        self.market_state = {
            "interest_rate": MARKET_PARAMS.get("interest_rate", 0.02),
            "inflation_rate": MARKET_PARAMS.get("inflation_rate", 0.03),
            "market_volatility": MARKET_PARAMS.get("market_volatility", 0.15),
            "liquidity_factor": MARKET_PARAMS.get("liquidity_factor", 1.0),
            "market_sentiment": 0.0,  # -1.0 (极度悲观) 到 1.0 (极度乐观)
            "economic_growth": 0.02,  # 年化经济增长率
            "unemployment_rate": 0.05,  # 失业率
        }
        
        # 初始化资产价格
        self.asset_prices = {}
        for asset_class in ASSET_CLASSES:
            initial_price = 100.0  # 所有资产类别的初始价格设为100
            self.asset_prices[asset_class] = MarketUtils.generate_price_series(
                initial_price=initial_price,
                days=self.simulation_days,
                volatility=ASSET_CLASSES[asset_class].get("volatility", 0.01),
                drift=ASSET_CLASSES[asset_class].get("expected_return", 0.0001) / 252,
                random_seed=random_seed + hash(asset_class) % 1000
            )
        
        # 初始化金融主体
        self.agents = {}
        self._initialize_agents()
        
        # 初始化交易记录
        self.transactions = []
        
        # 初始化事件记录
        self.events = []
        
        self.logger.info(f"金融市场模拟初始化完成，共有 {len(self.agents)} 个金融主体")
    
    def _initialize_agents(self):
        """初始化所有金融主体"""
        # 遍历所有类型的金融主体
        for entity_type, entities in FINANCIAL_ENTITIES.items():
            self.logger.info(f"初始化 {entity_type} 类金融主体，共 {len(entities)} 个")
            
            for entity_config in entities:
                agent = self._create_agent(entity_type, entity_config)
                self.agents[agent.id] = agent
        
        # 建立金融主体之间的连接
        self._establish_connections()
    
    def _create_agent(self, entity_type: str, entity_config: Dict[str, Any]) -> FinancialAgent:
        """
        创建金融主体
        
        Args:
            entity_type: 主体类型
            entity_config: 主体配置
            
        Returns:
            创建的金融主体
        """
        agent = FinancialAgent(
            name=entity_config["name"],
            agent_type=entity_type,
            description=entity_config["description"],
            # 其他参数可以根据需要添加
        )
        
        # 设置初始余额
        agent.balance = entity_config.get("initial_balance", 0.0)
        
        # 根据不同类型的金融主体设置特定属性
        if entity_type == "regulators":
            agent.policy_tools = entity_config.get("policy_tools", [])
        elif entity_type == "financial_institutions":
            agent.services = entity_config.get("services", [])
            agent.risk_profile = entity_config.get("risk_profile", "中")
        elif entity_type == "market_infrastructure":
            agent.services = entity_config.get("services", [])
        elif entity_type == "auxiliary_services":
            agent.services = entity_config.get("services", [])
        elif entity_type == "direct_participants":
            if "sector" in entity_config:
                agent.sector = entity_config["sector"]
            if "credit_rating" in entity_config:
                agent.credit_rating = entity_config["credit_rating"]
            if "risk_preference" in entity_config:
                agent.risk_preference = entity_config["risk_preference"]
        elif entity_type == "international_organizations":
            agent.functions = entity_config.get("functions", [])
        
        return agent
    
    def _establish_connections(self):
        """建立金融主体之间的连接"""
        # 这里可以根据实际需求设置不同类型金融主体之间的连接关系
        # 例如，商业银行与中央银行、企业与商业银行等
        
        # 示例：中央银行与所有金融机构建立连接
        central_bank = None
        for agent in self.agents.values():
            if agent.name == "中央银行":
                central_bank = agent
                break
        
        if central_bank:
            for agent in self.agents.values():
                if agent.agent_type == "financial_institutions":
                    central_bank.add_connection(agent)
                    self.logger.debug(f"建立连接: {central_bank.name} <-> {agent.name}")
        
        # 示例：证券交易所与所有投资者和金融机构建立连接
        exchange = None
        for agent in self.agents.values():
            if agent.name == "证券交易所":
                exchange = agent
                break
        
        if exchange:
            for agent in self.agents.values():
                if agent.agent_type in ["financial_institutions", "direct_participants"]:
                    exchange.add_connection(agent)
                    self.logger.debug(f"建立连接: {exchange.name} <-> {agent.name}")
        
        # 可以根据需要添加更多连接关系
    
    def run_simulation(self):
        """运行模拟"""
        self.logger.info(f"开始运行金融市场模拟，共 {self.simulation_days} 天")
        
        for day in tqdm(range(self.simulation_days), desc="模拟进度"):
            self.current_day = day
            self.current_date = self.start_date + timedelta(days=day)
            
            self.logger.info(f"第 {day+1} 天 ({self.current_date.strftime('%Y-%m-%d')})")
            
            # 1. 更新市场状态
            self._update_market_state()
            
            # 2. 处理随机事件
            self._process_events()
            
            # 3. 执行监管活动
            self._execute_regulatory_activities()
            
            # 4. 执行金融主体之间的交互
            self._execute_agent_interactions()
            
            # 5. 更新资产价格
            self._update_asset_prices()
            
            # 6. 结算和清算
            self._perform_settlement()
            
            # 7. 记录状态
            self._record_state()
        
        self.logger.info("金融市场模拟完成")
    
    def _update_market_state(self):
        """更新市场状态"""
        # 随机波动市场参数
        self.market_state["interest_rate"] += np.random.normal(0, 0.0005)
        self.market_state["interest_rate"] = max(0.001, self.market_state["interest_rate"])
        
        self.market_state["inflation_rate"] += np.random.normal(0, 0.0003)
        self.market_state["inflation_rate"] = max(0, self.market_state["inflation_rate"])
        
        self.market_state["market_volatility"] += np.random.normal(0, 0.001)
        self.market_state["market_volatility"] = max(0.01, self.market_state["market_volatility"])
        
        self.market_state["liquidity_factor"] += np.random.normal(0, 0.01)
        self.market_state["liquidity_factor"] = max(0.5, min(2.0, self.market_state["liquidity_factor"]))
        
        self.market_state["market_sentiment"] += np.random.normal(0, 0.05)
        self.market_state["market_sentiment"] = max(-1.0, min(1.0, self.market_state["market_sentiment"]))
        
        self.market_state["economic_growth"] += np.random.normal(0, 0.0002)
        
        self.market_state["unemployment_rate"] += np.random.normal(0, 0.0005)
        self.market_state["unemployment_rate"] = max(0.01, min(0.2, self.market_state["unemployment_rate"]))
        
        self.logger.debug(f"市场状态更新: {self.market_state}")
    
    def _process_events(self):
        """处理随机事件"""
        # 检查是否发生随机事件
        if random.random() < EVENT_PARAMS.get("random_event_probability", 0.05):
            event_type = random.choice([
                "economic_news",
                "political_event",
                "natural_disaster",
                "technology_breakthrough",
                "regulatory_change",
            ])
            
            event_magnitude = random.uniform(-0.1, 0.1)
            event_description = f"{event_type} (影响幅度: {event_magnitude:.2f})"
            
            self.events.append({
                "day": self.current_day,
                "date": self.current_date,
                "type": event_type,
                "magnitude": event_magnitude,
                "description": event_description,
            })
            
            # 根据事件类型和幅度更新市场状态
            if event_type == "economic_news":
                self.market_state["market_sentiment"] += event_magnitude * 2
                self.market_state["economic_growth"] += event_magnitude * 0.01
            elif event_type == "political_event":
                self.market_state["market_volatility"] += abs(event_magnitude) * 0.05
                self.market_state["market_sentiment"] += event_magnitude
            elif event_type == "natural_disaster":
                self.market_state["market_sentiment"] -= abs(event_magnitude) * 0.5
                self.market_state["economic_growth"] -= abs(event_magnitude) * 0.005
            elif event_type == "technology_breakthrough":
                self.market_state["market_sentiment"] += abs(event_magnitude)
                self.market_state["economic_growth"] += abs(event_magnitude) * 0.002
            elif event_type == "regulatory_change":
                self.market_state["market_volatility"] += event_magnitude * 0.02
            
            # 限制市场状态参数在合理范围内
            self.market_state["market_sentiment"] = max(-1.0, min(1.0, self.market_state["market_sentiment"]))
            self.market_state["market_volatility"] = max(0.01, self.market_state["market_volatility"])
            
            self.logger.info(f"事件发生: {event_description}")
    
    def _execute_regulatory_activities(self):
        """执行监管活动"""
        # 定期执行监管活动，如压力测试、报告等
        if self.current_day % REGULATORY_PARAMS.get("stress_test_frequency", 30) == 0:
            self.logger.info("执行压力测试")
            # 这里可以实现压力测试逻辑
        
        if self.current_day % REGULATORY_PARAMS.get("reporting_frequency", 90) == 0:
            self.logger.info("生成监管报告")
            # 这里可以实现报告生成逻辑
        
        # 中央银行根据经济状况调整利率
        if self.current_day % 30 == 0:  # 每30天调整一次
            central_bank = None
            for agent in self.agents.values():
                if agent.name == "中央银行":
                    central_bank = agent
                    break
            
            if central_bank:
                # 根据通胀率和经济增长调整利率
                if self.market_state["inflation_rate"] > 0.04:
                    # 通胀高，提高利率
                    rate_change = min(0.0025, (self.market_state["inflation_rate"] - 0.02) * 0.1)
                    self.market_state["interest_rate"] += rate_change
                    self.logger.info(f"中央银行提高利率 {rate_change:.4f}，当前利率: {self.market_state['interest_rate']:.4f}")
                elif self.market_state["economic_growth"] < 0.01:
                    # 经济增长低，降低利率
                    rate_change = min(0.0025, (0.02 - self.market_state["economic_growth"]) * 0.1)
                    self.market_state["interest_rate"] = max(0.001, self.market_state["interest_rate"] - rate_change)
                    self.logger.info(f"中央银行降低利率 {rate_change:.4f}，当前利率: {self.market_state['interest_rate']:.4f}")
    
    def _execute_agent_interactions(self):
        """执行金融主体之间的交互"""
        # 这里可以实现金融主体之间的交互逻辑
        # 例如，银行之间的拆借、投资者的交易等
        
        # 示例：随机选择一些金融主体进行交互
        num_interactions = min(10, len(self.agents) // 2)
        for _ in range(num_interactions):
            agent1 = random.choice(list(self.agents.values()))
            agent2 = random.choice([a for a in self.agents.values() if a.id != agent1.id])
            
            # 如果两个主体之间有连接，则可能进行交互
            if agent2 in agent1.connections:
                interaction_type = random.choice(["message", "transaction"])
                
                if interaction_type == "message":
                    # 消息交互
                    message = f"日期: {self.current_date.strftime('%Y-%m-%d')}, 市场状态: {self.market_state}"
                    # 在实际应用中，这里可以使用agent.send_message方法
                    self.logger.debug(f"{agent1.name} 向 {agent2.name} 发送消息")
                
                elif interaction_type == "transaction":
                    # 交易交互
                    if agent1.balance > 0:
                        amount = random.uniform(0, agent1.balance * 0.01)
                        success, result = agent1.transfer_funds(agent2, amount, "随机交易")
                        
                        if success:
                            self.transactions.append(result)
                            self.logger.debug(f"{agent1.name} 向 {agent2.name} 转账 {amount:.2f}")
    
    def _update_asset_prices(self):
        """更新资产价格"""
        # 使用当前日期的资产价格
        for asset_class in self.asset_prices:
            current_price = self.asset_prices[asset_class].iloc[self.current_day]
            
            # 根据市场状态调整价格
            sentiment_factor = 1.0 + self.market_state["market_sentiment"] * 0.01
            volatility_factor = 1.0 + (self.market_state["market_volatility"] - 0.15) * 0.1
            
            # 应用调整因子
            adjusted_price = current_price * sentiment_factor * volatility_factor
            
            # 更新价格
            self.asset_prices[asset_class].iloc[self.current_day] = adjusted_price
            
            self.logger.debug(f"{asset_class} 价格: {adjusted_price:.2f}")
    
    def _perform_settlement(self):
        """执行结算和清算"""
        # 这里可以实现日终结算和清算逻辑
        pass
    
    def _record_state(self):
        """记录当前状态"""
        # 这里可以实现状态记录逻辑，用于后续分析和可视化
        pass
    
    def get_simulation_results(self) -> Dict[str, Any]:
        """
        获取模拟结果
        
        Returns:
            模拟结果字典
        """
        return {
            "market_state": self.market_state,
            "asset_prices": self.asset_prices,
            "agents": {agent_id: agent.get_info() for agent_id, agent in self.agents.items()},
            "transactions": self.transactions,
            "events": self.events,
        }


if __name__ == "__main__":
    # 设置日志级别
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 创建并运行模拟
    simulation = MarketSimulation()
    simulation.run_simulation()
    
    # 获取并打印结果
    results = simulation.get_simulation_results()
    print(f"模拟完成，共记录了 {len(results['transactions'])} 笔交易和 {len(results['events'])} 个事件") 