# API 規格說明

## 參考網頁
- **API Path**: `https://api.practicesoftwaretesting.com`

## API 可用方法

### GET 請求
- **產品查詢**: `https://api.practicesoftwaretesting.com/products?between=price,1,78`
- **產品排序**: `https://api.practicesoftwaretesting.com/products?sort=name,asc&between=price,1,100&page=0`
- **單一產品**: `https://api.practicesoftwaretesting.com/products/01JP2ABXF9J8J0YADSKV8BXH92`

### POST 請求
- **發送訊息**: `https://api.practicesoftwaretesting.com/messages`

## API 查詢參數

### GET 參數
- **page**: 分頁參數，例如: `page=1`
- **between**: 價格範圍查詢，例如: `between=price,1,21`
- **sort**: 排序參數，例如: `sort=name,asc` 或 `sort=name,desc`

## API 回應欄位/屬性

### GET 產品回應範例
```json
{
  "id": "1",
  "name": "new brand",
  "description": "Lorum ipsum",
  "price": 9.99,
  "is_location_offer": 1,
  "is_rental": 0,
  "in_stock": 0,
  "brand": {
    "id": "string",
    "name": "new brand",
    "slug": "new-brand"
  },
  "category": {
    "id": "string",
    "parent_id": "string",
    "name": "new category",
    "slug": "new-category",
    "sub_categories": [
      "string"
    ]
  },
  "product_image": {
    "by_name": "string",
    "by_url": "string",
    "source_name": "string",
    "source_url": "string",
    "file_name": "string",
    "title": "string",
    "id": "string"
  }
}
```

## API Product Request Object/屬性

### POST 訊息請求範例
```json
{
  "name": "AA AA",
  "subject": "return",
  "message": "Quality is not an act, it is a habit. Strive for excellence every day!",
  "email": "AAAA@gmail.com"
}
```

## 測試重點
1. **GET 產品查詢功能**
   - 基本查詢功能
   - 價格範圍篩選
   - 排序功能
   - 分頁功能
   - 單一產品查詢

2. **POST 訊息功能**
   - 訊息發送
   - 資料驗證
   - 錯誤處理

3. **邊界條件測試**
   - 無效參數
   - 空值處理
   - 極限值測試 