# flask 快速开发模板

### 一、操作说明

仅需要在`src`目录下编辑您的api代码即可，事关部署，请使用`docker-compose up -d`来进行

### 二、结构说明

```shell
.
├── Dockerfile
├── LICENSE
├── README.md
├── build.py
├── cert
│   ├── example.crt
│   ├── example.key
│   └── readme.md
├── db
│   ├── mysql
│   │   ├── init
│   │   │   └── init.sql
│   │   └── mysql_env
│   └── redis
│       ├── Dockerfile
│       └── redis.conf
├── docker-compose.yml
├── nginx
│   ├── APIProxy
│   │   ├── Dockerfile
│   │   └── nginx
│   │       ├── certs
│   │       ├── conf.d
│   │       │   ├── default.conf
│   │       │   └── server.conf
│   │       ├── fastcgi.conf
│   │       ├── fastcgi_params
│   │       ├── mime.types
│   │       ├── modules
│   │       ├── nginx.conf
│   │       ├── scgi_params
│   │       └── uwsgi_params
│   └── StaticProxy
│       ├── Dockerfile
│       ├── html
│       │   ├── 50x.html
│       │   └── index.html
│       └── nginx
│           ├── certs
│           ├── conf.d
│           │   └── default.conf
│           ├── fastcgi.conf
│           ├── fastcgi_params
│           ├── mime.types
│           ├── modules
│           ├── nginx.conf
│           ├── scgi_params
│           └── uwsgi_params
├── requirements.txt
└── src
    ├── app
    │   └── app.py
    └── main.py
```

### 三、其他

1. src

    ```shell
    您可以在当前目录编辑您的生产代码
    ```

2. db

    ```shell
    mysql
        mysql_env是启动mysql docker环境的虚拟环境，您可以直接在这里配置您的root密码、配置其他账户、密码以及您将要建立的数据库名
    
        init 用户当前docker启动时需要执行的SQL，这里我们可以为创建的用户分配权限、导入一些基本数据等等
    
    redis
        redis.conf redis的配置文件，我们可以结合自己需求进行更改
    ```

3. nginx

    ```shell
    APIProxy 用于对用户api部分的代理

    StaticProxy 用于对用户静态资源的代理，当然也可以将APIProxy挂载在当前nginx上

    上述均可自由配置nginx.conf
    ```
