import pytest
import requests
import json
import time
from datetime import datetime

class TestProductsAPI:
    """產品API測試類別"""
    
    @pytest.mark.p1
    def test_get_products_basic(self, session, api_base_url):
        """測試基本產品查詢功能 (P1)"""
        url = f"{api_base_url}/products"
        response = session.get(url)
        
        assert response.status_code == 200, f"預期狀態碼200，實際為{response.status_code}"
        
        data = response.json()
        assert 'data' in data, "回應中應包含data欄位"
        assert isinstance(data['data'], list), "data應為陣列格式"
        assert len(data['data']) > 0, "data陣列不應為空"
        
        # 驗證產品基本欄位
        product = data['data'][0]
        required_fields = ['id', 'name', 'price']
        for field in required_fields:
            assert field in product, f"產品應包含{field}欄位"
    
    @pytest.mark.p1
    def test_get_products_price_range(self, session, api_base_url, test_data):
        """測試價格範圍篩選功能 (P1)"""
        price_range = test_data['price_ranges'][0]  # 1-78
        url = f"{api_base_url}/products?between=price,{price_range['min']},{price_range['max']}"
        response = session.get(url)
        
        assert response.status_code == 200, f"預期狀態碼200，實際為{response.status_code}"
        
        data = response.json()
        assert 'data' in data, "回應中應包含data欄位"
        
        # 驗證所有產品價格都在指定範圍內
        for product in data['data']:
            price = product['price']
            assert price_range['min'] <= price <= price_range['max'], \
                f"產品價格{price}應在範圍{price_range['min']}-{price_range['max']}內"
    
    @pytest.mark.p1
    def test_get_products_sort_and_page(self, session, api_base_url):
        """測試排序和分頁功能 (P1)"""
        url = f"{api_base_url}/products?sort=name,asc&between=price,1,100&page=0"
        response = session.get(url)
        
        assert response.status_code == 200, f"預期狀態碼200，實際為{response.status_code}"
        
        data = response.json()
        assert 'data' in data, "回應中應包含data欄位"
        
        # 驗證排序（升序）
        if len(data['data']) > 1:
            names = [product['name'] for product in data['data']]
            sorted_names = sorted(names)
            assert names == sorted_names, "產品應按名稱升序排列"
    
    @pytest.mark.p1
    def test_get_single_product(self, session, api_base_url):
        """測試單一產品查詢功能 (P1)"""
        # 先獲取一個產品ID
        products_url = f"{api_base_url}/products"
        products_response = session.get(products_url)
        products_data = products_response.json()
        
        if products_data['data']:
            product_id = products_data['data'][0]['id']
            url = f"{api_base_url}/products/{product_id}"
            response = session.get(url)
            
            assert response.status_code == 200, f"預期狀態碼200，實際為{response.status_code}"
            
            product = response.json()
            required_fields = ['id', 'name', 'price', 'description', 'brand', 'category']
            for field in required_fields:
                assert field in product, f"產品應包含{field}欄位"
    
    @pytest.mark.p2
    def test_get_products_invalid_id(self, session, api_base_url):
        """測試無效產品ID查詢 (P2)"""
        url = f"{api_base_url}/products/invalid-id-12345"
        response = session.get(url)
        
        # 預期404或400錯誤
        assert response.status_code in [404, 400], \
            f"無效ID應返回404或400，實際為{response.status_code}"
    
    @pytest.mark.p2
    def test_get_products_invalid_price_range(self, session, api_base_url):
        """測試無效價格範圍 (P2)"""
        url = f"{api_base_url}/products?between=price,100,1"  # 最大值小於最小值
        response = session.get(url)
        
        # 預期400錯誤或空結果
        assert response.status_code in [200, 400], \
            f"無效價格範圍應返回400或200，實際為{response.status_code}"
    
    @pytest.mark.p3
    def test_get_products_special_characters(self, session, api_base_url):
        """測試特殊字符處理 (P3)"""
        url = f"{api_base_url}/products?sort=name,invalid_sort"
        response = session.get(url)
        
        # 預期400錯誤或忽略無效參數
        assert response.status_code in [200, 400], \
            f"無效排序參數應返回400或200，實際為{response.status_code}"


class TestMessagesAPI:
    """訊息API測試類別"""
    
    @pytest.mark.p1
    def test_post_message_valid(self, session, api_base_url, test_data):
        """測試發送有效訊息 (P1)"""
        url = f"{api_base_url}/messages"
        payload = test_data['valid_message']
        
        response = session.post(url, json=payload)
        
        # 預期200或201成功狀態
        assert response.status_code in [200, 201], \
            f"有效訊息應返回200或201，實際為{response.status_code}"
        
        # 驗證回應內容
        response_data = response.json()
        assert 'message' in response_data or 'success' in str(response_data).lower(), \
            "回應應包含成功訊息"
    
    @pytest.mark.p2
    def test_post_message_invalid_data(self, session, api_base_url, test_data):
        """測試發送無效訊息 (P2)"""
        url = f"{api_base_url}/messages"
        payload = test_data['invalid_message']
        
        response = session.post(url, json=payload)
        
        # 預期400或422錯誤
        assert response.status_code in [400, 422], \
            f"無效資料應返回400或422，實際為{response.status_code}"
        
        # 驗證錯誤訊息
        response_data = response.json()
        assert 'error' in response_data or 'message' in response_data, \
            "錯誤回應應包含錯誤訊息"
    
    @pytest.mark.p2
    def test_post_message_missing_fields(self, session, api_base_url):
        """測試缺少必填欄位 (P2)"""
        url = f"{api_base_url}/messages"
        payload = {
            "name": "Test User"
            # 缺少其他必填欄位
        }
        
        response = session.post(url, json=payload)
        
        # 預期400或422錯誤
        assert response.status_code in [400, 422], \
            f"缺少必填欄位應返回400或422，實際為{response.status_code}"
    
    @pytest.mark.p3
    def test_post_message_empty_payload(self, session, api_base_url):
        """測試空載荷 (P3)"""
        url = f"{api_base_url}/messages"
        payload = {}
        
        response = session.post(url, json=payload)
        
        # 預期400或422錯誤
        assert response.status_code in [400, 422], \
            f"空載荷應返回400或422，實際為{response.status_code}"


class TestAPIPerformance:
    """API效能測試類別"""
    
    @pytest.mark.p2
    def test_response_time(self, session, api_base_url):
        """測試回應時間 (P2)"""
        url = f"{api_base_url}/products"
        
        start_time = time.time()
        response = session.get(url)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # 轉換為毫秒
        
        assert response.status_code == 200, f"預期狀態碼200，實際為{response.status_code}"
        assert response_time < 5000, f"回應時間應小於5秒，實際為{response_time:.2f}ms"
    
    @pytest.mark.p3
    def test_concurrent_requests(self, session, api_base_url):
        """測試並發請求 (P3)"""
        import threading
        import queue
        
        url = f"{api_base_url}/products"
        results = queue.Queue()
        
        def make_request():
            try:
                response = session.get(url)
                results.put(response.status_code)
            except Exception as e:
                results.put(f"Error: {e}")
        
        # 建立5個並發請求
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # 等待所有線程完成
        for thread in threads:
            thread.join()
        
        # 檢查結果
        success_count = 0
        while not results.empty():
            result = results.get()
            if result == 200:
                success_count += 1
        
        assert success_count >= 4, f"至少4個請求應成功，實際成功{success_count}個"


if __name__ == "__main__":
    # 直接執行測試
    pytest.main([__file__, "-v", "--html=reports/report.html", "--self-contained-html"]) 