"""
金融市场模拟系统主程序入口
"""

import os
import logging
import json
import argparse
from datetime import datetime
import autogen

from market_simulation import MarketSimulation
from visualization import MarketVisualizer
from config import LLM_CONFIG


def setup_logging(log_level="INFO", log_file=None):
    """
    设置日志
    
    Args:
        log_level: 日志级别
        log_file: 日志文件路径
    """
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"无效的日志级别: {log_level}")
    
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    if log_file:
        logging.basicConfig(
            level=numeric_level,
            format=log_format,
            filename=log_file,
            filemode='w'
        )
        # 同时输出到控制台
        console = logging.StreamHandler()
        console.setLevel(numeric_level)
        console.setFormatter(logging.Formatter(log_format))
        logging.getLogger('').addHandler(console)
    else:
        logging.basicConfig(
            level=numeric_level,
            format=log_format
        )


def save_results(results, output_dir="results"):
    """
    保存模拟结果
    
    Args:
        results: 模拟结果
        output_dir: 输出目录
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 将结果转换为可序列化的格式
    serializable_results = {
        "market_state": results["market_state"],
        "asset_prices": {k: v.to_dict() for k, v in results["asset_prices"].items()},
        "agents": results["agents"],
        "transactions": results["transactions"],
        "events": results["events"],
    }
    
    # 保存为JSON文件
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"simulation_results_{timestamp}.json")
    
    with open(output_file, 'w') as f:
        json.dump(serializable_results, f, indent=2)
    
    logging.info(f"模拟结果已保存到 {output_file}")
    
    return output_file


def run_simulation(args):
    """
    运行模拟
    
    Args:
        args: 命令行参数
    """
    # 设置日志
    setup_logging(args.log_level, args.log_file)
    
    # 创建并运行模拟
    simulation = MarketSimulation()
    simulation.run_simulation()
    
    # 获取结果
    results = simulation.get_simulation_results()
    
    # 保存结果
    output_file = save_results(results, args.output_dir)
    
    # 可视化结果
    if args.visualize:
        visualizer = MarketVisualizer(results, os.path.join(args.output_dir, "visualization"))
        visualizer.visualize_all()
        logging.info(f"可视化结果已保存到 {os.path.join(args.output_dir, 'visualization')}")


def run_agent_conversation(args):
    """
    运行代理对话
    
    Args:
        args: 命令行参数
    """
    # 设置日志
    setup_logging(args.log_level, args.log_file)
    
    # 配置LLM
    config_list = LLM_CONFIG["config_list"]
    
    # 创建用户代理
    user_proxy = autogen.UserProxyAgent(
        name="用户",
        human_input_mode="TERMINATE",
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={"work_dir": "agent_workspace"},
        llm_config={"config_list": config_list},
    )
    
    # 创建金融市场专家代理
    market_expert = autogen.AssistantAgent(
        name="金融市场专家",
        system_message="""你是一位金融市场专家，精通各类金融主体、市场机制和金融产品。
你可以解释金融市场的运作原理，分析不同金融主体之间的关系，并提供关于金融市场的专业见解。
请基于你的专业知识回答用户的问题，并在必要时提供详细的解释和例子。""",
        llm_config={"config_list": config_list},
    )
    
    # 创建中央银行代理
    central_bank = autogen.AssistantAgent(
        name="中央银行",
        system_message="""你是中央银行，负责制定和执行货币政策，维护金融稳定，监管支付系统。
你的主要工具包括利率调整、公开市场操作和存款准备金率调整。
请从中央银行的角度回答问题，考虑货币政策、金融稳定和经济增长的平衡。""",
        llm_config={"config_list": config_list},
    )
    
    # 创建商业银行代理
    commercial_bank = autogen.AssistantAgent(
        name="商业银行",
        system_message="""你是一家大型商业银行，提供存款、贷款和支付结算服务。
你的主要业务包括吸收存款、发放贷款、支付结算和外汇业务。
请从商业银行的角度回答问题，考虑盈利能力、风险管理和监管合规。""",
        llm_config={"config_list": config_list},
    )
    
    # 创建投资者代理
    investor = autogen.AssistantAgent(
        name="投资者",
        system_message="""你是一位投资者，关注各类投资机会和市场动态。
你的投资组合可能包括股票、债券、基金和其他金融产品。
请从投资者的角度回答问题，考虑风险收益、资产配置和市场趋势。""",
        llm_config={"config_list": config_list},
    )
    
    # 创建监管机构代理
    regulator = autogen.AssistantAgent(
        name="监管机构",
        system_message="""你是金融监管机构，负责监管金融市场和金融机构，保护投资者权益，维护市场秩序。
你的主要职责包括制定监管规则、监督市场参与者、调查违规行为和处理投诉。
请从监管机构的角度回答问题，考虑市场公平、投资者保护和系统性风险。""",
        llm_config={"config_list": config_list},
    )
    
    # 根据用户选择的代理类型启动对话
    if args.agent_type == "market_expert":
        user_proxy.initiate_chat(market_expert, message=args.initial_message or "请介绍一下金融市场的主要参与者及其作用。")
    elif args.agent_type == "central_bank":
        user_proxy.initiate_chat(central_bank, message=args.initial_message or "作为中央银行，你如何通过货币政策影响经济？")
    elif args.agent_type == "commercial_bank":
        user_proxy.initiate_chat(commercial_bank, message=args.initial_message or "作为商业银行，你如何管理资产负债和流动性风险？")
    elif args.agent_type == "investor":
        user_proxy.initiate_chat(investor, message=args.initial_message or "作为投资者，你如何构建一个多元化的投资组合？")
    elif args.agent_type == "regulator":
        user_proxy.initiate_chat(regulator, message=args.initial_message or "作为监管机构，你如何防范系统性金融风险？")
    elif args.agent_type == "group_chat":
        # 创建群聊
        groupchat = autogen.GroupChat(
            agents=[user_proxy, market_expert, central_bank, commercial_bank, investor, regulator],
            messages=[],
            max_round=50,
        )
        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})
        
        user_proxy.initiate_chat(
            manager,
            message=args.initial_message or "让我们讨论一下当前的金融市场状况和各方的看法。"
        )
    else:
        logging.error(f"未知的代理类型: {args.agent_type}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="金融市场模拟系统")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # 模拟子命令
    simulate_parser = subparsers.add_parser("simulate", help="运行金融市场模拟")
    simulate_parser.add_argument("--output-dir", default="results", help="输出目录")
    simulate_parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="日志级别")
    simulate_parser.add_argument("--log-file", help="日志文件路径")
    simulate_parser.add_argument("--visualize", action="store_true", help="是否生成可视化结果")
    
    # 代理对话子命令
    agent_parser = subparsers.add_parser("agent", help="运行代理对话")
    agent_parser.add_argument("--agent-type", default="market_expert", choices=["market_expert", "central_bank", "commercial_bank", "investor", "regulator", "group_chat"], help="代理类型")
    agent_parser.add_argument("--initial-message", help="初始消息")
    agent_parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="日志级别")
    agent_parser.add_argument("--log-file", help="日志文件路径")
    agent_parser.add_argument("--output-dir", default="agent_results", help="输出目录")
    
    args = parser.parse_args()
    
    if args.command == "simulate":
        run_simulation(args)
    elif args.command == "agent":
        run_agent_conversation(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 