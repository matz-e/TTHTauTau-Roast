#  vim: set fileencoding=utf-8 :
import codecs
import logging
import os
import pickle
import yaml

import numpy as np
import pandas as pd

from array import array
from root_numpy.tmva import evaluate_reader

from sklearn import cross_validation
from sklearn.cross_validation import ShuffleSplit
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import AdaBoostClassifier
from sklearn.feature_selection import RFECV
from sklearn.learning_curve import learning_curve
from sklearn.metrics import roc_auc_score
from sklearn import grid_search

import ROOT as r

from root_numpy import array2tree, root2array, rec2array, tree2array

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

r.gROOT.SetBatch()

matplotlib.style.use('ggplot')

CV = 5
NJOBS = 48


def load(config, name):
    datadir = os.path.join(os.environ["LOCALRT"], 'src', 'ttH', 'TauRoast', 'data')
    with open(os.path.join(datadir, 'mva_{}.yaml'.format(name))) as f:
        setup = yaml.load(f)
    return setup


def read_inputs(config, setup):
    from ttH.TauRoast.processing import Process

    fn = os.path.join(config.get("indir", config["outdir"]), "ntuple.root")

    signal = None
    signal_weights = None
    for proc, weight in sum([cfg.items() for cfg in setup['signals']], []):
        for p in sum([Process.expand(proc)], []):
            logging.debug('reading {}'.format(p))
            d = rec2array(root2array(fn, str(p), setup['variables']))
            if isinstance(weight, float) or isinstance(weight, int):
                w = np.array([weight] * len(d))
            else:
                w = rec2array(root2array(fn, str(p), [weight])).ravel()
            w *= p.cross_section / p.events
            if signal is not None:
                signal = np.concatenate((signal, d))
                signal_weights = np.concatenate((signal_weights, w))
            else:
                signal = d
                signal_weights = w

    background = None
    background_weights = None
    for proc, weight in sum([cfg.items() for cfg in setup['backgrounds']], []):
        for p in sum([Process.expand(proc)], []):
            logging.debug('reading {}'.format(p))
            d = rec2array(root2array(fn, str(p), setup['variables']))
            if isinstance(weight, float) or isinstance(weight, int):
                w = np.array([weight] * len(d))
            else:
                w = rec2array(root2array(fn, str(p), [weight])).ravel()
            w *= p.cross_section / p.events
            if background is not None:
                background = np.concatenate((background, d))
                background_weights = np.concatenate((background_weights, w))
            else:
                background = d
                background_weights = w

    factor = np.sum(signal_weights) / np.sum(background_weights)
    logging.info("renormalizing background events by factor {}".format(factor))
    background_weights *= factor

    return signal, signal_weights, background, background_weights


def evaluate(config, tree, names, transform=None):
    output = []
    dtype = []
    for name in names:
        setup = load(config, name.split("_")[1])
        data = rec2array(tree2array(tree.raw(), list(transform(setup["variables"])) if transform else setup["variables"]))
        if name.startswith("sklearn"):
            fn = os.path.join(config["mvadir"], name + ".pkl")
            with open(fn, 'rb') as fd:
                bdt, label = pickle.load(fd)
            scores = []
            if len(data) > 0:
                scores = bdt.predict_proba(data)[:, 1]
            output += [scores]
            dtype += [(name, 'float64')]

        fn = os.path.join(config["mvadir"], name + ".xml")
        reader = r.TMVA.Reader("Silent")
        for var in setup['variables']:
            reader.AddVariable(var, array('f', [0.]))
        reader.BookMVA("BDT", fn)
        scores = evaluate_reader(reader, "BDT", data)
        output += [scores]
        dtype += [(name.replace("sklearn", "tmvalike"), 'float64')]

    f = r.TFile(os.path.join(config.get("mvadir", config.get("indir", config["outdir"])), "mapping.root"), "READ")
    if f.IsOpen():
        likelihood = f.Get("hTargetBinning")

        def lh(values):
            return likelihood.GetBinContent(likelihood.FindBin(*values))
        indices = dict((v, n) for n, (v, _) in enumerate(dtype))
        tt = output[indices['tmvalike_tt']]
        ttZ = output[indices['tmvalike_ttZ']]
        if len(tt) == 0:
            output += [[]]
        else:
            output += [np.apply_along_axis(lh, 1, np.array([tt, ttZ]).T)]
        dtype += [('tmvalike_likelihood', 'float64')]
        f.Close()

    data = np.array(zip(*output), dtype)
    tree.mva(array2tree(data))


