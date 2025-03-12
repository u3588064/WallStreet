"""
可视化工具模块，用于可视化金融市场模拟结果
"""

import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import networkx as nx
from pyvis.network import Network
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

from config import VISUALIZATION_PARAMS


class MarketVisualizer:
    """金融市场可视化类，用于可视化模拟结果"""
    
    def __init__(self, results: Dict[str, Any], output_dir: str = "visualization_results"):
        """
        初始化可视化器
        
        Args:
            results: 模拟结果
            output_dir: 输出目录
        """
        self.results = results
        self.output_dir = output_dir
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 设置绘图样式
        plt.style.use(VISUALIZATION_PARAMS.get("plot_style", "ggplot"))
        self.figure_size = VISUALIZATION_PARAMS.get("figure_size", (12, 8))
        self.dpi = VISUALIZATION_PARAMS.get("dpi", 100)
        self.save_figures = VISUALIZATION_PARAMS.get("save_figures", True)
        self.figure_format = VISUALIZATION_PARAMS.get("figure_format", "png")
    
    def visualize_all(self):
        """生成所有可视化图表"""
        self.visualize_asset_prices()
        self.visualize_market_state()
        self.visualize_transactions()
        self.visualize_events()
        self.visualize_agent_network()
        self.visualize_agent_balances()
    
    def visualize_asset_prices(self):
        """可视化资产价格"""
        plt.figure(figsize=self.figure_size, dpi=self.dpi)
        
        for asset_class, prices in self.results["asset_prices"].items():
            plt.plot(prices.index, prices.values, label=asset_class)
        
        plt.title("资产价格走势")
        plt.xlabel("日期")
        plt.ylabel("价格")
        plt.legend()
        plt.grid(True)
        
        # 设置日期格式
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.gcf().autofmt_xdate()
        
        if self.save_figures:
            plt.savefig(os.path.join(self.output_dir, f"asset_prices.{self.figure_format}"))
        
        plt.close()
    
    def visualize_market_state(self):
        """可视化市场状态"""
        # 创建时间序列数据
        market_state = self.results["market_state"]
        
        # 绘制市场状态参数
        plt.figure(figsize=self.figure_size, dpi=self.dpi)
        
        for key, value in market_state.items():
            if isinstance(value, (int, float)):
                plt.plot([value], label=key)
        
        plt.title("当前市场状态")
        plt.ylabel("数值")
        plt.legend()
        plt.grid(True)
        
        if self.save_figures:
            plt.savefig(os.path.join(self.output_dir, f"market_state.{self.figure_format}"))
        
        plt.close()
    
    def visualize_transactions(self):
        """可视化交易"""
        transactions = self.results["transactions"]
        
        if not transactions:
            return
        
        # 提取交易数据
        amounts = [t["amount"] for t in transactions]
        timestamps = [t["timestamp"] for t in transactions]
        
        # 转换时间戳为日期
        dates = [datetime.fromisoformat(ts.replace("Z", "+00:00")) for ts in timestamps]
        
        # 绘制交易金额随时间的变化
        plt.figure(figsize=self.figure_size, dpi=self.dpi)
        plt.scatter(dates, amounts, alpha=0.6)
        plt.title("交易金额随时间的变化")
        plt.xlabel("日期")
        plt.ylabel("交易金额")
        plt.grid(True)
        
        # 设置日期格式
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.gcf().autofmt_xdate()
        
        if self.save_figures:
            plt.savefig(os.path.join(self.output_dir, f"transactions.{self.figure_format}"))
        
        plt.close()
        
        # 绘制交易金额分布
        plt.figure(figsize=self.figure_size, dpi=self.dpi)
        plt.hist(amounts, bins=30, alpha=0.7)
        plt.title("交易金额分布")
        plt.xlabel("交易金额")
        plt.ylabel("频率")
        plt.grid(True)
        
        if self.save_figures:
            plt.savefig(os.path.join(self.output_dir, f"transaction_distribution.{self.figure_format}"))
        
        plt.close()
    
    def visualize_events(self):
        """可视化事件"""
        events = self.results["events"]
        
        if not events:
            return
        
        # 提取事件数据
        event_types = [e["type"] for e in events]
        event_magnitudes = [e["magnitude"] for e in events]
        event_days = [e["day"] for e in events]
        
        # 绘制事件影响
        plt.figure(figsize=self.figure_size, dpi=self.dpi)
        
        # 为不同类型的事件使用不同颜色
        event_type_set = set(event_types)
        colors = plt.cm.tab10(np.linspace(0, 1, len(event_type_set)))
        color_map = {event_type: color for event_type, color in zip(event_type_set, colors)}
        
        for event_type, day, magnitude in zip(event_types, event_days, event_magnitudes):
            plt.scatter(day, magnitude, color=color_map[event_type], label=event_type, alpha=0.7)
        
        # 去除重复的图例
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())
        
        plt.title("事件影响")
        plt.xlabel("模拟天数")
        plt.ylabel("影响幅度")
        plt.grid(True)
        
        if self.save_figures:
            plt.savefig(os.path.join(self.output_dir, f"events.{self.figure_format}"))
        
        plt.close()
        
        # 绘制事件类型分布
        plt.figure(figsize=self.figure_size, dpi=self.dpi)
        event_type_counts = {event_type: event_types.count(event_type) for event_type in event_type_set}
        plt.bar(event_type_counts.keys(), event_type_counts.values(), alpha=0.7)
        plt.title("事件类型分布")
        plt.xlabel("事件类型")
        plt.ylabel("次数")
        plt.xticks(rotation=45)
        plt.grid(True)
        
        if self.save_figures:
            plt.savefig(os.path.join(self.output_dir, f"event_distribution.{self.figure_format}"))
        
        plt.close()
    
    def visualize_agent_network(self):
        """可视化金融主体网络"""
        agents = self.results["agents"]
        
        # 创建网络图
        G = nx.Graph()
        
        # 添加节点
        for agent_id, agent_info in agents.items():
            G.add_node(
                agent_id,
                name=agent_info["name"],
                type=agent_info["type"],
                balance=agent_info["balance"],
            )
        
        # 添加边
        for agent_id, agent_info in agents.items():
            for connection_name in agent_info["connections"]:
                # 查找连接的代理ID
                for other_id, other_info in agents.items():
                    if other_info["name"] == connection_name:
                        G.add_edge(agent_id, other_id)
                        break
        
        # 使用pyvis创建交互式网络图
        net = Network(
            height="800px",
            width="100%",
            bgcolor="#ffffff",
            font_color="black",
        )
        
        # 设置不同类型节点的颜色
        type_colors = {
            "regulators": "#ff9999",  # 红色
            "financial_institutions": "#99ff99",  # 绿色
            "market_infrastructure": "#9999ff",  # 蓝色
            "auxiliary_services": "#ffff99",  # 黄色
            "direct_participants": "#ff99ff",  # 粉色
            "international_organizations": "#99ffff",  # 青色
        }
        
        # 添加节点到pyvis网络
        for node_id in G.nodes():
            node_info = G.nodes[node_id]
            net.add_node(
                node_id,
                label=node_info["name"],
                title=f"类型: {node_info['type']}<br>余额: {node_info['balance']:,.2f}",
                color=type_colors.get(node_info["type"], "#cccccc"),
                size=10 + np.log1p(node_info["balance"]) * 0.01,  # 根据余额调整节点大小
            )
        
        # 添加边到pyvis网络
        for edge in G.edges():
            net.add_edge(edge[0], edge[1])
        
        # 保存交互式网络图
        net.save_graph(os.path.join(self.output_dir, "agent_network.html"))
        
        # 使用matplotlib绘制静态网络图
        plt.figure(figsize=self.figure_size, dpi=self.dpi)
        
        # 设置节点颜色
        node_colors = [type_colors.get(G.nodes[node_id]["type"], "#cccccc") for node_id in G.nodes()]
        
        # 设置节点大小
        node_sizes = [10 + np.log1p(G.nodes[node_id]["balance"]) * 0.01 for node_id in G.nodes()]
        
        # 使用spring布局
        pos = nx.spring_layout(G, seed=42)
        
        # 绘制网络
        nx.draw(
            G,
            pos,
            with_labels=False,
            node_color=node_colors,
            node_size=node_sizes,
            edge_color="#cccccc",
            alpha=0.8,
        )
        
        # 添加标签
        labels = {node_id: G.nodes[node_id]["name"] for node_id in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
        
        plt.title("金融主体网络")
        plt.axis("off")
        
        if self.save_figures:
            plt.savefig(os.path.join(self.output_dir, f"agent_network.{self.figure_format}"))
        
        plt.close()
    
    def visualize_agent_balances(self):
        """可视化金融主体余额"""
        agents = self.results["agents"]
        
        # 按类型分组
        agent_types = {}
        for agent_id, agent_info in agents.items():
            agent_type = agent_info["type"]
            if agent_type not in agent_types:
                agent_types[agent_type] = []
            agent_types[agent_type].append(agent_info)
        
        # 为每种类型创建一个图表
        for agent_type, agent_list in agent_types.items():
            plt.figure(figsize=self.figure_size, dpi=self.dpi)
            
            # 按余额排序
            agent_list.sort(key=lambda x: x["balance"], reverse=True)
            
            names = [agent["name"] for agent in agent_list]
            balances = [agent["balance"] for agent in agent_list]
            
            # 绘制条形图
            plt.bar(names, balances, alpha=0.7)
            plt.title(f"{agent_type} 余额")
            plt.xlabel("金融主体")
            plt.ylabel("余额")
            plt.xticks(rotation=45, ha="right")
            plt.grid(True)
            plt.tight_layout()
            
            if self.save_figures:
                plt.savefig(os.path.join(self.output_dir, f"{agent_type}_balances.{self.figure_format}"))
            
            plt.close()
        
        # 绘制所有金融主体的余额分布
        plt.figure(figsize=self.figure_size, dpi=self.dpi)
        
        all_balances = [agent_info["balance"] for agent_info in agents.values()]
        
        # 使用对数刻度
        plt.hist(all_balances, bins=30, alpha=0.7)
        plt.xscale("log")
        plt.title("所有金融主体余额分布")
        plt.xlabel("余额 (对数刻度)")
        plt.ylabel("频率")
        plt.grid(True)
        
        if self.save_figures:
            plt.savefig(os.path.join(self.output_dir, f"all_balances.{self.figure_format}"))
        
        plt.close()


if __name__ == "__main__":
    # 从文件加载模拟结果
    with open("simulation_results.json", "r") as f:
        results = json.load(f)
    
    # 创建可视化器并生成所有图表
    visualizer = MarketVisualizer(results)
    visualizer.visualize_all() 