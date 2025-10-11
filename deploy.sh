#!/bin/bash

# 快速部署脚本
echo "🚀 准备部署到 Vercel..."

# 检查必需文件
echo "📋 检查必需文件..."
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt 不存在"
    exit 1
fi

if [ ! -f "vercel.json" ]; then
    echo "❌ vercel.json 不存在"
    exit 1
fi

if [ ! -f "src/main.py" ]; then
    echo "❌ src/main.py 不存在"
    exit 1
fi

echo "✅ 所有必需文件都存在"

# 检查 Git 状态
echo "📡 检查 Git 状态..."
if [[ -n $(git status --porcelain) ]]; then
    echo "📝 发现未提交的更改，准备提交..."
    git add .
    git commit -m "feat: ready for Vercel deployment"
    echo "✅ 代码已提交"
else
    echo "✅ 工作目录是干净的"
fi

# 推送到 GitHub
echo "📤 推送到 GitHub..."
git push origin main
echo "✅ 代码已推送到 GitHub"

echo ""
echo "🎉 准备工作完成！"
echo ""
echo "📋 下一步操作："
echo "1. 访问 https://supabase.com 创建数据库"
echo "2. 访问 https://vercel.com 导入此项目"
echo "3. 配置环境变量 DATABASE_URL 和 SECRET_KEY"
echo "4. 部署！"
echo ""
echo "📖 详细步骤请查看 DEPLOYMENT_GUIDE.md"