#!/bin/sh

cat <<EOF
========================================================================
This script is creating a working directory for ntuplizing and plotting
the ttH→ττ analysis in 80X

Output is in setup.log
========================================================================
EOF

(
   set -e
   set -o xtrace

   export SCRAM_ARCH=slc6_amd64_gcc530
   scramv1 project CMSSW CMSSW_8_0_21
   cd CMSSW_8_0_21/src
   set +o xtrace
   eval $(scramv1 runtime -sh)
   set -o xtrace
   git cms-init > /dev/null

   git cms-merge-topic cms-met:METRecipe_8020
   git cms-merge-topic ikrav:egm_id_80X_v2

   git clone -b CMSSW_8_0_24_v1_sync git@github.com:cms-ttH/MiniAOD.git
   git clone git@github.com:cms-ttH/ttH-LeptonID.git ttH/LeptonID
   git clone git@github.com:cms-ttH/ttH-TauRoast.git ttH/TauRoast

   git cms-addpkg PhysicsTools/JetMCAlgos/
   cd PhysicsTools/JetMCAlgos/plugins/
   rm GenHFHadronMatcher.cc
   wget https://twiki.cern.ch/twiki/pub/CMSPublic/GenHFHadronMatcher/GenHFHadronMatcher.cc
   wget https://twiki.cern.ch/twiki/pub/CMSPublic/GenHFHadronMatcher/GenTtbarCategorizer.cc
   cd -
   cd PhysicsTools/JetMCAlgos/python/
   wget https://twiki.cern.ch/twiki/pub/CMSPublic/GenHFHadronMatcher/GenTtbarCategorizer_cfi.py.txt
   mv GenTtbarCategorizer_cfi.py.txt GenTtbarCategorizer_cfi.py
   cd -

   scram b -j 8

   cd $CMSSW_BASE/external/$SCRAM_ARCH/
   git clone -b egm_id_80X_v1 https://github.com/ikrav/RecoEgamma-ElectronIdentification.git data/RecoEgamma/ElectronIdentification/data
) > setup.log


cat <<EOF
========================================================================
Output is in setup.log
========================================================================
EOF
