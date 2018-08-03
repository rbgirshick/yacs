from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import tempfile
import unittest

import yacs.config
from yacs.config import CfgNode as CN


def get_cfg():
    cfg = CN()

    cfg.NUM_GPUS = 8

    cfg.TRAIN = CN()
    cfg.TRAIN.HYPERPARAMETER_1 = 0.1
    cfg.TRAIN.SCALES = (2, 4, 8, 16)

    cfg.MODEL = CN()
    cfg.MODEL.TYPE = "a_foo_model"

    cfg.register_deprecated_key("FINAL_MSG")
    cfg.register_deprecated_key("MODEL.DILATION")

    cfg.register_renamed_key(
        "EXAMPLE.OLD.KEY",
        "EXAMPLE.NEW.KEY",
        message="Please update your config fil config file.",
    )

    return cfg


class TestCfgNode(unittest.TestCase):
    def test_immutability(self):
        # Top level immutable
        a = CN()
        a.foo = 0
        a.freeze()
        with self.assertRaises(AttributeError):
            a.foo = 1
            a.bar = 1
        assert a.is_frozen()
        assert a.foo == 0
        a.defrost()
        assert not a.is_frozen()
        a.foo = 1
        assert a.foo == 1

        # Recursively immutable
        a.level1 = CN()
        a.level1.foo = 0
        a.level1.level2 = CN()
        a.level1.level2.foo = 0
        a.freeze()
        assert a.is_frozen()
        with self.assertRaises(AttributeError):
            a.level1.level2.foo = 1
            a.level1.bar = 1
        assert a.level1.level2.foo == 0

        # Serialize immutability state
        a.freeze()
        a2 = yacs.config.load_cfg(a.dump())
        assert a.is_frozen()
        assert a2.is_frozen()


class TestCfg(unittest.TestCase):
    def test_copy_cfg(self):
        cfg = get_cfg()
        cfg2 = cfg.clone()
        s = cfg.MODEL.TYPE
        cfg2.MODEL.TYPE = "dummy"
        assert cfg.MODEL.TYPE == s

    def test_merge_cfg_from_cfg(self):
        # Test: merge from clone
        cfg = get_cfg()
        s = "dummy0"
        cfg2 = cfg.clone()
        cfg2.MODEL.TYPE = s
        cfg.merge_from_other_cfg(cfg2)
        assert cfg.MODEL.TYPE == s

        # Test: merge from yaml
        s = "dummy1"
        cfg2 = yacs.config.load_cfg(cfg.dump())
        cfg2.MODEL.TYPE = s
        cfg.merge_from_other_cfg(cfg2)
        assert cfg.MODEL.TYPE == s

        # Test: merge with a valid key
        s = "dummy2"
        cfg2 = CN()
        cfg2.MODEL = CN()
        cfg2.MODEL.TYPE = s
        cfg.merge_from_other_cfg(cfg2)
        assert cfg.MODEL.TYPE == s

        # Test: merge with an invalid key
        s = "dummy3"
        cfg2 = CN()
        cfg2.FOO = CN()
        cfg2.FOO.BAR = s
        with self.assertRaises(KeyError):
            cfg.merge_from_other_cfg(cfg2)

        # Test: merge with converted type
        cfg2 = CN()
        cfg2.TRAIN = CN()
        cfg2.TRAIN.SCALES = [1]
        cfg.merge_from_other_cfg(cfg2)
        assert type(cfg.TRAIN.SCALES) is tuple
        assert cfg.TRAIN.SCALES[0] == 1

        # Test: merge with invalid type
        cfg2 = CN()
        cfg2.TRAIN = CN()
        cfg2.TRAIN.SCALES = 1
        with self.assertRaises(ValueError):
            cfg.merge_from_other_cfg(cfg2)

    def test_merge_cfg_from_file(self):
        with tempfile.NamedTemporaryFile(mode="wt") as f:
            cfg = get_cfg()
            f.write(cfg.dump())
            f.flush()
            s = cfg.MODEL.TYPE
            cfg.MODEL.TYPE = "dummy"
            assert cfg.MODEL.TYPE != s
            cfg.merge_from_file(f.name)
            assert cfg.MODEL.TYPE == s

    def test_merge_cfg_from_list(self):
        cfg = get_cfg()
        opts = ["TRAIN.SCALES", "(100, )", "MODEL.TYPE", "foobar", "NUM_GPUS", 2]
        assert len(cfg.TRAIN.SCALES) > 0
        assert cfg.TRAIN.SCALES[0] != 100
        assert cfg.MODEL.TYPE != "foobar"
        assert cfg.NUM_GPUS != 2
        cfg.merge_from_list(opts)
        assert type(cfg.TRAIN.SCALES) is tuple
        assert len(cfg.TRAIN.SCALES) == 1
        assert cfg.TRAIN.SCALES[0] == 100
        assert cfg.MODEL.TYPE == "foobar"
        assert cfg.NUM_GPUS == 2

    def test_deprecated_key_from_list(self):
        # You should see logger messages like:
        #   "Deprecated config key (ignoring): MODEL.DILATION"
        cfg = get_cfg()
        opts = ["FINAL_MSG", "foobar", "MODEL.DILATION", 2]
        with self.assertRaises(AttributeError):
            _ = cfg.FINAL_MSG  # noqa
        with self.assertRaises(AttributeError):
            _ = cfg.MODEL.DILATION  # noqa
        cfg.merge_from_list(opts)
        with self.assertRaises(AttributeError):
            _ = cfg.FINAL_MSG  # noqa
        with self.assertRaises(AttributeError):
            _ = cfg.MODEL.DILATION  # noqa

    def test_deprecated_key_from_file(self):
        # You should see logger messages like:
        #   "Deprecated config key (ignoring): MODEL.DILATION"
        cfg = get_cfg()
        with tempfile.NamedTemporaryFile("wt") as f:
            cfg2 = cfg.clone()
            cfg2.MODEL.DILATION = 2
            f.write(cfg2.dump())
            f.flush()
            with self.assertRaises(AttributeError):
                _ = cfg.MODEL.DILATION  # noqa
            cfg.merge_from_file(f.name)
            with self.assertRaises(AttributeError):
                _ = cfg.MODEL.DILATION  # noqa

    def test_renamed_key_from_list(self):
        cfg = get_cfg()
        opts = ["EXAMPLE.OLD.KEY", "foobar"]
        with self.assertRaises(AttributeError):
            _ = cfg.EXAMPLE.OLD.KEY  # noqa
        with self.assertRaises(KeyError):
            cfg.merge_from_list(opts)

    def test_renamed_key_from_file(self):
        cfg = get_cfg()
        with tempfile.NamedTemporaryFile("wt") as f:
            cfg2 = cfg.clone()
            cfg2.EXAMPLE = CN()
            cfg2.EXAMPLE.RENAMED = CN()
            cfg2.EXAMPLE.RENAMED.KEY = "foobar"
            f.write(cfg2.dump())
            f.flush()
            with self.assertRaises(AttributeError):
                _ = cfg.EXAMPLE.RENAMED.KEY  # noqa
            with self.assertRaises(KeyError):
                cfg.merge_from_file(f.name)


if __name__ == "__main__":
    unittest.main()
