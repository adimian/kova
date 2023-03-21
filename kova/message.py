from kova.types import Dependable


class Publish(Dependable):
    def __call__(self, subject: str, payload: bytes):
        raise NotImplementedError("you should not see this")

    @classmethod
    def get_instance(cls, router, **kwargs):
        async def publish(subject: str, payload: bytes):
            await router.queue.publish(  # type: ignore
                subject=subject, payload=payload
            )

        return publish


Dependable.register(Publish)


class Reply(Dependable):
    def __call__(self, payload: bytes):
        raise NotImplementedError("you should not see this")

    @classmethod
    def get_instance(cls, router, msg, **kwargs):
        if msg.reply:

            async def reply(payload: bytes):
                p = Publish().get_instance(router=router)
                await p(subject=msg.reply, payload=payload)

            return reply
        else:
            return None


Dependable.register(Reply)
