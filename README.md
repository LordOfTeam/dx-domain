请求接口：domain/check?domain=xxx

响应：
    成功：
        status = 200
    失败：
        status = 400
    数据部分：
        {
            "status": 200, // 状态码
            "data": {
                "ipv4": "",
                "ipv6": "",
                "localdns": "",
                "pinginfo": ,
                "checktime": "",
                "mediacdn": ""
            }
        }