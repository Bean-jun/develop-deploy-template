FROM    python:latest
LABEL   version="0.1"
RUN     mkdir /var/runtime
ENV     work_path=/var/runtime
WORKDIR ${work_path}
COPY    requirements.txt ${work_path}
COPY    src ${work_path}
RUN     python -m pip install --user -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE  5000
CMD     [ "python", "main.py" ]
