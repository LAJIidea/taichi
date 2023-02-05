import taichi as ti


class AutoDaggerStructure:

    def __enter__(self):
        pass

    def __exit__(self):
        pass


class ApplyStructure:

    def __enter__(self):
        pass

    def __exit__(self):
        pass


@ti.func
def uncompute():
    return AutoDaggerStructure()


@ti.func
def apply():
    return ApplyStructure()
