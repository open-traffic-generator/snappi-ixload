# snappi extension for IxLoad

This extension allows executing tests written using [snappi](https://github.com/open-traffic-generator/snappi) against  
IxLoad, (one of) Keysight's implementation of [Open Traffic Generator](https://github.com/open-traffic-generator/models/releases).

> The repository is under active development.

## Install on a client

```sh
python -m pip install --upgrade "snappi[ixload]"
```

## Start scripting

```python
# TODO: add complete description and snippet

import snappi
# host is IxNetwork API Server
api = snappi.api(location='https://localhost:8444', ext='ixload')
# new config
config = api.config()
```

