
import os
import copy
import inspect

# Get base Dir
def GetBaseDir(RefDir=''):
 ThisDir = os.path.realpath(os.getcwd())
 Directories = ThisDir.split(os.sep)
 if RefDir in Directories:
  BaseDir_idx = Directories.index(RefDir)
  BaseDir = os.sep.join(Directories[:BaseDir_idx]) + os.sep
  return BaseDir
 else:
  print ("ERROR: Base directory ("+RefDir+") not found")
  exit(0)

configurations = GetBaseDir('PlotsConfigurationsRun3')
print("Dir:" + configurations)

aliases = {}
aliases = OrderedDict()

mc = [skey for skey in samples if skey not in ('Fake', 'DATA')]

eleWP = 'mvaFall17V2Iso_WP90'
muWP  = 'cut_Tight80x'

aliases['LepWPCut'] = {
    'expr': 'LepCut2l__ele_mvaFall17V2Iso_WP90__mu_cut_Tight80x*\
    ( ((abs(Lepton_pdgId[0])==13 && Muon_mvaTTH[Lepton_muonIdx[0]]>0.82) || (abs(Lepton_pdgId[0])==11 && Lepton_mvaTTH_UL[0]>0.90))\
    && ((abs(Lepton_pdgId[1])==13 && Muon_mvaTTH[Lepton_muonIdx[1]]>0.82) || (abs(Lepton_pdgId[1])==11 && Lepton_mvaTTH_UL[1]>0.90)) )',
    'samples': mc + ['DATA','Fake']
}

aliases['LepWPSF'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc
}

# Fake leptons transfer factor
aliases['fakeW'] = {
    'linesToAdd' : ['#include "'+configurations+'/PlotsConfigurationsRun3/HWW_polarization/Extended/fake_rate_reader_class.cc"'],
    'linesToProcess':["ROOT.gInterpreter.Declare('fake_rate_reader fr_reader = fake_rate_reader(\"2016_HIPM\", \"90\", \"82\", 0.90, 0.82, \"nominal\", 2, \"std\");')"],
    'expr': 'fr_reader(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_cut_Tight80x, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'    : ['Fake']
}


# gen-matching to prompt only (GenLepMatch2l matches to *any* gen lepton)
aliases['PromptGenLepMatch2l'] = {
    'expr': 'Alt(Lepton_promptgenmatched,0,0)*Alt(Lepton_promptgenmatched,1,0)',
    'samples': mc
}


####################################################################################
# b tagging WPs: https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL18
####################################################################################

# DeepB = DeepCSV
bWP_loose_deepB  = '0.2027'
bWP_medium_deepB = '0.6001'
bWP_tight_deepB  = '0.8819'

# DeepFlavB = DeepJet
bWP_loose_deepFlavB  = '0.0508'
bWP_medium_deepFlavB = '0.2598'
bWP_tight_deepFlavB  = '0.6502'

# Actual algo and WP definition. BE CONSISTENT!!
bAlgo = 'DeepFlavB' # ['DeepB','DeepFlavB']
bWP   = bWP_loose_deepFlavB
bSF   = 'deepjet' # ['deepcsv','deepjet']  ## deepflav is new b-tag SF


# b veto
aliases['bVeto'] = {
    'expr': 'Sum(CleanJet_pt > 19. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{}, CleanJet_jetIdx) > {}) == 0'.format(bAlgo, bWP)
}


aliases['SFweight'] = {
    'expr': ' 1 ',
    'samples': mc
}

###########################################
##      AC/EFT Analysis specific         ##
###########################################

## VBF AC sample normalisation from scripts/ACSampleNorms.py

aliases['VBF_H0PM_N']     = { 'expr': ' 1'                     }
aliases['VBF_H0PH_N']     = { 'expr': ' 10.51137843428809 '    }
aliases['VBF_H0M_N']      = { 'expr': ' 3.6372762023765777 '   }
aliases['VBF_H0L1_N']     = { 'expr': ' 1.135094754638813e-15 '}
aliases['VBF_H0L1Zg_N']   = { 'expr': ' 5.460125187867415e-08 '}
aliases['VBF_H0PHf05_N']  = { 'expr': ' 3.331308468063125 '    }
aliases['VBF_H0Mf05_N']   = { 'expr': ' 2.0559478898477845 '   }
aliases['VBF_H0L1f05_N']  = { 'expr': ' 2.1078248105823407 '   }
aliases['VBF_H0L1Zgf05_N']= { 'expr': ' 1.6251558253108431 '   }

## gen ME weight for each signal reweighting

aliases['MELALib'] = {
  'linesToAdd':['#include "'+configurations+'/mkShapesRDF/JHUGenMELA/MELA/interface/Mela.h"'],
  'linesToProcess':['ROOT.gSystem.Load("'+configurations+'/mkShapesRDF/JHUGenMELA/MELA/data/slc7_amd64_gcc920/libmcfm_707.so","", ROOT.kTRUE)',
                    'ROOT.gSystem.Load("'+configurations+'/mkShapesRDF/JHUGenMELA/MELA/data/slc7_amd64_gcc920/libJHUGenMELAMELA.so","", ROOT.kTRUE)']
}

aliases['MELA_vbf'] = {
   'linesToAdd':['.L '+configurations+'/PlotsConfigurationsRun3/HWW_CouplingStudy/macros/JJZJJH_MELA.cc+g'],
   'linesToProcess':['ROOT.gInterpreter.Declare("RECOME_JJZJJH_MELA mVBF;")'],
   'expr' :   'mVBF(nCleanJet, nLepton, PuppiMET_pt, PuppiMET_phi, Lepton_pt, Lepton_phi, Lepton_eta, CleanJet_pt, CleanJet_phi, CleanJet_eta)',
   'afterNuis': True
}

aliases['m_higgs']   = { 'expr': 'MELA_vbf[0]', 'afterNuis': True }
aliases['D_ZDYvsHVBF_MELA'] = { 'expr': 'MELA_vbf[1]', 'afterNuis': True }