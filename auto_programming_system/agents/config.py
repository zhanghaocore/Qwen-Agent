from typing import Dict, Any

# 需求理解代理配置
REQUIREMENT_AGENT_CONFIG: Dict[str, Any] = {
    "model": "qwen-agent",
    "temperature": 0.7,
    "max_tokens": 2000,
    "preprocessing": {
        "remove_special_chars": True,
        "normalize_whitespace": True,
        "lowercase": False
    },
    "analysis": {
        "max_requirements": 10,
        "min_confidence": 0.8
    }
}

# 技术决策代理配置
TECHNICAL_AGENT_CONFIG: Dict[str, Any] = {
    "model": "qwen-agent",
    "temperature": 0.5,
    "max_tokens": 1500,
    "decision": {
        "max_alternatives": 5,
        "min_confidence": 0.7,
        "consider_constraints": True
    }
}

# 规范优化代理配置
SPECIFICATION_AGENT_CONFIG: Dict[str, Any] = {
    "model": "qwen-agent",
    "temperature": 0.3,
    "max_tokens": 1000,
    "optimization": {
        "max_iterations": 3,
        "min_improvement": 0.1
    },
    "validation": {
        "strict_mode": True,
        "check_completeness": True
    }
}

# 知识库配置
KNOWLEDGE_BASE_CONFIG: Dict[str, Any] = {
    "path": "data/knowledge_base.json",
    "auto_save": True,
    "backup": {
        "enabled": True,
        "interval": 3600,  # 1小时
        "max_backups": 5
    },
    "search": {
        "max_results": 10,
        "min_relevance": 0.6
    }
}

# 代理系统全局配置
AGENT_SYSTEM_CONFIG: Dict[str, Any] = {
    "log_level": "INFO",
    "async_mode": True,
    "timeout": 30,
    "retry": {
        "max_attempts": 3,
        "delay": 1
    },
    "cache": {
        "enabled": True,
        "ttl": 3600  # 1小时
    }
} 