def run_cross_validation(outdir, bdts, x, y):
    logging.info("starting cross validation")
    for n, bdt in enumerate(bdts):
        scores = cross_validation.cross_val_score(bdt, x, y, scoring="roc_auc", n_jobs=NJOBS, cv=CV)
        out = u'training accuracy: {} ± {}\n'.format(scores.mean(), scores.std())
        with codecs.open(os.path.join(outdir, "bdt-{}".format(n), "log-accuracy.txt"), "w", encoding="utf8") as fd:
            fd.write(out)


def plot_validation_curve(outdir, bdt, x_train, y_train, w_train, x_test, y_test, w_test):
    logging.info("saving validation curve")
    test_score, train_score = np.empty(len(bdt.estimators_)), np.empty(len(bdt.estimators_))

    for i, pred in enumerate(bdt.staged_decision_function(x_test)):
        test_score[i] = 1 - roc_auc_score(y_test, pred, sample_weight=w_test)
    for i, pred in enumerate(bdt.staged_decision_function(x_train)):
        train_score[i] = 1 - roc_auc_score(y_train, pred, sample_weight=w_train)

    best = np.argmin(test_score)
    line = plt.plot(test_score, label=bdt.label)
    plt.plot(train_score, '--', color=line[-1].get_color())

    plt.xlabel("Number of boosting iterations")
    plt.ylabel("1 - area under ROC")
    plt.axvline(x=best, color=line[-1].get_color())
    plt.legend(loc='best')
    plt.savefig(os.path.join(outdir, 'validation-curve.png'))
    plt.savefig(os.path.join(outdir, 'validation-curve.pdf'))
    plt.close()


def run_feature_elimination(outdir, bdts, x, y, setup):
    logging.info("starting feature selection")
    for n, bdt in enumerate(bdts):
        rfecv = RFECV(estimator=bdt, step=1, cv=CV, scoring='roc_auc')  # new in 18.1: , n_jobs=NJOBS)
        rfecv.fit(x, y)

        plot_feature_elimination(outdir, rfecv, n)

        out = u'Feature selection\n=================\n\n'
        out += u'optimal feature count: {}\n\nranking\n-------\n'.format(rfecv.n_features_)
        for i, v in enumerate(setup["variables"]):
            out += u'{:30}: {:>5}\n'.format(v, rfecv.ranking_[i])
        with codecs.open(os.path.join(outdir, "bdt-{}".format(n), "log-feature-elimination.txt"), "w", encoding="utf8") as fd:
            fd.write(out)


def run_grid_search(outdir, bdt, x, y):
    logging.info('starting hyper-parameter optimization')
    param_grid = {
        "n_estimators": [500, 1000, 2000, 5000],
        "max_depth": [3, 4, 5, 6, 7, 8],
        "learning_rate": [.002, .005, .01, .02, .1, .2]
    }

    clf = grid_search.GridSearchCV(bdt, param_grid, cv=CV, scoring='roc_auc', n_jobs=NJOBS)
    clf.fit(x, y)

    out = '\nHyper-parameter optimization\n'
    out += '============================\n\n'
    out += 'Best estimator: {}\n'.format(clf.best_estimator_)
    out += '\nFull Scores\n'
    out += '-----------\n\n'
    for params, mean_score, scores in clf.grid_scores_:
        out += u'{:0.4f} (±{:0.4f}) for {}\n'.format(mean_score, scores.std(), params)
    with codecs.open(os.path.join(outdir, "log-hyper-parameters.txt"), "w", encoding="utf8") as fd:
        fd.write(out)


