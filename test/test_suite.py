# # coding: utf-8
import decimal

from sqlalchemy.testing.suite import *
# from sqlalchemy.testing.suite.test_select import *
# from sqlalchemy.testing.suite.test_select import FetchLimitOffsetTest

from sqlalchemy.testing.assertions import AssertsCompiledSQL
from sqlalchemy import Table, Column, Integer, MetaData, select
from sqlalchemy import schema

from sqlalchemy.testing import fixtures
from sqlalchemy import testing, literal
from sqlalchemy.testing.assertions import eq_, is_
from sqlalchemy.sql.sqltypes import Float


class CompileTest(fixtures.TestBase, AssertsCompiledSQL):

    __only_on__ = "starrocks"

    def test_create_table_with_properties(self):
        m = MetaData()
        tbl = Table(
            'atable', m, Column("id", Integer),
            starrocks_properties=(
                ("storage_medium", "SSD"),
                ("storage_cooldown_time", "2015-06-04 00:00:00"),
            ))
        self.assert_compile(
            schema.CreateTable(tbl),
            "CREATE TABLE atable (id INTEGER)PROPERTIES(\"storage_medium\"=\"SSD\",\"storage_cooldown_time\"=\"2015-06-04 00:00:00\")")

#     def test_reserved_words(self):
#         table = Table("pg_table", MetaData(),
#                       Column("col1", Integer),
#                       Column("variadic", Integer))
#         x = select(table.c.col1, table.c.variadic)
#
#         self.assert_compile(
#             x,
#             '''SELECT pg_table.col1, pg_table."variadic" FROM pg_table''')
#


# Float test fixes below for "Data type of first column cannot be FLOAT" error given by starrocks
class _LiteralRoundTripFixture2(object):
    supports_whereclause = True

    @testing.fixture
    def literal_round_trip(self, metadata, connection):
        """test literal rendering"""

        # for literal, we test the literal render in an INSERT
        # into a typed column.  we can then SELECT it back as its
        # official type; ideally we'd be able to use CAST here
        # but MySQL in particular can't CAST fully

        def run(type_, input_, output, filter_=None):
            t = Table("t", metadata, Column("a", Integer), Column("x", type_))
            t.create(connection)

            for value in input_:
                ins = (
                    t.insert()
                    .values(x=literal(value, type_))
                    .compile(
                        dialect=testing.db.dialect,
                        compile_kwargs=dict(literal_binds=True),
                    )
                )
                connection.execute(ins)

            if self.supports_whereclause:
                stmt = t.select().where(t.c.x == literal(value))
            else:
                stmt = t.select()

            stmt = stmt.compile(
                dialect=testing.db.dialect,
                compile_kwargs=dict(literal_binds=True),
            )
            for row in connection.execute(stmt):
                value = row[0]
                if filter_ is not None:
                    value = filter_(value)
                assert value in output

        return run


class FloatTest(_LiteralRoundTripFixture2, fixtures.TestBase):
    __backend__ = True

    @testing.fixture
    def do_numeric_test(self, metadata, connection):
        @testing.emits_warning(
            r".*does \*not\* support Decimal objects natively"
        )
        def run(type_, input_, output, filter_=None, check_scale=False):
            t = Table("t", metadata, Column("a", Integer), Column("x", type_))
            t.create(connection)
            connection.execute(t.insert(), [{"x": x} for x in input_])

            result = {row[1] for row in connection.execute(t.select())}
            output = set(output)
            if filter_:
                result = set(filter_(x) for x in result)
                output = set(filter_(x) for x in output)
            eq_(result, output)
            if check_scale:
                eq_([str(x) for x in result], [str(x) for x in output])

        return run

    @testing.requires.floats_to_four_decimals
    def test_float_as_decimal(self, do_numeric_test):
        do_numeric_test(
            Float(precision=8, asdecimal=True),
            [15.7563, decimal.Decimal("15.7563"), None],
            [decimal.Decimal("15.7563"), None],
            filter_=lambda n: n is not None and round(n, 4) or None,
        )

    def test_float_as_float(self, do_numeric_test):
        do_numeric_test(
            Float(precision=8),
            [15.7563, decimal.Decimal("15.7563")],
            [15.7563],
            filter_=lambda n: n is not None and round(n, 5) or None,
        )

    # ToDo - Fix, or omit
    @testing.requires.precision_generic_float_type
    def test_float_custom_scale(self, do_numeric_test):
        do_numeric_test(
            Float(None, decimal_return_scale=7, asdecimal=True),
            [15.7563827, decimal.Decimal("15.7563827")],
            [decimal.Decimal("15.7563827")],
            check_scale=True,
        )

    def test_render_literal_float(self, literal_round_trip):
        literal_round_trip(
            Float(4),
            [15.7563, decimal.Decimal("15.7563")],
            [15.7563],
            filter_=lambda n: n is not None and round(n, 5) or None,
        )