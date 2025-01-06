#
# I M B A L A N C E
#
#
import argparse
import os.path
import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Classifier import ImbalanceCorrection
from Classifier import classifierFactory
from Classifier import Classifier
from Classifier import LogisticRegressionClassifier, KNNClassifier, DecisionTree, RandomForest, \
    GradientBoosting, SuppportVectorMachineClassifier, LDA, MLP
from Classifier import ClassificationTechniques
from Classifier import Subset
from OptionsFile import OptionsFile
import constants

import logging
import logging.config

class Imbalances:
    def __init__(self):
        self._df = pd.DataFrame(columns=['classification', 'ratio', 'correction', 'auc', 'f1', 'fpr', 'score', 'auc-delta', 'f1-delta', 'fpr-delta'])
        self._uncorrected = pd.DataFrame(columns=['classification', 'ratio', 'auc', 'f1', 'fpr', 'score'])
        self._results = []
        self._resultsUncorrected = []
        self._base = {}
        self._rocResults = {}

    def recordResult(self,
                     classificationTechnique: str,
                     correctionTechnique: str,
                     desiredRatio: str,
                     classifier: Classifier,
                     corrected: bool):
        if corrected:
            f1Uncorrected = self._base[classificationTechnique + "-" + desiredRatio]['f1']
            fprUncorrected = self._base[classificationTechnique + "-" + desiredRatio]['fpr']
            aucUncorrected = self._base[classificationTechnique + "-" + desiredRatio]['auc']
            self._results.append({'classification': classificationTechnique,
                                  'ratio': desiredRatio,
                                  'correction': correctionTechnique,
                                  'auc': classifier.auc,
                                  'f1': classifier.f1,
                                  'fpr': classifier.fpr,
                                  'score': classifier.scores,
                                  'auc-delta': classifier.auc - aucUncorrected,
                                  'f1-delta': classifier.f1 - f1Uncorrected,
                                  'fpr-delta': 0})
        else:
            self._resultsUncorrected.append({'classification': classificationTechnique,
                                      'ratio': desiredRatio,
                                      'auc': classifier.auc,
                                      'f1': classifier.f1,
                                      'fpr': classifier.fpr,
                                      'score': classifier.scores})

            self._base[classificationTechnique + "-" + desiredRatio] = {'classification': classificationTechnique,
                                      'ratio': desiredRatio,
                                      'auc': classifier.auc,
                                      'f1': classifier.f1,
                                      'fpr': classifier.fpr,
                                      'score': classifier.scores}

        self._rocResults[classifier.name] = {'FPR': classifier.fpr, "TPR": classifier.tpr}

    def visualizeROC(self):
        plt.title(f'Receiver Operating Characteristic')
        for techniqueName, rates in self._rocResults.items():
            plt.plot(rates["FPR"], rates["TPR"], label=techniqueName)
        plt.legend(loc='lower right')
        plt.plot([0, 1], [0, 1], 'r--')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
        plt.title(f'ROC Curve')
        plt.show()

    def write(self, correctedFile: str, uncorrectedFile: str):
        self._df = pd.DataFrame(self._results)
        self._uncorrected = pd.DataFrame(self._resultsUncorrected)

        self._df.to_csv(correctedFile)
        self._uncorrected.to_csv(uncorrectedFile)

ALL_OVER = "ALL-OVER"
ALL_COMBINED = "ALL-COMBINED"
imbalanceCorrectionChoices = [i.name.lower() for i in ImbalanceCorrection]
imbalanceCorrectionChoices.append(ALL_OVER)
imbalanceCorrectionChoices.append(ALL_COMBINED)
imbalanceCorrectionChoices.append("NONE")

classificationChoices = [i.name.lower() for i in ClassificationTechniques]
classificationChoices.append("ALL")

subsetChoices = [i.name.lower() for i in Subset]

parser = argparse.ArgumentParser("Imbalance analysis")

parser.add_argument('-a', '--algorithm', action="store", required=False, default=ImbalanceCorrection.SMOTE.name, choices=imbalanceCorrectionChoices)
parser.add_argument('-c', '--classifier', action="store", required=False, default=LogisticRegressionClassifier.name, choices=classificationChoices)
parser.add_argument('-d', "--directory", action="store", required=False, default=".", help="Output directory")
parser.add_argument("-df", "--data", action="store", help="Name of the data in CSV for use in logistic regression or KNN")
parser.add_argument('-ini', '--ini', action="store", required=False, default=constants.PROPERTY_FILENAME, help="Options INI")
#parser.add_argument('-mi', '--minority', action="store", required=False, type=float, default=0.2, help="Adjust minority class to represent this percentage. 0.0 = Choose several values. -1.0 == Do not correct")
parser.add_argument('-ir', '--ratio', action="store", required=False, type=str, default="0:0", help="Adjust ratio (N:M) of subset. Specify a fixed value (10:1) or a range (10:1-10")
parser.add_argument('-is', '--steps', action="store", required=False, type=int, default=5, help="Steps within range specified")
parser.add_argument("-lg", "--logging", action="store", default="logging.ini", help="Logging configuration file")
parser.add_argument('-o', '--output', action="store", required=False, default="imbalance.csv", help="Output CSV")
parser.add_argument('-s', '--subset', action="store", required=False, default=Subset.TRAIN.name, choices=subsetChoices, help="Subset to apply correction")
arguments = parser.parse_args()

