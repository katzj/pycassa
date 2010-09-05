import logging

class PycassaLogger:

    __shared_state = {}

    _LOG_FILENAME = '/var/log/pycassa/system.log'

    _levels = {'debug': logging.DEBUG,
               'info': logging.INFO,
               'warn': logging.WARN,
               'error': logging.ERROR,
               'critical': logging.CRITICAL}

    def __init__(self, level='info', logger_name='pycassa'):
        self.__dict__ = self.__shared_state
        level = PycassaLogger._levels[level]
        logging.basicConfig(level=level)
        self.logger = logging.getLogger(logger_name)
        self.pool_logger = logging.getLogger('%s.pool' % logger_name)


    ### Connection Pool Logging ###

    def connection_created(self, dic):
        level = PycassaLogger._levels[dic.get('level', 'info')]
        conn = dic.get('connection')
        if level <= logging.INFO:
            self.pool_logger.log(level,
                    "Connection %s (%s) opened for %s (id = %s)",
                    id(conn), conn._servers._servers[0], dic.get('pool_type'),
                    dic.get('pool_id'))
        else:
            self.pool_logger.log(level,
                    "Error opening connection (%s) for %s (id = %s): %s",
                    conn._servers._servers[0], dic.get('pool_type'),
                    dic.get('pool_id'), dic.get('error'))

    def connection_checked_out(self, dic):
        level = PycassaLogger._levels[dic.get('level', 'info')]
        conn = dic.get('connection')
        self.pool_logger.log(level,
                "Connection %s (%s) was checked out from %s (id = %s)",
                id(conn), conn._servers._servers[0], dic.get('pool_type'),
                dic.get('pool_id'))

    def connection_checked_in(self, dic):
        level = PycassaLogger._levels[dic.get('level', 'info')]
        conn = dic.get('connection')
        self.pool_logger.log(level,
                "Connection %s (%s) was checked in to %s (id = %s)",
                id(conn), conn._servers._servers[0], dic.get('pool_type'),
                dic.get('pool_id'))
 
    def connection_disposed(self, dic):
        level = PycassaLogger._levels[dic.get('level', 'info')]
        conn = dic.get('connection')
        if level <= logging.INFO:
            self.pool_logger.log(level,
                    "Connection %s (%s) was closed; pool %s (id = %s), reason: %s",
                    id(conn), conn._servers._servers[0], dic.get('pool_type'),
                    dic.get('pool_id'), dic.get('message'))
        else:
            error = dic.get('error')
            self.pool_logger.log(level,
                    "Error closing connection %s (%s) in %s (id = %s), "
                    "reason: %s, error: %s %s",
                    id(conn), conn._servers._servers[0],
                    dic.get('pool_type'), dic.get('pool_id'),
                    dic.get('message'), error.__class__, error)

    def connection_recycled(self, dic):
        level = PycassaLogger._levels[dic.get('level', 'info')]
        old_conn = dic.get('old_conn')
        new_conn = dic.get('new_conn')
        self.pool_logger.log(level,
                "Connection %s (%s) is being recycled in %s (id = %s) "
                "after %d operations; it is replaced by connection %s (%s)",
                id(old_conn), old_conn._servers._servers[0],
                dic.get('pool_type'), dic.get('pool_id'),
                old_conn.operation_count, id(new_conn))

    def connection_failed(self, dic):
        level = PycassaLogger._levels[dic.get('level', 'info')]
        conn = dic.get('connection')
        self.pool_logger.log(level,
                "Connection %s (%s) in %s (id = %s) failed: %s",
                id(conn), dic.get('server'), dic.get('pool_type'),
                dic.get('pool_id'), str(dic.get('error')))

    def obtained_server_list(self, dic):
        level = PycassaLogger._levels[dic.get('level', 'info')]
        self.pool_logger.log(level,
                "Server list obtained for %s (id = %s): [%s]",
                 dic.get('pool_type'), dic.get('pool_id'), ", ".join(dic.get('server_list')))

    def pool_recreated(self, dic):
        level = PycassaLogger._levels[dic.get('level', 'info')]
        self.pool_logger.log(level,
                "%s (id = %s) was recreated",
                dic.get('pool_type'), dic.get('pool_id'))

    def pool_disposed(self, dic):
        level = PycassaLogger._levels[dic.get('level', 'info')]
        self.pool_logger.log(level,
                "%s (id = %s) was disposed",
                dic.get('pool_type'), dic.get('pool_id'))

    def pool_at_max(self, dic):
        level = PycassaLogger._levels[dic.get('level', 'info')]
        self.pool_logger.log(level,
                "%s (id = %s) had a checkout request but was already "
                "at its max size (%s)",
                dic.get('pool_type'), dic.get('pool_id'), dic.get('pool_max'))