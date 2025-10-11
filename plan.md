# Lab 2 部署计划：将笔记应用从 SQLite 迁移到云数据库并部署到 Vercel

## 项目概述
将现有的基于 SQLite 的笔记应用重构为使用云数据库（PostgreSQL），并成功部署到 Vercel 平台。

## 当前应用架构
- **后端框架**: Flask + SQLAlchemy
- **数据库**: SQLite (本地文件数据库)
- **前端**: 静态 HTML/JS 文件
- **API 路由**: `/api/user` 和 `/api/note`
- **模型**: User 和 Note 实体
- **前端**: 静态 HTML/CSS/JavaScript

## 问题分析
1. **SQLite 限制**: Vercel 的 serverless 环境不支持持久的文件系统
2. **环境变量**: 需要从环境变量中获取数据库连接和其他配置
3. **部署结构**: 需要调整文件结构以适配 Vercel 的 serverless 函数

## 实施计划

### 阶段 1: 数据库迁移准备
**目标**: 将应用从 SQLite 迁移到 PostgreSQL

#### 1.1 更新项目依赖
- 添加 `psycopg2-binary` (PostgreSQL 驱动)
- 添加 `python-dotenv` (环境变量管理)

#### 1.2 环境变量配置
- 创建 `.env.example` 模板文件
- 设置数据库连接字符串格式
- 配置密钥管理

#### 1.3 数据库配置重构
- 修改 `src/main.py` 支持环境变量
- 添加 PostgreSQL 连接逻辑
- 保留 SQLite 作为本地开发备选

### 阶段 2: Vercel 部署配置
**目标**: 准备应用在 Vercel 上运行

#### 2.1 创建 Vercel 配置
- 创建 `vercel.json` 配置文件
- 设置 Python 运行时
- 配置路由规则

#### 2.2 应用结构调整
- 确保静态文件正确服务
- 配置应用入口点
- 处理 serverless 环境限制

### 阶段 3: 云数据库设置
**目标**: 配置 Supabase PostgreSQL 数据库

#### 3.1 Supabase 配置
- 创建 Supabase 项目
- 获取数据库连接字符串
- 设置表结构 (users, notes)

#### 3.2 本地测试
- 使用本地 PostgreSQL 测试连接
- 验证数据模型创建
- 测试所有 CRUD 操作

### 阶段 4: 部署和验证
**目标**: 完成部署并验证功能

#### 4.1 GitHub 准备
- 更新 `.gitignore` 排除敏感文件
- 提交所有代码更改
- 确保仓库状态良好

#### 4.2 Vercel 部署
- 连接 GitHub 仓库到 Vercel
- 配置环境变量
  - `DATABASE_URL`: Supabase 连接字符串
  - `SECRET_KEY`: Flask 应用密钥
- 部署应用

#### 4.3 功能验证
- 测试前端界面加载
- 验证用户注册/登录
- 测试笔记创建、编辑、删除
- 检查数据持久化

### 阶段 5: 文档编写
**目标**: 记录完整的迁移过程

#### 5.1 技术文档
创建 `lab2_writeup.md` 包含：
- 迁移步骤详述
- 遇到的技术挑战
- 解决方案说明
- 部署过程截图
- 功能演示
- 经验总结

## 技术要求

### 必需的环境变量
```env
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-flask-secret-key
```

### 关键配置文件
- `requirements.txt`: Python 依赖
- `vercel.json`: Vercel 部署配置
- `.env.example`: 环境变量模板
- `.gitignore`: Git 忽略文件

### 数据库表结构
保持现有的 User 和 Note 模型不变，确保与 PostgreSQL 兼容。

## 预期挑战和解决方案

### 1. 数据库连接问题
- **挑战**: PostgreSQL 连接字符串格式和 SSL 要求
- **解决**: 正确配置连接参数和 SSL 设置

### 2. Vercel 环境限制
- **挑战**: Serverless 函数的冷启动和超时限制
- **解决**: 优化数据库连接和查询性能

### 3. 静态文件服务
- **挑战**: Vercel 中静态文件的正确服务
- **解决**: 调整路由配置和文件路径

## 成功标准
- [ ] 应用成功部署到 Vercel
- [ ] 所有 API 端点正常工作
- [ ] 前端界面完全功能
- [ ] 数据正确存储在 PostgreSQL 中
- [ ] 环境变量安全配置
- [ ] 完整的技术文档

## 时间预估
- 阶段 1-2: 代码重构 (1-2小时)
- 阶段 3: 数据库设置和测试 (1小时)
- 阶段 4: 部署和验证 (30分钟-1小时)
- 阶段 5: 文档编写 (30分钟)

**总计**: 3-4.5小时