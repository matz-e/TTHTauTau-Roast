import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing('analysis')
options.inputFiles = '/store/mc/RunIISpring15MiniAODv2/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/50000/1278547D-C26D-E511-874F-842B2B185AAA.root'
options.register("data", False,
        VarParsing.VarParsing.multiplicity.singleton,
        VarParsing.VarParsing.varType.bool,
        "Indicate if data is being used (or MC)")
options.parseArguments()

process = cms.Process("Taus")

process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 2000

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32( options.maxEvents ) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.GlobalTag.globaltag = ("74X_dataRun2_v4" if options.data else "74X_mcRun2_asymptotic_v2")

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(options.inputFiles)
)

process.TFileService = cms.Service("TFileService",
        closeFileFast = cms.untracked.bool(True),
        fileName = cms.string("test.root")
)

from JetMETCorrections.Configuration.JetCorrectionServices_cff import *

process.ak4PFCHSL1Fastjet = cms.ESProducer(
        'L1FastjetCorrectionESProducer',
        level       = cms.string('L1FastJet'),
        algorithm   = cms.string('AK4PFchs'),
        srcRho      = cms.InputTag('fixedGridRhoFastjetAll')
)
process.ak4PFchsL2Relative = ak4CaloL2Relative.clone(algorithm = 'AK4PFchs')
process.ak4PFchsL3Absolute = ak4CaloL3Absolute.clone(algorithm = 'AK4PFchs')
process.ak4PFchsL1L2L3 = cms.ESProducer("JetCorrectionESChain",
        correctors = cms.vstring(
            'ak4PFCHSL1Fastjet',
            'ak4PFchsL2Relative',
            'ak4PFchsL3Absolute')
)

# process.load("ttH.LeptonID.ttHLeptons_cfi")

process.taus = cms.EDAnalyzer("TauProcessor",
        data = cms.bool(options.data),
        # electrons = cms.InputTag("ttHLeptons"),
        # muons = cms.InputTag("ttHLeptons"),
        electrons = cms.InputTag("slimmedElectrons"),
        muons = cms.InputTag("slimmedMuons"),
        minJets = cms.uint32(2),
        minTags = cms.uint32(1),
        maxTags = cms.int32(2),
        minPreselectedLeptons = cms.uint32(1),
        minLooseLeptons = cms.uint32(1),
        minTightLeptons = cms.uint32(1),
        maxLooseLeptons = cms.int32(1),
        maxTightLeptons = cms.int32(1),
        minTaus = cms.uint32(2),
        minTightTaus = cms.uint32(0),
        subtractLeptons = cms.bool(False),
        minLooseLeptonPt = cms.double(10.),
        minTightLeptonPt = cms.double(30.),
        maxLooseLeptonEta = cms.double(2.4),
        maxTightLeptonEta = cms.double(2.1),
        minJetPt = cms.double(30.),
        minTagPt = cms.double(30.),
        maxJetEta = cms.double(2.4),
        filterPUJets = cms.bool(False),
        printPreselection = cms.bool(False),
        triggerSelection = cms.string("HLT_Ele27_eta2p1_WPLoose_Gsf_v2 OR HLT_IsoMu27_v3")
)

# process.p = cms.Path(process.ttHLeptons * process.taus)
process.p = cms.Path(process.taus)
