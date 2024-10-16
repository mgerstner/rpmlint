import os

import pytest
from rpmlint.checks.PolkitCheck import PolkitCheck
from rpmlint.filter import Filter

import Testing
from Testing import get_tested_package, get_tested_path


def get_polkit_check(config_path):
    from rpmlint.config import Config

    if not os.path.isabs(config_path):
        config_path = get_tested_path('configs', config_path)
    config = Config([config_path])
    config.info = True
    output = Filter(config)
    test = PolkitCheck(config, output)
    return output, test


@pytest.fixture(scope='function', autouse=True)
def polkit_check():
    return get_polkit_check(Testing.TEST_CONFIG[0])


@pytest.mark.parametrize('package', ['binary/testpolkitcheck'])
def test_check_actions_malformatted(tmp_path, package, polkit_check):
    output, test = polkit_check
    test.check(get_tested_package(package, tmp_path))
    out = output.print_results(output.results)
    assert 'testpolkitcheck.x86_64: E: polkit-xml-exception /usr/share/polkit-1/actions/malformatted.xml.policy raised an exception: mismatched tag: line 23, column 51' in out


@pytest.mark.parametrize('package', ['binary/testpolkitcheck'])
def test_check_actions_ghost_file(tmp_path, package, polkit_check):
    output, test = polkit_check
    test.check(get_tested_package(package, tmp_path))
    out = output.print_results(output.results)
    assert 'testpolkitcheck.x86_64: E: polkit-ghost-file /usr/share/polkit-1/actions/ghost.policy' in out


@pytest.mark.parametrize('package', ['binary/testpolkitcheck'])
def test_check_actions_missing_allow_type(tmp_path, package, polkit_check):
    output, test = polkit_check
    test.check(get_tested_package(package, tmp_path))
    out = output.print_results(output.results)
    assert 'testpolkitcheck.x86_64: E: polkit-untracked-privilege missing.allow.type (no:auth_admin_keep:auth_admin_keep)' in out


@pytest.mark.parametrize('package', ['binary/testpolkitcheck'])
def test_check_actions_auth_admin(tmp_path, package, polkit_check):
    output, test = polkit_check
    test.check(get_tested_package(package, tmp_path))
    out = output.print_results(output.results)
    assert 'testpolkitcheck.x86_64: E: polkit-untracked-privilege auth.admin.policy (auth_admin:no:auth_admin_keep)' in out
