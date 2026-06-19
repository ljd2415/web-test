# 小区门禁信息系统

基于 Django 6 和 Vue 3 的小区住户门禁信息管理网站。

## 本地运行

```bash
python -m venv .venv
pip install -r requirements.txt
cd frontend && npm install && npm run build && cd ..
python manage.py migrate
python manage.py runserver
```

## 环境变量

复制 `.env.example` 并设置 Django 密钥、允许的主机及 MySQL 连接信息。不要提交真实 `.env`。

## Vercel

项目通过 `config.wsgi:application` 运行，使用 Python 3.12。生产环境需要在 Vercel 项目设置中配置 `.env.example` 所列变量。
