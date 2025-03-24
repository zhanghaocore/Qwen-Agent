#!/usr/bin/env python3
"""
高级使用示例 - 全自动Python后端编程系统

本示例展示了系统的高级功能，包括：
1. 构建完整应用程序
2. 使用自定义优化策略
3. 从文档需求生成代码
4. 定制安全沙箱参数
"""

import os
from autoprogrammer import (
    AutoProgrammingSystem, 
    ApplicationGenerator, 
    ValidationExtensionManager,
    SafeSandbox,
    OptimizationConfig
)

def build_complete_application():
    """构建完整的Web应用程序"""
    # 初始化应用生成器
    app_gen = ApplicationGenerator(
        model="gpt-4",  # 使用更强大的模型
        architecture="layered"  # 使用分层架构
    )
    
    # 定义应用程序需求
    requirements = """
    创建一个任务管理API，要求：
    1. 使用FastAPI框架
    2. 支持用户注册和登录（JWT认证）
    3. 任务管理功能（增删改查）
    4. 任务分类和标签
    5. 提醒功能（基于到期日）
    6. 使用SQLite数据库
    7. 包含单元测试
    """
    
    # 生成应用程序
    app = app_gen.create_application(
        description=requirements,
        database="sqlite",
        features=["authentication", "rest_api", "testing"]
    )
    
    # 输出项目结构
    print("=== 生成的项目结构 ===")
    for file_path in app.get_files():
        print(file_path)
    
    # 获取启动指令
    print("\n=== 启动指令 ===")
    for step in app.get_setup_instructions():
        print(f"- {step}")
    
    # 导出项目到目录
    output_dir = "./generated_app"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    app.export(output_dir)
    print(f"\n应用程序已导出到: {output_dir}")
    
    return app

def custom_optimization_strategy():
    """使用自定义优化策略"""
    # 创建自定义优化配置
    opt_config = OptimizationConfig(
        strategies=["performance", "security", "readability"],
        max_iterations=5,
        improvement_threshold=0.05,  # 如果改进小于5%，则停止迭代
        preserve_comments=True,
        target_complexity={"cyclomatic": 10, "cognitive": 8},
        optimization_level="aggressive"
    )
    
    # 初始化系统
    aps = AutoProgrammingSystem(optimization_config=opt_config)
    
    # 添加自定义约束
    code_constraints = [
        "使用类型注解",
        "遵循SOLID原则",
        "使用异常处理",
        "包含详细注释"
    ]
    
    # 生成代码
    result = aps.build(
        user_input="创建一个数据处理管道，从CSV文件读取数据，清洗后导出为JSON格式",
        constraints=code_constraints
    )
    
    print("\n=== 优化历史 ===")
    for i, version in enumerate(result['optimization_history']):
        print(f"版本 {i+1}: 质量分数 {version['metrics']['quality_score']}")
        print(f"   改进: {version['metrics'].get('improvement', 'N/A')}")
    
    return result['final_code']

def generate_from_documentation():
    """从详细文档生成代码"""
    # 准备详细需求文档
    doc_path = "requirements_doc.md"
    with open(doc_path, "w") as f:
        f.write("""
        # 图像处理模块需求
        
        ## 概述
        开发一个图像处理模块，能够对图像进行基本操作，如调整大小、裁剪、旋转、滤镜应用等。
        
        ## 功能需求
        1. 加载图像（支持PNG、JPEG、BMP格式）
        2. 图像缩放（保持或不保持宽高比）
        3. 图像裁剪（指定区域）
        4. 图像旋转（任意角度）
        5. 亮度/对比度调整
        6. 应用滤镜（至少支持灰度、模糊、锐化滤镜）
        7. 保存处理后的图像
        
        ## 技术约束
        - 使用Python 3.8+
        - 基于Pillow库实现核心功能
        - 提供友好的API接口
        - 包含详细文档
        - 异常处理
        - 单元测试覆盖率不低于80%
        
        ## 性能要求
        - 图像加载速度：1秒内（对于10MB以下图像）
        - 基本操作响应时间：不超过500ms
        - 内存占用：处理20MB图像时不超过100MB内存
        """)
    
    # 从文档生成代码
    aps = AutoProgrammingSystem()
    result = aps.build_from_document(doc_path)
    
    print("=== 从文档生成的代码 ===")
    print(f"生成的文件数量: {len(result['generated_files'])}")
    print(f"主模块: {result['main_module_path']}")
    
    # 清理示例文件
    os.remove(doc_path)
    
    return result

def custom_sandbox_execution():
    """使用自定义沙箱参数"""
    # 创建自定义沙箱
    sandbox = SafeSandbox(
        security_level="data_science",  # 允许数据科学相关库
        max_execution_time=10,  # 10秒超时
        memory_limit=200,  # 200MB内存限制
        allowed_modules=[
            "pandas", "numpy", "matplotlib",
            "sklearn.preprocessing", "sklearn.cluster"
        ]
    )
    
    # 使用自定义沙箱初始化系统
    aps = AutoProgrammingSystem(execution_sandbox=sandbox)
    
    # 生成并测试数据科学代码
    code = """
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    import matplotlib.pyplot as plt
    
    def analyze_data(csv_path, n_clusters=3):
        # 加载数据
        df = pd.read_csv(csv_path)
        
        # 预处理
        features = df.select_dtypes(include=['float64', 'int64']).dropna()
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        
        # 聚类分析
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        df['cluster'] = kmeans.fit_predict(scaled_features)
        
        # 可视化
        plt.figure(figsize=(10, 6))
        for cluster in range(n_clusters):
            plt.scatter(
                df.loc[df['cluster'] == cluster, features.columns[0]],
                df.loc[df['cluster'] == cluster, features.columns[1]],
                label=f'Cluster {cluster}'
            )
        plt.title('K-means Clustering Results')
        plt.xlabel(features.columns[0])
        plt.ylabel(features.columns[1])
        plt.legend()
        
        return {
            'clusters': df['cluster'].value_counts().to_dict(),
            'centers': kmeans.cluster_centers_.tolist(),
            'df': df
        }
    """
    
    # 在沙箱中执行代码
    try:
        # 创建测试CSV
        with open("test_data.csv", "w") as f:
            import numpy as np
            f.write("x,y,z\n")
            for i in range(100):
                f.write(f"{np.random.random()},{np.random.random()},{np.random.random()}\n")
        
        result = sandbox.execute(
            code=code,
            inputs={"csv_path": "test_data.csv", "n_clusters": 3}
        )
        
        print("=== 沙箱执行结果 ===")
        print(f"状态: {result['status']}")
        print(f"聚类结果: {result.get('result', {}).get('clusters', 'N/A')}")
        
    except Exception as e:
        print(f"执行错误: {e}")
    finally:
        # 清理测试文件
        if os.path.exists("test_data.csv"):
            os.remove("test_data.csv")

if __name__ == "__main__":
    print("高级示例1: 构建完整应用程序")
    print("=" * 60)
    try:
        build_complete_application()
    except Exception as e:
        print(f"示例1执行错误: {e}")
    
    print("\n\n高级示例2: 自定义优化策略")
    print("=" * 60)
    try:
        custom_optimization_strategy()
    except Exception as e:
        print(f"示例2执行错误: {e}")
    
    print("\n\n高级示例3: 从文档生成代码")
    print("=" * 60)
    try:
        generate_from_documentation()
    except Exception as e:
        print(f"示例3执行错误: {e}")
    
    print("\n\n高级示例4: 自定义沙箱执行")
    print("=" * 60)
    try:
        custom_sandbox_execution()
    except Exception as e:
        print(f"示例4执行错误: {e}") 