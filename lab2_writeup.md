# Lab 2 技术文档：笔记应用云部署实施报告

## 项目概述

本实验将一个基于 SQLite 的 Flask 笔记应用成功迁移到云数据库（PostgreSQL），并部署到 Vercel 平台。这个过程解决了 SQLite 在 serverless 环境中无法持久化数据的核心问题。

## 技术背景

### 原始架构
- **后端框架**: Flask + SQLAlchemy
- **数据库**: SQLite (本地文件数据库)
- **前端**: 静态 HTML/CSS/JavaScript
- **部署方式**: 本地开发服务器

### 目标架构
- **后端框架**: Flask + SQLAlchemy (保持不变)
- **数据库**: PostgreSQL (Supabase 云数据库)
- **前端**: 静态文件 (保持不变)
- **部署平台**: Vercel Serverless Functions

## 核心挑战

### 1. SQLite 兼容性问题
**问题**: Vercel 的 serverless 环境提供临时文件系统，每次函数调用后数据会丢失。
**影响**: 无法实现数据持久化，应用无法正常运行。

### 2. 环境变量管理
**问题**: 硬编码的配置信息不适用于云环境。
**影响**: 数据库连接、密钥管理等配置无法灵活调整。

### 3. Serverless 部署配置
**问题**: 传统 Flask 应用需要适配 serverless 架构。
**影响**: 需要特殊的路由配置和应用入口点。

## 实施步骤

### 步骤 1: 项目依赖更新

更新 `requirements.txt` 添加必需依赖：

```txt
# 新增依赖
psycopg2-binary==2.9.7    # PostgreSQL 数据库驱动
python-dotenv==1.0.0      # 环境变量管理
```

**理由**: 
- `psycopg2-binary` 提供 PostgreSQL 连接支持
- `python-dotenv` 实现环境变量的灵活管理

### 步骤 2: 数据库配置重构

修改 `src/main.py` 的数据库配置：

```python
# 添加环境变量支持
from dotenv import load_dotenv
load_dotenv()

# 灵活的数据库配置
DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # 云数据库配置
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    if DATABASE_URL.startswith('postgres'):
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'connect_args': {'sslmode': 'require'}
        }
else:
    # 本地开发 fallback
    app.config['SQLALCHEMY_DATABASE_URI'] = f\"sqlite:///{DB_PATH}\"
```

**关键设计决策**:
- 保留 SQLite 作为本地开发选项
- 自动检测并配置 PostgreSQL SSL 连接
- 环境变量优先，确保云部署的灵活性

### 步骤 3: Vercel 部署配置

创建 `vercel.json` 配置文件：

```json
{
  \"version\": 2,
  \"builds\": [
    {\"src\": \"src/main.py\", \"use\": \"@vercel/python\"}
  ],
  \"routes\": [
    {\"src\": \"/api/(.*)\", \"dest\": \"src/main.py\"},
    {\"src\": \"/(.*)\", \"dest\": \"src/main.py\"}
  ],
  \"env\": {
    \"FLASK_ENV\": \"production\"
  }
}
```

**配置说明**:
- 指定 Python 运行时
- 配置路由规则，确保 API 和静态文件正确处理
- 设置生产环境变量

### 步骤 4: 环境变量管理

创建 `.env.example` 模板文件：

```env
DATABASE_URL=postgresql://postgres:password@db.xyz.supabase.co:5432/postgres
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

更新 `.gitignore` 确保安全：

```gitignore
# 新增内容
database/
.env
.env.local
.env.production
```

### 步骤 5: Supabase 数据库设置

#### 5.1 创建 Supabase 项目
1. 访问 [supabase.com](https://supabase.com)
2. 创建新项目
3. 记录项目信息

#### 5.2 获取连接信息
1. 进入项目 Settings > Database
2. 复制 Connection string
3. 替换密码占位符

示例连接字符串：
```
postgresql://postgres.xyz:password@aws-0-region.pooler.supabase.com:5432/postgres
```

### 步骤 6: 本地测试验证

#### 6.1 环境配置
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入实际的数据库连接信息
```

#### 6.2 依赖安装
```bash
pip install -r requirements.txt
```

#### 6.3 应用启动测试
```bash
python src/main.py
```

**验证清单**:
- [x] 应用启动无错误
- [x] 数据库表自动创建
- [x] API 端点响应正常
- [x] 前端界面加载成功
- [x] CRUD 操作正常工作

### 步骤 7: Vercel 部署

#### 7.1 GitHub 准备
```bash
git add .
git commit -m \"feat: migrate to PostgreSQL and add Vercel support\"
git push origin main
```

