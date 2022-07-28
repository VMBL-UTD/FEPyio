from dataclasses import dataclass
from typing import Literal, Optional

from .feb_base import FebBase


@dataclass
class Solver(FebBase):
    """FEBio > Control > Solver.

    Parameters
    ----------
    etol : float, optional
        Convergence tolerance on energy.
    rtol : float, optional
        Convergence tolerance on residual.
    lstol : float, optional
        Convergence tolerance on line search.
    dtol : float, optional
        Convergence tolerance on displacement.
    max_refs : int, optional
        Max number of stiffness reformation.
    max_ups : int, optional
        Max number of BFGS/Broyden stiffness updates.
    diverge_reform : int, optional
        Flag for reforming stiffness matrix when the solution diverges.
    reform_each_time_step : int, optional
        Flag for reforming stiffness matrix at the start of each time step.
    min_residual : float, optional
        Sets minimal value for residual tolerance.
    qnmethod : {"BFGS", "Broyden"}, optional
        Quasi-Newton update method.
    rhoi : float, optional
        Spectral radius parameter. :math:`\\rho_{\\infty}`.
    symmetric_stiffness : {0, 1, 2}, optional
        Use symmetric stiffness matrix flag. 0: unsymmetric, 1: symmetric, 2:
        structurally symmetric

    Attributes
    ----------
    etol : float, optional
        Convergence tolerance on energy.
    rtol : float, optional
        Convergence tolerance on residual.
    lstol : float, optional
        Convergence tolerance on line search.
    dtol : float, optional
        Convergence tolerance on displacement.
    max_refs : int, optional
        Max number of stiffness reformation.
    max_ups : int, optional
        Max number of BFGS/Broyden stiffness updates.
    diverge_reform : int, optional
        Flag for reforming stiffness matrix when the solution diverges.
    reform_each_time_step : int, optional
        Flag for reforming stiffness matrix at the start of each time step.
    min_residual : float, optional
        Sets minimal value for residual tolerance.
    qnmethod : {"BFGS", "Broyden"}, optional
        Quasi-Newton update method.
    rhoi : float, optional
        Spectral radius parameter. :math:`\\rho_{\\infty}`.
    symmetric_stiffness : {0, 1, 2}, optional
        Use symmetric stiffness matrix flag. 0: unsymmetric, 1: symmetric, 2:
        structurally symmetric
    _key = "Solver"

    Notes
    -----
    See: [FEBio manual section 3.3.3](https://help.febio.org/FebioUser/FEBio_um_3-4-Subsection-3.3.3.html).
    """

    # fmt: off
    etol:  Optional[float] = None
    rtol:  Optional[float] = None
    lstol: Optional[float] = None
    dtol:  Optional[float] = None
    max_refs: Optional[int] = None
    max_ups:  Optional[int] = None
    diverge_reform:        Optional[int] = None
    reform_each_time_step: Optional[int] = None
    min_residual:          Optional[float] = None
    qnmethod: Optional[Literal["BFGS", "Broyden"]] = None
    rhoi:     Optional[float] = None
    symmetric_stiffness:   Optional[Literal[0, 1, 2]] = None
    # fmt: on
    _key: str = "solver"


@dataclass
class TimeStepper(FebBase):
    """FEBio > Control > Time Stepper.

    Parameters
    ----------
    dtmin : float
        Minimum time step size.
    dtmax : float
        Maximum time step size.
    max_retries : int, optional
        Maximum number of times a time step is restarted.
    opt_iter : int, optional
        Optimal, or desired, number of iterations per time step.
    _key = "time_stepper"

    Attributes
    ----------
    dtmin : float
        Minimum time step size.
    dtmax : float
        Maximum time step size.
    max_retries : int, optional
        Maximum number of times a time step is restarted.
    opt_iter : int, optional
        Optimal, or desired, number of iterations per time step.
    _key = "time_stepper"

    Notes
    -----
    See [FEBio manual section 3.3.2](https://help.febio.org/FebioUser/FEBio_um_3-4-Subsection-3.3.2.html).
    """

    dtmin: float
    dtmax: float
    max_retries: Optional[int] = None
    opt_iter: Optional[int] = None
    _key: str = "time_stepper"


@dataclass
class Control(FebBase):
    """FEBio control section

    Parameters
    ----------
    analysis : {"STATIC", "STEADY-STATE", "DYNAMIC"}
    time_steps : int
        Total number of time steps.
    step_size : float
        The initial time step size.
    solver : feb.Solver, optional.
        Set the FEBio Solver.
    time_stepper : feb.TimeStepper, optional
        Set the FEBio Time Stepper.
    output_level : {"OUTPUT_NEVER", "OUTPUT_MUST_POINTS", "OUTPUT_MAJOR_ITS", "OUTPUT_MINOR_ITRS", "OUTPUT_FINAL"}, optional

    Attributes
    ----------
    analysis : {"STATIC", "STEADY-STATE", "DYNAMIC"}
        Sets the analysis type.
    time_steps : int
        Total number of time steps.
    step_size : float
        The initial time step size.
    solver : feb.Solver, optional.
        Set the FEBio Solver.
    time_stepper : feb.TimeStepper, optional
        Set the FEBio Time Stepper.
    output_level : {"OUTPUT_NEVER", "OUTPUT_MUST_POINTS", "OUTPUT_MAJOR_ITS", "OUTPUT_MINOR_ITRS", "OUTPUT_FINAL"}, optional
        Controls when to output data to file
    _key = "Control"

    Notes
    -----
    See: [FEBio manaul section 3.3](https://help.febio.org/FebioUser/FEBio_um_3-4-Section-3.3.html).
    """

    analysis: Literal["STATIC", "STEADY-STATE", "DYNAMIC"]
    time_steps: int
    step_size: float
    solver: Optional[Solver] = None
    time_stepper: Optional[TimeStepper] = None
    output_level: Optional[
        Literal[
            "OUTPUT_NEVER",
            "OUTPUT_MUST_POINTS",
            "OUTPUT_MAJOR_ITRS",
            "OUTPUT_MINOR_ITRS",
            "OUTPUT_FINAL",
        ]
    ] = None
