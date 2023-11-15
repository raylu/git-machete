.. _clean:

clean
=====
**Usage:**

.. code-block:: shell

    git machete clean [-y|--yes]

    Deletes managed branches with missing tracking branches that have no downstream branch.

    Generally, branches get into this state by being pushed and then having the remote branch deleted.

No branch will be deleted unless explicitly confirmed by the user (or unless ``-y/--yes`` option is passed).

**Options:**

-y, --yes                  Don't ask for confirmation when deleting branches from git.
