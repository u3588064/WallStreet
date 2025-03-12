import autogen

# 配置基础设置
config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4"],
    },
)

# 定义市场参与者配置
MARKET_PARTICIPANTS = {
    # 1. 核心监管与政策机构
    "central_bank": {
        "name": "中央银行",
        "functions": ["货币政策", "利率调控", "市场监管"],
        "type": "regulatory"
    },
    "financial_regulator": {
        "name": "金融监管机构",
        "functions": ["市场监管", "风险防控", "政策制定"],
        "type": "regulatory"
    },
    "treasury": {
        "name": "财政部",
        "functions": ["国债发行", "财政政策", "预算管理"],
        "type": "regulatory"
    },

    # 2. 金融机构
    "commercial_bank": {
        "name": "商业银行",
        "functions": ["存款业务", "贷款业务", "结算服务"],
        "type": "financial_institution"
    },
    "investment_bank": {
        "name": "投资银行",
        "functions": ["证券承销", "并购咨询", "资产管理"],
        "type": "financial_institution"
    },
    "mutual_fund": {
        "name": "公募基金",
        "functions": ["基金管理", "投资组合", "风险控制"],
        "type": "financial_institution"
    },
    "private_fund": {
        "name": "私募基金",
        "functions": ["另类投资", "股权投资", "量化交易"],
        "type": "financial_institution"
    },

    # 3. 市场基础设施
    "stock_exchange": {
        "name": "证券交易所",
        "functions": ["证券交易", "市场监管", "信息披露"],
        "type": "infrastructure"
    },
    "clearing_house": {
        "name": "清算机构",
        "functions": ["清算结算", "风险管理", "担保交收"],
        "type": "infrastructure"
    },
    "payment_system": {
        "name": "支付系统",
        "functions": ["支付结算", "清算服务", "跨境支付"],
        "type": "infrastructure"
    },

    # 4. 辅助服务机构
    "rating_agency": {
        "name": "评级机构",
        "functions": ["信用评级", "风险评估", "市场研究"],
        "type": "service"
    },
    "accounting_firm": {
        "name": "会计师事务所",
        "functions": ["审计", "财务咨询", "尽职调查"],
        "type": "service"
    },
    "law_firm": {
        "name": "律师事务所",
        "functions": ["法律咨询", "合规审查", "争议解决"],
        "type": "service"
    },

    # 5. 直接参与者
    "corporation": {
        "name": "企业",
        "functions": ["融资", "投资", "风险管理"],
        "type": "participant"
    },
    "individual_investor": {
        "name": "个人投资者",
        "functions": ["证券投资", "基金投资", "理财规划"],
        "type": "participant"
    },
    "market_maker": {
        "name": "做市商",
        "functions": ["报价", "流动性提供", "风险对冲"],
        "type": "participant"
    },

    # 6. 国际机构
    "imf": {
        "name": "国际货币基金组织",
        "functions": ["国际监管", "政策协调", "金融援助"],
        "type": "international"
    },
    "world_bank": {
        "name": "世界银行",
        "functions": ["发展援助", "技术支持", "政策研究"],
        "type": "international"
    },
    "bis": {
        "name": "国际清算银行",
        "functions": ["国际清算", "政策协调", "研究分析"],
        "type": "international"
    }
}

# 定义市场参与者之间的互动规则
INTERACTION_RULES = {
    "regulatory": {
        "can_regulate": ["financial_institution", "infrastructure", "participant"],
        "can_cooperate": ["regulatory", "international"],
        "can_monitor": ["all"]
    },
    "financial_institution": {
        "can_serve": ["participant"],
        "can_trade_with": ["financial_institution", "participant"],
        "must_comply": ["regulatory", "international"]
    },
    "infrastructure": {
        "can_serve": ["all"],
        "must_comply": ["regulatory", "international"]
    },
    "service": {
        "can_serve": ["all"],
        "must_comply": ["regulatory"]
    },
    "participant": {
        "can_trade_with": ["financial_institution", "participant"],
        "must_comply": ["regulatory"]
    },
    "international": {
        "can_regulate": ["regulatory"],
        "can_monitor": ["all"]
    }
}
