
# 🛠️ PC Builder 项目 API 接口文档

0.管理员页面

## 1. 获取所有组件类别（大类）
- **路径 (URL)**: `/api/component-types/`
- **方法**: GET
- **说明**: 获取所有组件类别（如 CPU, GPU, 主板等）
- **请求参数**: 无
- **返回示例**:
```json
{
  "types": ["CPU", "GPU", "Mainboard"]
}
```
错误示例:
```json
{
  "error": "Internal Server Error",
  "message": "无法获取组件类别"
}
```
---

## 2. 获取某类别下的所有产品（列表）

- **路径 (URL)**: `/api/products/`
- **方法**: `GET`
- **说明**: 获取某一类别下所有产品

### 请求参数:

| 参数名 | 类型    | 是否必须 | 说明                          |
|------|-------|------|-----------------------------|
| type | string | 必须   | 组件类别 (如 `CPU`, `GPU`) |

---

### 返回示例:

```json
{
  "type": "CPU",  // 当前查询的组件类别
  "products": [
    { "sku": 123, "productName": "Intel i7 12700K", "brand": "Intel" },
    { "sku": 234, "productName": "AMD Ryzen 5800X", "brand": "AMD" }
  ]
}

```
错误示例: (如果没有找到对应类别的产品)
```json
{
  "error": "Not Found",
  "message": "无法找到该类别的产品"
}
```


---

## 3. 获取某个产品的详细规格
- **路径 (URL)**: `/api/product/<sku>/specs/`
- **方法**: GET
- **说明**: 获取指定产品的所有规格
- **请求参数**: 无（通过 URL 提供 SKU）
- **返回示例**:
```json
{
  "specs": {
    "socket": "AM4",
    "功耗": "95W",
    "接口": "PCIe 4.0"
  }
}
```
错误示例: (如果没有找到对应 SKU 的产品)
```json
{
  "error": "Not Found",
  "message": "无法找到该产品的规格"
}
```

---

## 4. 动态检查兼容性 + 返回剩余可选产品
- **路径 (URL)**: `/api/compatible-products/`
- **方法**: GET
- **说明**: 根据当前已选组件，自动屏蔽不兼容产品，返回剩余可选产品
- **请求参数**:
  - `selected` (string): 已选产品 SKU 列表，用逗号分隔，如 `123,234`
- **返回示例**:
```json
{
  "compatible": {
    "CPU": [
      { "sku": 123, "product_name": "Intel i7 12700K" }
    ],
    "GPU": [
      { "sku": 345, "product_name": "NVIDIA RTX 4080" }
    ],
    "Mainboard": []
  }
}
```
错误示例  (如果没有找到对应 SKU 的产品):
```json
{
  "error": "Not Found",
  "message": "无法找到该产品"
}
```

---

## 5. 添加产品到 PC List
- **路径 (URL)**: `/api/pc-list/`
- **方法**: POST
- **说明**: 添加产品到用户 PC List
- **请求体 (body)**:
```json
{
  "sku": 123
}
```
- **返回示例**:
```json
{
  "success": true,
  "message": "已添加到 PC List"
}
```


---

## 6. 查看当前 PC List
- **路径 (URL)**: `/api/pc-list/`
- **方法**: GET
- **说明**: 获取当前已选 PC List
- **请求参数**: 无
- **返回示例**:
```json
{
  "pc_list": [
    { "sku": 123, "product_name": "Intel i7 12700K", "category": "CPU" },
    { "sku": 345, "product_name": "华硕主板 Z690", "category": "Mainboard" }
  ]
}
```

---

## 7. 从 PC List 中移除组件
- **路径 (URL)**: `/api/pc-list/remove/`
- **方法**: POST
- **说明**: 从 PC List 中移除指定产品
- **请求体 (body)**:
```json
{
  "sku": 123
}
```
- **返回示例**:
```json
{
  "success": true,
  "message": "已从 PC List 移除"
}
```

---

## 8. 完成并保存最终 PC List
- **路径 (URL)**: `/api/pc-list/save/`
- **方法**: POST
- **说明**: 保存当前 PC List 作为最终配置
- **请求体 (body)**:
```json
{
  "pc_list": [123, 345, 567]
}
```
- **返回示例**:
```json
{
  "success": true,
  "message": "配置已保存"
}
```
