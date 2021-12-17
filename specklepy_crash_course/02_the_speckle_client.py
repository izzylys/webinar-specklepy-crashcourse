from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import (
    StreamWrapper,
    get_local_accounts,
    get_default_account,
)

# ~ 1. Creating and initialising a `SpeckleClient`

# initialise the client
client = SpeckleClient("speckle.xyz")  # or whatever your host is (default is xyz)
# client = SpeckleClient(host="localhost:3000", use_ssl=False) or use local server

# authenticate the client with a token
all_accounts = get_local_accounts()
selected_account = next(
    acct for acct in all_accounts if client.url in acct.serverInfo.url
)
client.authenticate(token=selected_account.token)

# you can also get the default account on your machine like this
account = get_default_account()

# ~ 2. Using the client to talk to your server

# let's retrieve data from this stream
stream_id = "7b253e5c4c"

# get the stream
stream = client.stream.get(stream_id)
print(stream, "\n")
# get a specific branch on the stream
branch = client.branch.get(stream_id, name="main")

# get a specific commit on the stream
commit = client.commit.get(stream_id, commit_id="025fcbb9cf")
print(commit, "\n")

# you can create, edit, delete, manage permissions, etc all with the client! have a play around

# new_stream_id = client.stream.create(
#     name="A Shiny New Stream", description="we're playing with python over here"
# )

# ~ 3. The `StreamWrapper` shorthand using URLs

# if you just want to grab something from a url, this can make it easy!
# you can use a url to a stream, commit, branch, or object
wrapper = StreamWrapper("https://speckle.xyz/streams/3073b96e86/commits/604bea8cc6")

# use `get_client` to get an authenticated client (if you have a corresponding local account)
client_from_wrapper = wrapper.get_client()

# the wrapper stores any important info from the url which you can use with the client
commit = client_from_wrapper.commit.get(wrapper.stream_id, wrapper.commit_id)
print(commit, "\n")

# it can also provide you with a `ServerTransport`
transport = wrapper.get_transport()
