import argparse

from redbot.core.commands import BadArgument, Converter
from redbot.core.commands.converter import TimedeltaConverter


class NoExitParser(argparse.ArgumentParser):
    def error(self, message):
        raise BadArgument()


import logging

log = logging.getLogger("red.flare.giveaways")


class Args(Converter):
    async def convert(self, ctx, argument):
        argument = argument.replace("—", "--")
        parser = NoExitParser(description="Giveaway Created", add_help=False)

        parser.add_argument("--prize", "--p", dest="prize", nargs="*", default=[])
        parser.add_argument("--duration", "--d", dest="duration", nargs="*", default=[])
        parser.add_argument("--channel", "--c", dest="channel", default=None, type=int, nargs="?")

        parser.add_argument("--restrict", "--r", dest="exclusive", nargs="*", default=[])

        parser.add_argument("--multiplier", "--m", dest="multi", default=None, type=int, nargs="?")
        parser.add_argument("--multi-roles", "--mr", nargs="*", dest="multi-roles", default=[])

        try:
            vals = vars(parser.parse_args(argument.split(" ")))
        except Exception as error:
            log.error("Error in Args: ", exc_info=error)
            raise BadArgument() from error

        if not vals["prize"]:
            raise BadArgument("You must specify a prize. Use `--prize` or `-p`")  #

        if not vals["duration"]:
            raise BadArgument("You must specify a duration. Use `--duration` or `-d`")

        if vals["channel"]:
            channel = ctx.guild.get_channel(vals["channel"])
            if not channel:
                raise BadArgument("Invalid channel.")

        if vals["multi"] or vals["multi-roles"]:
            if not (vals["multi"] and vals["multi-roles"]):
                raise BadArgument(
                    "You must specify a multiplier and roles. Use `--multiplier` or `-m` and `--multi-roles` or `-mr`"
                )

        vals["prize"] = " ".join(vals["prize"])
        tc = TimedeltaConverter()
        try:
            vals["duration"] = await tc.convert(ctx, " ".join(vals["duration"]))
        except BadArgument:
            raise BadArgument("Invalid duration. Use `--duration` or `-d`")

        return vals
