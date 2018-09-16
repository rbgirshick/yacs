# NB: This file is used in unit tests in tests.py; do not change unless you know
# what you're doing

from yacs.config import CfgNode as CN

HYPERPARAMETER_1_BASE_VALUE = 1.0

cfg = CN()

cfg.TRAIN = CN()
cfg.TRAIN.HYPERPARAMETER_1 = 0.9 * HYPERPARAMETER_1_BASE_VALUE
