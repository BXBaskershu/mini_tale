# 数据库
## Customer
| 字段名 | 含义 | 类型 | 说明 |
| :------: | :------: | :------: | :------: |
| id | 主键id | int | 自增 |
| short_name | 简称 | str |  |
| full_name | 全称 | str |  |
| customer_type | 客户类型 | int | 0 :公司; 1: 个人 |
| telephone | 电话 | str |  |
| create_time | 创建时间 | int | 时间戳 | 

# 接口
接口出错的返回没有列全
## 用户展示
### 简要描述
分页展示用户信息
### 请求路径
`/customer`
### 请求方式
POST
### 请求参数
| 参数名 | 含义 | 类型 | 说明 |
| :------: | :------: | :------: | :------: |
| page | 页码 | int |  |
| per_page | 每页的数目 | int |  |
### 请求示例
```json
{
     "page": 1,
     "per_page": 10
 }
```
### 返回示例
#### 正确
```json
{
    "total": 2,
    "page": 1,
    "pages": 1,
    "customers": [
        {
            "short_name": "hi",
            "full_name": "hiiii",
            "customer_type": "公司用户",
            "telephone": "123456789",
            "create_time": "2019-04-04 17:58:27"
        },
        {
            "short_name": "ysz",
            "full_name": "baskershu",
            "customer_type": "个人用户",
            "telephone": "1234567897",
            "create_time": "2019-04-08 14:18:39"
        }
    ]
}
```
#### 错误
```json
{
    "code": 0,
    "desc": "请求出错",
    "msg": "404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
    "status": 1
}
```
## customer更新
### 简要描述
更新用户的类型，在公司和个人之间进行切换
### 请求路径
`/customer/update`
### 请求方式
POST
### 请求参数
| 参数名 | 含义 | 类型 | 说明 |
| :------: | :------: | :------: | :------: |
| customer_id  | 更新用户的主键id | int |  |
| custoemr_type | 用户lei xing类型| int | 0 :公司; 1: 个人 |
### 请求示例
```json
{
    "customer_id": 1,
    "customer_type": 10
}
```
### 返回示例
#### 正确
```json
{
    "desc": "customer的状态修改成功",
    "msg": "success",
    "status": 0
}
```
#### 错误
```json
{
    "code": 0,
    "desc": "请求出错",
    "msg": "custoemr_id无法定位到一个具体的customer对象",
    "status": 1
}
```
## customer删除
### 简要描述
删除某一固定的customer
### 请求路径
`/customer/delete`
### 请求方式
POST
### 请求参数
| 参数名 | 含义 | 类型 | 说明 |
| :------: | :------: | :------: | :------: |
| customer_id  | 更新用户的主键id | int |  |
### 请求示例
```json
{
    "customer_id": 1,
}
```
### 返回示例
#### 正确
 ```json
 {
     "desc": "删除成功",
     "msg": "success",
     "status": 0
}
```
#### 错误
```json
{
    "code": 0,
    "desc": "请求出错",
    "msg": "custoemr_id无法定位到一个具体的customer对象",
    "status": 1
}
```
## customer新增
### 简要描述
新增一个customer
### 请求路径
`/customer/add`
### 请求方式
POST
### 请求参数
| 参数名 | 含义 | 类型 | 说明 |
| :------: | :------: | :------: | :------: |
| short_name  | 简称 | str |  |
| full_name  | 全称 | str |  |
| telephone  | 电话号码 | str |  |
| customer_typ  | 客户类型 | int | 0 :公司; 1: 个人 |
### 请求示例
```json
{
    "short_name": "ysz",
    "full_name": "baskershu",
    "telephone": "123567897",
    "customer_type": 1
}
```
### 返回示例
#### 正确
```json
{
    "desc": "添加成功",
    "msg": "success",
    "status": 0
}
```
#### 错误
```json
{
    "code": 0,
    "desc": "请求出错",
    "msg": "telephone不是一个有效的电话号码",
    "status": 1
}
```



