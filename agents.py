import autogen
from config import MARKET_PARTICIPANTS, INTERACTION_RULES, config_list

class FinancialAgent:
    def __init__(self, agent_type, name, functions):
        self.agent_type = agent_type
        self.name = name
        self.functions = functions
        self.agent = self._create_agent()

    def _create_agent(self):
        return autogen.AssistantAgent(
            name=self.name,
            system_message=f"""你是{self.name}，一个{self.agent_type}类型的金融市场参与者。
            你的主要职能包括：{', '.join(self.functions)}
            你必须遵守相关监管规则和市场规范。""",
            llm_config={"config_list": config_list}
        )

def create_market_agents():
    """创建所有市场参与者的代理"""
    agents = {}
    for key, info in MARKET_PARTICIPANTS.items():
        agents[key] = FinancialAgent(
            agent_type=info["type"],
            name=info["name"],
            functions=info["functions"]
        )
    return agents

# 创建用户代理（作为市场观察者和交互发起者）
user_proxy = autogen.UserProxyAgent(
    name="市场观察者",
    system_message="你是金融市场的观察者，可以与任何市场参与者进行交互和对话。",
    human_input_mode="TERMINATE",
    code_execution_config={"work_dir": "financial_market"}
)

# 创建群聊管理器
groupchat = autogen.GroupChat(
    agents=[user_proxy] + [agent.agent for agent in create_market_agents().values()],
    messages=[],
    max_round=50
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config={"config_list": config_list}
) 