-- Load the library containing the matrix element
load_modules('/afs/cern.ch/user/c/cgarcias/workspace/private/Run3/mkShapesRDF/momemta/JJZ_ME/build/libme_JJZ_ME.so')

Z = declare_input("Z")
jet1 = declare_input("jet1")
jet2 = declare_input("jet2")


parameters = {
    energy = 13000.,
}

--[[ GaussianTransferFunctionOnEnergy.tf_jet1 = {
  ps_point = add_dimension(), -- A transfer function integrates over a variable (the particle's energy), so we need a new dimension in the integrated volume
  reco_particle = jet1.reco_p4, -- Pass the input tag corresponding to the experimentally reconstructed 4-vector of the particle, given to 'computeWeights()'
  sigma = 0.05, -- Take 5% resolution on the energy
}

GaussianTransferFunctionOnEnergy.tf_jet2 = {
  ps_point = add_dimension(), -- A transfer function integrates over a variable (the particle's energy), so we need a new dimension in the integrated volume
  reco_particle = jet2.reco_p4, -- Pass the input tag corresponding to the experimentally reconstructed 4-vector of the particle, given to 'computeWeights()'
  sigma = 0.05, -- Take 5% resolution on the energy
}
 ]]
-- Set the gen p4 of the input to be the output of the transfer function
--[[ jet1.set_gen_p4("tf_jet1::output")
jet2.set_gen_p4("tf_jet2::output") ]]

inputs = {
    higgs.reco_p4,
    jet1.reco_p4,
    jet2.reco_p4,
}

-- Build the partonic initial state
BuildInitialState.boost = {
    do_transverse_boost = true,
    particles = inputs,
}

-- Call matrix element on fully defined partonic event
MatrixElement.JJZ = {
    pdf = "CT10nlo",
    pdf_scale = 91.,
    matrix_element = "JJZ_ME_sm_P1_Sigma_sm_gg_zuux",
    matrix_element_parameters = {
        card = "/afs/cern.ch/user/c/cgarcias/workspace/private/Run3/mkShapesRDF/momemta/JJZ_ME/Cards/param_card.dat"
    },
    initialState = "boost::partons",
    particles = {
        inputs = inputs,
        ids = {
            {
                pdg_id = 23,
                me_index = 1,
            },
            {
                pdg_id = 1,
                me_index = 2,
            },
            {
                pdg_id = -1,
                me_index = 3,
            },
        }
    },
}

-- Define quantity to be returned to MoMEMta
integrand("JJZ::output")
