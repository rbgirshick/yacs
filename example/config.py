from yacs.config import CfgNode as CN

_C = CN()

_C.SYSTEM = CN()
_C.SYSTEM.NUM_GPUS = 8
_C.SYSTEM.NUM_WORKERS = 4

_C.TRAIN = CN()
_C.TRAIN.HYPERPARAMETER_1 = 0.1
_C.TRAIN.SCALES = (2, 4, 8, 16)

cfg = _C
