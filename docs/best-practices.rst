Best Practices
==============

This page illustrates the best practices used within orbital applications.

Code Organization
*****************

The following hierarchy is recommended:

* <app_name>
  * clients/ - clients to external services, databases
    * client_name.py - should be named after the client itself.
  * lib/ - business logic lives here.
  * routes/ - APIs exposed.
  * tests


Test Code Organization
**********************

If the test is specific to one module, the test should live in a file that
matches that module in path and name. For example, if testing a user client
which should be located at app/clients/user.py, you would put your test in
app/tests/clients/test_user.py.

Why Package Test Code with the Service?
---------------------------------------

There is a separate practice of moving tests into a directory separate from the
application itself. This has a couple disadvantages:

1. It is not possible to do relative imports.

2. The test code is not deployed alongside the application code, so you
   are not able to quickly glance at unit tests to get a better understanding
   of how code is intended to be used.


Interface should be HTTP over JSON
**********************************

For a majority of applications, the interface exposed should be HTTP over JSON.
Although this is not a hard rule, standardizing around some common protocol ensures
maximum tool sharing to faciliate these interactions.
