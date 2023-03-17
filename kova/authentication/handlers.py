from google.protobuf.message import Message

from kova.router import Handler, Context, Reply, Publish


class LoginHandler(Handler):
    async def __call__(
        self,
        context: Context,
        message: Message,
        reply: Reply,
        publish: Publish,
    ):
        pass
