## YACS

To use YACS in your project, you first create a project config
file, typically called `config.py`. This file is the one-stop
reference point for all configurable options. It should be very
well documented and provide sensible defaults for all options.

```python
# config.py
from yacs.config import CfgNode as CN


_C = CN()

_C.SYSTEM = CN()
# Number of GPUS to use in the experiment
_C.SYSTEM.NUM_GPUS = 8
# Number of workers for doing things
_C.SYSTEM.NUM_WORKERS = 4

_C.TRAIN = CN()
# A very important hyperparameter
_C.TRAIN.HYPERPARAMETER_1 = 0.1
# The all important scales for the stuff
_C.TRAIN.SCALES = (2, 4, 8, 16)

# Exporting as cfg is a nice convention
cfg = _C
```

Next, you'll create YAML configuration files; typically you'll make
one for each experiment. Each configuration file only overrides the
options that are changing in that experiment.

```yaml
# my_experiment.yaml
SYSTEM:
  NUM_GPUS: 2
TRAIN:
  SCALES: (1, 2)
```

Finally, you'll have your actual project code that uses the config
system. Since the cfg is global, after any initial setup it's a good
idea to freeze it (by calling the `freeze()` method).

```python
# main.py
import pprint

from config import cfg


if __name__ == "__main__":
  cfg.merge_from_file("my_experiment.yaml")
  cfg.freeze()
  pprint.pprint(cfg)
```

### Additional Options and Tips

TODO:
- document command line overrides
- give usual tips

### Bugs

- Change `yaml.load` to `yaml.safe_load`
