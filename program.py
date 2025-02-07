from random import randint as _randint
import random as _random
from types import SimpleNamespace as _SN

def _randstrat(*args):
    strat_weights = args[::2]
    strat_population = args[1::2]
    return _random.choices(strat_population, strat_weights)[0]

def _enter_nonpunct(ctx, chars):
    if ctx.result != "":
        ctx.result += " "
    ctx.result += chars

# , . ? ! <word> <number> <new paragraph> <parens>

def _beginning(ctx):
    _randstrat(
        7, _word,
        1, _number,
    )(ctx)
    return _paragraph

def _afternum()

def _paragraph(ctx):
    _randstrat(
        15, _word
    )

def _enter_nonpunct(data, after):
    def inner(ctx):
        if ctx.result != "":
            ctx.result += " "
        _enter(data)(ctx)
        return after
    return inner

def _enter(data, after):
    def inner(ctx):
        ctx.result += data
    return inner

def _new_paragraph(ctx):
    ctx.result += "\n\n"

_period = _enter_nonpunct(".")
_comma = _enter_nonpunct(",")
_exclamation_mark = _enter_nonpunct("!")
_question_mark = _enter_nonpunct("?")

def _period():
    return _enter_nonpunct(".")

def _comma():
    return _enter_nonpunct(",")

def _exclamation_mark():
    return _enter_nonpunct("!")

def _word(ctx):
    pass

def _question_mark(ctx):
    pass

def _number(ctx):


def _parens(ctx):
    _enter_nonpunct(ctx, "(")
    for i in range(randint()):
        _parens_randstrat(ctx)
    ctx.result += ")"
    ctx.space_needed = True

def encode(octets: "iterable of ints"):
    n = 0
    for octet in octets:
        n *= 257
        n += octet + 1
    letters = []
    while n != 0:
        quot, n = divmod(n, 26)
        letters.append("abcdefghijklmnopqrstuvwxyz"[quot])
    ctx = _SN(
        letters=letters,
        result="",
        should_capitalize=False
    )
    thunk = _beginning
    while True:
        thunk = thunk(ctx)
        if thunk is None:
            return ctx.result
