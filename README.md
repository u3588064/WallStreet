# 金融市场模拟系统

这是一个基于 AutoGen 的金融市场多智能体模拟系统，模拟了现代金融市场中各类参与者之间的互动关系。

## 系统架构

系统包含以下主要组件：

1. 核心监管与政策机构（中央银行、监管机构、财政部）
2. 金融机构（商业银行、投资银行、基金公司等）
3. 市场基础设施（交易所、清算机构、支付系统）
4. 辅助服务机构（评级机构、会计师事务所、律师事务所）
5. 直接参与者（企业、个人投资者、做市商）
6. 国际机构（IMF、世界银行、BIS）

## 安装要求

```bash
pip install -r requirements.txt
```

## 配置说明

1. 创建 `OAI_CONFIG_LIST` 文件，配置 OpenAI API 密钥
2. 根据需要在 `config.py` 中调整市场参与者配置
3. 在 `main.py` 中定义模拟场景

## 使用方法

1. 配置环境：
```bash
# 创建并激活虚拟环境（可选）
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

2. 运行模拟：
```bash
python main.py
```

## 示例场景

系统预置了三个示例场景：

1. 利率调整影响模拟
2. 新股IPO流程模拟
3. 金融风险防控模拟

## 自定义场景

可以通过修改 `main.py` 中的 `scenarios` 列表来添加新的模拟场景。每个场景应该包含清晰的步骤和预期的市场参与者互动过程。

## 注意事项

1. 需要有效的 OpenAI API 密钥
2. 建议在测试环境中先进行小规模模拟
3. 模拟过程中的对话轮次可以在 `agents.py` 中调整

## 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 许可证

MIT License 
