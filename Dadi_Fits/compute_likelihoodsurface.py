import sys
import os
import logging
import time
import argparse
import warnings

import numpy as np
import pandas as pd
import dadi
import dadi.DFE as DFE
import Selection
import scipy.stats.distributions
import scipy.integrate
import scipy.optimize
from tqdm import tqdm


###############
## FUNCTIONS ##
###############

def likelihood(nu, tau, syn_data, func_ex, pts_l):
    """Calculate the likelihood of the model given the parameters nu and tau,
    and a function func_ex"""

    p0 = [nu, tau]
    popt = p0
    syn_ns = syn_data.sample_sizes  # Number of samples.
    non_scaled_spectrum = func_ex(popt, syn_ns, pts_l)
    theta = dadi.Inference.optimal_sfs_scaling(
        non_scaled_spectrum, syn_data)
    loglik = dadi.Inference.ll_multinom(
        model=non_scaled_spectrum, data=syn_data)
    return(loglik)


def two_epoch(params, ns, pts):
    """Define a two-epoch demography, i.e., an instantaneous size change.

    params = (nu, T)
        nu: Ratio of contemporary to ancient population size.
        T: Time in the past at which size change occured,
            in units of 2*N_a.
    ns = (n1, )
        n1: Number of samples in resulting Spectrum object.
    pts: Number of grid points to use in integration.
    """
    nu, T = params  # Define given parameters.
    xx = dadi.Numerics.default_grid(pts)  # Define likelihood surface.
    phi = dadi.PhiManip.phi_1D(xx)  # Define initial phi.

    phi = dadi.Integration.one_pop(phi, xx, T, nu)  # Integrate.

    # Construct Spectrum object.
    fs = dadi.Spectrum.from_phi(phi, ns, (xx,))
    return fs


def one_epoch(params, ns, pts):
    """Define a one-epoch demography, equivalent to a standard neutral model. 

    ns = (n1, )
        n1: Number of samples in resulting Spectrum object.
    pts: Number of grid points to use in integration.
    """
    xx = dadi.Numerics.default_grid(pts)  # Define likelihood surface.
    phi = dadi.PhiManip.phi_1D(xx)  # Define initial phi.

    # Construct Spectrum object.
    fs = dadi.Spectrum.from_phi(phi, ns, (xx, ))
    return fs


#############
##MAIN CODE##
#############

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Compute likelihood surface for demographic models.")
    parser.add_argument("--demography_file", type=str, required=True,
                        help="Path to the two-epoch demographic model file.")
    parser.add_argument("--syn_data_file", type=str, required=True,
                        help="Path to the synonymous data file.")
    parser.add_argument("--npts", type=int, default=10,
                        help="Number of points in the grid for likelihood surface.")
    parser.add_argument("--suffix", type=str, default="",
                        help="Suffix for the output files.")
    args = parser.parse_args()
    

    #Inputs
    syn_sfs = args.syn_data_file
    demography_file = args.demography_file
    npts = args.npts
    suffix = args.suffix

    #Set up log file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(script_dir, f"compute_loglikesurface_log_{suffix}.log")
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Add a StreamHandler to output logs to stdout
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Set the logging level for the console
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    console_handler.flush = True # Ensure immediate output to stdout
    logging.getLogger().addHandler(console_handler) # Add the console handler to the root logger

    logging.info("Parsing demographic model and synonymous data file.")

    #Parse the scaled two-epoch demography
    with open(demography_file, 'r') as file:
        for line in file:
            if 'Maximum multinomial log composite likelihood: ' in line:
                parsed_params=line.strip().strip('.').split(': ')[1]
                logging.info(parsed_params)
                likelihood_model=float(parsed_params)
            elif 'Scaled best-fit model spectrum: ' in line:
                parsed_params=line.strip().strip('.').split(': ')[1]
                parsed_params=parsed_params.strip('[--').strip('--]')
                values=parsed_params.split()
            #Get the theta value
            elif 'Optimal value of theta_syn: ' in line:
                parsed_params=line.strip().strip('.').split(': ')[1]
                theta_syn=float(parsed_params)
                logging.info(theta_syn)
            #Get the best fit parameteres
            elif 'Best fit parameters: ' in line:
                parsed_params=line.strip().strip('.').split(': ')[1]
                parsed_params=parsed_params.strip('[').strip(']')
                demog_params=[float(x.strip(',')) for x in parsed_params.split()]
                logging.info(demog_params)# Load the demographic model


    # Construct initial Spectrum object from input synonymous sfs.
    syn_data = dadi.Spectrum.from_file(syn_sfs)
    syn_ns = syn_data.sample_sizes  # Number of samples.
    pts_l = [1200, 1400, 1600]

    #Set up the demographic functions
    models={}

    for model in [one_epoch, two_epoch]:
        func_ex = dadi.Numerics.make_extrap_log_func(model)
        models[model.__name__] = func_ex

    func_ex=models['two_epoch']

    #Set up the computation of the likelihood surfaces
    x,y = demog_params #Input nu, T
    input_nu, input_tau = demog_params

    #Setting up nu,T grid
    if (x * 3.99) < 2.0:
        x_max = 2.0
    else:
        x_max = x * 3.99

    min_val = min([0.01, x, y])
    max_val = max([x_max, y * 3.99])

    x_range = np.linspace(min_val, max_val, npts)
    y_range = np.linspace(min_val, max_val, npts)
    X, Y = np.meshgrid(x_range, y_range)
    Z = np.empty((npts, npts))

    logging.info("Setup done")
    logging.info("Input nu, tau: ", input_nu, input_tau)
    logging.info("Number of points: ", npts)
    logging.info("x_range: ", x_range)
    logging.info("y_range: ", y_range)

    #The original chosen liklihood
    max_likelihood = likelihood(input_nu, input_tau, syn_data, func_ex, pts_l)
    new_maxlike_found = False

    logging.info("Initial maximum likelihood: ", max_likelihood)
    logging.info("Initial parameters: ", input_nu, input_tau)

    #Computing the log-likelihood surface
    x_val = []
    y_val = []
    z_val = []
    for i in tqdm(range(0, npts)):
        if i % 10 == 0:
            logging.info("Processing row: ", i, flush=True)
        for j in range(0, npts):
            Z[i, j] = likelihood(x_range[i], y_range[j], syn_data, func_ex, pts_l)
            x_val.append(x_range[i])
            y_val.append(y_range[j])
            z_val.append(Z[i, j])
            if Z[i, j] > max_likelihood + 0.01:
                logging.info("New maximum likelihood found:")
                logging.info(max_likelihood)
                logging.info(Z[i, j])
                logging.info(x_range[i], y_range[j])
                max_likelihood_new = Z[i, j] * 1.0
                best_params_new = [x_range[i], y_range[j]]
                new_maxlike_found = True
    df = pd.DataFrame({'X': x_val, 'Y': y_val, 'Z': z_val})
    likelihood_surface = f"likelihood_surface_{suffix}.csv"
    df.to_csv(likelihood_surface)

    if new_maxlike_found:
        logging.info("New maximum likelihood found:")
        logging.info(max_likelihood_new)
        logging.info(best_params_new)

    logging.info("Execution completed successfully.")
