#!/bin/bash

BASE_URL="http://127.0.0.1:8000"

exec > test_api_result.txt 2>&1

echo "========================================="
echo "开始测试所有接口"
echo "========================================="
echo ""

# 1. 生成测试数据
echo "1. 生成测试数据"
curl -s -X POST "$BASE_URL/test-data/" | jq .
echo ""

# 2. 用户管理
echo "========================================="
echo "2. 用户管理"
echo "========================================="

# 创建用户
echo "2.1 创建用户"
USER_ID=$(curl -s -X POST "$BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "hello",
    "email": "hello@example.com",
    "name": "Test Hello",
    "password": "password12356"
  }' | jq -r '.id')
echo "创建的用户ID: $USER_ID"
echo ""

# 用户登录
echo "2.2 用户登录"
curl -s -X POST "$BASE_URL/users/login/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }' | jq .
echo ""

# 获取用户信息
echo "2.3 获取用户信息"
curl -s -X GET "$BASE_URL/users/$USER_ID/" | jq .
echo ""

# 获取用户列表
echo "2.4 获取用户列表"
curl -s -X GET "$BASE_URL/users/" | jq .
echo ""

# 更新用户信息
echo "2.5 更新用户信息"
curl -s -X PUT "$BASE_URL/users/$USER_ID/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newemail@example.com",
    "name": "Updated Name"
  }' | jq .
echo ""

# 3. 反馈管理
echo "========================================="
echo "3. 反馈管理"
echo "========================================="

# 提交反馈
echo "3.1 提交反馈"
FEEDBACK_ID=$(curl -s -X POST "$BASE_URL/feedback/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "测试反馈标题",
    "content": "这是一个测试反馈内容",
    "user_id": 1
  }' | jq -r '.id')
echo "创建的反馈ID: $FEEDBACK_ID"
echo ""

# 获取反馈列表
echo "3.2 获取反馈列表"
curl -s -X GET "$BASE_URL/feedback/" | jq .
echo ""

# 获取单个反馈详情
echo "3.3 获取单个反馈详情"
curl -s -X GET "$BASE_URL/feedback/$FEEDBACK_ID/" | jq .
echo ""

# 按状态过滤反馈
echo "3.4 按状态过滤反馈"
curl -s -X GET "$BASE_URL/feedback/?status=pending" | jq .
echo ""

# 更新反馈
echo "3.5 更新反馈"
curl -s -X PUT "$BASE_URL/feedback/$FEEDBACK_ID/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "更新后的反馈标题",
    "content": "更新后的反馈内容"
  }' | jq .
echo ""

# 更新反馈状态
echo "3.6 更新反馈状态"
curl -s -X PATCH "$BASE_URL/feedback/$FEEDBACK_ID/status/" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "resolved"
  }' | jq .
echo ""

# 搜索反馈
echo "3.7 搜索反馈"
curl -s -X GET "$BASE_URL/feedback/search/?keyword=登录" | jq .
echo ""

# 4. 评论管理
echo "========================================="
echo "4. 评论管理"
echo "========================================="

# 创建评论
echo "4.1 创建评论"
COMMENT_ID=$(curl -s -X POST "$BASE_URL/comments/" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "这是一个测试评论",
    "user_id": 1,
    "feedback_id": 1
  }' | jq -r '.id')
echo "创建的评论ID: $COMMENT_ID"
echo ""

# 获取反馈的评论列表
echo "4.2 获取反馈的评论列表"
curl -s -X GET "$BASE_URL/feedback/1/comments/" | jq .
echo ""

# 更新评论
echo "4.3 更新评论"
curl -s -X PUT "$BASE_URL/comments/$COMMENT_ID/" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "更新后的评论内容"
  }' | jq .
echo ""

# 5. 标签管理
echo "========================================="
echo "5. 标签管理"
echo "========================================="

# 创建标签
echo "5.1 创建标签"
TAG_ID=$(curl -s -X POST "$BASE_URL/tags/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-tag",
    "description": "测试标签"
  }' | jq -r '.id')
echo "创建的标签ID: $TAG_ID"
echo ""

# 获取标签列表
echo "5.2 获取标签列表"
curl -s -X GET "$BASE_URL/tags/" | jq .
echo ""

# 为反馈添加标签
echo "5.3 为反馈添加标签"
curl -s -X POST "$BASE_URL/feedback/1/tags/bug/" | jq .
echo ""

# 从反馈移除标签
echo "5.4 从反馈移除标签"
curl -s -X DELETE "$BASE_URL/feedback/1/tags/bug/" | jq .
echo ""

# 6. 统计功能
echo "========================================="
echo "6. 统计功能"
echo "========================================="

# 获取用户数量统计
echo "6.1 获取用户数量统计"
curl -s -X GET "$BASE_URL/stats/users/" | jq .
echo ""

# 获取反馈状态统计
echo "6.2 获取反馈状态统计"
curl -s -X GET "$BASE_URL/stats/feedback/" | jq .
echo ""

# 获取热门标签
echo "6.3 获取热门标签"
curl -s -X GET "$BASE_URL/stats/hot-tags/" | jq .
echo ""

# 获取反馈提交趋势
echo "6.4 获取反馈提交趋势"
curl -s -X GET "$BASE_URL/stats/feedback-trend/" | jq .
echo ""

# 7. 通知功能
echo "========================================="
echo "7. 通知功能"
echo "========================================="

# 获取用户通知列表
echo "7.1 获取用户通知列表"
curl -s -X GET "$BASE_URL/users/1/notifications/" | jq .
echo ""

# 标记所有通知为已读
echo "7.2 标记所有通知为已读"
curl -s -X PATCH "$BASE_URL/users/1/notifications/read-all/" | jq .
echo ""

# 清除所有通知
echo "7.3 清除所有通知"
curl -s -X DELETE "$BASE_URL/users/1/notifications/" | jq .
echo ""

# 8. 删除操作
echo "========================================="
echo "8. 删除操作"
echo "========================================="

# 删除评论
echo "8.1 删除评论"
curl -s -X DELETE "$BASE_URL/comments/$COMMENT_ID/" | jq .
echo ""

# 删除反馈
echo "8.2 删除反馈"
curl -s -X DELETE "$BASE_URL/feedback/$FEEDBACK_ID/" | jq .
echo ""

# 删除标签
echo "8.3 删除标签"
curl -s -X DELETE "$BASE_URL/tags/$TAG_ID/" | jq .
echo ""

# 删除用户
echo "8.4 删除用户"
curl -s -X DELETE "$BASE_URL/users/$USER_ID/" | jq .
echo ""

echo "========================================="
echo "测试完成"
echo "========================================="
