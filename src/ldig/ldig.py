import codecs
import json
import os
import pickle
import re
import sys

import numpy

from . import da


FEATURES = None
TRIE = None
LABELS = None
PARAM = None


def check_loaded_model():
    # feature calculation is quite expensive
    global FEATURES
    global TRIE
    global LABELS
    global PARAM

    dirname = os.environ["DATA_LOCATION"]

    if FEATURES is None:
        if os.path.exists(f"{dirname}/model.latin/features.pickle"):
            with open(f"{dirname}/model.latin/features.pickle", "rb") as file:
                FEATURES = pickle.load(file)
        else:
            FEATURES = load_features()
            with open(f"{dirname}/model.latin/features.pickle", "wb") as file:
                pickle.dump(FEATURES, file)

    if TRIE is None:
        TRIE = load_da()
    if LABELS is None:
        LABELS = load_labels()
    if PARAM is None:
        PARAM = numpy.load(f"{dirname}/model.latin/parameters.npy")

    return FEATURES, TRIE, LABELS, PARAM


re_ignore_i = re.compile(r"[^I]")
vietnamese_norm = {
    "\u0041\u0300": "\u00C0",
    "\u0045\u0300": "\u00C8",
    "\u0049\u0300": "\u00CC",
    "\u004F\u0300": "\u00D2",
    "\u0055\u0300": "\u00D9",
    "\u0059\u0300": "\u1EF2",
    "\u0061\u0300": "\u00E0",
    "\u0065\u0300": "\u00E8",
    "\u0069\u0300": "\u00EC",
    "\u006F\u0300": "\u00F2",
    "\u0075\u0300": "\u00F9",
    "\u0079\u0300": "\u1EF3",
    "\u00C2\u0300": "\u1EA6",
    "\u00CA\u0300": "\u1EC0",
    "\u00D4\u0300": "\u1ED2",
    "\u00E2\u0300": "\u1EA7",
    "\u00EA\u0300": "\u1EC1",
    "\u00F4\u0300": "\u1ED3",
    "\u0102\u0300": "\u1EB0",
    "\u0103\u0300": "\u1EB1",
    "\u01A0\u0300": "\u1EDC",
    "\u01A1\u0300": "\u1EDD",
    "\u01AF\u0300": "\u1EEA",
    "\u01B0\u0300": "\u1EEB",
    "\u0041\u0301": "\u00C1",
    "\u0045\u0301": "\u00C9",
    "\u0049\u0301": "\u00CD",
    "\u004F\u0301": "\u00D3",
    "\u0055\u0301": "\u00DA",
    "\u0059\u0301": "\u00DD",
    "\u0061\u0301": "\u00E1",
    "\u0065\u0301": "\u00E9",
    "\u0069\u0301": "\u00ED",
    "\u006F\u0301": "\u00F3",
    "\u0075\u0301": "\u00FA",
    "\u0079\u0301": "\u00FD",
    "\u00C2\u0301": "\u1EA4",
    "\u00CA\u0301": "\u1EBE",
    "\u00D4\u0301": "\u1ED0",
    "\u00E2\u0301": "\u1EA5",
    "\u00EA\u0301": "\u1EBF",
    "\u00F4\u0301": "\u1ED1",
    "\u0102\u0301": "\u1EAE",
    "\u0103\u0301": "\u1EAF",
    "\u01A0\u0301": "\u1EDA",
    "\u01A1\u0301": "\u1EDB",
    "\u01AF\u0301": "\u1EE8",
    "\u01B0\u0301": "\u1EE9",
    "\u0041\u0303": "\u00C3",
    "\u0045\u0303": "\u1EBC",
    "\u0049\u0303": "\u0128",
    "\u004F\u0303": "\u00D5",
    "\u0055\u0303": "\u0168",
    "\u0059\u0303": "\u1EF8",
    "\u0061\u0303": "\u00E3",
    "\u0065\u0303": "\u1EBD",
    "\u0069\u0303": "\u0129",
    "\u006F\u0303": "\u00F5",
    "\u0075\u0303": "\u0169",
    "\u0079\u0303": "\u1EF9",
    "\u00C2\u0303": "\u1EAA",
    "\u00CA\u0303": "\u1EC4",
    "\u00D4\u0303": "\u1ED6",
    "\u00E2\u0303": "\u1EAB",
    "\u00EA\u0303": "\u1EC5",
    "\u00F4\u0303": "\u1ED7",
    "\u0102\u0303": "\u1EB4",
    "\u0103\u0303": "\u1EB5",
    "\u01A0\u0303": "\u1EE0",
    "\u01A1\u0303": "\u1EE1",
    "\u01AF\u0303": "\u1EEE",
    "\u01B0\u0303": "\u1EEF",
    "\u0041\u0309": "\u1EA2",
    "\u0045\u0309": "\u1EBA",
    "\u0049\u0309": "\u1EC8",
    "\u004F\u0309": "\u1ECE",
    "\u0055\u0309": "\u1EE6",
    "\u0059\u0309": "\u1EF6",
    "\u0061\u0309": "\u1EA3",
    "\u0065\u0309": "\u1EBB",
    "\u0069\u0309": "\u1EC9",
    "\u006F\u0309": "\u1ECF",
    "\u0075\u0309": "\u1EE7",
    "\u0079\u0309": "\u1EF7",
    "\u00C2\u0309": "\u1EA8",
    "\u00CA\u0309": "\u1EC2",
    "\u00D4\u0309": "\u1ED4",
    "\u00E2\u0309": "\u1EA9",
    "\u00EA\u0309": "\u1EC3",
    "\u00F4\u0309": "\u1ED5",
    "\u0102\u0309": "\u1EB2",
    "\u0103\u0309": "\u1EB3",
    "\u01A0\u0309": "\u1EDE",
    "\u01A1\u0309": "\u1EDF",
    "\u01AF\u0309": "\u1EEC",
    "\u01B0\u0309": "\u1EED",
    "\u0041\u0323": "\u1EA0",
    "\u0045\u0323": "\u1EB8",
    "\u0049\u0323": "\u1ECA",
    "\u004F\u0323": "\u1ECC",
    "\u0055\u0323": "\u1EE4",
    "\u0059\u0323": "\u1EF4",
    "\u0061\u0323": "\u1EA1",
    "\u0065\u0323": "\u1EB9",
    "\u0069\u0323": "\u1ECB",
    "\u006F\u0323": "\u1ECD",
    "\u0075\u0323": "\u1EE5",
    "\u0079\u0323": "\u1EF5",
    "\u00C2\u0323": "\u1EAC",
    "\u00CA\u0323": "\u1EC6",
    "\u00D4\u0323": "\u1ED8",
    "\u00E2\u0323": "\u1EAD",
    "\u00EA\u0323": "\u1EC7",
    "\u00F4\u0323": "\u1ED9",
    "\u0102\u0323": "\u1EB6",
    "\u0103\u0323": "\u1EB7",
    "\u01A0\u0323": "\u1EE2",
    "\u01A1\u0323": "\u1EE3",
    "\u01AF\u0323": "\u1EF0",
    "\u01B0\u0323": "\u1EF1",
}
re_vietnamese = re.compile(
    "[AEIOUYaeiouy\u00C2\u00CA\u00D4\u00E2\u00EA\u00F4\u0102\u0103\u01A0\u01A1\u01AF\u01B0][\u0300\u0301\u0303\u0309\u0323]"
)
re_latin_cont = re.compile("([a-z\u00e0-\u024f])\\1{2,}")
re_symbol_cont = re.compile("([^a-z\u00e0-\u024f])\\1{1,}")


