# 🔑 环境变量配置示例

## Supabase 连接字符串格式

当你在 Supabase 创建项目后，连接字符串会是这样的格式：

```
postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres
```

### 示例 (替换为你的实际值)：
```
DATABASE_URL=postgresql://postgres.abcdefghijklmnop:mypassword123@aws-0-us-west-1.pooler.supabase.com:5432/postgres
```

## Vercel 环境变量配置

在 Vercel 项目设置中添加这两个环境变量：

| Name | Value | Environment |
|------|-------|-------------|
| `DATABASE_URL` | 你的Supabase连接字符串 | Production, Preview, Development |
| `SECRET_KEY` | `note-app-secret-key-2024` | Production, Preview, Development |

## 💡 重要提示

1. **密码安全**: 不要在代码中硬编码密码
2. **环境选择**: 为所有环境 (Production, Preview, Development) 都配置变量
3. **连接测试**: 部署前可以在本地 .env 文件中测试连接

## 🧪 本地测试

创建 `.env` 文件 (不会提交到Git)：
```env
DATABASE_URL=postgresql://postgres.xyz:password@aws-0-region.pooler.supabase.com:5432/postgres
SECRET_KEY=your-secret-key
```

然后运行：
```bash
python src/main.py
```

访问 http://localhost:5001 测试功能。