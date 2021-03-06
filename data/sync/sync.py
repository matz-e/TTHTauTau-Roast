from ttH.TauRoast.botany import Leaf
from ttH.TauRoast.plotting import Plot
from ttH.TauRoast.processing import BasicProcess

BasicProcess(
    name="syncTree",
    paths=['ttH'],
    cross_section=45140,
    events=45611
)

BasicProcess(
    name="syncTree_1l2tau_SR",
    paths=['ttH_skim'],
    cross_section=45140,
    events=45611,
    cutflow='signal'
)

BasicProcess(
    name="syncTree_1l2tau_Fake",
    paths=['ttH_skim'],
    cross_section=45140,
    events=45611,
    cutflow='fake'
)

BasicProcess(
    name="ttH_mva",
    paths=['ttH'],
    cross_section=45140,
    events=45140,
    cutflow="mva"
)

BasicProcess(
    name="ttH_signal",
    paths=['ttH'],
    cross_section=45140,
    events=45140,
    cutflow="signal"
)

BasicProcess(
    name="ttH_os",
    paths=['ttH'],
    cross_section=45140,
    events=45140,
    cutflow="os"
)


BasicProcess(
    name="ttjets",
    paths=['ttjets'],
    cross_section=45140,
    events=41812
)

Leaf('FR_weight', 'f', 'result = weights["fake"]')
Leaf('PU_weight', 'f', 'result = weights["puweight"]')
Leaf('MC_weight', 'f', 'result = weights["generator"]')
Leaf('bTagSF_weight', 'f', 'result = weights["csvweight"]')
Leaf('leptonSF_weight', 'f', 'result = weights["leptonsf"]')
Leaf('triggerSF_weight', 'f', 'result = weights["triggersf"]')
Leaf('tauSF_weight', 'f', 'result = weights["tauideff"]')

Leaf('events', 'f', 'result = .5')
Plot(
    name="general/Events",
    values=["events"],
    labels=["", "Events"],
    binning=[1, 0, 1]
)

Leaf('ntv', 'f', 'result = event.ntv()')

Leaf('nelectrons', 'f', 'result = leptons.size() > 1 ? leptons[0].electron() + leptons[1].electron() : 0')
Leaf('nmuons', 'f', 'result = leptons.size() > 1 ? leptons[0].muon() + leptons[1].muon() : 0')
Leaf('ntaus', 'i', 'result = std::count_if(std::begin(taus), std::end(taus), [](const superslim::Tau& t) { return t.isolationMVA03() >= superslim::id::Medium; })')

Leaf('njets_inclusive', 'f', 'result = jets.size()')
Leaf('ntags_loose', 'f', 'result = btags(jets, true)')
Leaf('ht', 'f', """
float ht = 0.;
for (const auto& j: jets)
    ht += j.p4().Pt();
for (const auto& t: all_taus)
    ht += t.p4().Pt();
for (const auto& l: leptons)
    ht += l.p4().Pt();
result = ht
""")
Leaf('HT', 'f', """
float HT = 0.;
for (const auto& j: jets)
    HT += j.p4().Pt();
for (const auto& t: all_taus)
    HT += t.p4().Pt();
for (const auto& l: leptons)
    HT += l.p4().Pt();
result = HT
""")
Leaf('avg_dr_jet', 'f',
     '''std::vector<float> drs;
        for (auto i = 0; i < jets.size(); ++i)
            for (auto j = i + 1; j < jets.size(); ++j)
                drs.push_back(dR(jets[i], jets[j]));
        result = std::accumulate(drs.begin(), drs.end(), 0.) / drs.size()''')
Leaf('jet_deltaRavg', 'f',
     '''std::vector<float> drs;
        for (auto i = 0; i < jets.size(); ++i)
            for (auto j = i + 1; j < jets.size(); ++j)
                drs.push_back(dR(jets[i], jets[j]));
        result = std::accumulate(drs.begin(), drs.end(), 0.) / drs.size()''')
Leaf('jet_deltaRmax', 'f',
     '''std::vector<float> drs;
        for (auto i = 0; i < jets.size(); ++i)
            for (auto j = i + 1; j < jets.size(); ++j)
                drs.push_back(dR(jets[i], jets[j]));
        result = drs.size() > 0 ? *std::max_element(drs.begin(), drs.end()) : -666.''')
