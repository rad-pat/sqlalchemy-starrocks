# # coding: utf-8


from sqlalchemy.testing.suite import *
# from sqlalchemy.testing.suite.test_select import *
# from sqlalchemy.testing.suite.test_select import FetchLimitOffsetTest

from sqlalchemy.testing.assertions import AssertsCompiledSQL
from sqlalchemy import Table, Column, Integer, MetaData, select
from sqlalchemy import schema


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