logging.config.fileConfig(arguments.logging)
log = logging.getLogger("imbalance")

options = OptionsFile(arguments.ini)
options.load()

selections = [e.strip() for e in options.option(constants.PROPERTY_SECTION_IMAGE_PROCESSING, constants.PROPERTY_FACTORS).split(',')]
log.debug(f"Selected parameters from INI file: {selections}")

if not os.path.isdir(arguments.directory):
    print(f"Unable to access directory: {arguments.directory}")
    sys.exit(-1)

# Select the correction technique to be used
if arguments.algorithm == ALL_OVER:
    imbalanceCorrectionChoices = Classifier.oversampleCorrectionChoices
elif arguments.algorithm == ALL_COMBINED:
    imbalanceCorrectionChoices = Classifier.combinedCorrectionChoices
else:
    imbalanceCorrectionChoices = [arguments.algorithm.upper()]

if arguments.classifier == "ALL":
    classificationChoices = [i.name for i in ClassificationTechniques]
else:
    classificationChoices = [arguments.classifier.upper()]

# Ratio is expected to be something like 10:1-10 or 10:2
splitForSubset = arguments.ratio.split(':')
if len(splitForSubset) != 2:
    print(f"Invalid ratio specified: {arguments.ratio}")
    sys.exit(-1)
else:
    desiredCrop = float(splitForSubset[0])
    # This is where there is a range
    weedRange = splitForSubset[1].split('-')
    if len(weedRange) == 2:
        weedRangeLower = float(weedRange[0])
        weedRangeUpper = float(weedRange[1])
        weedRange = np.linspace(weedRangeLower, weedRangeUpper, arguments.steps)
    # This is the case where there is a single value
    else:
        weedRange = [float(splitForSubset[1])]
print(f"{desiredCrop}:{weedRange}")

# if arguments.minority == 0.0:
#     minorities = np.linspace(.1, .9, 5)
# else:
#     minorities = [arguments.minority]


results = Imbalances()

# Establish the uncorrected rates
uncorrected = {}
for classificationAlgorithm in classificationChoices:
    for desiredWeed in weedRange:
        desiredRatio = f"{desiredCrop}:{desiredWeed}"
        log.debug(f"Establish uncorrected base: {classificationAlgorithm} Ratio: {desiredRatio}")
        classifier = classifierFactory(classificationAlgorithm)
        classifier.selections = selections
        classifier.correctSubset = Subset[arguments.subset.upper()]
        classifier.writeDatasetToDisk = False
        classifier.outputDirectory = arguments.directory
        classifier.correct = False
        classifier.targetImbalanceRatio = desiredRatio
        # Only random forest requires the data be stratified
        stratification = isinstance(classifier, RandomForest)

        log.debug(f"Loading classifier with: {arguments.data}")
        classifier.load(arguments.data, stratify=stratification)
        classifier.createModel(True)
        classifier.assess()
        results.recordResult(classificationAlgorithm, "None", desiredRatio, classifier, False)

log.debug(f"Uncorrected")
log.debug(f"{uncorrected}")

for classificationAlgorithm in classificationChoices:
    for imbalanceAlgorithm in imbalanceCorrectionChoices:
        for desiredWeed in weedRange:
            desiredRatio = f"{desiredCrop}:{desiredWeed}"
            log.debug(f"Classify: {classificationAlgorithm} Imbalance: {imbalanceAlgorithm} Ratio: {desiredRatio}")
            classifier = classifierFactory(classificationAlgorithm)
            classifier.selections = selections
            classifier.correctSubset = Subset[arguments.subset.upper()]
            classifier.writeDatasetToDisk = True
            classifier.outputDirectory = arguments.directory

            if arguments.algorithm.upper() == "NONE":
                classifier.correct = False
            else:
                classifier.correct = True
                classifier.correctionAlgorithm = ImbalanceCorrection[imbalanceAlgorithm.upper()]
            classifier.targetImbalanceRatio = desiredRatio
            log.debug(f"Loaded selections: {classifier.selections}")

            # Only random forest requires the data be stratified
            stratification = isinstance(classifier, RandomForest)

            log.debug(f"Loading classifier with: {arguments.data}")
            classifier.load(arguments.data, stratify=stratification)
            classifier.createModel(True)
            classifier.assess()
            results.recordResult(classificationAlgorithm,
                                 imbalanceAlgorithm,
                                 desiredRatio,
                                 classifier,
                                 True)

results.write(os.path.join(arguments.directory, arguments.output), os.path.join(arguments.directory, "uncorrected-" + arguments.output))
results.visualizeROC()

sys.exit(0)
