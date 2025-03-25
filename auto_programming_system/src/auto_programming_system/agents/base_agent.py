from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseAgent(ABC):
    """基础代理类，定义所有代理都需要实现的基本接口"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化代理
        
        Args:
            config: 代理配置信息
        """
        self.config = config or {}
        self.context = {}
        
    @abstractmethod
    async def process(self, input_data: Any) -> Any:
        """
        处理输入数据
        
        Args:
            input_data: 输入数据
            
        Returns:
            处理结果
        """
        pass
    
    @abstractmethod
    async def update_context(self, new_context: Dict[str, Any]) -> None:
        """
        更新代理上下文
        
        Args:
            new_context: 新的上下文信息
        """
        pass
    
    def get_context(self) -> Dict[str, Any]:
        """
        获取当前上下文
        
        Returns:
            当前上下文信息
        """
        return self.context.copy()
    
    def clear_context(self) -> None:
        """清除当前上下文"""
        self.context.clear() 