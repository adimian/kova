from kova.our_types import Dependable


class ReplyNameException(Exception):
    pass


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


class ReplyStream(Dependable):
    def __call__(self, payload: bytes, subject: str):
        raise NotImplementedError("you should not see this")

    @classmethod
    def get_instance(cls, router, msg, **kwargs):
        if msg.reply:

            async def reply(payload: bytes, subject: str):
                check = subject.split(".")
                if check[-1] != "reply":
                    raise ReplyNameException(
                        "Reply subject should finish with reply"
                    )
                p = Publish().get_instance(router=router)
                await p(subject=subject, payload=payload)

            return reply
        else:
            return None

    @classmethod
    def get_reply_subject(cls, stream_name: str, current_user: str):
        # stream_name = router.queue._subs[1].subject()
        modified_stream = stream_name.replace("*", current_user)
        name = f"{modified_stream}.reply"
        return name


Dependable.register(ReplyStream)
