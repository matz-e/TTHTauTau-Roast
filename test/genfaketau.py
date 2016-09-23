#!/usr/bin/env python

import matplotlib.pyplot as plt
# import pandas as pd
from root_pandas import read_root

numbers_in = ['nloosetaus', 'ntighttaus', 'nfaketaus', 'nfaketighttaus', 'nrealtaus', 'nrealtighttaus']
numbers = read_root("test/genfaketau/out/ntuple.root", "ttjets", columns=numbers_in)

fig = plt.figure()
numbers.plot.hist(
    stacked=False,
    subplots=True,
    layout=(3, 2),
    sharey=True,
    ylim=(.5, 1e5),
    logy=True,
    figsize=(8.5, 11),
    grid=True
)
for ax in fig.get_axes():
    ax.set_yscale('log', nonposy='clip')
plt.savefig('jetfakes_numbers.png')

taus_in = 'pt eta isoMVA03 genjet_pt genjet_eta genjetcharged_pt genjetcharged_eta match genjet_constituents genjetcharged_constituents'
taus_in = ['tau_' + v for v in taus_in.split()]
taus = read_root("test/genfaketau/out/ntuple.root", "ttjets", columns=taus_in, flatten=True)

gen_in = 'chargedconstituents constituents chargedpt pt eta'
gen_in = ['genjet_' + v for v in gen_in.split()]
jets = read_root("test/genfaketau/out/ntuple.root", "ttjets", columns=gen_in, flatten=True)

fakes = taus[(taus.tau_match == 6)]
selection = taus[(taus.tau_match == 6) & (taus.tau_isoMVA03 >= 5) & (taus.tau_pt >= 20.)]

labels = ['genjets', u'genjet fakes']
nbins = range(0, 201, 10)

fig = plt.figure()
n, bins, patches = plt.hist([jets.genjet_pt, selection.tau_genjet_pt], bins=nbins, normed=1)
plt.legend(patches, labels)
plt.savefig('jetfakes_genjet_pt.png')

fig = plt.figure()
n, bins, patches = plt.hist([jets.genjet_chargedpt, selection.tau_genjetcharged_pt], bins=nbins, normed=1)
plt.legend(patches, labels)
plt.savefig('jetfakes_genjet_chargedpt.png')

nbins = range(0, 31, 1)

fig = plt.figure()
n, bins, patches = plt.hist([jets.genjet_constituents, selection.tau_genjet_constituents], bins=nbins, normed=1)
plt.legend(patches, labels)
plt.savefig('jetfakes_genjet_constituents.png')

fig = plt.figure()
n, bins, patches = plt.hist([jets.genjet_chargedconstituents, selection.tau_genjetcharged_constituents], bins=nbins, normed=1)
plt.legend(patches, labels)
plt.savefig('jetfakes_genjet_chargedconstituents.png')

nbins = [range(0, 100, 5), range(0, 20, 1)]

fig = plt.figure()
plt.hist2d(jets.genjet_chargedpt, jets.genjet_chargedconstituents, bins=nbins)
plt.xlabel('genjet charged pt')
plt.ylabel('genjet charged constituents')
plt.savefig('genjet_chargedpt_vs_chargedconstituents.png')

fig = plt.figure()
plt.hist2d(selection.tau_genjetcharged_pt, selection.tau_genjetcharged_constituents, bins=nbins)
plt.xlabel('fake tau charged pt')
plt.ylabel('fake tau charged constituents')
plt.savefig('faketau_chargedpt_vs_chargedconstituents.png')

fig = plt.figure()
plt.hist2d(jets.genjet_pt, jets.genjet_constituents, bins=nbins)
plt.xlabel('genjet pt')
plt.ylabel('genjet constituents')
plt.savefig('genjet_pt_vs_constituents.png')

fig = plt.figure()
plt.hist2d(selection.tau_genjet_pt, selection.tau_genjet_constituents, bins=nbins)
plt.xlabel('fake tau pt')
plt.ylabel('fake tau constituents')
plt.savefig('faketau_pt_vs_constituents.png')
