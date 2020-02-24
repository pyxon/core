import os
import queue
import sys
import threading
import time
from uuid import uuid4

import grpc

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "build"))


from build import control_pb2
from build import control_pb2_grpc


def print_stream(stream):
    for message in stream:
        print("<<<\n")
        print(message)


def generate_heartbeats():
    global control_queue
    while True:
        control_queue.put(control_pb2.PlatformInboundInstruction(heartbeat=control_pb2.Heartbeat()))
        time.sleep(5)


def process_control_messages():
    global control_queue
    while True:
        message = control_queue.get()
        print(f'>>> Message:\n{message}')
        yield message
        control_queue.task_done()


def run_control_stream():
    print_stream(stub.OpenStream(process_control_messages()))


channel = grpc.insecure_channel("localhost:8124")
stub = control_pb2_grpc.PlatformServiceStub(channel)
client_identification = control_pb2.ClientIdentification(client_id=uuid4().hex, component_name='test-client')

print(">>> GetPlatformServer")
platform_info = stub.GetPlatformServer(client_identification)
print(f"<<< PlatformInfo:\n{platform_info}")

control_queue = queue.Queue()
control_queue.put(control_pb2.PlatformInboundInstruction(register=client_identification))
control_thread = threading.Thread(target=run_control_stream)
control_thread.start()

heartbeat_thread = threading.Thread(target=generate_heartbeats)
heartbeat_thread.start()
