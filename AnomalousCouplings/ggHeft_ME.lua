-- Load the library containing the matrix element
load_modules('/afs/cern.ch/user/c/cgarcias/workspace/private/Run3/mkShapesRDF/momemta/ggHeft_ME/build/libme_ggHeft_ME.so')

higgs = declare_input("higgs")
jet1 = declare_input("jet1")
jet2 = declare_input("jet2")

cuba = {
    algorithm = "cuhre"
}

parameters = {
    energy = 13000.,
}

GaussianTransferFunctionOnEnergy.tf_higgs = {
  ps_point = add_dimension(), -- A transfer function integrates over a variable (the particle's energy), so we need a new dimension in the integrated volume
  reco_particle = higgs.reco_p4, -- Pass the input tag corresponding to the experimentally reconstructed 4-vector of the particle, given to 'computeWeights()'
  sigma = 0.10, -- Take 10% resolution on the energy
  sigma_range = 5.0 -- Integrate from -5*sigma*E to +5*sigma*E
}

higgs.set_gen_p4("tf_higgs::output") -- Set the gen p4 of the input to be the output of the transfer function

inputs = {
    higgs.gen_p4,
    jet1.reco_p4,
    jet2.reco_p4,
}

-- Build the partonic initial state
BuildInitialState.boost = {
    do_transverse_boost = true,
    particles = inputs,
}

-- Call matrix element on fully defined partonic event
MatrixElement.ggHeft = {
    pdf = "CT10nlo",
    pdf_scale = 125.,
    matrix_element = "ggHeft_ME_heft_P1_Sigma_heft_gg_hgg",
    matrix_element_parameters = {
        card = "/afs/cern.ch/user/c/cgarcias/workspace/private/Run3/mkShapesRDF/momemta/ggHeft_ME/Cards/param_card.dat"
    },
    initialState = "boost::partons",
    particles = {
        inputs = inputs,
        ids = {
            {
                pdg_id = 25,
                me_index = 1,
            },
            {
                pdg_id = 2,
                me_index = 2,
            },
            {
                pdg_id = -2,
                me_index = 3,
            },
        }
    },
}

-- Define quantity to be returned to MoMEMta
integrand("ggHeft::output")