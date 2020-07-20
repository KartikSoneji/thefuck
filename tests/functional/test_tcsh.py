import pytest
from tests.functional.plots import with_confirmation, without_confirmation, \
    refuse_with_confirmation, select_command_with_arrows

dockerfile = ('thefuck/tcsh',
              u'''FROM python:3
                   RUN apt-get update
                   RUN apt-get install -yy tcsh''',
              u'tcsh')


@pytest.fixture(params=[dockerfile])
def proc(request, spawnu, TIMEOUT):
    proc = spawnu(*request.param)
    proc.sendline(u'pip install /src')
    assert proc.expect([TIMEOUT, u'Successfully installed'])
    proc.sendline(u'tcsh')
    proc.sendline(u'setenv PYTHONIOENCODING utf8')
    proc.sendline(u'eval `thefuck --alias`')
    return proc


@pytest.mark.functional
def test_with_confirmation(proc, TIMEOUT):
    with_confirmation(proc, TIMEOUT)


@pytest.mark.functional
def test_select_command_with_arrows(proc, TIMEOUT):
    select_command_with_arrows(proc, TIMEOUT)


@pytest.mark.functional
def test_refuse_with_confirmation(proc, TIMEOUT):
    refuse_with_confirmation(proc, TIMEOUT)


@pytest.mark.functional
def test_without_confirmation(proc, TIMEOUT):
    without_confirmation(proc, TIMEOUT)

# TODO: ensure that history changes.
