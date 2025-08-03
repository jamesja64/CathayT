import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

// 自定義指標
const errorRate = new Rate('errors');

// 測試配置
export const options = {
  stages: [
    // 預熱階段
    { duration: '10s', target: 1 },
    // 情境一：高並發用戶測試 (10位用戶)
    { duration: '30s', target: 10 },
    { duration: '30s', target: 10 },
    // 情境一：高並發用戶測試 (20位用戶)
    { duration: '30s', target: 20 },
    { duration: '30s', target: 20 },
    // 情境二：持續負載測試 (每秒1位用戶)
    { duration: '60s', target: 1 },
    // 冷卻階段
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95%的請求回應時間應小於500ms
    http_req_failed: ['rate<0.01'],   // 錯誤率應小於1%
    errors: ['rate<0.01'],            // 自定義錯誤率應小於1%
  },
};

// 測試URL
const BASE_URL = 'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@2024-10-01/v1/currencies/twd.json';

// 主要測試函數
export default function () {
  // 發送GET請求
  const response = http.get(BASE_URL);
  
  // 驗證條件一：Response code = 200
  const statusCheck = check(response, {
    'status is 200': (r) => r.status === 200,
  });
  
  // 驗證條件二：Response context 包含 "jpy"
  const contentCheck = check(response, {
    'response contains jpy': (r) => r.body.includes('jpy'),
  });
  
  // 記錄錯誤
  if (!statusCheck || !contentCheck) {
    errorRate.add(1);
  }
  
  // 驗證回應時間
  check(response, {
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  // 驗證回應格式
  check(response, {
    'response is JSON': (r) => {
      try {
        JSON.parse(r.body);
        return true;
      } catch (e) {
        return false;
      }
    },
  });
  
  // 驗證回應內容結構
  if (response.status === 200) {
    try {
      const data = JSON.parse(response.body);
      check(data, {
        'has twd property': (d) => d.hasOwnProperty('twd'),
        'twd is object': (d) => typeof d.twd === 'object',
      });
    } catch (e) {
      errorRate.add(1);
    }
  }
  
  // 隨機等待時間 (0.1-1秒)
  sleep(Math.random() * 0.9 + 0.1);
}

// 設置階段
export function setup() {
  console.log('開始壓力測試...');
  console.log('測試URL:', BASE_URL);
  console.log('預期TPS > 5');
  console.log('預期錯誤率 < 1%');
  console.log('預期回應時間 < 500ms');
}

// 清理階段
export function teardown(data) {
  console.log('壓力測試完成');
  console.log('請查看Summary Report獲取詳細結果');
}

// 處理器函數 - 用於自定義指標
export function handleSummary(data) {
  console.log('=== 壓力測試摘要 ===');
  console.log('總請求數:', data.metrics.http_reqs.values.count);
  console.log('平均回應時間:', data.metrics.http_req_duration.values.avg, 'ms');
  console.log('95%回應時間:', data.metrics.http_req_duration.values['p(95)'], 'ms');
  console.log('錯誤率:', (data.metrics.http_req_failed.values.rate * 100).toFixed(2), '%');
  console.log('TPS:', data.metrics.http_reqs.values.rate.toFixed(2));
  
  // 驗證驗收標準
  const tps = data.metrics.http_reqs.values.rate;
  const errorRate = data.metrics.http_req_failed.values.rate;
  const responseTime = data.metrics.http_req_duration.values['p(95)'];
  
  console.log('\n=== 驗收標準檢查 ===');
  console.log('TPS > 5:', tps > 5 ? '通過' : '失敗');
  console.log('錯誤率 < 1%:', errorRate < 0.01 ? '通過' : '失敗');
  console.log('回應時間 < 500ms:', responseTime < 500 ? '通過' : '失敗');
  
  return {
    'stdout': JSON.stringify(data, null, 2),
    'stress_test_summary.json': JSON.stringify(data, null, 2),
  };
} 