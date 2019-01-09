## YACS

### Introduction

YACS was created as a lightweight library to define and manage
system configurations, such as those commonly found in software
designed for scientific experimentation. These "configurations"
typically cover concepts like hyperparameters used in training a
machine learning model or configurable model hyperparameters, such
as the depth of a convolutional neural network. Since you're doing
science, **reproducibility is paramount** and thus you need a reliable
way to serialize experimental configurations. YACS
uses YAML as a simple, human readable serialization format.
The paradigm is: `your code + a YACS config for experiment E (+
external dependencies + hardware + other nuisance terms ...) =
reproducible experiment E`. While you might not be able to control
everything, at least you can control your code and your experimental
configuration. YACS is here to help you with that.

YACS grew out of the experimental configuration systems used in:
[py-faster-rcnn](https://github.com/rbgirshick/py-faster-rcnn) and
[Detectron](https://github.com/facebookresearch/Detectron).

### Usage

YACS can be used in a variety of flexible ways. There are two main
paradigms:

- Configuration as *local variable*
- Configuration as a *global singleton*

It's up to you which you prefer to use, though the local variable
route is recommended.

To use YACS in your project, you first create a project config
file, typically called `config.py` or `defaults.py`. *This file
is the one-stop reference point for all configurable options.
It should be very well documented and provide sensible defaults
for all options.*

```python
# my_project/config.py
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


def get_cfg_defaults():
  """Get a yacs CfgNode object with default values for my_project."""
  # Return a clone so that the defaults will not be altered
  # This is for the "local variable" use pattern
  return _C.clone()

# Alternatively, provide a way to import the defaults as
# a global singleton:
# cfg = _C  # users can `from config import cfg`
```

Next, you'll create YAML configuration files; typically you'll make
one for each experiment. Each configuration file only overrides the
options that are changing in that experiment.

```yaml
# my_project/experiment.yaml
SYSTEM:
  NUM_GPUS: 2
TRAIN:
  SCALES: (1, 2)
```

Finally, you'll have your actual project code that uses the config
system. After any initial setup it's a good idea to freeze it to
prevent further modification by calling the `freeze()` method. As
illustrated below, the config options can either be used a global
set of options by importing `cfg` and accessing it directly, or
the `cfg` can be copied and passed as an argument.

```python
# my_project/main.py

import my_project
from config import get_cfg  # local variable usage pattern, or:
# from config import cfg  # global singleton usage pattern


if __name__ == "__main__":
  cfg = get_cfg_defaults()
  cfg.merge_from_file("experiment.yaml")
  cfg.freeze()
  print(cfg)

  # Example of using the cfg as global access to options
  if cfg.SYSTEM.NUM_GPUS > 0:
    my_project.setup_multi_gpu_support()

  model = my_project.create_model(cfg)
```

#### Command line overrides

You can update a `CfgNode` using a list of fully-qualified key, value pairs.
This makes it easy to consume override options from the command line. For example:

```python
cfg.merge_from_file("experiment.yaml")
# Now override from a list (opts could come from the command line)
opts = ["SYSTEM.NUM_GPUS", 8, "TRAIN.SCALES", "(1, 2, 3, 4)"]
cfg.merge_from_list(opts)
```

The following principle is recommended: "There is only one way to
configure the same thing." This principle means that if an option
is defined in a YACS config object, then your program should set
that configuration option using `cfg.merge_from_list(opts)` and
not by defining, for example, `--train-scales` as a command line
argument that is then used to set `cfg.TRAIN.SCALES`.

#### Python config files (instead of YAML)

`yacs>= 0.1.4` supports loading `CfgNode` objects from Python source files. The
convention is that the Python source must export a module variable named `cfg` of
type `dict` or `CfgNode`. See examples using a [CfgNode](example/config_override.py)
and a [dict](example/config_override_from_dict.py) as well as usage in the unit tests.
