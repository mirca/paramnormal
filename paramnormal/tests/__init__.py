from warnings import simplefilter
from numpy import errstate
from numpy.testing import Tester

class _NoseWrapper(Tester):  # pragma: no cover
    """
    This is simply a monkey patch for numpy.testing.Tester.
    It allows extra_argv to be changed from its default None to ['--exe'] so
    that the tests can be run the same across platforms.  It also takes kwargs
    that are passed to numpy.errstate to suppress floating point warnings.
    """
    def test(self, label='fast', verbose=1, extra_argv=['--exe'],
             doctests=False, coverage=False, **kwargs):
        ''' Run tests for module using nose
        %(test_header)s
        doctests : boolean
            If True, run doctests in module, default False
        coverage : boolean
            If True, report coverage of NumPy code, default False
            (Requires the coverage module:
             http://nedbatchelder.com/code/modules/coverage.html)
        kwargs
            Passed to numpy.errstate.  See its documentation for details.
        '''

        # cap verbosity at 3 because nose becomes *very* verbose beyond that
        verbose = min(verbose, 3)

        from numpy.testing import utils
        utils.verbose = verbose

        if doctests:
            print("Running unit tests and doctests for %s" % self.package_name)
        else:
            print("Running unit tests for %s" % self.package_name)

        self._show_system_info()

        # reset doctest state on every run
        import doctest
        from numpy.testing.noseclasses import NumpyTestProgram

        doctest.master = None

        argv, plugins = self.prepare_test_args(label, verbose, extra_argv,
                                               doctests, coverage)
        with errstate(**kwargs):
            simplefilter('ignore', category=DeprecationWarning)
            t = NumpyTestProgram(argv=argv, exit=False, plugins=plugins)

        return t.result

test = _NoseWrapper().test