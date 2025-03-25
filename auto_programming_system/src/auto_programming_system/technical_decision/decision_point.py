"""决策点定义模块

此模块定义了技术决策系统中的决策点类型和结构。
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime

@dataclass
class DecisionPoint:
    """决策点类
    
    表示一个需要做出技术决策的点，包含决策点的类型、描述、约束条件等信息。
    """
    
    id: str
    type: str
    description: str
    confidence: float
    constraints: Dict[str, Any]
    dependencies: List[str]
    created_at: datetime
    updated_at: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """将决策点转换为字典格式"""
        return {
            "id": self.id,
            "type": self.type,
            "description": self.description,
            "confidence": self.confidence,
            "constraints": self.constraints,
            "dependencies": self.dependencies,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DecisionPoint':
        """从字典创建决策点实例"""
        return cls(
            id=data["id"],
            type=data["type"],
            description=data["description"],
            confidence=data["confidence"],
            constraints=data["constraints"],
            dependencies=data["dependencies"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"])
        )

class DecisionPointType:
    """决策点类型定义"""
    
    DATA_PROCESSING = "data_processing"
    STORAGE = "storage"
    PERFORMANCE = "performance"
    SECURITY = "security"
    SCALABILITY = "scalability"
    
    @classmethod
    def get_all_types(cls) -> List[str]:
        """获取所有决策点类型"""
        return [
            cls.DATA_PROCESSING,
            cls.STORAGE,
            cls.PERFORMANCE,
            cls.SECURITY,
            cls.SCALABILITY
        ]
    
    @classmethod
    def get_type_keywords(cls) -> Dict[str, List[str]]:
        """获取每种类型的关键词"""
        return {
            cls.DATA_PROCESSING: [
                "处理", "计算", "分析", "转换", "过滤",
                "process", "compute", "analyze", "transform", "filter"
            ],
            cls.STORAGE: [
                "存储", "保存", "数据库", "文件", "缓存",
                "store", "save", "database", "file", "cache"
            ],
            cls.PERFORMANCE: [
                "性能", "速度", "优化", "效率", "延迟",
                "performance", "speed", "optimize", "efficiency", "latency"
            ],
            cls.SECURITY: [
                "安全", "加密", "认证", "授权", "保护",
                "security", "encrypt", "authenticate", "authorize", "protect"
            ],
            cls.SCALABILITY: [
                "扩展", "并发", "负载", "分布式", "集群",
                "scale", "concurrent", "load", "distributed", "cluster"
            ]
        }
    
    @classmethod
    def get_type_description(cls, type_name: str) -> str:
        """获取决策点类型的描述"""
        descriptions = {
            cls.DATA_PROCESSING: "数据处理相关的技术决策，包括数据清洗、转换、分析等",
            cls.STORAGE: "数据存储相关的技术决策，包括数据库选择、文件存储、缓存策略等",
            cls.PERFORMANCE: "性能优化相关的技术决策，包括算法优化、并发处理、资源利用等",
            cls.SECURITY: "安全性相关的技术决策，包括加密算法、认证方式、访问控制等",
            cls.SCALABILITY: "可扩展性相关的技术决策，包括架构设计、负载均衡、分布式处理等"
        }
        return descriptions.get(type_name, "未知的决策点类型") 