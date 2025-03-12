import autogen
from agents import user_proxy, manager, create_market_agents
from config import MARKET_PARTICIPANTS

def simulate_market_scenario(scenario):
    """模拟特定的市场场景"""
    print(f"开始模拟场景: {scenario}")
    
    # 初始化对话
    user_proxy.initiate_chat(
        manager,
        message=scenario
    )

def main():
    # 创建所有市场代理
    market_agents = create_market_agents()
    
    # 示例场景
    scenarios = [
        """模拟中央银行调整利率对金融市场的影响：
        1. 中央银行宣布加息0.25%
        2. 商业银行调整存贷款利率
        3. 企业和个人投资者作出反应
        4. 金融市场各方进行相应调整""",
        
        """模拟新股IPO过程：
        1. 企业申请IPO
        2. 投资银行开展尽职调查
        3. 监管机构审核
        4. 证券交易所安排上市""",
        
        """模拟金融风险防控：
        1. 评级机构发现某金融机构风险
        2. 监管机构介入调查
        3. 市场各方反应
        4. 风险处置方案"""
    ]
    
    # 运行模拟场景
    for scenario in scenarios:
        simulate_market_scenario(scenario)
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main() 