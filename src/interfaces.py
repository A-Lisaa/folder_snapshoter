from abc import abstractmethod


class ICompressable:
    @abstractmethod
    def to_compressed_json(self) -> list:
        ...

    @classmethod
    @abstractmethod
    def from_compressed_json(cls, compressed_json: list):
        ...
