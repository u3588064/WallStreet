# 金融市场模拟系统

这个项目使用AutoGen框架模拟了一个完整的金融市场生态系统，类似于斯坦福小镇项目的交互方式。该系统模拟了各类金融主体之间的交互和市场运作机制。

## 项目结构

```
financial_market_simulation/
├── agents/                      # 各类金融主体代理
│   ├── regulators/              # 监管与政策机构
│   ├── financial_institutions/  # 金融机构
│   ├── market_infrastructure/   # 市场基础设施
│   ├── auxiliary_services/      # 辅助服务机构
│   ├── direct_participants/     # 直接参与者
│   └── international_organizations/ # 国际机构
├── config/                      # 配置文件
├── utils/                       # 工具函数
├── main.py                      # 主程序入口
├── market_simulation.py         # 市场模拟核心逻辑
├── visualization.py             # 可视化工具
└── requirements.txt             # 项目依赖
```

## 金融主体

本项目模拟了以下金融主体：

### 1. 核心监管与政策机构
- 中央银行（如美联储、中国人民银行）
- 金融监管机构（如证监会、银保监会、金融稳定委员会）
- 财政部（国债发行、财政政策）

### 2. 金融机构（资金中介）
- 商业银行（吸收存款、发放贷款、支付结算）
- 投资银行/券商（证券承销、并购咨询、自营交易）
- 公募基金（面向公众的开放式/封闭式基金）
- 私募基金（对冲基金、PE/VC、量化基金）
- 保险公司（寿险、财险、再保险）
- 信托公司（资产管理、信托计划）
- 资产管理公司（如黑石、贝莱德）
- 养老基金（社保基金、企业年金）
- 期货公司（衍生品交易、风险管理）

### 3. 市场基础设施
- 证券交易所（如NYSE、上交所、深交所）
- 清算结算机构（如中央结算公司、DTCC）
- 支付系统（SWIFT、支付宝、银联）
- 金融信息平台（Bloomberg、Reuters）

### 4. 辅助服务机构
- 信用评级机构（标普、穆迪、惠誉）
- 会计师事务所（审计、财务报告）
- 律师事务所（合规审查、IPO法律支持）
- 金融科技公司（支付、区块链、量化工具）

### 5. 直接参与者
- 企业（发行股票/债券、资金管理）
- 个人投资者（散户、高净值客户）
- 做市商（提供流动性、报价）
- 高频交易公司（算法交易、套利）

### 6. 国际机构
- 国际货币基金组织（IMF）
- 世界银行
- 国际清算银行（BIS）

## 安装与运行

1. 克隆仓库
```bash
git clone https://github.com/yourusername/financial_market_simulation.git
cd financial_market_simulation
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行模拟
```bash
python main.py
```

## 使用方法

详细的使用说明和示例将在项目完成后提供。

## 许可证

MIT 