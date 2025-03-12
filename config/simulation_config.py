"""
模拟配置模块，定义金融市场模拟的参数
"""

from typing import Dict, Any, List

# LLM配置
LLM_CONFIG = {
    "config_list": [
        {
            "model": "gpt-4",
            "api_key": "YOUR_API_KEY_HERE",
        }
    ],
    "temperature": 0.7,
    "max_tokens": 1500,
}

# 模拟参数
SIMULATION_PARAMS = {
    "simulation_days": 252,  # 一年交易日
    "time_step": "day",  # 时间步长
    "initial_date": "2023-01-01",  # 初始日期
    "random_seed": 42,  # 随机种子
    "log_level": "INFO",  # 日志级别
}

# 市场参数
MARKET_PARAMS = {
    "interest_rate": 0.02,  # 基准利率
    "inflation_rate": 0.03,  # 通胀率
    "market_volatility": 0.15,  # 市场波动率
    "liquidity_factor": 1.0,  # 流动性因子
}

# 资产类别
ASSET_CLASSES = {
    "stocks": {
        "volatility": 0.2,
        "expected_return": 0.08,
        "correlation_with_market": 0.8,
    },
    "bonds": {
        "volatility": 0.05,
        "expected_return": 0.03,
        "correlation_with_market": 0.3,
    },
    "commodities": {
        "volatility": 0.25,
        "expected_return": 0.06,
        "correlation_with_market": 0.5,
    },
    "real_estate": {
        "volatility": 0.15,
        "expected_return": 0.07,
        "correlation_with_market": 0.6,
    },
    "crypto": {
        "volatility": 0.8,
        "expected_return": 0.15,
        "correlation_with_market": 0.2,
    },
}

# 监管参数
REGULATORY_PARAMS = {
    "capital_requirement": 0.08,  # 资本充足率要求
    "leverage_limit": 10.0,  # 杠杆率限制
    "liquidity_requirement": 0.1,  # 流动性要求
    "stress_test_frequency": 30,  # 压力测试频率（天）
    "reporting_frequency": 90,  # 报告频率（天）
}

# 事件参数
EVENT_PARAMS = {
    "random_event_probability": 0.05,  # 随机事件概率
    "market_shock_probability": 0.02,  # 市场冲击概率
    "policy_change_probability": 0.01,  # 政策变化概率
    "natural_disaster_probability": 0.005,  # 自然灾害概率
    "technology_breakthrough_probability": 0.008,  # 技术突破概率
}

# 代理参数
AGENT_PARAMS = {
    "max_consecutive_auto_reply": 10,
    "human_input_mode": "NEVER",
    "memory_size": 100,  # 记忆大小
}

# 可视化参数
VISUALIZATION_PARAMS = {
    "plot_style": "ggplot",
    "figure_size": (12, 8),
    "dpi": 100,
    "save_figures": True,
    "figure_format": "png",
}

