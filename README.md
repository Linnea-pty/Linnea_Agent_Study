# Linnea Agent Study

一个基于 Python 的多模型个人 Agent 学习与实战项目，采用领域驱动设计（DDD）思想进行模块划分。

## 目录

- [项目状态](#项目状态)
- [核心特性](#核心特性)
- [技术栈](#技术栈)
- [目录结构](#目录结构)
- [安装与配置](#安装与配置)
- [使用指南](#使用指南)
- [架构与安全设计](#架构与安全设计)
- [常见问题](#常见问题)
- [贡献](#贡献)
- [许可证](#许可证)

## 项目状态

- **当前版本**：v0.1.0
- **项目状态**：开发中 / 实验性项目
- **适用场景**：学习和实践大模型 Agent 的底层架构、工具调用与路由机制。

## 核心特性

- **动态模型路由**：根据用户输入的意图（代码、推理、简单问答），自动将请求路由至不同的模型（如 DeepSeek、Qwen），平衡成本与效果。
- **丰富的工具生态**：内置数学计算、时间查询、Tavily 联网搜索、Playwright 网页抓取、沙箱文件读取等能力。
- **完善的会话记忆**：多端独立历史记录（Web 端、CLI 端），支持多轮对话并持久化到本地。
- **双端启动支持**：同时提供 Gradio Web 界面和 CLI 命令行交互。

## 技术栈

- **环境管理**：[uv](https://github.com/astral-sh/uv)
- **核心框架**：LangChain, LangGraph
- **大模型接入**：ChatOpenAI（兼容 DeepSeek、阿里通义千问）
- **前端 UI**：Gradio
- **网页解析**：Playwright, langchain-tavily

## 目录结构

项目采用 `src` 布局并按领域分包，确保各模块高内聚、低耦合：

```text
src/
├── main.py              # 统一入口（启动 Web 或 CLI）
├── agent/               # Agent 领域：组装模型、中间件与工具
├── chat/                # 聊天领域：Controller、业务编排、路由与持久化
├── tools/               # 工具领域：计算、时间、文件、网页与搜索的具体实现
└── shared/              # 共享基础设施：模型池、浏览器池、安全沙箱
```

## 安装与配置

### 1. 克隆项目并安装依赖

本项目使用 `uv` 进行环境和依赖管理（需提前安装 uv）。

```bash
git clone https://github.com/Linnea-pty/Linnea_Agent_Study.git
cd Linnea_Agent_Study
uv sync
```

### 2. 安装 Playwright 浏览器内核

由于包含网页读取工具，需安装 Chromium 内核：

```bash
uv run playwright install chromium
```

### 3. 配置环境变量

复制根目录的 `.env.example` 为 `.env`，并填入真实的 API Key：

```ini
# DeepSeek 配置
DEEPSEEK_API_KEY=sk-xxx
DEEPSEEK_MODEL=deepseek-chat

# 通义千问配置
QWEN_API_KEY=sk-xxx
QWEN_MODEL=qwen-flash

# Tavily 搜索配置
TAVILY_API_KEY=tvly-xxx
```

## 使用指南

### 启动 Web 界面（Gradio）

```bash
uv run linnea-agent
```

启动后在浏览器中访问提示的本地地址（如 `http://127.0.0.1:7860`）。

### 启动 CLI 终端模式

```bash
uv run linnea-agent-cli
```

## 架构与安全设计

项目在开发过程中重点解决了 Agent 落地常见的痛点：

- **路由一致性**：通过 `configurable` 参数传递路由决策，保证中间件执行与 UI 展示的模型档位绝对一致，避免重复计算。
- **历史记录安全**：使用显式类型映射表解析消息，结合临时文件 `os.replace` 实现原子写，杜绝历史文件损坏或上下文污染。
- **沙箱隔离**：`read_local_file` 工具限制了特定后缀和固定根目录，通过 `resolve` 阻断符号链接逃逸。
- **安全计算**：杜绝 `eval`，使用 `ast` 语法树白名单机制实现数学计算工具，防止代码注入。
- **高并发网页抓取**：基于 `threading.local` 和 `atexit` 实现 Playwright 浏览器的线程级复用与统一回收，大幅降低冷启动开销。

## 常见问题（FAQ）

**Q: 提示 `Missing credentials` 报错？**

A: 请检查根目录是否存在 `.env` 文件，且格式没有多余空格或引号。代码已通过绝对路径强制加载该文件。

**Q: 提示 `No module named 'app'` 或包导入失败？**

A: 确保你在项目根目录下执行 `uv run` 指令，而不是在 `src` 目录中单独运行 `python` 脚本。

**Q: 网页抓取报错 `Executable doesn't exist`？**

A: 请运行 `uv run playwright install chromium` 安装浏览器内核。

## 贡献

欢迎提交 Issue 或 Pull Request。如果是较大的改动，请先开 Issue 讨论。

## 许可证

本项目采用 MIT License 开源。
