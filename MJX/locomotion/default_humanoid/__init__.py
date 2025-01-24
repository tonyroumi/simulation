# Copyright 2025 Triton Droids

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import functools
from typing import Any, Callable, Dict, Optional, Tuple, Type, Union

import jax
from ml_collections import config_dict
from mujoco import mjx

from mujoco_playground import MjxEnv
from locomotion.default_humanoid import joystick as default_humanoid_joystick



_envs = {
    "DefaultHumanoidJoystickFlatTerrain": functools.partial(
        default_humanoid_joystick.Joystick, task="flat_terrain"
    ),
    "DefaultHumanoidJoystickRoughTerrain": functools.partial(
        default_humanoid_joystick.Joystick, task="rough_terrain"
    )
}

_cfgs = {
    "DefaultHumanoidJoystickFlatTerrain": (
        default_humanoid_joystick.default_config
    ),
    "DefaultHumanoidJoystickRoughTerrain": (
        default_humanoid_joystick.default_config
    )
}

ALL = list(_envs.keys())

def register_environment(
    env_name: str,
    env_class: Type[MjxEnv],
    cfg_class: Callable[[], config_dict.ConfigDict],
) -> None:
  """Register a new environment.

  Args:
      env_name: The name of the environment.
      env_class: The environment class.
      cfg_class: The default configuration.
  """
  _envs[env_name] = env_class
  _cfgs[env_name] = cfg_class

def get_default_config(env_name: str) -> config_dict.ConfigDict:
  """Get the default configuration for an environment."""
  if env_name not in _cfgs:
    raise ValueError(
        f"Env '{env_name}' not found in default configs. Available configs:"
        f" {list(_cfgs.keys())}"
    )
  return _cfgs[env_name]()

def load(
    env_name: str,
    config: Optional[config_dict.ConfigDict] = None,
    config_overrides: Optional[Dict[str, Union[str, int, list[Any]]]] = None,
) -> MjxEnv:
  """Get an environment instance with the given configuration.

  Args:
      env_name: The name of the environment.
      config: The configuration to use. If not provided, the default
        configuration is used.
      config_overrides: A dictionary of overrides for the configuration.

  Returns:
      An instance of the environment.
  """
  if env_name not in _envs:
    raise ValueError(f"Env '{env_name}' not found. Available envs: {ALL}")
  config = config or get_default_config(env_name)
  return _envs[env_name](config=config, config_overrides=config_overrides)