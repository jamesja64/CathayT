# Cathay API 測試專案

## 專案概述
本專案包含完整的API測試解決方案，涵蓋手動測試案例設計、Postman測試集合、自動化測試腳本和壓力測試。

## 專案結構
```
Cathay/
├── README.md                    # 專案說明
├── test_cases/                  # 測試案例
│   ├── API_Test_Cases.xlsx      # API測試案例設計
│   └── test_cases_summary.md    # 測試案例摘要
├── postman/                     # Postman測試集合
│   ├── Cathay_API_Tests.postman_collection.json
│   └── Cathay_API_Environment.postman_environment.json
├── automation/                  # 自動化測試
│   ├── requirements.txt         # Python依賴
│   ├── conftest.py             # Pytest配置
│   ├── test_api_automation.py  # 自動化測試腳本
│   └── reports/                # 測試報告
├── stress_test/                # 壓力測試
│   ├── k6_stress_test.js       # K6壓力測試腳本
│   ├── stress_test_plan.md     # 壓力測試計畫
│   └── reports/                # 壓力測試報告
└── docs/                       # 文檔
    └── api_specifications.md   # API規格說明
```

## 測試目標API
- Base URL: `https://api.practicesoftwaretesting.com`
- 主要端點: `/products`, `/messages`

## 執行方式

### 1. 手動測試案例
- 查看 `test_cases/API_Test_Cases.xlsx` 檔案

### 2. Postman測試
- 匯入 `postman/` 資料夾中的集合和環境檔案
- 執行測試集合

### 3. 自動化測試
```bash
cd automation
pip install -r requirements.txt
pytest test_api_automation.py -v --html=reports/report.html
```

### 4. 壓力測試
```bash
cd stress_test
k6 run k6_stress_test.js
```

## 測試優先級說明
- P1: 高優先級 - 核心功能測試
- P2: 中優先級 - 重要功能測試  
- P3: 低優先級 - 邊界條件測試

## 測試結果說明
- P: Pass (通過)
- F: Fail (失敗)
- U: Untested (未測試)
- B: Blocked (阻塞)
- N/A: Not Applicable (不適用) 