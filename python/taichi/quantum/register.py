import itertools
import numpy as np
from taichi.lang.util import python_scope, taichi_scope
from taichi.lang.exception import TaichiRuntimeError


class Register:
    """Implement a generic register"""

    # Counter for the number of instance in this class
    instance_counter = itertools.count()
    # Prefix to use for auto name
    prefix = 'reg'
    bit_type = None

    def __init__(self, size):
        try:
            size = int(size)
        except Exception:
            raise TaichiRuntimeError("Register size must be castable to an int (%s '%s' was provided"
                                     % (type(size).__name__, size))
        if size <= 0:
            raise TaichiRuntimeError("Register size must be positive (%s '%s' was provided"
                                     % (type(size).__name__, size))

        self._name = '%s%i' % (self.prefix, next(self.instance_counter))
        self._size = size
        self._bits = [self.bit_type(self, idx) for idx in range(size)]

    def __len__(self):
        """Return register size."""
        return self._size

    def __getitem__(self, key):
        """
        Get Qubit by subscript

        Args:
            key (int, slice, list): index of the bit to be retrieved

        Returns:
            Qubit, list(Qubit)

        Raises:

        """
        if not isinstance(key, (int, np.int, np.int32, np.int64, slice, list)):
            raise TaichiRuntimeError("expected integer or slice index into register")
        if isinstance(key, slice):
            return self._bits[key]
        elif isinstance(key, list):
            if max(key) < len(self):
                return [self._bits[idx] for idx in key]
            else:
                raise TaichiRuntimeError('register index out of range')
        else:
            return self._bits[key]

    def __iter__(self):
        for idx in range(self._size):
            yield self._bits[idx]


class QuBit:
    """Implement a generic qubit"""

    def __init__(self, register, index):
        """Create a new generic bit"""
        try:
            index = int(index)
        except Exception:
            raise TaichiRuntimeError("index needs to be castable to an int: type %s was provided"
                                     % type(index))

        if index < 0:
            index += len(register)

        self.register = register
        self.index = index

    def __eq__(self, other):
        if isinstance(other, QuBit):
            return other.index == self.index and other.register == self.register
        return False


class QRegister(Register):
    """Implement a quantum register"""

    instance_counter = itertools.count()
    prefix = 'q'
    bit_type = QuBit


class LocalRegister(Register):
    instance_counter = itertools.count()
    prefix = 'a'
    bit_type = QuBit


@python_scope
def qreg(size):
    """Defines a Taichi Global QRegister.

    A qreg can be viewed as a mapping of physical qubits
    Args:
        size (int): register size to be allocated

    Returns:
        QRegister

    Examples:
        The code below shows how a qreg can be declared and defined:
            >>> q = qreg(3)
    """
    return QRegister(size)


@taichi_scope
def local_qreg(size):
    """Defines a Taichi Local Ancilla QRegister.
    A qreg can be viewed as mapping of physical qubits, and it will be automatically
    uncompute by taichi.

    Args:
        size (int): register size to be allocated

    Returns:
        LocalRegister

    Examples:
        The code below shows how a qreg can be declared and defined:
            >>> anc = local_qreg(3)
    """
    return LocalRegister(size)
