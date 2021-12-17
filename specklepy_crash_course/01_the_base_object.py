import ujson as json
from devtools import debug
from specklepy.api import operations
from specklepy.objects import Base
from specklepy.objects.geometry import *
from specklepy.objects.other import *
from specklepy.transports.memory import MemoryTransport


# ~ 1. a simple base object
# can be initialised with no arguments, or with keyword arguments
base_obj = Base()
another_base = Base(units="feet")

# you can add whatever attributes you want - of pretty much any time (including other Base objects)
base_obj.name = "a simple speckle object"
base_obj["some_numbers"] = [1, 2, 3]
base_obj.more_bases = {"a": Base(label="a"), "b": Base(label="b")}

# you can access these attributes using either dict or dot notation
debug(base_obj["name"])
debug(base_obj.some_numbers)
debug(base_obj["more_bases"])

# prepend with `_` if you don't want the attribute to be serialised
base_obj["_stuff"] = "this stuff won't get serialised"

# prepend with `@` if you want to detach an attribute
base_obj["@detach this"] = another_base

# the `speckle_type` is a protected prop that cannot be changed because it is used in serialisation
base_obj.speckle_type = "this won't work"

# `units` is also a special prop in that in only supports valid units (stored as the string abbreviation) or None
# the setter will infer what unit you want regardless of if you use the abbreviation or american / intl spelling
another_base.units = "meter"
debug(another_base.units)  # 'm'
another_base.units = "cm"
debug(another_base.units)  # 'cm'
another_base.units = "metres"
debug(another_base.units)  # 'm'


# ~ 2. some handy methods on `Base`

# get the names of all attributes and properties that will get serialised
to_be_serialized = base_obj.get_serializable_attributes()

# get the names of all attributes that have been added dynamically (aka those not listed in the class definition)
dynamic_members = base_obj.get_dynamic_member_names()

# get the names of all the attributes that are defined in the class definition
typed_members = base_obj.get_typed_member_names()

# computes the id of a base object - useful for determining if two objects are the same
# (note that this serialises the whole object and therefore has a cost!)
object_id = base_obj.get_id()


# ~ 3. serialisation
# all base objects and objects that inherit from base will be serialisable through speckle
serialised_base = operations.serialize(base_obj)
debug(json.loads(serialised_base))

# when an attribute is detached, a reference object will be in its place
serialised_base = operations.serialize(base_obj, [MemoryTransport()])
debug(json.loads(serialised_base))


# ~ 4. included speckle objects
# `geometry` holds basic geometry (ex points, vectors, planes, lines, curves, meshes, breps)
pt1 = Point()
pt2 = Point(x=2, y=5)

line = Line(start=pt1, end=pt2)
debug(line)
debug(line.end)

# `other` holds things like materials, transforms, and blocks
material = RenderMaterial(name="cloudy", opacity=0.4)

identity_transform = Transform.from_list()

block_def = BlockDefinition(geometry=[line])

block_inst = BlockInstance(blockDefinition=block_def)
block_inst.transform = identity_transform

# ~ structural objects are coming soon!
