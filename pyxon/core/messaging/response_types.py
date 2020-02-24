from typing import Type


class ResponseType:
    pass


class ResponseTypes:

    @classmethod
    def instance_of(cls, response_class: Type) -> ResponseType:
        return ResponseType()
