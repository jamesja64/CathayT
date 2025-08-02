#!/bin/bash

# GitHub上傳腳本
# 作者: James
# 日期: 2024

echo "=== 上傳到GitHub ==="

# 檢查git是否安裝
if ! command -v git &> /dev/null; then
    echo "錯誤: Git未安裝"
    exit 1
fi

# 設定GitHub倉庫
REPO_URL="https://github.com/jamesja64/CathayT.git"
REPO_NAME="CathayT"

# 檢查是否已經是git倉庫
if [ ! -d ".git" ]; then
    echo "初始化Git倉庫..."
    git init
    git remote add origin $REPO_URL
fi

# 添加所有文件
echo "添加文件到Git..."
git add .

# 提交更改
echo "提交更改..."
git commit -m "Cathay API 測試專案 - 完整測試解決方案

包含:
- API測試案例設計 (CSV格式)
- Postman測試集合
- Python自動化測試腳本
- K6壓力測試腳本
- 完整文檔和執行腳本

測試覆蓋:
- GET /products 端點測試
- POST /messages 端點測試
- 邊界條件測試
- 效能測試
- 壓力測試

作者: James
日期: $(date)"

# 推送到GitHub
echo "推送到GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ 成功上傳到GitHub: https://github.com/jamesja64/CathayT"
    echo ""
    echo "專案包含:"
    echo "- 測試案例設計"
    echo "- Postman測試集合"
    echo "- 自動化測試腳本"
    echo "- 壓力測試腳本"
    echo "- 完整文檔"
else
    echo "❌ 上傳失敗"
    echo "請檢查GitHub認證和網路連線"
fi 