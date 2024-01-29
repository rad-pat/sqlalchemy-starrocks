
import pytest
from sqlalchemy.dialects import registry

registry.register("starrocks+pymysql", "sqlalchemy_starrocks.dialect", "StarRocksDialect")
registry.register("starrocks", "sqlalchemy_starrocks.dialect", "StarRocksDialect")
pytest.register_assert_rewrite("sqlalchemy.testing.assertions")

from sqlalchemy.testing.plugin.pytestplugin import *
