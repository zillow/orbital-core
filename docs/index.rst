.. orbital-core documentation master file, created by
   sphinx-quickstart on Fri Mar 16 14:27:15 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Orbital-Core
============

What is Orbital Core?
=====================

Orbital Core is a Python library which provides
basic scaffolding for Orbital applications. Although
it is tailored for Orbital's use case, it is usable
for anyone who would like an opinionated setup of aiohttp
applications.

This documentation explains not only how to use orbital-core, but also the
standards and practices that are followed in an orbital application. The
intention is to be a one-stop guide for someone to understand how orbital apps are constructed, and how to navigate the codebase.

Bootstrapping an Orbital Service
*********************************

During the initialization of your aiohttp app object, call orbital_core.bootstrap_app:

.. code-block:: python

    import os
    from orbital_core import bootstrap_app
    APP_ROOT = os.path.dirname(__file__)

    app = web.Application(loop=loop)
    bootstrap_app(app, APP_ROOT,
                  service_name="example",
                  service_description="example service")

This provides all common functionality across orbital apps. They
are explained in detail in the next section

What Orbital Core Provides
==========================

* aiohttp client via app["http"]
* health check url under /monitor/ping
* Simple landing page with statics mounted at the homepage
* mounting of Sphinx documentation, located at the application root directory, under /docs.
* command line to extract swagger json from bootstrapped app objects.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   best-practices
   libraries
   language-support



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
