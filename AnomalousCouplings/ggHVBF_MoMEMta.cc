/* Including ConfigurationReader.h library */
#include "momemta/ConfigurationReader.h"
/* Including MoMEMta.h library */
#include "momemta/MoMEMta.h"
/* Including Types.h library */
#include "momemta/Types.h"
/* Including ROOT and other necessary libraries */
#include "TLorentzVector.h"
#include <vector>
#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include <iostream>
#include <TMath.h>
#include <math.h>
#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;

class RECOME_ggHVBF_MoMEMta {
    public:
        float nCleanJet,  nLepton;
        float PuppiMet_pt,  PuppiMet_phi;
        RVecF Lepton_pt,  Lepton_phi,  Lepton_eta, CleanJet_pt,  CleanJet_phi,  CleanJet_eta;

        RECOME_ggHVBF_MoMEMta() {}

        void normalizeInput(LorentzVector& p4) {
            if (p4.M() > 0)
                return; // Increase the energy until M is positive                                                                                                                                 
            p4.SetE(p4.P());
            while (p4.M2() < 0) {
                double delta = p4.E() * 1e-5;
                p4.SetE(p4.E() + delta);
            };
        }
        RVecF operator()(float _nCleanJet,
            float _nLepton, float _PuppiMet_pt, float _PuppiMet_phi,
            RVecF _Lepton_pt, RVecF _Lepton_phi, RVecF _Lepton_eta,
            RVecF _CleanJet_pt, RVecF _CleanJet_phi, RVecF _CleanJet_eta) {

            nCleanJet=_nCleanJet;  nLepton=_nLepton;  PuppiMet_pt=_PuppiMet_pt;
            PuppiMet_phi=_PuppiMet_phi;
            Lepton_pt=_Lepton_pt;
            Lepton_phi=_Lepton_phi; Lepton_eta=_Lepton_eta;
            CleanJet_pt=_CleanJet_pt; CleanJet_phi=_CleanJet_phi; CleanJet_eta=_CleanJet_eta;

            RVecF MoMEMta_kin_prxy_h;

            if (nLepton > 1 && nCleanJet >= 2)
            {
                TLorentzVector L1(0.,0.,0.,0.);
                TLorentzVector L2(0.,0.,0.,0.);
                TLorentzVector LL(0.,0.,0.,0.);
                TLorentzVector J1(0.,0.,0.,0.);
                TLorentzVector J2(0.,0.,0.,0.);
                TLorentzVector prxyHiggs(0.,0.,0.,0.);
                TLorentzVector NuNu(0.,0.,0.,0.);

                L1.SetPtEtaPhiM(Lepton_pt[0], Lepton_eta[0], Lepton_phi[0], 0.0);
                L2.SetPtEtaPhiM(Lepton_pt[1], Lepton_eta[1], Lepton_phi[1], 0.0);

                J1.SetPtEtaPhiM(CleanJet_pt[0], CleanJet_eta[0], CleanJet_phi[0], 0.0);
                J2.SetPtEtaPhiM(CleanJet_pt[1], CleanJet_eta[1], CleanJet_phi[1], 0.0);

                // Calculate the Higgs boson 4-momentum
                LL = L1 + L2;
                double nunu_px = PuppiMet_pt*cos(PuppiMet_phi);
                double nunu_py = PuppiMet_pt*sin(PuppiMet_phi);
                double nunu_pz = LL.Pz();
                double nunu_m = 30.0; // Assuming a 30 GeV invariant mass for the neutrinos

                double nunu_e = abs(sqrt(nunu_px*nunu_px + nunu_py*nunu_py + nunu_pz*nunu_pz + nunu_m*nunu_m));

                NuNu.SetPxPyPzE(nunu_px, nunu_py, nunu_pz, nunu_e);
                prxyHiggs = LL + NuNu;

                ParameterSet parameters_JJH;
                ParameterSet parameters_ggHeft;

                parameters_JJH.set("algorithm", "cuhre");
                parameters_ggHeft.set("algorithm", "cuhre");

                ConfigurationReader configuration_JJH("/afs/cern.ch/user/c/cgarcias/workspace/private/Run3/mkShapesRDF/momemta/JJH_ME/JJH_ME.lua", parameters_JJH);
                MoMEMta weight_JJH(configuration_JJH.freeze());

                ConfigurationReader configuration_ggHeft("/afs/cern.ch/user/c/cgarcias/workspace/private/Run3/mkShapesRDF/momemta/ggHeft_ME/ggHeft_ME.lua", parameters_ggHeft);
                MoMEMta weight_ggHeft(configuration_ggHeft.freeze());

                momemta::Particle higgs {"higgs", LorentzVector {prxyHiggs.Px(), prxyHiggs.Py(), prxyHiggs.Pz(), prxyHiggs.E()}, 25};
                momemta::Particle jet1 {"jet1", LorentzVector {J1.Px(), J1.Py(), J1.Pz(), J1.E()}, 2};
                momemta::Particle jet2 {"jet2", LorentzVector {J2.Px(), J2.Py(), J2.Pz(), J2.E()}, -2};

                // Normalize the 4-momenta of the particles
                normalizeInput(higgs.p4);
                normalizeInput(jet1.p4);
                normalizeInput(jet2.p4);

                std::vector<std::pair<double, double>> weights_JJH = weight_JJH.computeWeights({higgs, jet1, jet2});
                std::vector<std::pair<double, double>> weights_ggHeft = weight_ggHeft.computeWeights({higgs, jet1, jet2});

                double wghtjjh = (float)weights_JJH.at(0).first;
                double wghtggHeft = (float)weights_ggHeft.at(0).first;
                MoMEMta_kin_prxy_h.push_back(abs(wghtjjh) / (abs(wghtjjh) + 100 * abs(wghtggHeft)));
            }
            else
                MoMEMta_kin_prxy_h.push_back(-999);
            return MoMEMta_kin_prxy_h;
        }
};
