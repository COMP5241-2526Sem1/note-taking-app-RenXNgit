# PowerShell 部署脚本
Write-Host "🚀 准备部署到 Vercel..." -ForegroundColor Green

# 检查必需文件
Write-Host "📋 检查必需文件..." -ForegroundColor Yellow
$requiredFiles = @("requirements.txt", "vercel.json", "src\main.py")
$missingFiles = @()

foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host "❌ 缺少必需文件:" -ForegroundColor Red
    foreach ($file in $missingFiles) {
        Write-Host "   - $file" -ForegroundColor Red
    }
    exit 1
}

Write-Host "✅ 所有必需文件都存在" -ForegroundColor Green

# 检查 Git 状态
Write-Host "📡 检查 Git 状态..." -ForegroundColor Yellow
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "📝 发现未提交的更改，准备提交..." -ForegroundColor Yellow
    git add .
    git commit -m "feat: ready for Vercel deployment"
    Write-Host "✅ 代码已提交" -ForegroundColor Green
} else {
    Write-Host "✅ 工作目录是干净的" -ForegroundColor Green
}

# 推送到 GitHub
Write-Host "📤 推送到 GitHub..." -ForegroundColor Yellow
git push origin main
Write-Host "✅ 代码已推送到 GitHub" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 准备工作完成！" -ForegroundColor Green
Write-Host ""
Write-Host "📋 下一步操作：" -ForegroundColor Cyan
Write-Host "1. 访问 https://supabase.com 创建数据库" -ForegroundColor White
Write-Host "2. 访问 https://vercel.com 导入此项目" -ForegroundColor White
Write-Host "3. 配置环境变量 DATABASE_URL 和 SECRET_KEY" -ForegroundColor White
Write-Host "4. 部署！" -ForegroundColor White
Write-Host ""
Write-Host "📖 详细步骤请查看 DEPLOYMENT_GUIDE.md" -ForegroundColor Cyan