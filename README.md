# flask 快速开发模板

### 一、操作说明

仅需要在`src`目录下编辑您的api代码即可，事关部署，请使用`docker-compose up -d`来进行

### 二、结构说明

```shell
.
├── Dockerfile          # api dockerfile
├── README.md           
├── build.py            # 部分命令行工具
├── db                  # 数据库相关 
│   └── password.txt    # mysql密码
├── docker-compose.yml  # 内容请结合实际情况进行插拔
├── nginx               # nginx
│   ├── APIProxy        # nginx api代理
│   └── StaticProxy     # nginx 静态文件代理
├── requirements.txt    # python 环境依赖
└── src                 # api server
    ├── app
    │   └── app.py
    └── main.py
```