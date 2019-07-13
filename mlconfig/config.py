from .utils import load_yaml, save_yaml


ALLOWED_LENGTH_ERROR_MSG = """
Found a mismatch in the allowed length.
Allowed lengths are 1 and {max_allowed_length},
but we found an item with length {current_length}.
Check your configuration.
"""

NOT_A_LIST_ERROR_MSG = """
The value associated with parameter '{key}' must be a list.
"""

class ConfigError(Exception):
    pass


class LoadMixin:
    @classmethod
    def from_file(cls, path):
        config_dict = load_yaml(path)
        return cls.from_dict(config_dict)

    @classmethod
    def from_dict(cls, config_dict):
        return cls(**config_dict)


class Config(LoadMixin):
    def __init__(self, **params):
        self.initialized = False
        self.update(**params)
        self.initialized = True

    def __getitem__(self, name):
        return getattr(self, name)

    def update(self, **params):
        for name, value in params.items():
            if self.initialized and not hasattr(self, name):
                raise ConfigError(f"Parameter '{name}' is not contained in this Config.")
            setattr(self, name, value)

    def save(self, path):
        save_yaml(self.__dict__, path)


class ModelSelectionConfig(LoadMixin):
    def __init__(self, **ms_dict):
        self.max_allowed_length = 1
        self._validate(ms_dict)
        self._dict = ms_dict

    def _validate(self, ms_dict):
        for name, value in ms_dict.items():
            if not isinstance(value, list):
                msg = NOT_A_LIST_ERROR_MSG.format(key=name)
                raise ConfigError(msg)

        for name, value in ms_dict.items():
            current_length = len(value)
            if self.max_allowed_length != 1 and current_length != self.max_allowed_length:
                msg = ALLOWED_LENGTH_ERROR_MSG.format(max_allowed_length=self.max_allowed_length,
                                                      current_length=current_length)
                raise ConfigError(msg)
            self.max_allowed_length = current_length

        for name, value in ms_dict.items():
            if len(value) == 1:
                ms_dict[name] = value * self.max_allowed_length

    def _get_config_dict(self, index):
        # We return dictionaries instead of Config objects,
        # as doing so creates problems in case of parallelization.
        # Config objects must be created inside the dedicated thread.
        return {k: v[index] for (k, v) in self._dict.items()}

    def __iter__(self):
        return iter(self._get_config_dict(i) for i in range(self.max_allowed_length))

    def __getitem__(self, index):
        return self._get_config_dict(index)

