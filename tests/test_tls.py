from nose.tools import (
    raises,
)
import datajoint as dj
from . import CONN_INFO
from pymysql.err import OperationalError


class TestTLS:
    @staticmethod
    def test_secure_connection():
        result = (
            dj.conn(reset=True, **CONN_INFO)
            .query("SHOW STATUS LIKE 'Ssl_cipher';")
            .fetchone()[1]
        )
        assert len(result) > 0

    @staticmethod
    def test_insecure_connection():
        result = (
            dj.conn(use_tls=False, reset=True, **CONN_INFO)
            .query("SHOW STATUS LIKE 'Ssl_cipher';")
            .fetchone()[1]
        )
        assert result == ""

    @staticmethod
    @raises(OperationalError)
    def test_reject_insecure():
        dj.conn(
            CONN_INFO["host"], user="djssl", password="djssl", use_tls=False, reset=True
        ).query("SHOW STATUS LIKE 'Ssl_cipher';").fetchone()[1]
