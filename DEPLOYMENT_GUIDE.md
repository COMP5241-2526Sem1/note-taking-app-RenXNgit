# Vercel 部署完整指南

## 🚀 部署步骤概览

### 步骤 1: 设置 Supabase 数据库

1. **访问 Supabase**
   - 打开 [https://supabase.com](https://supabase.com)
   - 使用 GitHub 账户登录

2. **创建新项目**
   - 点击 "New project"
   - 选择组织（或创建新的）
   - 填写项目信息：
     - Name: `note-taking-app`
     - Database Password: 记住这个密码！
     - Region: 选择最近的区域

3. **获取数据库连接信息**
   - 项目创建完成后，进入 Settings → Database
   - 在 "Connection parameters" 部分找到 "Connection string"
   - 复制连接字符串，格式类似：
     ```
     postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres
     ```

### 步骤 2: 准备代码提交

1. **检查文件完整性**
   确保以下文件存在并正确配置：
   - ✅ `requirements.txt` (包含 psycopg2-binary, python-dotenv)
   - ✅ `vercel.json` (Vercel 配置)
   - ✅ `src/main.py` (应用入口)
   - ✅ `.env.example` (环境变量模板)
   - ✅ `.gitignore` (排除 .env 文件)

2. **提交代码到 GitHub**
   ```bash
   git add .
   git commit -m "feat: ready for Vercel deployment with PostgreSQL"
   git push origin main
   ```

### 步骤 3: 创建 Vercel 项目

1. **访问 Vercel**
   - 打开 [https://vercel.com](https://vercel.com)
   - 使用 GitHub 账户登录

2. **导入项目**
   - 点击 "New Project"
   - 选择你的 GitHub 仓库 `note-taking-app-RenXNgit`
   - 点击 "Import"

3. **配置项目设置**
   - **Project Name**: 保持默认或自定义
   - **Framework Preset**: 选择 "Other" 
   - **Root Directory**: 保持默认 (./")
   - **Build Command**: 留空
   - **Output Directory**: 留空
   - **Install Command**: 留空

### 步骤 4: 配置环境变量

在 Vercel 项目配置页面：

1. **添加环境变量**
   - 点击 "Environment Variables" 部分
   - 添加以下变量：

   ```
   Name: DATABASE_URL
   Value: 你的 Supabase 连接字符串
   Environment: Production, Preview, Development (全选)
   ```

   ```
   Name: SECRET_KEY
   Value: 生成一个强随机字符串 (例如: your-super-secret-key-here)
   Environment: Production, Preview, Development (全选)
   ```

2. **点击 "Deploy"**

### 步骤 5: 验证部署

1. **等待部署完成**
   - 查看构建日志
   - 确保没有错误

2. **测试应用**
   - 访问生成的 Vercel URL
   - 测试以下功能：
     - [ ] 页面加载正常
     - [ ] 可以创建笔记
     - [ ] 可以编辑笔记
     - [ ] 可以删除笔记
     - [ ] 搜索功能正常

### 步骤 6: 监控和调试

如果遇到问题：

1. **查看 Vercel 日志**
   - 在 Vercel 面板查看 "Functions" 标签
   - 检查错误日志

2. **常见问题解决**
   - 数据库连接失败：检查 DATABASE_URL 格式
   - 模块导入错误：确认 requirements.txt 包含所有依赖
   - 静态文件 404：检查 vercel.json 路由配置

## 🔧 本地测试云配置

在部署前，可以在本地测试云数据库连接：

1. **创建本地 .env 文件**
   ```bash
   cp .env.example .env
   ```

2. **编辑 .env 文件**
   ```env
   DATABASE_URL=你的Supabase连接字符串
   SECRET_KEY=your-secret-key
   ```

3. **安装依赖并测试**
   ```bash
   pip install -r requirements.txt
   python src/main.py
   ```

4. **访问 http://localhost:5001 测试功能**

## 📱 部署后的优势

- **自动扩展**: Vercel 自动处理流量增长
- **全球 CDN**: 静态文件全球加速
- **免费 HTTPS**: 自动 SSL 证书
- **自动部署**: Git push 触发自动部署
- **预览部署**: Pull Request 自动生成预览环境

## 🎯 下一步

部署成功后，你可以：
- 设置自定义域名
- 配置监控和分析
- 添加更多功能
- 设置 CI/CD 流水线