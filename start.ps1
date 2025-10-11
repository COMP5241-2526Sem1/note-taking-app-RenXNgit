# 启动笔记应用 - 简单版本

Write-Host "🚀 启动笔记应用..." -ForegroundColor Green

# 检查 Python 是否安装
try {
    $pythonVersion = python --version 2>$null
    Write-Host "✅ Python 已安装: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 请先安装 Python" -ForegroundColor Red
    exit 1
}

# 安装依赖
Write-Host "📦 安装依赖包..." -ForegroundColor Yellow
pip install flask flask-sqlalchemy flask-cors python-dotenv psycopg2-binary

# 启动应用
Write-Host "🌟 启动应用..." -ForegroundColor Green
Write-Host "📱 应用将在 http://localhost:5001 运行" -ForegroundColor Cyan
Write-Host "🛑 按 Ctrl+C 停止应用" -ForegroundColor Yellow
Write-Host ""

# 运行应用
python src/main.py