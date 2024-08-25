# Heavy Query gRPC server

Simple gRPC server for getting user data from PostgreSQL with 1 million entry.

## How To Launch

```bash
$ docker compose up -d
```

## How To Use

Use `app/protobuf/server.proto` to load RPC API.

Use RPC func `sum_amount` with fields `user_id`, `datetime_from` and `datetime_to`.

You will get answer from server with fields `time_for_execution_ms` and `total_sum`

## Develop

For creating py files from `.proto`

```bash
$ python3 -m grpc_tools.protoc -I ./protobufs --python_out=./protobufs --grpc_python_out=./protobufs ./protobufs/server.proto
```

Than change 6 row from `app/protobufs/server_pb2_grpc.py` on 

```python
from . import server_pb2 as server__pb2
```