Leaf('tt_deltaR', 'f', 'result = taus.size() >= 2 ? dR(taus.at(0), taus.at(1)) : -9999.')
Leaf('tt_mvis', 'f', 'result = taus.size() >= 2 ? (taus.at(0).p4() + taus.at(1).p4()).M() : -9999.')
Leaf('tt_visiblemass', 'f', 'result = taus.size() >= 2 ? (taus.at(0).p4() + taus.at(1).p4()).M() : -9999.')
Leaf('tt_sumpt', 'f', 'result = taus.size() >= 2 ? (taus[0].p4() + taus[1].p4()).Pt() : -9999.')

Leaf('nEvent', 'i', 'result = event.event()')
Leaf('ls', 'i', 'result = event.lumi()')
Leaf('run', 'i', 'result = event.run()')
Leaf(
    'n_fakeablesel_ele', 'i', """
    result = std::count_if(
        std::begin(all_leptons),
        std::end(all_leptons),
        [](const superslim::Lepton& l) -> bool { return l.electron() and l.loose(superslim::Lepton::Fakeable); }
    )"""
)
Leaf(
    'n_fakeablesel_mu', 'i', """
    result = std::count_if(
        std::begin(all_leptons),
        std::end(all_leptons),
        [](const superslim::Lepton& l) -> bool { return l.muon() and l.loose(superslim::Lepton::Fakeable); }
    )"""
)
Leaf('n_presel_ele', 'i', """
    result = std::count_if(
        std::begin(all_leptons),
        std::end(all_leptons),
        [](const superslim::Lepton& l) -> bool { return l.electron(); }
    )
""")
Leaf('n_presel_mu', 'i', """
    result = std::count_if(
        std::begin(all_leptons),
        std::end(all_leptons),
        [](const superslim::Lepton& l) -> bool { return l.muon(); }
    )
""")
Leaf('n_mvasel_ele', 'i', """
    result = std::count_if(
        std::begin(electrons),
        std::end(electrons),
        [](const superslim::Lepton& l) -> bool { return l.mva() >= superslim::id::Loose; }
    )
""")
Leaf('n_mvasel_mu', 'i', """
    result = std::count_if(
        std::begin(muons),
        std::end(muons),
        [](const superslim::Lepton& l) -> bool { return l.mva() >= superslim::id::Loose; }
    )
""")
Leaf('n_presel_tau', 'i', 'result = len(all_taus)')
Leaf('n_presel_jet', 'i', 'result = len(jets)')
Leaf('PFMET', 'f', 'result = met.pt()')
Leaf('PFMETphi', 'f', 'result = met.phi()')

for i in range(2):
    Leaf('mu{}_pdgID'.format(i), 'f',
         'result = len(muons) <= {0} ? -9999 : muons[{0}].pdgId()'.format(i))
    Leaf('mu{}_pt'.format(i), 'f',
         'result = len(muons) <= {0} ? -9999 : muons[{0}].p4().pt()'.format(i))
    Leaf('mu{}_eta'.format(i), 'f',
         'result = len(muons) <= {0} ? -9999 : muons[{0}].p4().eta()'.format(i))
    Leaf('mu{}_phi'.format(i), 'f',
         'result = len(muons) <= {0} ? -9999 : muons[{0}].p4().phi()'.format(i))
    Leaf('mu{}_E'.format(i), 'f',
         'result = len(muons) <= {0} ? -9999 : muons[{0}].p4().E()'.format(i))
    Leaf('mu{}_charge'.format(i), 'f',
         'result = len(muons) <= {0} ? -9999 : muons[{0}].charge()'.format(i))
    Leaf('mu{}_dxy'.format(i), 'f',
         'result = len(muons) <= {0} ? -9999 : muons[{0}].dxy()'.format(i))
    Leaf('mu{}_dz'.format(i), 'f', 'result = len(muons) <= {0} ? -9999 : muons[{0}].dz()'.format(i))

    Leaf('mu{}_miniRelIso'.format(i), 'f',
         'result = len(muons) <= {0} ? -9999 : muons[{0}].relativeIsolation()'.format(i))
    Leaf('mu{}_miniIsoCharged'.format(i), 'f',
         'result = len(muons) <= {0} ? -9999 : muons[{0}].chargedIsolation()'.format(i))
    Leaf('mu{}_miniIsoNeutral'.format(i), 'f',
         'result = len(muons) <= {0} ? -9999 : muons[{0}].neutralIsolation()'.format(i))

    Leaf('mu{}_jetNDauChargedMVASel'.format(i), 'i',
         'result = len(muons) <= {0} ? -9999 : muons[{0}].nearestJetConstituents()'.format(i))
    Leaf('mu{}_jetPtRel'.format(i), 'f',
         'result = len(muons) <= {0} ? -9999. : muons[{0}].nearestJetRelativePt()'.format(i))
    Leaf('mu{}_jetPtRatio'.format(i), 'f',
         'result = len(muons) <= {0} ? -9999. : muons[{0}].nearestJetRatioPt()'.format(i))
    Leaf('mu{}_jetCSV'.format(i), 'f',
         'result = len(muons) <= {0} ? -9999 : muons[{0}].nearestJetCSV()'.format(i))

    Leaf('mu{}_sip3D'.format(i), 'f',
         'result = len(muons) <= {0} ? -9999 : muons[{0}].sip3D()'.format(i))
    Leaf('mu{}_leptonMVA'.format(i), 'f',
         'result = len(muons) <= {0} ? -9999 : muons[{0}].mvaRaw()'.format(i))
    Leaf('mu{}_segmentCompatibility'.format(i), 'f',
         'result = len(muons) <= {0} ? -9999 : muons[{0}].segmentCompatibility()'.format(i))

    # Leaf('mu{}_ismvasel'.format(i), 'i',
    #      'result = len(muons) <= {0} ? 0 : muons[{0}].mva() >= superslim::id::Loose'.format(i))

