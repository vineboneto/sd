```bash
$ source ./venv/bin/activate

$ pip install grpc_tools

$ python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. bingo.proto

$ protoc -I=. --python_out=. bingo.proto
```
