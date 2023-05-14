# Compile PROTO

`python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. auth_service.proto`

# Executar

`python3 server.py && python3 client.py`