def normalize_text(org):
    m = re.match(r"([-A-Za-z]+)\t(.+)", org)
    if m:
        label, org = m.groups()
    else:
        label = ""
    m = re.search(r"\t([^\t]+)$", org)
    if m:
        s = m.group(0)
    else:
        s = org

    s = re.sub("[\u2010-\u2015]", "-", s)
    s = re.sub("[0-9]+", "0", s)
    s = re.sub("[^\u0020-\u007e\u00a1-\u024f\u0300-\u036f\u1e00-\u1eff]+", " ", s)
    s = re.sub("  +", " ", s)

    # vietnamese normalization
    s = re_vietnamese.sub(lambda x: vietnamese_norm[x.group(0)], s)

    # lower case with Turkish
    s = re_ignore_i.sub(lambda x: x.group(0).lower(), s)

    # Romanian normalization
    s = s.replace("\u0219", "\u015f").replace("\u021b", "\u0163")

    s = re_latin_cont.sub(r"\1\1", s)
    s = re_symbol_cont.sub(r"\1", s)

    return label, s.strip(), org


def load_da():
    dirname = os.environ["DATA_LOCATION"]
    trie = da.DoubleArray()
    trie.load(f"{dirname}/model.latin/doublearray.npz")
    return trie


def load_features():
    dirname = os.environ["DATA_LOCATION"]
    features = []
    with codecs.open(f"{dirname}/model.latin/features", "rb", "utf-8") as f:
        pre_feature = ()
        for n, s in enumerate(f):
            m = re.match(r"(.+)\t([0-9]+)", s)
            if not m:
                sys.exit("irregular feature: " + s + " at " + str((n + 1)))
            if pre_feature >= m.groups(1):
                sys.exit("unordered feature: " + s + " at " + str((n + 1)))
            pre_feature = m.groups(1)
            features.append(m.groups())
    return features


def load_labels():
    dirname = os.environ["DATA_LOCATION"]
    with open(f"{dirname}/model.latin/labels.json", "r") as f:
        return json.load(f)


def detect(st):
    features, trie, labels, param = check_loaded_model()

    corrects = numpy.zeros(len(labels), dtype=int)
    counts = numpy.zeros(len(labels), dtype=int)

    label_map = {x: i for i, x in enumerate(labels)}

    n_available_data = 0
    log_likely = 0.0

    label, text, org_text = normalize_text(st)

    if label not in label_map:
        label_map[label] = -1
    label_k = label_map[label]

    events = trie.extract_features("\u0001" + text + "\u0001")

    y = predict(param, events)
    predict_k = y.argmax()

    if label_k >= 0:
        log_likely -= numpy.log(y[label_k])
        n_available_data += 1
        counts[label_k] += 1
        if label_k == predict_k and y[predict_k] >= 0.6:
            corrects[predict_k] += 1

    predict_lang = labels[predict_k]
    return predict_lang, round(y[predict_k], 2)


# prediction probability
def predict(param, events):
    sum_w = numpy.dot(
        param[list(events.keys()),].T, list(events.values())  # noqa: E231
    )
    exp_w = numpy.exp(sum_w - sum_w.max())
    return exp_w / exp_w.sum()