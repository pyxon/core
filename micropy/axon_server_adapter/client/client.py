import queue
import threading
import time
from uuid import uuid4

import grpc

from build import control_pb2
from build import control_pb2_grpc


class AxonServerClient:

    def __init__(self):
        self._channel = grpc.insecure_channel('localhost:8124')
        self._stub = control_pb2_grpc.PlatformServiceStub(self._channel)
        self._client_id = uuid4().hex
        self._control_queue = queue.Queue()
        self._is_running = False
        self._running_lock = threading.Lock()

    def run(self, component_name: str):
        with self._running_lock:
            if self._is_running:
                return
            self._is_running = True

        client_identification = control_pb2.ClientIdentification(
            client_id=self._client_id,
            component_name=component_name,
        )
        self._stub.GetPlatformServer(client_identification)
        self._control_queue.put(control_pb2.PlatformInboundInstruction(register=client_identification))
        control_thread = threading.Thread(target=self._run_control_stream)
        control_thread.start()
        heartbeat_thread = threading.Thread(target=self._generate_heartbeats)
        heartbeat_thread.start()

    def _run_control_stream(self):
        for message in self._stub.OpenStream(self._process_control_messages()):
            print(f"<<<\n{message}")

    def _process_control_messages(self):
        while True:
            message = self._control_queue.get()
            print(f'>>> Message:\n{message}')
            yield message
            self._control_queue.task_done()

    def _generate_heartbeats(self):
        while True:
            self._control_queue.put(control_pb2.PlatformInboundInstruction(heartbeat=control_pb2.Heartbeat()))
            time.sleep(5)

