# AI驱动的多源文档一致性检测系统

## 项目简介
本项目旨在使用 AI 技术自动检测软件项目中函数的 **代码实现、函数文档、外部文档** 之间的一致性。通过对比函数说明和实际实现，系统能够：
- 给出一致性评分
- 标注潜在问题
- 提供改进建议
- 生成自然语言解释

本系统基于国内 AI 模型（SiliconFlow / DeepSeek-V2.5）实现，支持本地 CSV 报告生成和可视化查看。

## 功能特点
- **多源输入**：函数实现代码、函数 docstring、外部文档
- **AI 驱动分析**：基于大语言模型生成一致性评分和自然语言解释
- **批量检测**：可一次处理多个函数
- **报告输出**：生成 CSV 文件，便于后续审查和归档

## 安装与依赖
1. 克隆仓库：
```bash
git clone https://github.com/yourusername/AI_MultiDoc_Consistency.git
cd AI_MultiDoc_Consistency
```
2. 安装依赖：
pip install -r requirements.txt
3. 配置环境变量：
.env 文件中添加：
    SILICONFLOW_API_KEY=你的SILICONFLOW_API_KEY
4. 运行程序：

使用方法

将待检测函数及外部文档准备好

```bash
python main.py
```

检查输出：

CSV 文件：reports/consistency_report.csv

包含函数名称、semantic 分数、问题、建议、自然语言解释

文件结构
AI_MultiDoc_Consistency/
│
├─ main.py                   # 主入口
├─ detectors/
│   ├─ siliconflow_llm.py    # AI 检测器模块
├─ docs/                     # 示例外部文档
├─ reports/
│   └─ consistency_report.csv
├─ requirements.txt
└─ README.md

示例

输入：

def add(a, b):
    """Add two numbers and return the result."""
    return a + b


对应外部文档：

Description: Add two numbers and return the result.
Inputs: a, b
Output: number