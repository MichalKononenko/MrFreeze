Tasks
=====

Tasks are the primary unit of execution in Mr Freeze. It is assumed that a
task can be submitted to an :class:`concurrent.futures.Executor`.

Abstract Tasks and Base classes
-------------------------------

These tasks are not meant to be instantiated directly, but instead serve as
base classes for more specific tasks.

Abstract Task
~~~~~~~~~~~~~

.. automodule:: mr_freeze.tasks.abstract_task
    :members:
    :undoc-members:

Report Variable Task
~~~~~~~~~~~~~~~~~~~~

.. automodule:: mr_freeze.tasks.report_variable_task
    :members:
    :undoc-members:

Concrete Tasks
--------------

Get Current Date
~~~~~~~~~~~~~~~~

.. automodule:: mr_freeze.tasks.get_current_date
    :members:
    :undoc-members:

Make Measurement
~~~~~~~~~~~~~~~~

.. automodule:: mr_freeze.tasks.make_measurement
    :members:
    :undoc-members:

Report Current
~~~~~~~~~~~~~~

.. automodule:: mr_freeze.tasks.report_current
    :members:
    :undoc-members:

Report Liquid Nitrogen Level
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: mr_freeze.tasks.report_liquid_nitrogen_level
    :members:
    :undoc-members:

Report Magnetic Field
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: mr_freeze.tasks.report_magnetic_field
    :members:
    :undoc-members:

Update Store
~~~~~~~~~~~~

.. automodule:: mr_freeze.tasks.update_store
    :members:
    :undoc-members:
