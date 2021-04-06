import asyncio
import datetime
import random
import typing
import types
from discord_slash.model import CogCommandObject


def cooldown_message(messages: typing.List[str] = None):
    def wrapper(func):
        def prepare_cooldowns(self, ctx):
            if self._buckets.valid:
                dt = ctx.created_at
                current = dt.replace(tzinfo=datetime.timezone.utc).timestamp()
                bucket = self._buckets.get_bucket(ctx, current)
                retry_after = bucket.update_rate_limit(current)
                if retry_after:
                    print(random.choice(messages or ["You are going too fast!"]))

        func_type = types.MethodType
        func._prepare_cooldowns = func_type(prepare_cooldowns, CogCommandObject)
        return func

    return wrapper