def plot_correlations(outdir, vars, sig, bkg):
    for data, label in ((sig, "Signal"), (bkg, "Background")):
        d = pd.DataFrame(data, columns=vars)
        sns.heatmap(d.corr(), annot=True, fmt=".2f", linewidth=.5)
        plt.title(label + " Correlations")
        plt.tight_layout()
        plt.savefig(os.path.join(outdir, 'correlations_{}.png'.format(label.lower())))
        plt.savefig(os.path.join(outdir, 'correlations_{}.png'.format(label.lower())))
        plt.close()


def plot_feature_elimination(outdir, cls, n):
    plt.plot(range(1, len(cls.grid_scores_) + 1), cls.grid_scores_)
    plt.xlabel('# features')
    plt.ylabel('Score (ROC auc)')
    plt.savefig(os.path.join(outdir, 'bdt-{}'.format(n), 'feature-elimination.png'))
    plt.savefig(os.path.join(outdir, 'bdt-{}'.format(n), 'feature-elimination.pdf'))
    plt.close()


def plot_inputs(outdir, vars, sig, sig_w, bkg, bkg_w):
    for n, var in enumerate(vars):
        _, bins = np.histogram(np.concatenate((sig[:, n], bkg[:, n])), bins=40)
        sns.distplot(bkg[:, n], hist_kws={'weights': bkg_w}, bins=bins, kde=False, norm_hist=True, label='background')
        sns.distplot(sig[:, n], hist_kws={'weights': sig_w}, bins=bins, kde=False, norm_hist=True, label='signal')
        plt.title(var)
        plt.legend()
        plt.savefig(os.path.join(outdir, 'input_{}.png'.format(var)))
        plt.savefig(os.path.join(outdir, 'input_{}.png'.format(var)))
        plt.close()


def plot_learning_curve(outdir, bdt, x, y):
    logging.info("creating learning curve")
    train_sizes, train_scores, test_scores = learning_curve(bdt, x, y,
                                                            cv=ShuffleSplit(len(x),
                                                                            n_iter=100,
                                                                            test_size=1.0 / CV),
                                                            n_jobs=NJOBS,
                                                            train_sizes=np.linspace(.1, 1., 7),
                                                            scoring='roc_auc')
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)

    plt.fill_between(train_sizes,
                     train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std,
                     alpha=.2, color='r')
    plt.fill_between(train_sizes,
                     test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std,
                     alpha=.2, color='g')
    plt.plot(train_sizes, train_scores_mean, 'o-', color='r', label='Training score')
    plt.plot(train_sizes, test_scores_mean, 'o-', color='g', label='Cross-validation score')

    plt.xlabel("Sample size")
    plt.ylabel("Score (ROC area)")

    plt.legend()
    plt.savefig(os.path.join(outdir, 'learning-curve.png'))
    plt.savefig(os.path.join(outdir, 'learning-curve.pdf'))
    plt.close()


def plot_output(outdir, bdt, data, filename, bins, fct):
    outputs = []
    for x, y, w, label in data:
        sig = fct(bdt, x[y > .5]).ravel()
        bkg = fct(bdt, x[y < .5]).ravel()
        w_sig = w[y > .5]
        w_bkg = w[y < .5]
        outputs.append((sig, bkg, w_sig, w_bkg, label))

    for sig, bkg, w_sig, w_bkg, label in outputs:
        if label == 'training':
            sns.distplot(bkg, hist_kws={'weights': w_bkg}, bins=bins, color='r', kde=False, norm_hist=True, label='background (training)')
            sns.distplot(sig, hist_kws={'weights': w_sig}, bins=bins, color='b', kde=False, norm_hist=True, label='signal (training)')
        else:
            centers = (bins[:-1] + bins[1:]) * .5
            bcounts, _ = np.histogram(bkg, weights=w_bkg, bins=bins, density=True)
            plt.plot(centers, bcounts, 'o', color='r', label='background (testing)')
            scounts, _ = np.histogram(sig, weights=w_sig, bins=bins, density=True)
            plt.plot(centers, scounts, 'o', color='b', label='signal (testing)')
    plt.xlabel('BDT score')

    plt.legend(loc='best')
    plt.savefig(os.path.join(outdir, filename))
    plt.close()