for i in range(2):
    Leaf('ele{}_pdgID'.format(i), 'f',
         'result = len(electrons) <= {0} ? -9999 : electrons[{0}].pdgId()'.format(i))
    Leaf('ele{}_pt'.format(i), 'f',
         'result = len(electrons) <= {0} ? -9999 : electrons[{0}].p4().pt()'.format(i))
    Leaf('ele{}_eta'.format(i), 'f',
         'result = len(electrons) <= {0} ? -9999 : electrons[{0}].p4().eta()'.format(i))
    Leaf('ele{}_phi'.format(i), 'f',
         'result = len(electrons) <= {0} ? -9999 : electrons[{0}].p4().phi()'.format(i))
    Leaf('ele{}_E'.format(i), 'f',
         'result = len(electrons) <= {0} ? -9999 : electrons[{0}].p4().E()'.format(i))
    Leaf('ele{}_charge'.format(i), 'f',
         'result = len(electrons) <= {0} ? -9999 : electrons[{0}].charge()'.format(i))
    Leaf('ele{}_dxy'.format(i), 'f',
         'result = len(electrons) <= {0} ? -9999 : electrons[{0}].dxy()'.format(i))
    Leaf('ele{}_dz'.format(i), 'f',
         'result = len(electrons) <= {0} ? -9999 : electrons[{0}].dz()'.format(i))

    Leaf('ele{}_miniRelIso'.format(i), 'f',
         'result = len(electrons) <= {0} ? -9999 : electrons[{0}].relativeIsolation()'.format(i))
    Leaf('ele{}_miniIsoCharged'.format(i), 'f',
         'result = len(electrons) <= {0} ? -9999 : electrons[{0}].chargedIsolation()'.format(i))
    Leaf('ele{}_miniIsoNeutral'.format(i), 'f',
         'result = len(electrons) <= {0} ? -9999 : electrons[{0}].neutralIsolation()'.format(i))

    Leaf('ele{}_jetNDauChargedMVASel'.format(i), 'i',
         'result = len(electrons) <= {0} ? -9999 : electrons[{0}].nearestJetConstituents()'.format(i))
    Leaf('ele{}_jetPtRel'.format(i), 'f',
         'result = len(electrons) <= {0} ? -9999 : electrons[{0}].nearestJetRelativePt()'.format(i))
    Leaf('ele{}_jetPtRatio'.format(i), 'f',
         'result = len(electrons) <= {0} ? -9999 : electrons[{0}].nearestJetRatioPt()'.format(i))
    Leaf('ele{}_jetCSV'.format(i), 'f',
         'result = len(electrons) <= {0} ? -9999 : electrons[{0}].nearestJetCSV()'.format(i))

    Leaf('ele{}_sip3D'.format(i), 'f',
         'result = len(electrons) <= {0} ? -9999 : electrons[{0}].sip3D()'.format(i))
    Leaf('ele{}_leptonMVA'.format(i), 'f',
         'result = len(electrons) <= {0} ? -9999 : electrons[{0}].mvaRaw()'.format(i))
    Leaf('ele{}_eleMVA'.format(i), 'f',
         'result = len(electrons) <= {0} ? -9999 : electrons[{0}].nonTriggeringId()'.format(i))

    # Leaf('ele{}_ismvasel'.format(i), 'i',
    #      'result = len(electrons) <= {0} ? 0 : electrons[{0}].mva() >= superslim::id::Loose'.format(i))

