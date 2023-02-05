from taichi.qtype.register import QuBit, Register
from taichi.lang.exception import TaichiRuntimeError
from taichi.lang.kernel_impl import func


class QGate:

    def __init__(self, name, target):
        self.target = target
        self.name = name
        self.ctrls = []

    def dagger(self):
        pass

    def control(self, condition):
        if not isinstance(condition, (QuBit, Register)):
            raise TaichiRuntimeError("The control variable must be Qubit or QRegister")
        if isinstance(condition, Register):
            for n in condition:
                self.ctrls.append(n)
        else:
            self.ctrls.append(condition)


@func
def h(q: QuBit):
    pass


@func
def x(q: QuBit):
    pass


@func
def y(q: QuBit):
    pass


@func
def z(q: QuBit):
    pass


@func
def cnot(target: QuBit, ctrl: QuBit):
    pass


@func
def phase(phi: float):
    pass


@func
def measure(target: Register) -> int:
    pass


@func
def u_measure(target: Register) -> int:
    pass
