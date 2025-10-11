# 🚀 如何运行笔记应用

## 方式1: 本地运行 (SQLite 数据库)

### 步骤 1: 安装 Python 依赖
```powershell
# 确保在项目根目录
cd "d:\xnren\polyu\25sem1\software_engineering_and_development\note_taking_app\note-taking-app-RenXNgit"

# 安装依赖
pip install -r requirements.txt
```

### 步骤 2: 直接运行
```powershell
# 运行应用
python src/main.py
```

### 步骤 3: 访问应用
打开浏览器访问: `http://localhost:5001`

**特点**: 
- 使用 SQLite 本地数据库
- 数据存储在 `database/app.db` 文件中
- 适合本地开发和测试

---

## 方式2: 本地运行 (PostgreSQL 云数据库)

### 步骤 1: 设置 Supabase 数据库
1. 访问 [https://supabase.com](https://supabase.com)
2. 创建新项目
3. 获取数据库连接字符串

### 步骤 2: 配置环境变量
```powershell
# 复制环境变量模板
copy .env.example .env
```

编辑 `.env` 文件：
```env
DATABASE_URL=postgresql://postgres.xyz:password@aws-0-region.pooler.supabase.com:5432/postgres
SECRET_KEY=your-secret-key
```

### 步骤 3: 安装依赖并运行
```powershell
pip install -r requirements.txt
python src/main.py
```

### 步骤 4: 访问应用
打开浏览器访问: `http://localhost:5001`

**特点**:
- 使用云 PostgreSQL 数据库
- 数据持久化到云端
- 与生产环境一致

---

## 方式3: 部署到 Vercel (生产环境)

### 步骤 1: 提交代码到 GitHub
```powershell
git add .
git commit -m "feat: ready for deployment"
git push origin main
```

### 步骤 2: 创建 Supabase 数据库
1. 访问 [https://supabase.com](https://supabase.com)
2. 创建新项目 
3. 记录连接字符串

### 步骤 3: 部署到 Vercel
1. 访问 [https://vercel.com](https://vercel.com)
2. 导入 GitHub 仓库
3. 配置环境变量:
   - `DATABASE_URL`: Supabase 连接字符串
   - `SECRET_KEY`: 随机密钥
4. 点击 Deploy

### 步骤 4: 访问生产应用
使用 Vercel 提供的 URL 访问应用

**特点**:
- 全球 CDN 加速
- 自动扩展
- 免费 HTTPS
- 每次推送自动部署

---

## 🧪 快速测试脚本

创建并运行测试脚本：

```powershell
# 创建测试脚本
@"
# 测试应用是否正常运行
echo "🧪 测试笔记应用..."

# 启动应用 (后台运行)
Start-Process python -ArgumentList "src/main.py" -WindowStyle Hidden

# 等待应用启动
Start-Sleep -Seconds 3

# 测试 API 端点
try {
    `$response = Invoke-RestMethod -Uri "http://localhost:5001/api/notes" -Method GET
    Write-Host "✅ API 测试通过" -ForegroundColor Green
    Write-Host "📝 当前笔记数量: `$(`$response.Count)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ API 测试失败: `$_" -ForegroundColor Red
}

# 打开浏览器
Start-Process "http://localhost:5001"
Write-Host "🌐 浏览器已打开，访问 http://localhost:5001" -ForegroundColor Yellow
"@ | Out-File -FilePath "test_app.ps1" -Encoding UTF8

# 运行测试
powershell -ExecutionPolicy Bypass -File test_app.ps1
```

---

## 🔧 常见问题解决

### 问题 1: 模块导入错误
```powershell
# 解决方案：安装缺失的依赖
pip install flask flask-sqlalchemy flask-cors python-dotenv psycopg2-binary
```

### 问题 2: 端口被占用
```powershell
# 查看占用端口的进程
netstat -ano | findstr :5001

# 结束进程 (替换 PID)
taskkill /PID <PID> /F
```

### 问题 3: 数据库连接失败
- 检查 `.env` 文件中的 `DATABASE_URL` 格式
- 确保 Supabase 项目正常运行
- 验证网络连接

### 问题 4: 静态文件无法加载
- 确保 `src/static/` 目录存在
- 检查 `index.html` 文件路径

---

## 📁 项目文件结构
```
note-taking-app-RenXNgit/
├── src/
│   ├── main.py              # 应用入口文件
│   ├── models/             # 数据模型
│   │   ├── note.py
│   │   └── user.py
│   ├── routes/             # API 路由
│   │   ├── note.py
│   │   └── user.py
│   └── static/             # 前端文件
│       └── index.html
├── requirements.txt         # Python 依赖
├── vercel.json             # Vercel 配置
├── .env.example            # 环境变量模板
└── README.md               # 项目说明
```

---

## 🎯 推荐运行方式

### 开发阶段:
```powershell
# 本地 SQLite 数据库
python src/main.py
```

### 测试阶段:
```powershell
# 本地 + 云数据库
# 1. 配置 .env 文件
# 2. python src/main.py
```

### 生产阶段:
```
部署到 Vercel + Supabase
```

现在您可以选择任一方式运行应用！需要我帮您执行哪个步骤？