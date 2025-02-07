from random import randint as _randint
import random as _random
from types import SimpleNamespace as _SN

def _randstrat(*args):
    strat_weights = args[::2]
    strat_population = args[1::2]
    return _random.choices(strat_population, strat_weights)[0]

def _enter_nonpunct(ctx, chars):
    if ctx.space_required:
        ctx.result += " "
    ctx.space_required = True
    ctx.punctuation_allowed = True
    ctx.capitalization_required = False
    if ctx.paragraph_time != 0:
        ctx.paragraph_time -= 1
    ctx.result += chars

def _simple_punctuation(chars, *, capitalization_required):
    def inner(ctx):
        ctx.capitalization_required = capitalization_required
        ctx.punctuation_allowed = False
        ctx.space_required = True
        ctx.result += chars
    return inner

# , . ? ! <word> <number> <new paragraph> <parens - NOT IMPLEMENTED YET>

def _number(ctx):
    _enter_nonpunct(ctx, str(_randint(0, 100)))

def _word(ctx):
    len_ = _randint(1, 10)
    word = "".join(ctx.letters[:len_])
    ctx.letters = ctx.letters[len_:]
    if ctx.capitalization_required:
        word = word.capitalize()
    _enter_nonpunct(ctx, word)

def _do_next(ctx):
    weights = []
    handlers = []
    def strat(weight, handler):
        weights.append(weight)
        handlers.append(handler)
    strat(70, _word)
    strat(7, _number)
    if ctx.paragraph_time == 0:
        ctx.paragraph_time = _get_new_paragraph_time()
        ctx.punctuation_allowed = False
        ctx.capitalization_required = True
        ctx.space_required = False
        ctx.result += "\n\n"
    if ctx.punctuation_allowed:
        strat(12, _simple_punctuation(",", capitalization_required=False))
        strat(8, _simple_punctuation(".", capitalization_required=True))
        strat(4, _simple_punctuation("!", capitalization_required=True))
        strat(4, _simple_punctuation("?", capitalization_required=True))
        strat(2, _simple_punctuation("...", capitalization_required=True))
        strat(2, _simple_punctuation("...", capitalization_required=False))
    _random.choices(handlers, weights)[0](ctx)

def _get_new_paragraph_time():
    return _randint(5, 30)

_LETTERS = "abcdefghijklmnopqrstuvwxyz"

def encode(octets: "iterable of ints"):
    accumulator = 0
    for octet in octets:
        accumulator *= 257
        accumulator += octet + 1
    letters = []
    while accumulator != 0:
        accumulator, rem = divmod(accumulator, len(_LETTERS))
        letters.append(_LETTERS[rem])
    ctx = _SN(
        letters=letters,
        result="",
        punctuation_allowed=False,
        capitalization_required=True,
        space_required=False,
        paragraph_time=_get_new_paragraph_time(),
    )
    while True:
        _do_next(ctx)
        if len(ctx.letters) == 0:
            return ctx.result

def decode(string):
    string = string[::-1]
    octets = []
    accumulator = 0
    for c in string:
        try:
            index = _LETTERS.index(c.lower())
        except ValueError:
            pass
        else:
            accumulator *= len(_LETTERS)
            accumulator += index
    while accumulator != 0:
        accumulator, rem = divmod(accumulator, 257)
        octets.append(rem - 1)
    return bytes(octets[::-1])
