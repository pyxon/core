import itertools
import threading
import time
from uuid import uuid4

import grpc

import control_pb2
import control_pb2_grpc


def print_stream(stream):
    for message in stream:
        print('=====')
        print(message)


def generate_heartbeats():
    while True:
        print('=== Heartbeat ===')
        yield control_pb2.PlatformInboundInstruction(heartbeat=control_pb2.Heartbeat())
        time.sleep(5)


def run_control_stream():
    output_stream = stub.OpenStream(itertools.chain(
        [control_pb2.PlatformInboundInstruction(register=client_identification, instruction_id=uuid4().hex)],
        generate_heartbeats(),
    ))
    print_stream(output_stream)


channel = grpc.insecure_channel('localhost:8124')
stub = control_pb2_grpc.PlatformServiceStub(channel)
client_identification = control_pb2.ClientIdentification(client_id=uuid4().hex, component_name='test-client')

print('=== GetPlatformServer ===')
print(stub.GetPlatformServer(client_identification))

control_thread = threading.Thread(target=run_control_stream)
control_thread.start()
