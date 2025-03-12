"""
基础代理类模块，定义所有金融主体的基类
"""

import autogen
from typing import Dict, List, Any, Optional, Callable
import uuid


class FinancialAgent:
    """金融主体基类，所有金融主体都继承自此类"""
    
    def __init__(
        self,
        name: str,
        agent_type: str,
        description: str,
        llm_config: Optional[Dict[str, Any]] = None,
        system_message: Optional[str] = None,
        human_input_mode: str = "NEVER",
        max_consecutive_auto_reply: Optional[int] = None,
        is_termination_msg: Optional[Callable[[Dict[str, Any]], bool]] = None,
        code_execution_config: Optional[Dict[str, Any]] = None,
    ):
        """
        初始化金融主体
        
        Args:
            name: 主体名称
            agent_type: 主体类型
            description: 主体描述
            llm_config: LLM配置
            system_message: 系统消息
            human_input_mode: 人类输入模式
            max_consecutive_auto_reply: 最大连续自动回复次数
            is_termination_msg: 终止消息判断函数
            code_execution_config: 代码执行配置
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.agent_type = agent_type
        self.description = description
        
        # 创建AutoGen代理
        if system_message is None:
            system_message = f"""
            你是{name}，一个{agent_type}。
            {description}
            
            你应该根据你的角色和职责行事，考虑实际金融市场中的规则和限制。
            """
        
        self.agent = autogen.AssistantAgent(
            name=name,
            system_message=system_message,
            llm_config=llm_config,
            human_input_mode=human_input_mode,
            max_consecutive_auto_reply=max_consecutive_auto_reply,
            is_termination_msg=is_termination_msg,
            code_execution_config=code_execution_config,
        )
        
        # 状态和属性
        self.balance = 0.0  # 资金余额
        self.assets = {}  # 资产
        self.liabilities = {}  # 负债
        self.connections = []  # 与其他主体的连接
        self.transaction_history = []  # 交易历史
        self.regulatory_status = "compliant"  # 监管状态
        
    def send_message(self, recipient, message: str, sender=None):
        """向其他主体发送消息"""
        if sender is None:
            sender = self.agent
        return self.agent.send(message, recipient.agent, sender=sender)
    
    def add_connection(self, other_agent):
        """添加与其他主体的连接"""
        if other_agent not in self.connections:
            self.connections.append(other_agent)
            # 如果对方还没有与自己建立连接，则建立双向连接
            if self not in other_agent.connections:
                other_agent.add_connection(self)
    
    def transfer_funds(self, recipient, amount: float, description: str = ""):
        """转账给其他主体"""
        if amount <= 0:
            return False, "转账金额必须为正数"
        
        if self.balance < amount:
            return False, "余额不足"
        
        # 执行转账
        self.balance -= amount
        recipient.balance += amount
        
        # 记录交易
        transaction = {
            "from": self.id,
            "to": recipient.id,
            "amount": amount,
            "description": description,
            "timestamp": autogen.get_utc_time(),
        }
        
        self.transaction_history.append(transaction)
        recipient.transaction_history.append(transaction)
        
        return True, transaction
    
    def update_state(self, **kwargs):
        """更新主体状态"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def get_info(self):
        """获取主体信息"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.agent_type,
            "description": self.description,
            "balance": self.balance,
            "assets": self.assets,
            "liabilities": self.liabilities,
            "connections": [conn.name for conn in self.connections],
            "regulatory_status": self.regulatory_status,
        }
    
    def __str__(self):
        return f"{self.name} ({self.agent_type})"
    
    def __repr__(self):
        return self.__str__() 