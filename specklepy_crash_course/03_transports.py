import ujson as json
from devtools import debug
from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import StreamWrapper, get_default_account

from specklepy.transports.server import ServerTransport
from specklepy.transports.memory import MemoryTransport
from specklepy.transports.sqlite import SQLiteTransport


# ~ 1. Creating transports manually
# transports allow you to:
# (1) serialise objects and persist them to storage
# (2) deserialise json from storage into objects in memory

client = SpeckleClient(host="latest.speckle.dev")
account = get_default_account()
client.authenticate(token=account.token)

# read and write from a speckle server
# it requires a client and a stream id
server_t = ServerTransport(stream_id="aea00799d3", client=client)

# read and write from memory
memory_t = MemoryTransport()  # no args required

# read and write from your local db (defaults to the one at APPDATA/Roaming/Speckle/Objects.db)
sqlite_t = SQLiteTransport()  # no args required


# ~ 2. Getting server transports from the `StreamWrapper`

wrapper = StreamWrapper(
    "https://latest.speckle.dev/streams/0c6ad366c4/commits/a48d5da671"
)

# the stream wrapper gives you an authenticated server transport provided you have a corresponding local account
transport = wrapper.get_transport()
wrapper_client = wrapper.get_client()

# ~ 3. Using transports to send and receive

commit = wrapper_client.commit.get(wrapper.stream_id, wrapper.commit_id)

commit_obj = operations.receive(commit.referencedObject, transport)
debug(commit_obj)

hash = operations.send(commit_obj, [transport])
debug(hash)

# if you want to, you can also serialise and deserialise yourself
json_string = operations.serialize(commit_obj)
debug(json.loads(json_string))
base_object = operations.deserialize(json_string)
debug(base_object)
