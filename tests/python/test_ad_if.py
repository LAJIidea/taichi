from taichi.lang import impl
from taichi.lang.misc import get_host_arch_list

import taichi as ti
from tests import test_utils


@test_utils.test(require=ti.extension.adstack)
def test_ad_if_simple():
    x = ti.field(ti.f32, shape=())
    y = ti.field(ti.f32, shape=())

    ti.root.lazy_grad()

    @ti.kernel
    def func():
        if x[None] > 0.:
            y[None] = x[None]

    x[None] = 1
    y.grad[None] = 1

    func()
    func.grad()

    assert x.grad[None] == 1


@test_utils.test(require=ti.extension.adstack)
def test_ad_if():
    x = ti.field(ti.f32, shape=2)
    y = ti.field(ti.f32, shape=2)

    ti.root.lazy_grad()

    @ti.kernel
    def func(i: ti.i32):
        if x[i] > 0:
            y[i] = x[i]
        else:
            y[i] = 2 * x[i]

    x[0] = 0
    x[1] = 1
    y.grad[0] = 1
    y.grad[1] = 1

    func(0)
    func.grad(0)
    func(1)
    func.grad(1)

    assert x.grad[0] == 2
    assert x.grad[1] == 1


@test_utils.test(require=ti.extension.adstack)
def test_ad_if_nested():
    n = 20
    x = ti.field(ti.f32, shape=n)
    y = ti.field(ti.f32, shape=n)
    z = ti.field(ti.f32, shape=n)

    ti.root.lazy_grad()

    @ti.kernel
    def func():
        for i in x:
            if x[i] < 2:
                if x[i] == 0:
                    y[i] = 0
                else:
                    y[i] = z[i] * 1
            else:
                if x[i] == 2:
                    y[i] = z[i] * 2
                else:
                    y[i] = z[i] * 3

    z.fill(1)

    for i in range(n):
        x[i] = i % 4

    func()
    for i in range(n):
        assert y[i] == i % 4
        y.grad[i] = 1
    func.grad()

    for i in range(n):
        assert z.grad[i] == i % 4


@test_utils.test(require=ti.extension.adstack)
def test_ad_if_mutable():
    x = ti.field(ti.f32, shape=2)
    y = ti.field(ti.f32, shape=2)

    ti.root.lazy_grad()

    @ti.kernel
    def func(i: ti.i32):
        t = x[i]
        if t > 0:
            y[i] = t
        else:
            y[i] = 2 * t

    x[0] = 0
    x[1] = 1
    y.grad[0] = 1
    y.grad[1] = 1

    func(0)
    func.grad(0)
    func(1)
    func.grad(1)

    assert x.grad[0] == 2
    assert x.grad[1] == 1


@test_utils.test(require=ti.extension.adstack)
def test_ad_if_parallel():
    x = ti.field(ti.f32, shape=2)
    y = ti.field(ti.f32, shape=2)

    ti.root.lazy_grad()

    @ti.kernel
    def func():
        for i in range(2):
            t = x[i]
            if t > 0:
                y[i] = t
            else:
                y[i] = 2 * t

    x[0] = 0
    x[1] = 1
    y.grad[0] = 1
    y.grad[1] = 1

    func()
    func.grad()

    assert x.grad[0] == 2
    assert x.grad[1] == 1


@test_utils.test(require=[ti.extension.adstack, ti.extension.data64],
                 default_fp=ti.f64)
def test_ad_if_parallel_f64():
    x = ti.field(ti.f64, shape=2)
    y = ti.field(ti.f64, shape=2)

    ti.root.lazy_grad()

    @ti.kernel
    def func():
        for i in range(2):
            t = x[i]
            if t > 0:
                y[i] = t
            else:
                y[i] = 2 * t

    x[0] = 0
    x[1] = 1
    y.grad[0] = 1
    y.grad[1] = 1

    func()
    func.grad()

    assert x.grad[0] == 2
    assert x.grad[1] == 1


@test_utils.test(require=ti.extension.adstack)
def test_ad_if_parallel_complex():
    x = ti.field(ti.f32, shape=2)
    y = ti.field(ti.f32, shape=2)

    ti.root.lazy_grad()

    @ti.kernel
    def func():
        ti.loop_config(parallelize=1)
        for i in range(2):
            t = 0.0
            if x[i] > 0:
                t = 1 / x[i]
            y[i] = t

    x[0] = 0
    x[1] = 2
    y.grad[0] = 1
    y.grad[1] = 1

    func()
    func.grad()

    assert x.grad[0] == 0
    assert x.grad[1] == -0.25


@test_utils.test(require=[ti.extension.adstack, ti.extension.data64],
                 default_fp=ti.f64)
def test_ad_if_parallel_complex_f64():
    x = ti.field(ti.f64, shape=2)
    y = ti.field(ti.f64, shape=2)

    ti.root.lazy_grad()

    @ti.kernel
    def func():
        ti.loop_config(parallelize=1)
        for i in range(2):
            t = 0.0
            if x[i] > 0:
                t = 1 / x[i]
            y[i] = t

    x[0] = 0
    x[1] = 2
    y.grad[0] = 1
    y.grad[1] = 1

    func()
    func.grad()

    assert x.grad[0] == 0
    assert x.grad[1] == -0.25


@test_utils.test(arch=get_host_arch_list())
def test_stack():
    @ti.kernel
    def func():
        impl.call_internal("test_stack")

    func()


#FIXME: amdgpu backend(assign gale)
@test_utils.test(exclude=ti.amdgpu)
def test_if_condition_depend_on_for_loop_index():
    scalar = lambda: ti.field(dtype=ti.f32)
    vec = lambda: ti.Vector.field(3, dtype=ti.f32)

    pos = vec()
    F = vec()
    f_bend = scalar()
    loss_n = scalar()
    ti.root.dense(ti.ij, (10, 10)).place(pos, F)
    ti.root.dense(ti.i, 1).place(f_bend)
    ti.root.place(loss_n)
    ti.root.lazy_grad()

    @ti.kernel
    def simulation(t: ti.i32):
        for i, j in pos:
            coord = ti.Vector([i, j])
            for n in range(12):
                f = ti.Vector([0.0, 0.0, 0.0])
                if n < 4:
                    f = ti.Vector([1.0, 1.0, 1.0])
                else:
                    f = f_bend[0] * pos[coord]
                F[coord] += f
            pos[coord] += 1.0 * t

    with ti.ad.Tape(loss=loss_n):
        simulation(5)
