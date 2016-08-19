# fusefit

## References

Docs used:

- http://www.dcrainmaker.com/tools
- http://lxml.de/tutorial.html#namespaces
- http://stackoverflow.com/questions/1786476/parsing-xml-in-python-using-elementtree-example
- https://docs.python.org/3/library/xml.etree.elementtree.html
- http://pandas.pydata.org/pandas-docs/version/0.15.0/generated/pandas.Series.interpolate.html?highlight=interpolate#pandas.Series.interpolate
- http://stackoverflow.com/questions/30530001/python-pandas-time-series-interpolation-and-regularization
- http://pandas.pydata.org/pandas-docs/stable/missing_data.html


## Setup the web app

`python -m venv flask`

In Windows: `flask\Scripts\pip install flask matplotlib numpy pandas lxml`

Virtual environments can be activated and deactivated, if desired. An activated environment adds the location of its bin folder to the system path, so that for example, when you type python you get the environment's version and not the system's one. But activating a virtual environment is not necessary, it is equally effective to invoke the interpreter by specifying its pathname.

If you want to activate a virtual environment, and if you are a Windows user, the following command is for you: `venv\scripts\activate`

Either way, you should now be using your virtualenv (notice how the prompt of your shell has changed to show the active environment).

And if you want to go back to the real world, use the following command: `deactivate`

After doing this, the prompt of your shell should be as familiar as before.


## Run our app

In Windows: `flask\Scripts\python run.py`

Goto: `http://localhost:5000`
