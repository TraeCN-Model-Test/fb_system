# Hasty Feedback System

基于 FastAPI 的反馈系统 API。

## 功能

- 用户管理：注册、登录、信息查询
- 反馈管理：提交、查询、更新、删除
- 评论管理：添加、查询、更新、删除
- 标签管理：创建、添加到反馈
- 统计功能：用户数、反馈数、热门标签
- 通知功能：查询、标记已读

## 技术栈

- FastAPI
- Pydantic
- Python 3.8+

## 安装运行

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

访问 http://127.0.0.1:8000/docs 查看 API 文档。
