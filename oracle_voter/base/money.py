import decimal

U_WEI = decimal.Decimal("10.00") ** -18


class Note:

    ctx_prec = 25

    def __init__(self, val, is_clone=False, config={}):

        self._val = val

        if config.get("ctx_prec"):
            self.ctx_prec = config.get("ctx_prec")

        if not is_clone:
            with decimal.localcontext() as ctx:
                ctx.prec = self.ctx_prec
                self._val = decimal.Decimal(
                    value=val,
                    context=ctx,
                ).quantize(U_WEI)

    def __add__(self, o):
        return Note(self._val + o._val, is_clone=True)

    def __sub__(self, o):
        return Note(self._val - o._val, is_clone=True)

    def __mul__(self, o):
        return Note(self._val * o._val, is_clone=True)

    def __truediv__(self, o):
        return Note(self._val / o._val, is_clone=True)

    def __str__(self):
        return str(self._val)

    def __repr__(self):
        return f"<Note: {self.__str__()}>"


ABSTAIN_NOTE = Note("-1.00")
