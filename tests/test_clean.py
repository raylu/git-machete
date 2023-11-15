from pytest_mock import MockerFixture

from .base_test import BaseTest
from .mockers import (assert_success, launch_command, mock_input_returning_y,
                      read_branch_layout_file, rewrite_branch_layout_file)
from .mockers_github import mock_github_token_for_domain_none


class TestClean(BaseTest):

    def test_clean(self, mocker: MockerFixture) -> None:
        self.patch_symbol(mocker, 'builtins.input', mock_input_returning_y)
        (
            self.repo_sandbox.new_branch('master')
                .commit()
                .push()
                .new_branch('bar')
                .commit()
                .new_branch('bar2')
                .commit()
                .check_out('master')
                .new_branch('foo')
                .commit()
                .push()
                .new_branch('foo2')
                .commit()
                .check_out('master')
                .new_branch('moo')
                .commit()
                .new_branch('moo2')
                .commit()
                .check_out('master')
                .new_branch('mars')
                .commit()
                .new_branch('baz')
                .commit()
                .push()
                .check_out('master')
        )

        body: str = \
            """
            master
                bar
                    bar2
                foo
                    foo2
                moo
                    moo2
            mars
            baz
            """
        rewrite_branch_layout_file(body)

        launch_command('clean')

        assert read_branch_layout_file() == "master\n    bar\n    foo\n    moo\nbaz\n"

        expected_status_output = (
            """
              master *
              |
              o-bar (untracked)
              |
              o-foo
              |
              o-moo (untracked)
              
              baz
            """
        )
        assert_success(['status'], expected_status_output)

        branches = self.repo_sandbox.get_local_branches()
        assert 'foo' in branches
        assert 'baz' in branches
        assert 'mars' not in branches
