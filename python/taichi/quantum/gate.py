import taichi as ti
from taichi.quantum.register import QuBit, Register
from taichi.lang.exception import TaichiRuntimeError


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


@ti.func
def h(q: QuBit):
    pass


@ti.func
def x(q: QuBit):
    pass


@ti.func
def y(q: QuBit):
    pass


@ti.func
def z(q: QuBit):
    pass


@ti.func
def cnot(target: QuBit, ctrl: QuBit):
    pass


@ti.func
def phase(phi: float):
    pass


@ti.func
def measure(target: Register) -> int:
    pass


@ti.func
def u_measure(target: Register) -> int:
    pass