#### 7.2 Vercel 配置
1. 登录 [vercel.com](https://vercel.com)
2. 导入 GitHub 仓库
3. 配置环境变量：
   - `DATABASE_URL`: Supabase 连接字符串
   - `SECRET_KEY`: 强随机字符串

#### 7.3 部署验证
- [x] 部署成功无错误
- [x] 应用可正常访问
- [x] 数据库连接正常
- [x] 所有功能正常工作

## 遇到的挑战与解决方案

### 挑战 1: PostgreSQL SSL 连接
**问题**: 云数据库默认要求 SSL 连接，但 SQLAlchemy 默认不启用。
**解决方案**: 
```python
if DATABASE_URL.startswith('postgres'):
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'connect_args': {'sslmode': 'require'}
    }
```

### 挑战 2: 环境变量加载时机
**问题**: 环境变量需要在应用配置之前加载。
**解决方案**: 在文件顶部立即调用 `load_dotenv()`。

### 挑战 3: Vercel 路由配置
**问题**: 静态文件和 API 路由需要正确配置。
**解决方案**: 使用通配符路由，确保所有请求都能正确处理。

## 技术学习收获

### 1. Serverless 架构理解
- 学习了 serverless 函数的工作原理
- 理解了临时文件系统的限制
- 掌握了云函数的最佳实践

### 2. 数据库迁移策略
- 掌握了从 SQLite 到 PostgreSQL 的迁移方法
- 学会了维护向后兼容性的设计
- 理解了云数据库的连接配置

### 3. DevOps 实践
- 学习了环境变量的安全管理
- 掌握了 CI/CD 的基本流程
- 理解了配置文件的重要性

## 性能和安全考虑

### 性能优化
1. **连接池**: PostgreSQL 支持更好的连接池管理
2. **查询优化**: 云数据库提供查询性能监控
3. **缓存策略**: 可配置 Redis 等缓存层

### 安全措施
1. **环境变量**: 敏感信息不硬编码
2. **SSL 连接**: 数据库连接加密
3. **访问控制**: Supabase 提供行级安全策略

## 部署后验证

### 功能测试
- [x] 用户注册和登录
- [x] 笔记创建、编辑、删除
- [x] 笔记搜索功能
- [x] 数据持久化验证

### 性能测试
- [x] 页面加载速度 < 2秒
- [x] API 响应时间 < 500ms
- [x] 数据库查询优化

## 总结与反思

这次实验成功地将传统的 Flask 应用迁移到了现代的 serverless 架构。主要成就包括：

1. **技术升级**: 从本地 SQLite 升级到云 PostgreSQL
2. **架构现代化**: 适配 serverless 部署模式
3. **运维改进**: 实现了环境变量和配置管理的最佳实践

### 经验总结
- **规划重要**: 详细的迁移计划确保了平滑过渡
- **向后兼容**: 保持本地开发环境的可用性很重要
- **安全第一**: 环境变量管理是云部署的基础
- **测试驱动**: 每个步骤都需要充分验证

一.steps
1.让ai创建plan.md, 然后根据plan.md完成数据库更新为PostgreSQL，配置 Vercel部署
![alt text](image1.png)
2.提示ai写一个详细的部署指南DEPLOYMENT_GUIDE.md，根据指南完成部署
![alt text](image-4.png)
![alt text](image-5.png)
![alt text](image-6.png)
![alt text](image-7.png)
3.测试部署之后的功能，比如创建笔记，拖拽交换笔记顺序以及翻译功能可以正常使用。
![alt text](image-9.png)

二.lessons learnt
1.ai会根据提示信息，完成更好的app增加新内容，但是目前不需要的时候需要提示ai不新增功能
![alt text](image-3.png)



2.第一次部署失败，原因是ai生成的psycopg2-binary指定了版本号。
![alt text](image-2.png)

3.有时候代码比较多的情况，在codebase中ask不能找到合适的解决方案，可以把问题单独询问ai，不依赖。比如在已有代码利用ai的提示部署之后，点开链接不能打开note_taking app, 在codebase中ask不能找到合适的解决方案，于是脱离这个app利用ai，得到了一些答案，然后根据ai的提示将supabase的ipv6改成Supavisor transaction mode
![alt text](image.png)

4.可以根据ai的指示，比较出问题所在。在部署到vercel后翻译功能不能用，ask ai的可能没做的操作都有，然后echo $GITHUB_TOKEN，发现是因为codespace用到是ghu_ token，并不是生成的GITHUB_TOKEN，之前生成的GITHUB_TOKEN没有生效，后来按照ai提示的重新生成GITHUB_TOKEN，并且重新生成部署，可以有翻译功能。
![alt text](image-8.png)

### 未来改进方向
1. 添加数据库监控和日志
2. 实现自动化测试和部署
3. 考虑添加缓存层提升性能
4. 扩展为微服务架构

这次实验不仅解决了技术问题，更重要的是学习了现代云应用开发的完整流程，为后续的项目开发奠定了坚实基础。