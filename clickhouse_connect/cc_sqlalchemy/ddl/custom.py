from sqlalchemy.sql.ddl import DDL
from sqlalchemy.exc import ArgumentError

from clickhouse_connect.driver.query import quote_identifier


class CreateDatabase(DDL):
    """
    SqlAlchemy DDL statement that is essentially an alternative to the built in CreateSchema DDL class
    """
    # pylint: disable-msg=too-many-arguments
    def __init__(self, name: str, engine: str = None, zoo_path: str = None, shard_name: str = '{shard}',
                 replica_name: str = '{replica}'):
        """
        :param name: Database name
        :param engine: Database ClickHouse engine type
        :param zoo_path: ClickHouse zookeeper path for Replicated database engine
        :param shard_name: Clickhouse shard name for Replicated database engine
        :param replica_name: Replica name for Replicated database engine
        """
        if engine and engine not in ('Ordinary', 'Atomic', 'Lazy', 'Replicated'):
            raise ArgumentError(f'Unrecognized engine type {engine}')
        stmt = f'CREATE DATABASE {quote_identifier(name)}'
        if engine:
            stmt += f' Engine {engine}'
            if engine == 'Replicated':
                if zoo_path:
                    stmt += f" ('{zoo_path}', '{shard_name}', '{replica_name}'"
                else:
                    raise ArgumentError('zoo_path is required for Replicated Database Engine')
        super().__init__(stmt)


class DropDatabase(DDL):
    """
    Alternative DDL statement for built in SqlAlchemy DropSchema DDL class
    """
    def __init__(self, name: str):
        super().__init__(f'DROP DATABASE {quote_identifier(name)}')
