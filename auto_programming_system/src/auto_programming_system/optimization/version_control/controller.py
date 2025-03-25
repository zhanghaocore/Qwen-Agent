"""
版本控制器模块
负责跟踪代码变更的历史
"""

import time
import json
from typing import Dict, Any, List, Optional


class VersionController:
    """版本控制器，跟踪代码版本历史"""
    
    def __init__(self):
        """初始化版本控制器"""
        self.versions = []
        self.current_version_index = -1
    
    def add_version(self, code: str, label: str = "") -> int:
        """
        添加新版本
        
        Args:
            code: 代码
            label: 版本标签
            
        Returns:
            版本索引
        """
        # 创建版本记录
        version = {
            "version_id": len(self.versions) + 1,
            "code": code,
            "label": label,
            "timestamp": int(time.time()),
            "changes": self._compute_changes(code)
        }
        
        # 添加到版本历史
        self.versions.append(version)
        self.current_version_index = len(self.versions) - 1
        
        return self.current_version_index
    
    def get_version(self, index: Optional[int] = None) -> Dict[str, Any]:
        """
        获取版本
        
        Args:
            index: 版本索引，默认为当前版本
            
        Returns:
            版本记录
            
        Raises:
            IndexError: 如果索引无效
        """
        if index is None:
            index = self.current_version_index
            
        if 0 <= index < len(self.versions):
            return self.versions[index]
        else:
            raise IndexError(f"无效的版本索引: {index}")
    
    def get_current_version(self) -> Dict[str, Any]:
        """
        获取当前版本
        
        Returns:
            当前版本记录
            
        Raises:
            IndexError: 如果没有版本
        """
        if self.current_version_index >= 0:
            return self.versions[self.current_version_index]
        else:
            raise IndexError("没有版本历史")
    
    def get_all_versions(self) -> List[Dict[str, Any]]:
        """
        获取所有版本
        
        Returns:
            版本历史列表
        """
        return self.versions
    
    def switch_version(self, index: int) -> Dict[str, Any]:
        """
        切换到指定版本
        
        Args:
            index: 版本索引
            
        Returns:
            切换后的版本记录
            
        Raises:
            IndexError: 如果索引无效
        """
        if 0 <= index < len(self.versions):
            self.current_version_index = index
            return self.versions[index]
        else:
            raise IndexError(f"无效的版本索引: {index}")
    
    def get_version_diff(self, from_index: int, to_index: int) -> Dict[str, Any]:
        """
        获取版本之间的差异
        
        Args:
            from_index: 起始版本索引
            to_index: 结束版本索引
            
        Returns:
            差异信息
            
        Raises:
            IndexError: 如果索引无效
        """
        if 0 <= from_index < len(self.versions) and 0 <= to_index < len(self.versions):
            from_version = self.versions[from_index]
            to_version = self.versions[to_index]
            
            # 简单地比较代码长度差异
            from_code = from_version["code"]
            to_code = to_version["code"]
            
            diff = {
                "from_version": from_index,
                "to_version": to_index,
                "from_label": from_version["label"],
                "to_label": to_version["label"],
                "line_count_diff": len(to_code.split("\n")) - len(from_code.split("\n")),
                "char_count_diff": len(to_code) - len(from_code),
                "is_longer": len(to_code) > len(from_code)
            }
            
            return diff
        else:
            raise IndexError(f"无效的版本索引: {from_index} 或 {to_index}")
    
    def _compute_changes(self, code: str) -> Dict[str, Any]:
        """
        计算与上一版本的变更
        
        Args:
            code: 新代码
            
        Returns:
            变更信息
        """
        changes = {
            "is_initial_version": True,
            "line_count_diff": 0,
            "char_count_diff": 0
        }
        
        # 如果有先前的版本，计算差异
        if self.versions:
            prev_code = self.versions[-1]["code"]
            prev_lines = prev_code.split("\n")
            curr_lines = code.split("\n")
            
            changes["is_initial_version"] = False
            changes["line_count_diff"] = len(curr_lines) - len(prev_lines)
            changes["char_count_diff"] = len(code) - len(prev_code)
            
            # 计算行级别的差异（简单实现）
            changed_lines = []
            for i, (prev, curr) in enumerate(zip(prev_lines, curr_lines)):
                if prev != curr:
                    changed_lines.append(i + 1)
            
            # 如果新代码行数更多，标记为新增行
            if len(curr_lines) > len(prev_lines):
                for i in range(len(prev_lines), len(curr_lines)):
                    changed_lines.append(i + 1)
                    
            changes["changed_lines"] = changed_lines
            
        return changes 