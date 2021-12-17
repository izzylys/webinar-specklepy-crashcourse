from random import random
from typing import List
from devtools import debug
from specklepy.objects import Base
from specklepy.objects.geometry import Box, Line, Point
from specklepy.api.credentials import StreamWrapper
from specklepy.api import operations
from specklepy.objects.other import RenderMaterial


class CustomObject(
    Base,
    speckle_type="MyCustomType",  # overwrite the class name (would default to `CustomObject`)
    chunkable={"vertices": 5000},  # will be detached and chunked
    detachable={"material"},  # will be detached
    serialize_ignore={"is_at_origin"},  # will not get serialised
):
    """An example custom object"""

    basePoint: Point = None
    vertices: List[float] = None
    material: RenderMaterial = None
    name: str = None
    bbox: Box = None

    def __init__(
        self, basePoint: Point = Point(), vertices: List[float] = [], **kwargs
    ) -> None:
        super().__init__(basePoint=basePoint, vertices=vertices, **kwargs)

    @property
    def is_at_origin(self):
        if not self.basePoint:
            return False
        return self.basePoint.to_list() == [0.0, 0.0, 0.0]


class Level(Base, speckle_type="Objects.BuiltElements.Level"):
    """A custom Level class"""

    name: str = None
    elevation: float = None

    def __repr__(self) -> str:
        return f"Level(id: {self.id}, name: {self.name}, elevation: {self.elevation})"


class RevitBeam(
    Base, speckle_type="Objects.BuiltElements.Revit.RevitBeam", detachable={"level"}
):
    """A custom RevitBeam class"""

    type: str = None
    baseLine: Line = None
    level: Level = None
    comment: str = None
    unit_price: float = None

    def __repr__(self) -> str:
        return f"RevitBeam(id: {self.id}, type: {self.type}, level: {self.level}, baseline: {self.baseLine})"


# create some beams
level = Level(name="Level 0", elevation=0)
beams = [
    RevitBeam(
        type="UB305x165x40",
        level=level,
        baseLine=Line(
            start=Point(x=i),
            end=Point(x=i, y=2 + 2 * random()),
        ),
    )
    for i in range(10)
]
# create a commit object
commit_obj = Base()
commit_obj["@Revit Beams From Python"] = beams


# get clients and transports
wrap = StreamWrapper("https://speckle.xyz/streams/4def62ca5a")
client = wrap.get_client()
transport = wrap.get_transport()

# send the object
object_id = operations.send(commit_obj, [transport])

# create the commit
client.commit.create(wrap.stream_id, object_id, message="sent some beams from Python")
