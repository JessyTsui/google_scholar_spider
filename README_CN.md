# Google Scholar Spider 2.0 - 学术文献搜索分析系统

<p align="center">
  <a href="README.md">English</a> •
  <a href="README_CN.md">中文</a> •
  <a href="README_JP.md">日本語</a>
</p>

## 📖 简介

Google Scholar Spider 是一个现代化的学术文献搜索分析系统，能够从 Google Scholar 获取学术论文数据，并提供强大的分析和可视化功能。

### ✨ 主要特性

- 🔍 **智能搜索**：支持关键词、年份范围等多维度搜索
- 📊 **数据可视化**：引用趋势图、发表时间分析等
- 💾 **数据管理**：搜索历史保存、多格式导出（CSV/JSON/Excel/BibTeX）
- 🎨 **现代界面**：响应式设计、深色模式、流畅动画
- 🚀 **高性能**：异步后端、高效数据获取

## 📸 界面截图

### 首页界面
![首页](docs/screenshots/homepage.png)

### 搜索结果与数据可视化
![搜索结果](docs/screenshots/search-results.png)

## 🛠️ 技术栈

- **后端**：FastAPI + SQLAlchemy + BeautifulSoup4
- **前端**：React + TypeScript + Tailwind CSS
- **数据库**：SQLite（本地存储）
- **可视化**：Chart.js

## 📋 环境要求

- Python 3.8+
- Node.js 16+
- Chrome/Chromium 浏览器（用于 Selenium）

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/houseofcat/google_scholar_spider.git
cd google_scholar_spider
```

### 2. 安装依赖

#### 后端依赖
```bash
cd backend
pip install -r requirements.txt
cd ..
```

#### 前端依赖
```bash
cd frontend
npm install
cd ..
```

### 3. 启动系统

```bash
# 在项目根目录运行
python start.py
```

或者使用快捷脚本：
```bash
./run.sh  # Linux/Mac
```

### 4. 访问系统

启动成功后，访问以下地址：
- 🌐 **前端界面**：http://localhost:3000
- 📡 **后端 API**：http://localhost:8001
- 📚 **API 文档**：http://localhost:8001/docs

## 📖 使用指南

### 搜索论文

1. 在首页输入搜索关键词
2. 可选：设置年份范围和结果数量
3. 选择排序方式（按引用数、年均引用等）
4. 点击搜索按钮

### 查看结果

- 浏览论文列表，包含标题、作者、引用数等信息
- 点击标题可访问原文链接
- 使用筛选器进一步精确结果

### 数据分析

- 查看引用趋势图表
- 分析年度发表量分布
- 识别高影响力论文

### 导出数据

支持多种格式导出：
- **CSV**：适合 Excel 分析
- **JSON**：程序化处理
- **Excel**：完整的表格文件
- **BibTeX**：用于 LaTeX 引用

## 🔧 配置选项

### 后端配置

编辑 `backend/core/config.py` 或创建 `.env` 文件：

```env
DATABASE_URL=sqlite+aiosqlite:///../data/scholar.db
REQUEST_DELAY=5.0
MAX_RETRIES=3
USE_SELENIUM_FALLBACK=true
```

### 前端配置

编辑 `frontend/vite.config.ts` 配置代理和端口。

## ⚠️ 注意事项

1. **学术用途**：本工具仅供学术研究使用
2. **访问频率**：请合理控制搜索频率，避免被封禁
3. **验证码**：遇到验证码时，需要手动在弹出的浏览器中解决

## 🐛 常见问题

### 搜索无结果

- 原因：Google Scholar 检测到自动化访问
- 解决：等待一段时间后重试，或使用不同的关键词

### 端口占用

- 错误：`Port already in use`
- 解决：运行 `./stop.sh` 或手动结束占用端口的进程

### 依赖安装失败

- 确保 Python 和 Node.js 版本符合要求
- 使用国内镜像源加速下载

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m '添加某个特性'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 开源协议

本项目采用 MIT 协议 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 👏 致谢

- 原始爬虫实现：[houseofcat](https://github.com/houseofcat)
- FastAPI 框架
- React 社区
- 所有贡献者

## 📞 联系方式

问题和功能请求请使用 [GitHub Issues](https://github.com/houseofcat/google_scholar_spider/issues)。