# 金融主体配置
FINANCIAL_ENTITIES = {
    # 1. 核心监管与政策机构
    "regulators": [
        {
            "name": "中央银行",
            "description": "负责货币政策、金融稳定和支付系统监管",
            "initial_balance": 1000000000000.0,
            "policy_tools": ["利率调整", "公开市场操作", "存款准备金率"],
        },
        {
            "name": "证券监管委员会",
            "description": "负责证券市场监管、投资者保护和市场透明度",
            "initial_balance": 10000000000.0,
            "policy_tools": ["市场监管", "信息披露要求", "反欺诈调查"],
        },
        {
            "name": "财政部",
            "description": "负责财政政策、国债发行和政府预算",
            "initial_balance": 5000000000000.0,
            "policy_tools": ["财政支出", "税收政策", "国债发行"],
        },
    ],
    
    # 2. 金融机构
    "financial_institutions": [
        {
            "name": "大型商业银行",
            "description": "提供存款、贷款和支付服务的大型银行",
            "initial_balance": 500000000000.0,
            "services": ["存款", "贷款", "支付结算", "外汇"],
            "risk_profile": "低",
        },
        {
            "name": "投资银行",
            "description": "提供证券承销、并购咨询和自营交易服务",
            "initial_balance": 100000000000.0,
            "services": ["证券承销", "并购咨询", "自营交易", "资产管理"],
            "risk_profile": "中高",
        },
        {
            "name": "公募基金管理公司",
            "description": "管理面向公众的开放式和封闭式基金",
            "initial_balance": 50000000000.0,
            "services": ["基金管理", "投资咨询", "资产配置"],
            "risk_profile": "中",
        },
        {
            "name": "对冲基金",
            "description": "采用多种策略追求绝对收益的私募基金",
            "initial_balance": 20000000000.0,
            "services": ["另类投资", "多策略交易", "杠杆投资"],
            "risk_profile": "高",
        },
        {
            "name": "保险公司",
            "description": "提供各类保险产品和服务",
            "initial_balance": 200000000000.0,
            "services": ["寿险", "财险", "再保险", "养老金管理"],
            "risk_profile": "中低",
        },
        {
            "name": "信托公司",
            "description": "提供信托服务和资产管理",
            "initial_balance": 30000000000.0,
            "services": ["信托计划", "资产管理", "财富管理"],
            "risk_profile": "中",
        },
        {
            "name": "大型资产管理公司",
            "description": "管理多种资产类别的大型资产管理公司",
            "initial_balance": 300000000000.0,
            "services": ["资产管理", "投资咨询", "风险管理"],
            "risk_profile": "中",
        },
        {
            "name": "养老基金",
            "description": "管理退休金和养老金的机构",
            "initial_balance": 400000000000.0,
            "services": ["养老金管理", "长期投资", "退休规划"],
            "risk_profile": "低",
        },
        {
            "name": "期货公司",
            "description": "提供期货和衍生品交易服务",
            "initial_balance": 10000000000.0,
            "services": ["期货交易", "风险管理", "商品交易"],
            "risk_profile": "高",
        },
    ],
    
    # 3. 市场基础设施
    "market_infrastructure": [
        {
            "name": "证券交易所",
            "description": "提供证券交易平台和市场监管",
            "initial_balance": 50000000000.0,
            "services": ["交易撮合", "市场监管", "信息披露"],
        },
        {
            "name": "清算结算机构",
            "description": "负责证券交易的清算和结算",
            "initial_balance": 20000000000.0,
            "services": ["清算", "结算", "存管", "风险管理"],
        },
        {
            "name": "支付系统",
            "description": "提供支付和资金转移服务",
            "initial_balance": 10000000000.0,
            "services": ["支付处理", "资金清算", "跨境支付"],
        },
        {
            "name": "金融信息平台",
            "description": "提供金融市场数据和信息服务",
            "initial_balance": 5000000000.0,
            "services": ["市场数据", "新闻资讯", "分析工具"],
        },
    ],
    
    # 4. 辅助服务机构
    "auxiliary_services": [
        {
            "name": "信用评级机构",
            "description": "评估企业和债券的信用风险",
            "initial_balance": 2000000000.0,
            "services": ["信用评级", "风险评估", "市场研究"],
        },
        {
            "name": "会计师事务所",
            "description": "提供审计和财务报告服务",
            "initial_balance": 3000000000.0,
            "services": ["审计", "财务报告", "税务咨询"],
        },
        {
            "name": "律师事务所",
            "description": "提供法律咨询和合规服务",
            "initial_balance": 2500000000.0,
            "services": ["法律咨询", "合规审查", "诉讼支持"],
        },
        {
            "name": "金融科技公司",
            "description": "提供金融技术解决方案",
            "initial_balance": 5000000000.0,
            "services": ["支付技术", "区块链", "量化交易工具"],
        },
    ],
    
    # 5. 直接参与者
    "direct_participants": [
        {
            "name": "大型企业",
            "description": "大型企业，发行股票和债券融资",
            "initial_balance": 10000000000.0,
            "sector": "科技",
            "credit_rating": "AA",
        },
        {
            "name": "中型企业",
            "description": "中型企业，主要通过银行贷款融资",
            "initial_balance": 1000000000.0,
            "sector": "制造业",
            "credit_rating": "BBB",
        },
        {
            "name": "小型企业",
            "description": "小型企业，依赖银行贷款和风险投资",
            "initial_balance": 100000000.0,
            "sector": "服务业",
            "credit_rating": "BB",
        },
        {
            "name": "个人投资者",
            "description": "普通散户投资者",
            "initial_balance": 1000000.0,
            "risk_preference": "中",
            "investment_horizon": "中长期",
        },
        {
            "name": "高净值客户",
            "description": "拥有大量资产的高净值个人",
            "initial_balance": 50000000.0,
            "risk_preference": "中高",
            "investment_horizon": "长期",
        },
        {
            "name": "做市商",
            "description": "提供市场流动性和报价的机构",
            "initial_balance": 5000000000.0,
            "markets": ["股票", "债券", "外汇"],
            "trading_strategy": "做市",
        },
        {
            "name": "高频交易公司",
            "description": "使用算法进行高频交易的公司",
            "initial_balance": 2000000000.0,
            "markets": ["股票", "期货", "期权"],
            "trading_strategy": "高频套利",
        },
    ],
    
    # 6. 国际机构
    "international_organizations": [
        {
            "name": "国际货币基金组织",
            "description": "促进全球货币合作和金融稳定",
            "initial_balance": 1000000000000.0,
            "functions": ["国际收支平衡", "汇率稳定", "经济政策建议"],
        },
        {
            "name": "世界银行",
            "description": "提供发展中国家金融和技术援助",
            "initial_balance": 500000000000.0,
            "functions": ["减贫", "可持续发展", "基础设施建设"],
        },
        {
            "name": "国际清算银行",
            "description": "促进中央银行合作和金融稳定",
            "initial_balance": 300000000000.0,
            "functions": ["中央银行合作", "金融研究", "国际标准制定"],
        },
    ],
} 