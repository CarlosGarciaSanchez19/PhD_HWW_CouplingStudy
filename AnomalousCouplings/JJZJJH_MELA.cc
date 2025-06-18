/* Including MELA's libraries */
#include "/afs/cern.ch/work/c/cgarcias/private/Run3/mkShapesRDF/JHUGenMELA/MELA/interface/Mela.h"
#include "/afs/cern.ch/work/c/cgarcias/private/Run3/mkShapesRDF/JHUGenMELA/MELA/interface/TUtil.hh"
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

class RECOME_JJZJJH_MELA {
    public:
        float nCleanJet,  nLepton;
        float PuppiMet_pt,  PuppiMet_phi;
        RVecF Lepton_pt,  Lepton_phi,  Lepton_eta, Lepton_pdgId, CleanJet_pt,  CleanJet_phi,  CleanJet_eta;

        Mela* mela;
        Double_t LHCsqrts_= 13., mh_= 125., mz_=91.;
        TVar::VerbosityLevel verbosity_ = TVar::SILENT;
        TVar::MatrixElement me_ = TVar::JHUGen;

        RECOME_JJZJJH_MELA()
        {
            mela = new Mela(LHCsqrts_, mh_, verbosity_);
        }
        
        /* void normalizeInput(LorentzVector& p4) {
            if (p4.M() > 0)
                return; // Increase the energy until M is positive                                                                                                                                 
            p4.SetE(p4.P());
            while (p4.M2() < 0) {
                double delta = p4.E() * 1e-5;
                p4.SetE(p4.E() + delta);
            };
        } */

        RVecF operator()(float _nCleanJet,
            float _nLepton, float _PuppiMet_pt, float _PuppiMet_phi,
            RVecF _Lepton_pt, RVecF _Lepton_phi, RVecF _Lepton_eta, RVecF _Lepton_pdgId,
            RVecF _CleanJet_pt, RVecF _CleanJet_phi, RVecF _CleanJet_eta) {

            nCleanJet=_nCleanJet;  nLepton=_nLepton;  PuppiMet_pt=_PuppiMet_pt;
            PuppiMet_phi=_PuppiMet_phi;
            Lepton_pt=_Lepton_pt;
            Lepton_phi=_Lepton_phi; Lepton_eta=_Lepton_eta; Lepton_pdgId=_Lepton_pdgId;
            CleanJet_pt=_CleanJet_pt; CleanJet_phi=_CleanJet_phi; CleanJet_eta=_CleanJet_eta;

            RVecF MELA_kin_prxy_h;

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

                float h_mass = prxyHiggs.M();
                MELA_kin_prxy_h.push_back(h_mass);

                SimpleParticleCollection_t daughter;
                SimpleParticleCollection_t associated;
                SimpleParticleCollection_t mother;

                /* Compute mela for H + 2jets */
                daughter.push_back(SimpleParticle_t(25, prxyHiggs));
                associated.push_back(SimpleParticle_t(1, J1));
                associated.push_back(SimpleParticle_t(-1, J2));
                mela->setCandidateDecayMode(TVar::CandidateDecay_Stable);
                mela->setInputEvent(&daughter, &associated, 0, 0);
                mela->setCurrentCandidateFromIndex(0);
                float me_hsm = -999;
                mela->setProcess(TVar::HSMHiggs, TVar::JHUGen, TVar::JJVBF);
                mela->computeProdP(me_hsm, true);
                mela->resetInputEvent();
            
                /* Compute mela for Z + 2jets */
                daughter.clear();
                daughter.push_back(SimpleParticle_t(Lepton_pdgId[0], L1));
                daughter.push_back(SimpleParticle_t(Lepton_pdgId[1], L2));
                associated.clear();
                associated.push_back(SimpleParticle_t(1, J1));
                associated.push_back(SimpleParticle_t(-1, J2));
                mela->setInputEvent(&daughter, &associated, 0, 0);
                mela->setCurrentCandidateFromIndex(0);
                float me_zsm = -999;
                mela->setProcess(TVar::bkgZJets, TVar::MCFM, TVar::JJQCD);
                mela->computeProdP(me_zsm, true);
                mela->resetInputEvent();

                float c = 1.0;
                MELA_kin_prxy_h.push_back(1 / (1 + abs(me_zsm) / abs(me_hsm) * c));
            }
            else
                MELA_kin_prxy_h.push_back(-999);
            return MELA_kin_prxy_h;
        }
};