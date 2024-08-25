import os
from concurrent import futures
from datetime import datetime
from time import perf_counter

import grpc
import psycopg2

from protobufs import server_pb2, server_pb2_grpc

PSQL_HOST = os.environ.get("PSQL_HOST", default="localhost")
PSQL_DB = os.environ.get("PSQL_DB", default="postgres")
PSQL_USER = os.environ.get("PSQL_USER", default="postgres")
PSQL_PASSWORD = os.environ.get("PSQL_PASSWORD", default="postgres")


class Server(server_pb2_grpc.ServerServicer):

    def sum_amount(self, request, context):
        with psycopg2.connect(
            host=PSQL_HOST,
            database=PSQL_DB,
            user=PSQL_USER,
            password=PSQL_PASSWORD,
        ) as conn:
            datetime_from = datetime.fromtimestamp(request.datetime_from)
            datetime_to = datetime.fromtimestamp(request.datetime_to)
            with conn.cursor() as cur:
                time_before = perf_counter()
                cur.execute(
                    """
                    SELECT sum(amount)
                    FROM transactions
                    WHERE user_id=%s AND timestamp>=%s AND timestamp<=%s;
                    """,
                    (request.user_id, datetime_from, datetime_to)
                )
                time_for_execution = perf_counter() - time_before
                row = cur.fetchone()

        return server_pb2.SumAmountResponse(
            time_for_execution_ms=time_for_execution * 1000,
            total_sum=row[0],
        )


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    server_pb2_grpc.add_ServerServicer_to_server(Server(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    run()
