import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

options = VarParsing.VarParsing('analysis')
options.parseArguments()

process = cms.Process("Taus")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 2000

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32( options.maxEvents ) )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = 'MCRUN2_74_V9::All'
process.prefer("GlobalTag")

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring([
            '/store/mc/RunIISpring15DR74/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/00D1004A-3B03-E511-8FE3-0025905A60B4.root',
            '/store/mc/RunIISpring15DR74/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/0A89FECB-2103-E511-900C-002590596498.root',
            '/store/mc/RunIISpring15DR74/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/0C61D8B5-0B03-E511-81B7-002590574776.root',
            '/store/mc/RunIISpring15DR74/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/145BE463-3B03-E511-A7D9-008CFA111314.root',
            '/store/mc/RunIISpring15DR74/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/14F3F854-0703-E511-8CF7-002590200908.root',
            '/store/mc/RunIISpring15DR74/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/3E1E6618-1D03-E511-AB80-0025905A608A.root',
            '/store/mc/RunIISpring15DR74/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/549DD972-2D03-E511-B843-0025905A48C0.root',
            '/store/mc/RunIISpring15DR74/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/648C0BFD-0D03-E511-A2E2-0025905B8598.root',
            '/store/mc/RunIISpring15DR74/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/8C0C8303-1A03-E511-8BE9-0025905A60A8.root',
            '/store/mc/RunIISpring15DR74/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/8EE3EB01-2003-E511-9EDD-0025905A613C.root',
            '/store/mc/RunIISpring15DR74/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/96039B4D-2503-E511-A57F-0025905B85AE.root',
            '/store/mc/RunIISpring15DR74/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/9E83B57D-FD02-E511-B17D-001E67397C33.root',
            '/store/mc/RunIISpring15DR74/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/A6F6DE52-0103-E511-B9FE-001E673971C5.root',
            '/store/mc/RunIISpring15DR74/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/C0AD48FB-1D03-E511-A028-0025905B85A2.root',
            '/store/mc/RunIISpring15DR74/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/CEF62DB0-3B03-E511-90EE-0025B3E063BA.root',
            '/store/mc/RunIISpring15DR74/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/DADC2BD4-0403-E511-BD9E-002590200B3C.root',
            '/store/mc/RunIISpring15DR74/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/E816F01A-0C03-E511-915B-002590200948.root',
            '/store/mc/RunIISpring15DR74/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/E8A54186-1503-E511-9CB8-0025905B860C.root',
            '/store/mc/RunIISpring15DR74/ttHJetToTT_M125_13TeV_amcatnloFXFX_madspin_pythia8/MINIAODSIM/Asympt25ns_MCRUN2_74_V9-v1/00000/FCF18EA0-1603-E511-8B2B-002481E14E14.root'
        ])
)

process.TFileService = cms.Service("TFileService",
        closeFileFast = cms.untracked.bool(True),
        fileName = cms.string("test.root")
)

process.taus = cms.EDAnalyzer("TauProcessor",
        minJets = cms.uint32(2),
        minTags = cms.uint32(1),
        maxTags = cms.int32(-1),
        minLeptons = cms.uint32(1),
        minTightLeptons = cms.uint32(1),
        maxLeptons = cms.int32(2),
        maxTightLeptons = cms.int32(1),
        minTaus = cms.uint32(0),
        minTightTaus = cms.uint32(0),
        ssLeptons = cms.bool(True)
)

process.p = cms.Path(process.taus)