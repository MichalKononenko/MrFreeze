Resources
=========

Resources are objects that Mr Freeze requires for manipulating data. These
include the application store and an output CSV file. The store is
responsible for holding the last measured values of variables, and for
notifying interested parties of changes in value.

Store
=====

Abstract Store
~~~~~~~~~~~~~~

The abstract store defines the interface to the application state.

.. automodule:: mr_freeze.resources.abstract_store
    :members:
    :undoc-members:

Application State
~~~~~~~~~~~~~~~~~

.. automodule:: mr_freeze.resources.application_state
    :members:
    :undoc-members:

CSV File
========

.. automodule:: mr_freeze.resources.csv_file
    :members:
    :undoc-members:
