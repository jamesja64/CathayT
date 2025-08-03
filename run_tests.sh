#!/bin/bash

# Cathay API 測試執行腳本
# 作者: James
# 日期: 2024

echo "=== Cathay API 測試專案 ==="
echo "開始執行測試..."

# 檢查Python虛擬環境
if [ ! -d "../venv" ]; then
    echo "錯誤: 找不到虛擬環境 ../venv"
    exit 1
fi

# 啟動虛擬環境
echo "啟動Python虛擬環境..."
source ../venv/bin/activate

# 檢查並安裝依賴
echo "檢查Python依賴..."
cd automation
pip install -r requirements.txt

# 執行自動化測試
echo "執行自動化測試..."
pytest test_api_automation.py -v --html=reports/report.html --self-contained-html

# 檢查測試結果
if [ $? -eq 0 ]; then
    echo "自動化測試完成"
else
    echo "自動化測試失敗"
fi

# 回到根目錄
cd ..

# 檢查K6是否安裝
if ! command -v k6 &> /dev/null; then
    echo "警告: K6未安裝，跳過壓力測試"
    echo "請安裝K6: https://k6.io/docs/getting-started/installation/"
else
    echo "執行壓力測試..."
    cd stress_test
    k6 run k6_stress_test.js
    cd ..
fi

echo "=== 測試完成 ==="
echo "測試報告位置:"
echo "- 自動化測試: automation/reports/report.html"
echo "- 壓力測試: stress_test/stress_test_summary.json"
echo ""
echo "請將專案上傳到GitHub: jamesja64/CathayT" 