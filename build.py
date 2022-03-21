import itertools
import os
import subprocess

import click
import paramiko

IMAGE_NAME = "flasktemplate:latest"
INNER_PORT = 5000
EXPORT = 5000
ZIP_FILENAME = "temp.tar.gz"
UNZIP_FILEPATH = "_temp"
CLEAN_BUILD_LIST = [
    "docker rm -f $(docker ps -aq)",
    "docker rmi -f %s" % IMAGE_NAME,
]

BUILD_LIST = [
    "docker build -t %s ." % IMAGE_NAME,
]

RUN_BUILD_LIST = [
    "docker run -itd -p %d:%d %s" % (EXPORT, INNER_PORT, IMAGE_NAME),
]


class SSHConnection(object):

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = password

    def connect(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.pwd)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def run_cmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        res = self.to_str(stdout.read())
        # 获取错误信息
        error = self.to_str(stderr.read())

        return res, error

    def upload(self, local_path, target_path):
        # 连接，上传
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.put(local_path, target_path, confirm=True)
        # 增加权限
        # sftp.chmod(target_path, os.stat(local_path).st_mode)
        sftp.chmod(target_path, 0o755)

    def download(self, target_path, local_path):
        # 连接，下载
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 将location.py 下载至服务器 /tmp/test.py
        sftp.get(target_path, local_path)

    def to_str(self, bytes_or_str):
        if isinstance(bytes_or_str, bytes):
            value = bytes_or_str.decode('utf-8')
        else:
            value = bytes_or_str
        return value

    def __del__(self):
        self.close()


@click.Group
def cli():
    pass


@cli.command(help="清理...")
def clean():
    for cmd in CLEAN_BUILD_LIST:
        subprocess.run(cmd, shell=True)


@cli.command(help="构建...")
def build():
    for cmd in BUILD_LIST:
        subprocess.run(cmd, shell=True)


@cli.command(help="运行...")
def run():
    for cmd in RUN_BUILD_LIST:
        subprocess.run(cmd, shell=True)


@cli.command(help="构建并运行...")
def build_run():
    for cmd in itertools.chain(CLEAN_BUILD_LIST, BUILD_LIST, RUN_BUILD_LIST):
        subprocess.run(cmd, shell=True)


@click.option("--port", default=22, help="远程服务器端口...")
@click.option("--password", "-p", required=True, hide_input=True, help="远程服务器密码...", prompt="远程服务器密码")
@click.option("--username", "-u", required=True, help="远程服务器用户名...", prompt="远程服务器用户名")
@click.option("--host", "-h", required=True, help="远程服务器地址...", prompt="远程服务器地址")
@cli.command(help="服务器编译启动...")
def remote_build(host, username, password, port):
    ssh = SSHConnection(host, port, username, password)
    ssh.connect()

    # 1. 压缩代码文件
    subprocess.run("tar --exclude env -zcf %s  *" % ZIP_FILENAME, shell=True)
    # 2. 将文件传输至远端
    ssh.upload(ZIP_FILENAME, ZIP_FILENAME)
    # 3. 远端解压
    ssh.run_cmd("tar -zxvf %s -C %s" % (ZIP_FILENAME, UNZIP_FILEPATH))
    # 4. 远端构建
    for cmd in CLEAN_BUILD_LIST:
        ssh.run_cmd("cd %s;%s" % (UNZIP_FILEPATH, cmd))
    for cmd in BUILD_LIST:
        ssh.run_cmd("cd %s;%s" % (UNZIP_FILEPATH, cmd))
    # 5. 清理文件
    ssh.run_cmd("rm -rf %s" % ZIP_FILENAME)
    ssh.run_cmd("rm -rf %s" % UNZIP_FILEPATH)
    os.remove(ZIP_FILENAME)


if __name__ == "__main__":
    cli()
