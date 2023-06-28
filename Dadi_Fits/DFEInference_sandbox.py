# Load in nonsynonymous data
nonsyn_data = dadi.Spectrum.from_file(nonsyn_input_sfs)
nonsyn_ns = nonsyn_data.sample_sizes

# Use best fit demographic model for DFE inference
best_model = max(model_LL_dict, key=model_LL_dict.get)

one_epoch_bool = False
if best_model == 'exponential_growth':
    func_sel = self.growth_sel
elif best_model == 'two_epoch':
    func_sel = self.two_epoch_sel
elif best_model == 'bottleneck_growth':
    func_sel = self.bottlegrowth_sel
elif best_model == 'three_epoch':
    func_sel = self.three_epoch_sel
else:
    # Best model is one-epoch
    # There is no way to incorporate selection in a one-epoch model
    # We use two epoch assumption instead
    one_epoch_bool = True
    best_model = 'two_epoch'
    func_sel = self.two_epoch_sel

# Infer DFE based on best demographic parameters
demog_params = model_params_dict[best_model]

# Define standard mutation rates and lenghts
Ls = 9728061 #Change this as necessary, currently set to E4_Zero lenght
mu = 1.5E-8 # Change this as necessary
Na = theta_syn / (4 * mu * Ls)
max_s = 0.5
max_gam = max_s * 2 * Na

#Change this according to sample size
# Redefine grid for MLE search
pts_l = [200, 210, 220]

logger.info('Generating spectra object.')

spectra = DFE.Cache1D(demog_params, nonsyn_ns,
    func_sel, pts_l=pts_l,
    gamma_bounds=(1e-5, max_gam),
    gamma_pts=300, verbose=True, mp=True)

# Assume gamma-distributed DFE
BETAinit = 3 * max_gam
initial_guess = [1e-3, BETAinit]
upper_beta = 12 * max_gam
lower_bound = [1e-3, 0]
upper_bound = [100, upper_beta]

# Track DFE inferences to find best MLE
gamma_max_likelihoods = []
gamma_guesses = dict()
for i in range(25):
    p0 = initial_guess
    # Randomly perturb around initial guess
    p0 = dadi.Misc.perturb_params(p0, lower_bound=lower_bound,
                                  upper_bound=upper_bound)
    logger.info(
        'Beginning optimization with guess, {0}.'.format(p0))
    # MLE search for DFE
    popt = numpy.copy(dadi.Inference.optimize_log(p0, nonsyn_data, spectra.integrate, pts=None,
              func_args=[DFE.PDFs.gamma, theta_nonsyn],
              lower_bound=lower_bound, upper_bound=upper_bound,
              verbose=len(best_params), maxiter=25, multinom=True))
    logger.info(
        'Finished optomization, results are {0}.'.format(popt))
    #Compute the poisson log likelihood
    expected_sfs = spectra.integrate(
        popt, None, DFE.PDFs.gamma, theta_nonsyn, None)
    poisson_ll_nonsyn = dadi.Inference.ll(model=expected_sfs, data=nonsyn_data)
    gamma_max_likelihoods.append(poisson_ll_nonsyn)
    gamma_guesses[poisson_ll_nonsyn] = popt

logger.info('Finished DFE inference.')

# Sort likelihoods
gamma_max_likelihoods.sort(reverse=True)

logger.info('Integrating expected site-frequency spectrum.')

logger.info('Outputting results.')

with open(inferred_DFE, 'w') as f:
    if one_epoch_bool:
        f.write('The best demographic model is one-epoch.\n')
        f.write('Take these inferences with a grain of salt.\n')
    else:
        f.write('Best demographic model: {0}.\n'.format(best_model))
    f.write('Assuming a gamma-distributed DFE...\n')
    f.write('Outputting MLE estimates in order.\n')
    for i in range(25):
        best_popt = gamma_guesses[gamma_max_likelihoods[i]]
        # Compute model SFS under inferred DFE
        expected_sfs = spectra.integrate(
            best_popt, None, DFE.PDFs.gamma, theta_nonsyn, None)
        f.write('The population-scaled '
                'best-fit parameters: {0}.\n'.format(best_popt))
        #Compute the poisson likelihood of the nonsyn model given by the gamma
        poisson_ll_nonsyn = dadi.Inference.ll(model=expected_sfs, data=nonsyn_data)
        f.write('The maximum poisson log '
                'composite likelihood is: {0}.\n'.format(poisson_ll_nonsyn))
        # Divide output scale parameter by 2 * N_a
        f.write(
            'The non-scaled best-fit parameters: '
            '[{0}, array({1})].\n'.format(
                best_popt[0],
                numpy.divide(best_popt[1],
                             numpy.array([1, 2 * Na]))))
        f.write('The expected SFS is: {0}.\n\n'.format(
            expected_sfs))
logger.info('Pipeline executed succesfully.')
