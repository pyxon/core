import json
import queue
import threading
import time
from json import JSONEncoder
from uuid import UUID
from uuid import uuid4

import dataclasses
import grpc

from build import common_pb2
from build import command_pb2
from build import command_pb2_grpc
from build import control_pb2
from build import control_pb2_grpc


class CustomJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, UUID):
            return o.hex
        return super().default(o)


class AxonServerClient:

    def __init__(self, component_name: str):
        self._client_id = uuid4().hex
        self._component_name = component_name
        self._channel = grpc.insecure_channel('localhost:8124')
        self._platform_service = control_pb2_grpc.PlatformServiceStub(self._channel)
        self._command_service = command_pb2_grpc.CommandServiceStub(self._channel)
        self._control_queue = queue.Queue()
        self._subscribe_command_queue = queue.Queue()
        self._is_running = False
        self._running_lock = threading.Lock()

    def run(self):
        with self._running_lock:
            if self._is_running:
                return
            self._is_running = True

        client_identification = control_pb2.ClientIdentification(
            client_id=self._client_id,
            component_name=self._component_name,
        )
        self._platform_service.GetPlatformServer(client_identification)
        self._control_queue.put(control_pb2.PlatformInboundInstruction(register=client_identification))
        control_thread = threading.Thread(target=self._run_control_stream)
        control_thread.start()
        heartbeat_thread = threading.Thread(target=self._generate_heartbeats)
        heartbeat_thread.start()
        subscribe_command_thread = threading.Thread(target=self._subscribe_commands)
        subscribe_command_thread.start()

    def _run_control_stream(self):
        for message in self._platform_service.OpenStream(self._process_control_messages()):
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
            time.sleep(300)

    def dispatch_command(self, command):
        command_response = self._command_service.Dispatch(command_pb2.Command(
            message_identifier=uuid4().hex,
            name=command.__class__.__name__,
            timestamp=int(time.time()),
            payload=common_pb2.SerializedObject(
                type=command.__class__.__name__,
                revision='1',
                data=json.dumps(dataclasses.asdict(command), cls=CustomJSONEncoder).encode(),
            ),
            processing_instructions=[],
            client_id=self._client_id,
            component_name=self._component_name,
        ))
        print(f'>>> CommandResponse:\n{command_response}')

    def subscribe_commands(self, commands):
        for command in commands:
            self._subscribe_command_queue.put(command_pb2.CommandProviderOutbound(
            subscribe=command_pb2.CommandSubscription(
                message_id=uuid4().hex,
                command=command.__name__,
                component_name=self._component_name,
                client_id=self._client_id,
                load_factor=0,
            ),
        ))

    def _subscribe_commands(self):
        for message in self._command_service.OpenStream(self._process_subscribe_command_messages()):
            print(f"<<<\n{message}")

    def _process_subscribe_command_messages(self):
        while True:
            message = self._subscribe_command_queue.get()
            print(f'>>> Subscribe Command Message:\n{message}')
            yield message
            self._subscribe_command_queue.task_done()
