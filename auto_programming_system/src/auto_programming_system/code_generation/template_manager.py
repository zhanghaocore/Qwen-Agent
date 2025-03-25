"""
代码模板管理器
负责管理和应用代码生成模板
"""

from typing import Dict, Any, Optional
import os
import jinja2

class TemplateManager:
    """代码模板管理器"""
    
    def __init__(self, templates_dir: Optional[str] = None):
        """
        初始化模板管理器
        
        Args:
            templates_dir: 模板目录路径，如果为None则使用默认目录
        """
        if templates_dir is None:
            templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        
        self.templates_dir = templates_dir
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(templates_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        渲染指定模板
        
        Args:
            template_name: 模板名称
            context: 模板上下文数据
            
        Returns:
            渲染后的代码字符串
            
        Raises:
            jinja2.exceptions.TemplateNotFound: 如果模板不存在
        """
        template = self.env.get_template(template_name)
        return template.render(**context)
    
    def list_templates(self) -> list:
        """
        列出所有可用的模板
        
        Returns:
            模板名称列表
        """
        return self.env.list_templates()
    
    def get_template_content(self, template_name: str) -> str:
        """
        获取模板原始内容
        
        Args:
            template_name: 模板名称
            
        Returns:
            模板原始内容
            
        Raises:
            jinja2.exceptions.TemplateNotFound: 如果模板不存在
        """
        if not self.env.loader:
            raise ValueError("Template loader is not initialized")
        return self.env.loader.get_source(self.env, template_name)[0] 