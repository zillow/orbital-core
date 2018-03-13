

def bootstrap_app(app, root_dir=None,
                  service_name="my service",
                  service_description="this is a service.",
                  min_cpu_percent_for_capture=None):
    """
    :param min_cpu_percent_for_capture: setting this to a floating point value
        configures the percentage that is required to capture that stack
        for flamegraph analysis.
    """
    app[SHUTDOWN_KEY] = False
    app["service_name"] = service_name
    app["service_description"] = service_description
    # app["cpu_capture"] = CpuStackCollector(min_cpu_percent_for_capture)
    app.on_startup.append(on_startup)
    add_routes(app, root_dir)
    _add_signal_handler(app)
    if app.get('config', {}).get('zdc'):
        _init_zdc_metrics(app)


async def on_startup(app):
    pass
    #app["cpu_capture"].start_polling()
