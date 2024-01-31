
import logging
from typing import Optional, List, Any, Type, Dict, Callable, Literal
from datetime import date

# from sqlalchemy import Numeric, Integer, Float
from sqlalchemy.engine import Dialect
from sqlalchemy.sql import sqltypes
from sqlalchemy.sql.type_api import TypeEngine
from sqlalchemy.dialects.mysql.types import TINYINT, SMALLINT, INTEGER, BIGINT, DECIMAL, DOUBLE, FLOAT, CHAR, VARCHAR, DATETIME
from sqlalchemy.dialects.mysql.json import JSON

logger = logging.getLogger(__name__)

#
# class INTEGER(sqltypes.INTEGER):
#
#     def __init__(self, *args, **kwargs):
#         """Construct an INTEGER.
#
#         :param display_width: Optional, maximum display width for this number.
#
#         :param unsigned: a boolean, optional.
#
#         :param zerofill: Optional. If true, values will be stored as strings
#           left-padded with zeros. Note that this does not effect the values
#           returned by the underlying database API, which continue to be
#           numeric.
#
#         """
#         pass

# class TINYINT(sqltypes.Integer):  # pylint: disable=no-init
#     __visit_name__ = "TINYINT"
#
#     def __init__(self, *args, **kwargs):
#         """Construct an BIGINT.
#
#         :param display_width: Optional, maximum display width for this number.
#
#         :param unsigned: a boolean, optional.
#
#         :param zerofill: Optional. If true, values will be stored as strings
#           left-padded with zeros. Note that this does not effect the values
#           returned by the underlying database API, which continue to be
#           numeric.
#
#         """
#         pass

#
# class BIGINT(sqltypes.Integer):  # pylint: disable=no-init
#     __visit_name__ = "BIGINT"
#
#     def __init__(self, *args, **kwargs):
#         """Construct an BIGINT.
#
#         :param display_width: Optional, maximum display width for this number.
#
#         :param unsigned: a boolean, optional.
#
#         :param zerofill: Optional. If true, values will be stored as strings
#           left-padded with zeros. Note that this does not effect the values
#           returned by the underlying database API, which continue to be
#           numeric.
#
#         """
#         pass

class LARGEINT(sqltypes.Integer):  # pylint: disable=no-init
    __visit_name__ = "LARGEINT"


# class DOUBLE(sqltypes.Float):  # pylint: disable=no-init
#     __visit_name__ = "DOUBLE"
#
#
# class FLOAT(sqltypes.FLOAT):  # pylint: disable=no-init
#     __visit_name__ = "FLOAT"


class DATE(sqltypes.DATE):
    __visit_name__ = "DATE"
    def literal_processor(self, dialect: Dialect) -> Callable[[date], str]:
        def process(value: date) -> str:
            return f"TO_DATE('{value}')"

        return process


class HLL(sqltypes.Numeric):  # pylint: disable=no-init
    __visit_name__ = "HLL"


class BITMAP(sqltypes.Numeric):  # pylint: disable=no-init
    __visit_name__ = "BITMAP"


class PERCENTILE(sqltypes.Numeric):  # pylint: disable=no-init
    __visit_name__ = "PERCENTILE"


class ARRAY(TypeEngine):  # pylint: disable=no-init
    __visit_name__ = "ARRAY"

    @property
    def python_type(self) -> Optional[Type[List[Any]]]:
        return list


class MAP(TypeEngine):  # pylint: disable=no-init
    __visit_name__ = "MAP"

    @property
    def python_type(self) -> Optional[Type[Dict[Any, Any]]]:
        return dict


class STRUCT(TypeEngine):  # pylint: disable=no-init
    __visit_name__ = "STRUCT"

    @property
    def python_type(self) -> Optional[Type[Any]]:
        return None

#
# _type_map = {
#     # === Boolean ===
#     "boolean": sqltypes.BOOLEAN,
#     # === Integer ===
#     "tinyint": sqltypes.SMALLINT,
#     "smallint": sqltypes.SMALLINT,
#     "int": sqltypes.INTEGER,
#     "bigint": sqltypes.BIGINT,
#     "largeint": LARGEINT,
#     # === Floating-point ===
#     "float": sqltypes.FLOAT,
#     "double": DOUBLE,
#     # === Fixed-precision ===
#     "decimal": sqltypes.DECIMAL,
#     "decimal64": sqltypes.DECIMAL,
#     # === String ===
#     "varchar": sqltypes.VARCHAR,
#     "char": sqltypes.CHAR,
#     "json": sqltypes.JSON,
#     # === Date and time ===
#     "date": sqltypes.DATE,
#     "timestamp": sqltypes.DATETIME,
#     # === Structural ===
#     'array': ARRAY,
#     'map': MAP,
#     'struct': STRUCT,
#     'hll': HLL,
#     'percentile': PERCENTILE,
#     'bitmap': BITMAP,
# }
#
#
# def parse_sqltype(type_str: str) -> TypeEngine:
#     type_str = type_str.strip().lower()
#     match = re.match(r"^(?P<type>\w+)\s*(?:\((?P<options>.*)\))?", type_str)
#     if not match:
#         logger.warning(f"Could not parse type name '{type_str}'")
#         return sqltypes.NULLTYPE
#     type_name = match.group("type")
#
#     if type_name not in _type_map:
#         logger.warning(f"Did not recognize type '{type_name}'")
#         return sqltypes.NULLTYPE
#     type_class = _type_map[type_name]
#     return type_class()
