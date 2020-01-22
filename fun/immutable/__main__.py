# TODO : strict minimal ipython REPL launcher to use aiokraken.
# Nice TUI|GUI can be done in another project.

# !/usr/bin/env python
# Ref : https://ipython.org/ipython-doc/stable/interactive/reference.html#embedding-ipython


"""
__main__ has only the code required to start IPython and provide interactive introspection of aiokraken while running
"""

import click


def ipshell_embed_setup():

    from traitlets.config.loader import Config

    try:
        get_ipython
    except NameError:
        nested = 0
        cfg = Config()
    else:
        print("Running nested copies of IPython.")
        print("The prompts for the nested copy have been modified")
        cfg = Config()
        nested = 1

    # First import the embeddable shell class
    from IPython.terminal.embed import InteractiveShellEmbed

    # Now create an instance of the embeddable shell. The first argument is a
    # string with options exactly as you would type them if you were starting
    # IPython at the system command line. Any parameters you want to define for
    # configuration can thus be specified here.
    ipshell = InteractiveShellEmbed(config=cfg,
                                    banner1='Dropping into IPython',
                                    banner2='To introspect: %whos',
                                    exit_msg='Leaving Interpreter, back to program.')

    # Remember the dummy mode to disable all embedded shell calls!

    return ipshell



@click.group()
def cli():
    pass



if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        # we use click to run a simple command
        cli()
    else:
        # or we go full interactive mode (no args)

        # First create a config object from the traitlets library
        from traitlets.config import Config
        c = Config()

        # Now we can set options as we would in a config file:
        #   c.Class.config_value = value
        # For example, we can set the exec_lines option of the InteractiveShellApp
        # class to run some code when the IPython REPL starts
        c.InteractiveShellApp.exec_lines = [
            'print("\\nimporting immutable...\\n")',
            'from immutable.looperlist import looperlist',
            "from immutable.looperset import looperset"
        ]
        c.InteractiveShell.colors = 'LightBG'
        c.InteractiveShell.confirm_exit = False
        c.TerminalIPythonApp.display_banner = False

        #TODO : %autoawait to easily run requests

        # Now we start ipython with our configuration
        import IPython
        IPython.start_ipython(config=c, )