for i in range(2):
    Leaf('tau{}_pt'.format(i), 'f',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].p4().pt()'.format(i))
    Leaf('tau{}_eta'.format(i), 'f',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].p4().eta()'.format(i))
    Leaf('tau{}_phi'.format(i), 'f',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].p4().phi()'.format(i))
    Leaf('tau{}_E'.format(i), 'f',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].p4().E()'.format(i))
    Leaf('tau{}_charge'.format(i), 'f',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].charge()'.format(i))
    Leaf('tau{}_dxy'.format(i), 'f',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].dxy()'.format(i))
    Leaf('tau{}_dz'.format(i), 'f',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].dz()'.format(i))

    Leaf('tau{}_decayModeFinding'.format(i), 'f',
         'result = len(taus) <= {0} ? -9999 : 1'.format(i))

    Leaf('tau{}_byLooseCombinedIsolationDeltaBetaCorr3Hits'.format(i), 'i',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].isolation3Hits05() >= superslim::id::Loose'.format(i))
    Leaf('tau{}_byMediumCombinedIsolationDeltaBetaCorr3Hits'.format(i), 'i',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].isolation3Hits05() >= superslim::id::Medium'.format(i))
    Leaf('tau{}_byTightCombinedIsolationDeltaBetaCorr3Hits'.format(i), 'i',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].isolation3Hits05() >= superslim::id::Tight'.format(i))
    Leaf('tau{}_byLooseCombinedIsolationDeltaBetaCorr3HitsdR03'.format(i), 'i',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].isolation3Hits03() >= superslim::id::Loose'.format(i))
    Leaf('tau{}_byMediumCombinedIsolationDeltaBetaCorr3HitsdR03'.format(i), 'i',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].isolation3Hits03() >= superslim::id::Medium'.format(i))
    Leaf('tau{}_byTightCombinedIsolationDeltaBetaCorr3HitsdR03'.format(i), 'i',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].isolation3Hits03() >= superslim::id::Tight'.format(i))
    Leaf('tau{}_byLooseIsolationMVArun2v1DBdR03oldDMwLT'.format(i), 'i',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].isolationMVA03() >= superslim::id::Loose'.format(i))
    Leaf('tau{}_byMediumIsolationMVArun2v1DBdR03oldDMwLT'.format(i), 'i',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].isolationMVA03() >= superslim::id::Medium'.format(i))
    Leaf('tau{}_byTightIsolationMVArun2v1DBdR03oldDMwLT'.format(i), 'i',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].isolationMVA03() >= superslim::id::Tight'.format(i))
    # Leaf('tau{}_byVTightIsolationMVArun2v1DBdR03oldDMwLT'.format(i), 'i',
    #      'result = len(taus) <= {0} ? -9999 : taus[{0}].isolationMVA03() >= superslim::id::VTight'.format(i))

    Leaf('tau{}_againstMuonLoose3'.format(i), 'i',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].vetoMuon() >= superslim::id::Loose'.format(i))
    Leaf('tau{}_againstMuonMedium3'.format(i), 'i',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].vetoMuon() >= superslim::id::Medium'.format(i))
    Leaf('tau{}_againstMuonTight3'.format(i), 'i',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].vetoMuon() >= superslim::id::Tight'.format(i))
    Leaf('tau{}_againstElectronVLooseMVA6'.format(i), 'i',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].vetoElectron() >= superslim::id::VLoose'.format(i))
    Leaf('tau{}_againstElectronLooseMVA6'.format(i), 'i',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].vetoElectron() >= superslim::id::Loose'.format(i))
    Leaf('tau{}_againstElectronMediumMVA6'.format(i), 'i',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].vetoElectron() >= superslim::id::Medium'.format(i))
    Leaf('tau{}_againstElectronTightMVA6'.format(i), 'i',
         'result = len(taus) <= {0} ? -9999 : taus[{0}].vetoElectron() >= superslim::id::Tight'.format(i))

for i in range(4):
    Leaf('jet{}_pt'.format(i), 'f',
         'result = len(jets) <= {0} ? -9999 : jets[{0}].p4().pt()'.format(i))
    Leaf('jet{}_eta'.format(i), 'f',
         'result = len(jets) <= {0} ? -9999 : jets[{0}].p4().eta()'.format(i))
    Leaf('jet{}_phi'.format(i), 'f',
         'result = len(jets) <= {0} ? -9999 : jets[{0}].p4().phi()'.format(i))
    Leaf('jet{}_E'.format(i), 'f',
         'result = len(jets) <= {0} ? -9999 : jets[{0}].p4().E()'.format(i))
    Leaf('jet{}_CSV'.format(i), 'f',
         'result = len(jets) <= {0} ? -9999 : jets[{0}].csv()'.format(i))
