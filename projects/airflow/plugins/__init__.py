from airflow.plugins_manager import AirflowPlugin

import operators

# Defining the plugin class
class AdrienPlugin(AirflowPlugin):
    name = "adrien_plugin"
    operators = [
        operators.CreateTripsRedshiftOperator,
        operators.FactsCalculatorOperator,
        operators.HasRowsOperator,
        operators.S3ToRedshiftOperator
    ]
    hooks = []
    # A list of class(es) derived from BaseExecutor
    executors = []
    # A list of references to inject into the macros namespace
    macros = []
    # A list of objects created from a class derived
    # from flask_admin.BaseView
    admin_views = []
    # A list of Blueprint object created from flask.Blueprint
    flask_blueprints = []
    # A list of menu links (flask_admin.base.MenuLink)
    menu_links = []
