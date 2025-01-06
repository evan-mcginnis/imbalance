#
# C L A S S I F I E R
#
import csv
import random

#import random

import constants
from constants import Score
from constants import Classification
#import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import logging
import warnings
from sklearn.model_selection import train_test_split, cross_validate, cross_val_score, cross_val_score, KFold, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.tree import plot_tree

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.exceptions import ConvergenceWarning

from imblearn.over_sampling import SMOTE, ADASYN, BorderlineSMOTE, KMeansSMOTE, SVMSMOTE
from imblearn.combine import SMOTETomek
from imblearn.combine import SMOTEENN
from imblearn.under_sampling import TomekLinks

from WeedExceptions import ProcessingError
from abc import ABC, abstractmethod

import os.path
from enum import Enum

import warnings
warnings.filterwarnings("error")

from Utility import Utility

class Subset(Enum):
    TRAIN = 0
    TEST = 1
    ALL = 2
    NONE = 3

class Type(Enum):
    CROP = 0
    WEED = 1

class ImbalanceCorrection(Enum):
    # Undersampling
    SMOTE = 0
    ADASYN = 1
    BORDERLINE = 2
    KMEANS = 3
    SVM = 4
    # Combined Under+Over
    SMOTE_TOMEK = 5
    SMOTE_ENN = 6

    def __str__(self):
        return self.name

class ClassificationTechniques(Enum):
    KNN = 0
    RANDOMFOREST = 1
    DECISIONTREE = 2
    SVM = 3
    LDA = 4
    MLP = 5
    LOGISTIC = 6
    GRADIENT = 7
    EXTRA = 8

    def __str__(self):
        return self.name

class Classifier:
    name = "Base"

    # Oversample correction techniques
    oversampleCorrectionChoices = [ImbalanceCorrection.SMOTE.name.lower(),
                                   ImbalanceCorrection.ADASYN.name.lower(),
                                   ImbalanceCorrection.BORDERLINE.name.lower(),
                                   ImbalanceCorrection.KMEANS.name.lower(),
                                   ImbalanceCorrection.SVM.name.lower()]

    # Combined correction techniques
    combinedCorrectionChoices = [ImbalanceCorrection.SMOTE_TOMEK.name.lower(),
                                 ImbalanceCorrection.SMOTE_ENN.name.lower()]

    def __init__(self):

        self._model = None
        self._df = pd.DataFrame()
        self._rawData = pd.DataFrame()

        self._xTrain = []
        self._yTrain = pd.Series
        self._xTest = []
        self._yTest = []
        # The actual type of the blob
        self._actual = np.empty([1, 1])
        self._predictions = np.empty([1, 1])

        # Scoring
        self._confusion = []
        self._scoring = Score.UNDEFINED

        # ROC items
        self._fpr = 0.0
        self._tpr = 0.0
        self._auc = 0.0
        self._y_scores = []
        self._threshold = 0.0

        self._accuracy = 0.0
        self._precision = 0.0
        self._recall = 0.0
        self._f1 = 0.0
        self._map = 0.0

        self._blobsInView = pd.DataFrame()
        self._selections = []
        self._scores = []
        self._name = "Base"
        self._loaded = False

        # Imbalance
        self._correctImbalance = False
        self._writeDatasetToDisk = False
        self._correctImbalanceAlgorithm = ImbalanceCorrection.SMOTE
        self._desiredImbalanceRatio = "0:0" # unchanged
        self._desiredCrop = 0
        self._desiredWeed = 0
        self._correctSubset = Subset.TRAIN

        # Expect dedicated train and test sets if the split is 0
        self._split = 0

        self.log = logging.getLogger(__name__)
        # # The ANN for the classifier
        # self._ann = cv.ml.ANN_MLP_create()
        # self._ann.setLayerSizes(np.array([3, 8, 3], np.uint8))
        # # Symetrical sigmoid activation
        # self._ann.setActivationFunction(cv.ml.ANN_MLP_SIGMOID_SYM, 0.6, 1.0)
        # # Backpropogation
        # self._ann.setTrainMethod(cv.ml.ANN_MLP_BACKPROP, 0.1, 0.1)
        # self._ann.setTermCriteria((cv.TERM_CRITERIA_MAX_ITER | cv.TERM_CRITERIA_EPS, 100, 1.0))
        self._scaler = StandardScaler()
        self._scalerTest = StandardScaler()

        self._outputDirectory = "."
        self._assessed = False

    # ANN Support routines start
    # def _record(self, sample: [], classification: []):
    #     return (np.array([sample], np.float32), np.array([classification], np.float32))
    #
    # def _vectorized(self, i: int) -> []:
    #     """
    #     A utility function to convert a value into an array where the ith value is 1.0
    #     :param i:
    #     :return:
    #     Numpy array with the ith element as 1.0
    #     """
    #     #e = np.zeros((4,), np.float32)
    #     e = [0.0, 0.0, 0.0, 0.0]
    #     e[i] = 1.0
    #     return e
    #
    # def _constructData(self):
    #     """
    #     Construct the data in the form opencv wants it
    #     """
    #     self._records = []
    #     for blobName, blobAttributes in self._blobs.items():
    #         self._records.append(self._record([blobAttributes[constants.NAME_AREA],
    #                                            blobAttributes[constants.NAME_RATIO],
    #                                            blobAttributes[constants.NAME_RATIO]],
    #                                           self._vectorized(blobAttributes[constants.NAME_TYPE])))
    # def train(self, blobs: {}):
    #     EPOCHS = 10
    #
    #     self._constructData()
    #
    #     for e in range(0, EPOCHS):
    #         print("Train %d\n" % e)
    #         for (t, c) in self._records:
    #             data = cv.ml.TrainData_create(t, cv.ml.ROW_SAMPLE, c)
    #             if self._ann.isTrained():
    #                 self._ann.train(data,
    #                                 cv.ml.ANN_MLP_UPDATE_WEIGHTS,
    #                                 cv.ml.ANN_MLP_NO_INPUT_SCALE,
    #                                 cv.ml.ANN_MLP_NO_OUTPUT_SCALE)
    #             else:
    #                 self._ann.train(data, cv.ml.ANN_MLP_NO_INPUT_SCALE, cv.ml.ANN_MLP_NO_OUTPUT_SCALE)
    #     return
    # ANN support routines end

    @classmethod
    def correctionAlgorithms(cls) -> []:
        """
        Supported algorithms for imbalance correction
        :return: list of names
        """
        choices = []
        for choice in ImbalanceCorrection:
            choices.append(choice.name)
        return choices

    @property
    def outputDirectory(self) -> str:
        return self._outputDirectory

    @outputDirectory.setter
    def outputDirectory(self, directory: str):
        if not os.path.isdir(directory):
            self.log.error(f"Unable to access directory: {self._outputDirectory}")
            raise ValueError(f"Unable to access directory: {self._outputDirectory}")
        self._outputDirectory = directory


    @property
    def correctSubset(self) -> Subset:
        return self._correctSubset

    @correctSubset.setter
    def correctSubset(self, theSubset: Subset):
        self._correctSubset = theSubset

    @property
    def writeDatasetToDisk(self) -> bool:
        return self._writeDatasetToDisk

    @writeDatasetToDisk.setter
    def writeDatasetToDisk(self, writeData: bool):
        self._writeDatasetToDisk = writeData

    @property
    def targetImbalanceRatio(self) -> str:
        return self._desiredImbalanceRatio

    @targetImbalanceRatio.setter
    def targetImbalanceRatio(self, ratio: str):
        self.log.debug(f"Imbalance ratio: {ratio}")
        desiredRatio = ratio.split(':')
        if len(desiredRatio) != 2:
            raise ValueError(f"Ratio must be float:float.  Got: {ratio}")
        else:
            self._desiredCrop = float(desiredRatio[0])
            self._desiredWeed = float(desiredRatio[1])
            self._desiredImbalanceRatio = ratio

    @property
    def correct(self) -> bool:
        """
        Correct imbalances in dataset
        :return:
        """
        return self._correctImbalance

    @correct.setter
    def correct(self, theCorrection: bool):
        self._correctImbalance = theCorrection

    @property
    def correctionAlgorithm(self) -> ImbalanceCorrection:
        """
        The algorithm used in correction
        :return:
        """
        return self._correctImbalanceAlgorithm

    @correctionAlgorithm.setter
    def correctionAlgorithm(self, theAlgorithm: ImbalanceCorrection):
        self._correctImbalanceAlgorithm = theAlgorithm

    @property
    def yTrain(self) -> pd.Series:
        return self._yTrain

    def createImbalance(self, location: Subset) -> bool:
        """
        Create an imbalance in the data set -- should be called before a split
        :param location: Create imbalance in train, test, or all
        """
        # If things are unchanged, just return
        if self._desiredImbalanceRatio == "0:0":
            self.log.info("No imbalance requested")
            return False

        # More crop than weeds
        if self._desiredCrop > self._desiredWeed:
            dropDenominator = self._desiredCrop / self._desiredWeed
        elif self._desiredCrop == self._desiredWeed:
            self.log.debug(f"Imbalance is 1:1 ({self._desiredImbalanceRatio}).  No action taken")
            return False
        else:
            self.log.error(f"Unable to correct to ratio: {self.imbalanceRatio}")
            return False


        self.log.debug(f"Imbalance before creation: {self.imbalanceRatio(location)}")
        if location == Subset.ALL:
            candidates = self._df.index[self._df[constants.NAME_TYPE] == 0].tolist()
            indicesToDrop = []
            random.seed(42)
            for index in candidates:
                if random.random() > percentage:
                    indicesToDrop.append(index)
            self._df.drop(index=indicesToDrop, inplace=True)
            self.log.debug(f"Created imbalance in {location.name} by dropping {indicesToDrop}")
        elif location == Subset.TRAIN:
            # Find all the weeds
            candidates = self._yTrain.index[self._yTrain == 1].tolist()
            crop = self._yTrain.index[self._yTrain == 0].tolist()
            finalWeedCount = len(crop) / dropDenominator
            dropPercentage = finalWeedCount / len(candidates)
            indicesToDrop = []
            random.seed(42)
            for index in candidates:
                if random.random() > dropPercentage:
                    indicesToDrop.append(index)
            self._xTrain.drop(index=indicesToDrop, inplace=True)
            self._yTrain.drop(index=indicesToDrop, inplace=True)
            self.log.debug(f"Final weed count: {finalWeedCount}  Achieved by dropping: {dropPercentage}")
            self.log.debug(f"Created imbalance in {location.name} by dropping {indicesToDrop}")
        elif location == Subset.NONE:
            return False
        else:
            self.log.error(f"Unable to create imbalance in subset of data")
        self.log.debug(f"Imbalance after: {self.imbalanceRatio(location)}")
        return True

    def correctImbalance(self, location: Subset = Subset.NONE):
        """
        Correct imbalance between majority and minority classes in dataset.
        This updates the training dataset.
        Should be called only after the training split.
        """
        # Follow the explanation here:
        # https://stackoverflow.com/questions/15065833/imbalance-in-scikit-learn
        # if not self._loaded:
        #     raise ProcessingError("Data must be loaded before imbalances can be corrected")

        # debug the correction
        # df = pd.DataFrame(self._xTrain)
        # df.to_csv("before-imbalance-correction.csv")
        corrected = False

        self.log.debug(f"Correcting imbalance in {location.name} using {self._correctImbalanceAlgorithm.name}  Currently {self.imbalanceRatio(location)}")

        if self._correctImbalanceAlgorithm == ImbalanceCorrection.SMOTE:
            corrector = SMOTE(random_state=2)
        elif self._correctImbalanceAlgorithm == ImbalanceCorrection.SMOTE_TOMEK:
            corrector = SMOTETomek(random_state=2, tomek=TomekLinks(sampling_strategy='majority'))
        elif self._correctImbalanceAlgorithm == ImbalanceCorrection.SMOTE_ENN:
            corrector = SMOTEENN(random_state=2)
        elif self._correctImbalanceAlgorithm == ImbalanceCorrection.ADASYN:
            corrector = ADASYN(random_state=2)
        elif self._correctImbalanceAlgorithm == ImbalanceCorrection.BORDERLINE:
            corrector = BorderlineSMOTE(random_state=2)
        elif self._correctImbalanceAlgorithm == ImbalanceCorrection.KMEANS:
            corrector = KMeansSMOTE(random_state=2, cluster_balance_threshold=0.01)
        elif self._correctImbalanceAlgorithm == ImbalanceCorrection.SVM:
            corrector = SVMSMOTE(random_state=2)
        else:
            raise AttributeError(f"Requested algorithm not supported: {self._correctImbalanceAlgorithm.name}")


        try:
            if location == Subset.TRAIN:
                self._xTrain, self._yTrain = corrector.fit_resample(self._xTrain, self._yTrain)
            elif location == Subset.ALL:
                self._x, self._y = corrector.fit_resample(self._x, self._y)
            elif location == Subset.TEST:
                raise NotImplementedError("Unable to correct test subset")
            elif location == Subset.NONE:
                self.log.debug("No subset selected for correction")
            else:
                raise AttributeError(f"Unknown location {location}")
            self.log.debug(f"Corrected imbalance.  Currently {self.imbalanceRatio(location)}")
        except RuntimeError as run:
            self.log.error(f"Unable to correct {location} with {self._correctImbalanceAlgorithm} to {self._desiredImbalanceRatio}: {run}")
            return False
        except ValueError as val:
            self.log.error(f"Unable to correct {location} with {self._correctImbalanceAlgorithm} to {self._desiredImbalanceRatio}: {val}")
            return False

        return True

        # debug the correction
        # df = pd.DataFrame(self._xTrain)
        # df.to_csv("after-imbalance-correction.csv")


    def imbalanceRatio(self, location: Subset) -> str:
        """
        The imbalance ratio between the majority and minority classes
        :return:
        """
        # if not self._loaded:
        #     raise ProcessingError("Data must be loaded before imbalances can be corrected")

        unique = []
        counts = []

        if location == Subset.TRAIN:
            counts = self._yTrain.value_counts()
        elif location == Subset.ALL:
            counts = self._y.value_counts()
        elif location == Subset.TEST:
            # The counts of the classes
            unique, counts = np.unique(self._yTest, return_counts=True)
        elif location == Subset.NONE:
            return "0"
        else:
            raise NotImplementedError(f"Unknown location: {location}")

        #self.log.debug(f"Class counts: {counts}")
        # There should be only 2 counts for the two classes
        assert len(counts) == 2

        ratio = str(counts[0]) + ':' + str(counts[1]) + ' ' + Type(0).name + ':' + Type(1).name + ' (' + str(counts[0] / counts[1]) + ')'

        return ratio

    @property
    def model(self):
        return self._model

    @property
    def scoring(self) -> Score:
        """
        The current scoring model of the classifier
        :return: Score
        """
        return self._scoring

    @scoring.setter
    def scoring(self, theScoring: Score):
        """
        Set the scoring model for the classifier
        :param theScoring:
        """
        self._scoring = theScoring

    def accuracy(self) -> float:
        # Original code for only one split
        # self._model.predict(self._xTest)
        # return self._model.score(self._xTest, self._yTest)
        return self.averageOfCrossValidation()

    def averageOfCrossValidation(self) -> float:
        """
        The average of the model cross validations
        :return:
        """
        assert (len(self._scores) > 0)
        return sum(self._scores) / len(self._scores)

    @property
    def tpr(self) -> float:
        """
        The true positive rate
        :return:
        """
        return self._tpr

    @property
    def fpr(self) -> float:
        """
        The false positive rate
        :return:
        """
        return self._fpr

    @property
    def auc(self) -> float:
        return self._auc

    # @property
    # def accuracy(self) -> float:
    #     return self._accuracy

    @property
    def precision(self) -> float:
        return self._precision

    @property
    def recall(self) -> float:
        return self._recall

    @property
    def f1(self) -> float:
        return self._f1

    @property
    def map(self) -> float:
        return self._map

    @property
    def actual(self) -> []:
        return self._actual

    @property
    def scores(self) -> []:
        return self._scores

    @property
    def blobs(self):
        return self._blobs

    @blobs.setter
    def blobs(self, blobSet: {}):
        self._blobs = blobSet

    @property
    def rawData(self) -> pd.DataFrame:
        return self._rawData

    def classifyWithinCropRow(self):
        return

    def assess(self):
        try:
            self._predictions = self._model.predict(self._xTest)
            # Check if this predicted all 0s
            if np.all(self._predictions == 0):
                self._predictions[0] = 1

            self._confusion = confusion_matrix(self._yTest, self._predictions)
            self.log.debug(f"Confusion: \t {self._confusion}")
            self._accuracy = accuracy_score(self._yTest, self._predictions)
            self._precision = precision_score(self._yTest, self._predictions)
            self._recall = recall_score(self._yTest, self._predictions)
            self._f1 = f1_score(self._yTest, self._predictions)
            self._map = accuracy_score(self._yTest, self._predictions)

            self.log.debug(f"Confusion: \t {self._confusion}")
            self.log.debug(f"Accuracy: \t {accuracy_score(self._yTest, self._predictions):.2%}")
            self.log.debug(f"Precision: \t {precision_score(self._yTest, self._predictions):.3f}")
            self.log.debug(f"Recall: \t {recall_score(self._yTest, self._predictions):.3f}")
            self.log.debug(f"F1: \t {f1_score(self._yTest, self._predictions):.2f}")
        except Exception as e:
            self.log.error(e)

    def classifyByDamage(self, rectangles: []):
        self.log.disabled = False
        for rectName, rectAttributes in rectangles.items():
            (x, y, w, h) = rectAttributes[constants.NAME_LOCATION]
            (cX, cY) = rectAttributes[constants.NAME_CENTER]
            self.log.debug("Bounding: ({},{}) {}x{} Center ({},{})".format(x, y, w, h, cX, cY))

    #
    # The only real purpose here is to mark the items that are at the edge of the image as such
    #
    def classifyByPosition(self, size : ()):
        """
        Classify items as unknown if they extend off the edge of the image.
        :param size: Unused. Should be refactored out.
        """
        self.log.info("Classify by position")
        (maxY, maxX, depth) = size
        for blobName, blobAttributes in self._blobs.items():
            (x, y, w, h) = blobAttributes.get(constants.NAME_LOCATION)
            if (x == 0 or x + w >= maxX):
                blobAttributes[constants.NAME_TYPE] = constants.TYPE_UNKNOWN
                blobAttributes[constants.NAME_REASON] = constants.REASON_AT_EDGE

    def classifyAs(self, vegType: int):
        """
        Just for debugging -- set the classification type manually
        :param vegType:
        """
        for blobName, blobAttributes in self._blobs.items():
            blobAttributes[constants.NAME_TYPE] = vegType
            blobAttributes[constants.NAME_REASON] = constants.REASON_AT_EDGE

    def classifyByRatio(self, largest: int, size : (),ratio: int):
        """
        Classify blobs in the image my size ratio.
        :param size: size of the images
        :param largest: the size in pixels of the blob with the largest area
        :param ratio: the threshold ratio
        """
        (maxY, maxX, depth) = size
        try:
            largestArea = self._blobs[largest].get(constants.NAME_AREA)
            for blobName, blobAttributes in self._blobs.items():

                # Only for items that have not already been classified

                if blobAttributes[constants.NAME_TYPE] == constants.TYPE_UNKNOWN:
                    # If the area of the blob is much smaller than the largest object, it must be undesirable
                    if largestArea > ratio * blobAttributes.get(constants.NAME_AREA):

                        # But, if the view of this is only partial in that it is at the edge of the image,
                        # we can't say with confidence that it is
                        (x, y, w, h) = blobAttributes.get(constants.NAME_LOCATION)
                        if(x == 0 or x+w >= maxX):
                            blobAttributes[constants.NAME_TYPE] = constants.TYPE_UNKNOWN
                            blobAttributes[constants.NAME_REASON] = constants.REASON_AT_EDGE
                        else:
                            blobAttributes[constants.NAME_TYPE] = constants.TYPE_UNDESIRED
                            blobAttributes[constants.NAME_REASON] = constants.REASON_SIZE_RATIO
                    else:
                        (x, y, w, h) = blobAttributes.get(constants.NAME_LOCATION)
                        if(x == 0 or x+w >= maxX):
                            blobAttributes[constants.NAME_TYPE] = constants.TYPE_UNKNOWN
                            blobAttributes[constants.NAME_REASON] = constants.REASON_AT_EDGE
                        else:
                            blobAttributes[constants.NAME_TYPE] = constants.TYPE_DESIRED
                            blobAttributes[constants.NAME_REASON] = constants.REASON_SIZE_RATIO
        except KeyError:
            return

    def classify(self, reason: int):
        assert self._model is not None

        self._prepareData()

        self.log.info("Classify")
        predictions = self._model.predict(self._blobsInView)
                # Mark up the current view
        i = 0
        for blobName, blobAttributes in self._blobs.items():
            if blobAttributes[constants.NAME_REASON] != constants.REASON_AT_EDGE:
                blobAttributes[constants.NAME_TYPE] = predictions[i]
                blobAttributes[constants.NAME_REASON] = reason
            i = i + 1
        return

    def classifyPixel(self, band0: float, band1: float, band2: float) -> int:
        """
        Classifies the pixel using the readings provided as class 0 or class 1
        :param band0: float for band 0
        :param band1: float for band 1
        :param band2: float for band 2
        :return: 0 or 1
        """

        assert self._model is not None

        # Prepare the data
        _features = []
        # This is the list of features we have chosen to use
        selectedFeatureNames = tuple(self._selections)

        # Build up the list of features we will use.
        # Reading some performance comparisons, this is the fastest way to create a dataframe

        # Build up a list of features in the same order as the names
        features = [[band0, band1, band2]]

        # Create a dataframe from the with the column names we want and the feature values
        _pixel = pd.DataFrame(features, columns=selectedFeatureNames)
        _pixel.sort_index(axis=1, inplace=True)

        # Predict if this is ground or vegetation
        try:
            predictions = self._model.predict(_pixel)
        except RuntimeWarning as r:
            self.log.fatal(f"Runtime error encountered: {r}")
            raise RuntimeError("Unable to classify pixel")
        except Exception as e:
            self.log.fatal(f"{e}")
            raise RuntimeError("Exception encountered in pixel classification")

        return predictions[0]


    def loadSelections(self, filename: str):
        """
        Read in the selections from a CSV file with only one line.
        :param filename:
        :return:
        """

        # This is no longer needed, as we get the selections from the INI file
        raise NotImplementedError

        # if not os.path.isfile(filename):
        #     raise FileNotFoundError
        #
        # self.log.info("Load parameter selections")
        # # The selection file is just a single line of CSV
        # with open(filename) as f:
        #     reader = csv.reader(f)
        #     row = next(reader)
        # self._selections = row

        # return True

    @property
    def selections(self) -> []:
        return self._selections

    @selections.setter
    def selections(self, selectionList: []):
        self._selections = selectionList

    def _clean(self):
        """
        Clean the dataset by removing rows with zeros in them
        """
        columns = self._df.columns.tolist()
        columns.remove(constants.NAME_TYPE)

        lengthBefore = len(self._df)
        # This would probably be much easier if we had NANs instead of 0
        # to get rid of -- replace all the 0s with NANs
        for column in columns:
            self._df[column] = self._df[column].replace(0, np.nan)

        # And then drop rows where there is a NAN for any of the columns
        # This should work in the case where we had 0s as well as NANs, so if we switch over, it has no effect

        self._df = self._df.dropna()
        lengthAfter = len(self._df)

        if lengthBefore > lengthAfter:
            self.log.warning(f"Dropped {lengthBefore - lengthAfter} rows from dataset.")

    def load(self, filename: str, stratify: bool):
        imbalanceCreated = False
        # Confirm the file exists
        if not os.path.isfile(filename):
            self.log.critical("Unable to load file: {}".format(filename))
            raise FileNotFoundError

        if self._loaded:
            self.log.info(f"Data is already loaded.")
            return

        self.log.info("Load training file")

        # Get the type as well as everything in the selection
        s = list(self._selections)
        s.append(constants.NAME_TYPE)
        self.log.debug("Using columns: {}".format(s))
        self._df = pd.read_csv(filename, usecols=s)

        self._clean()

        # Keep a copy of this -- we will use this elsewhere
        self._rawData = self._df.copy(deep=True)

        # Extract the type -- there should be only two, desired and undesired
        y = self._df.type
        self._y = y
        # Drop the type column
        self._df.drop("type", axis='columns', inplace=True)
        # Sort by the column names, so the train columns and the features extracted match.
        # Mixing up the order does not cause a failure in scikit-learn, but this is required.
        self._df.sort_index(axis=1, inplace=True)

        self._x = self._df
        # Drop any data that is not part of the factors we want to consider

        #self.log.debug(f"Entire dataset imbalance before correction: {self.imbalanceRatio(Subset.ALL)}")

        if self._writeDatasetToDisk:
            df = pd.DataFrame(self._xTrain, columns=s)
            df.type = self._yTrain
            self.log.debug(os.path.join(self._outputDirectory, f"before-{self._correctImbalanceAlgorithm.name.lower()}-{Utility.validAsFilename(self._desiredImbalanceRatio)}-correction.csv"))
            df.to_csv(os.path.join(self._outputDirectory, f"before-{self._correctImbalanceAlgorithm.name.lower()}-{Utility.validAsFilename(self._desiredImbalanceRatio)}-correction.csv"))

        # If we want the entire dataset corrected, do so before the split into train and test
        if self._correctImbalance and self._correctSubset == Subset.ALL:
            self.correctImbalance(Subset.ALL)

        # Split up the data
        if stratify:
            X_train, X_test, y_train, y_test = train_test_split(self._df,y,train_size=0.4, stratify=y,random_state=42)
        else:
            X_train, X_test, y_train, y_test = train_test_split(self._df,y,train_size=0.4,random_state=42)
        self._xTrain = X_train
        self._yTrain = y_train
        self._xTest = X_test
        self._yTest = y_test

        # Create the imbalance before anything else is done
        if self._desiredImbalanceRatio != "0:0":
            imbalanceCreated = self.createImbalance(Subset.TRAIN)

        # If we are correcting just the train portion, that should be done after the split
        if self._correctImbalance and self._correctSubset == Subset.TRAIN and imbalanceCreated:
            self.correctImbalance(Subset.TRAIN)

        if self._writeDatasetToDisk:
            df = pd.DataFrame(self._xTrain, columns=s)
            df.type = self._yTrain
            self.log.debug(f"Writing: {os.path.join(self._outputDirectory, f'after-{self._correctImbalanceAlgorithm.name.lower()}-{Utility.validAsFilename(self._desiredImbalanceRatio)}-correction.csv')}")
            df.to_csv(os.path.join(self._outputDirectory, f"after-{self._correctImbalanceAlgorithm.name.lower()}-{Utility.validAsFilename(self._desiredImbalanceRatio)}-correction.csv"))

        self._loaded = True

    def _prepareData(self ):

        features = []
        _features = []
        Xfeatures = []
        # This is the list of features we have chosen to use
        selectedFeatureNames = tuple(self._selections)


        # Build up the list of features we will use.
        # Reading some performance comparisons, this is the fastest way to create a dataframe
        for blobName, blobAttributes in self._blobs.items():

            # Build up a list of features in the same order as the names
            _features = []
            for feature in self._selections:
                _features.append(blobAttributes[feature])

            # Put these in a format so we can initialize the dataframe
            features.append(_features)
            # This is the original, hard-coded version before I transitioned to using just color and GLCM
            # 23 May 2023 this works just fine when I use all the attributes
            # Xfeatures.append([blobAttributes[constants.NAME_RATIO],
            #                  blobAttributes[constants.NAME_SHAPE_INDEX],
            #                  blobAttributes[constants.NAME_DISTANCE],
            #                  blobAttributes[constants.NAME_DISTANCE_NORMALIZED],
            #                  blobAttributes[constants.NAME_HUE],
            #                  blobAttributes[constants.NAME_I_YIQ]])
            # This is the Color+GLCM version 23 May 2023
            # 27 Feb 2024 Not needed
            # Xfeatures.append([blobAttributes[constants.NAME_SATURATION],
            #                  blobAttributes[constants.NAME_I_YIQ],
            #                  blobAttributes[constants.NAME_BLUE_DIFFERENCE],
            #                  blobAttributes[constants.NAME_GREYSCALE + constants.DELIMETER + constants.NAME_HOMOGENEITY + constants.DELIMETER + "0"],
            #                  blobAttributes[constants.NAME_GREYSCALE + constants.DELIMETER + constants.NAME_ENERGY + constants.DELIMETER + "0"],
            #                  blobAttributes[constants.NAME_GREYSCALE + constants.DELIMETER + constants.NAME_CONTRAST + constants.DELIMETER + "0"],
            #                  blobAttributes[constants.NAME_GREYSCALE + constants.DELIMETER + constants.NAME_DISSIMILARITY + constants.DELIMETER + "0"],
            #                  blobAttributes[constants.NAME_GREYSCALE + constants.DELIMETER + constants.NAME_ASM + constants.DELIMETER + "0"]])

            # Construct the dataframe we will use
            #self._blobsInView = pd.DataFrame(features, columns=('ratio', 'shape', 'distance','normalized_distance', 'hue'))
            # 23 May 2023 the original with shape attributes
            # self._blobsInView = pd.DataFrame(Xfeatures, columns=(constants.NAME_RATIO,
            #                                                     constants.NAME_SHAPE_INDEX, #'shape',
            #                                                     constants.NAME_DISTANCE, # 'distance',
            #                                                     constants.NAME_DISTANCE_NORMALIZED, # 'normalized_distance',
            #                                                     constants.NAME_HUE, # 'hue'
            #                                                     constants.NAME_I_YIQ)) # I std deviation

            self._blobsInView = pd.DataFrame(Xfeatures, columns=(constants.NAME_SATURATION,
                                                                 constants.NAME_I_YIQ,
                                                                 constants.NAME_BLUE_DIFFERENCE,
                                                                 constants.NAME_HOMOGENEITY,
                                                                 constants.NAME_ENERGY,
                                                                 constants.NAME_CONTRAST,
                                                                 constants.NAME_DISSIMILARITY,
                                                                 constants.NAME_ASM))
            # Create a dataframe from the with the column names we want and the feature values
            self._blobsInView = pd.DataFrame(features, columns=selectedFeatureNames)
            self._blobsInView.sort_index(axis=1, inplace=True)

    def visualize(self):
        plt.title(f'{self.name} Receiver Operating Characteristic')
        plt.plot(self._fpr, self._tpr, 'b', label='AUC = %0.2f' % self._auc)
        plt.legend(loc='lower right')
        plt.plot([0, 1], [0, 1], 'r--')
        plt.xlim([0, 1])
        plt.ylim([0, 1])
        plt.ylabel('True Positive Rate')
        plt.xlabel('False Positive Rate')
        plt.title(f'ROC Curve of {self.name}')
        plt.show()

    def visualizeFolds(self):
        # Adapted from:
        # https://stackoverflow.com/questions/57708023/plotting-the-roc-curve-of-k-fold-cross-validation

        cv = StratifiedKFold(n_splits=5)
        #classifier = SVC(kernel='sigmoid', probability=True, random_state=0)

        tprs = []
        aucs = []
        mean_fpr = np.linspace(0, 1, 100)
        plt.figure(figsize=(10, 10))
        #plt.style.use('ggplot')
        i = 0
        # Original
        #for train, test in cv.split(X_train_res, y_train_res):
        #self._xTrain.reset_index(inplace=True)
        #self._yTrain = self._yTrain.reset_index()
        for train, test in cv.split(self._x, self._y):
            # Original
            # probas_ = classifier.fit(X_train_res[train], y_train_res[train]).predict_proba(X_train_res[test])
            probas_ = self._model.fit(self._x.iloc[train], self._y.iloc[train]).predict_proba(self._x.iloc[test])
            # Compute ROC curve and area the curve
            fpr, tpr, thresholds = roc_curve(self._y[test], probas_[:, 1])
            tprs.append(np.interp(mean_fpr, fpr, tpr))
            tprs[-1][0] = 0.0
            roc_auc = auc(fpr, tpr)
            aucs.append(roc_auc)
            plt.plot(fpr, tpr, lw=1, alpha=0.6,
                     label='ROC fold %d (AUC = %0.2f)' % (i, roc_auc))

            i += 1
        plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
                 label='Chance', alpha=.8)

        mean_tpr = np.mean(tprs, axis=0)
        mean_tpr[-1] = 1.0
        mean_auc = auc(mean_fpr, mean_tpr)
        std_auc = np.std(aucs)
        plt.plot(mean_fpr, mean_tpr, color='b',
                 label=r'Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
                 lw=2, alpha=.8)

        std_tpr = np.std(tprs, axis=0)
        tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
        tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
        plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color='grey', alpha=.2,
                         label=r'$\pm$ 1 std. dev.')

        plt.xlim([-0.01, 1.01])
        plt.ylim([-0.01, 1.01])
        plt.xlabel('False Positive Rate', fontsize=18)
        plt.ylabel('True Positive Rate', fontsize=18)
        plt.title(f'Cross-Validation ROC of {self.name}', fontsize=18)
        plt.legend(loc="lower right", prop={'size': 15})
        plt.show()

    def createModel(self, score: bool):
        raise NotImplementedError

    def reset(self):
        self._model = None

    def visualizeModel(self):
        raise NotImplementedError

class MLP(Classifier):
    name = ClassificationTechniques.MLP.name

    def __init__(self):
        super().__init__()
        self._xTrainScaled = None
        self._xTestScaled = None

    def createModel(self, score: Score):
        self.log.debug(f"Create MLP Model")
        # Scale the data
        xTrainAsList = self._xTrain.values.tolist()
        self._scaler.fit(xTrainAsList)
        #self._scaler.fit(self._xTrain)
        self._xTrainScaled = self._scaler.transform(xTrainAsList)

        # debug begin
        # Scale the data
        xTestAsList = self._xTest.values.tolist()
        self._scalerTest.fit(xTestAsList)
        #self._scaler.fit(self._xTrain)
        self._xTestScaled = self._scalerTest.transform(xTrainAsList)
        # debug end

        # Keeping this as a numpy array is causing problems
        #scaledXTrain = self._scaler.transform(self._xTrain)
        xTestAsList = self._xTest.values.tolist()
        self._xTestScaled = self._scaler.transform(xTestAsList)

        # The lbfgs solver runs into problems.  Use adam
        self._model = MLPClassifier(solver='sgd', max_iter=5000, alpha=1e-5, hidden_layer_sizes=(20), random_state=42)
        with warnings.catch_warnings():
            warnings.filterwarnings('error')
            try:
                # Use the scaled data
                self._model.fit(self._xTrainScaled, self._yTrain)
                # self._model.fit(self._xTrain, self._yTrain)
            except ConvergenceWarning:
                self.log.error(f"Failed to converge: {self._selections}")

        self._scores = cross_val_score(self._model, self._x.values.tolist(), self._y)
        #self._scores = cross_val_score(self._model, self._x, self._y)

        self._y_scores = self._model.predict_proba(self._xTestScaled)
        #self.log.debug(f"Probablilities: {self._y_scores}")
        self._fpr, self._tpr, self._threshold = roc_curve(self._yTest, self._y_scores[:, 1])
        self._auc = auc(self._fpr, self._tpr)

        if score:
            self.log.debug(f"MLP cross validation scores: {self._scores}")

            # This causes error: X has feature names, but MLPClassifier was fitted without feature names
            # print(self._model.predict(self._xTest))
            self.log.debug(self._model.predict(self._xTestScaled))
            try:
                self.log.debug("Training Score: {:.3f}".format(self._model.score(self._xTrainScaled, self._yTrain)))
                self.log.debug("Testing Score: %s" % self._model.score(self._xTestScaled, self._yTest))
            except Exception as e:
                self.log.fatal(f"{e}")
                raise RuntimeError("Exception encountered in model scoring")
            self.log.debug(f"Score completed")

    # Overload the function for the MLP to reference the scaled data
    def accuracy(self) -> float:
        self._model.predict(self._xTestScaled)
        return self._model.score(self._xTestScaled, self._yTest)

    def classify(self):
        self.log.debug(f"Classify by MLP")
        #super().classify(constants.REASON_MLP)
        self._prepareData()

        predictions = self._model.predict(self._blobsInView)
         # Mark up the current view
        i = 0
        for blobName, blobAttributes in self._blobs.items():
            if blobAttributes[constants.NAME_REASON] != constants.REASON_AT_EDGE:
                blobAttributes[constants.NAME_TYPE] = predictions[i]
                blobAttributes[constants.NAME_REASON] = constants.REASON_RANDOM_FOREST
            i = i + 1
        return

    def classifyPixel(self, band0: float, band1: float, band2: float) -> int:
        """
        Classifies the pixel using the readings provided as class 0 or class 1
        :param band0: float for band 0
        :param band1: float for band 1
        :param band2: float for band 2
        :return: 0 or 1
        """

        assert self._model is not None

        # Prepare the data
        _features = []
        # This is the list of features we have chosen to use
        selectedFeatureNames = tuple(self._selections)

        # Build up the list of features we will use.
        # Reading some performance comparisons, this is the fastest way to create a dataframe

        # Build up a list of features in the same order as the names
        features = [[band0, band1, band2]]

        # Create a dataframe from the with the column names we want and the feature values
        # This is the only difference with the method in the superclass -- the lack of column names
        # causes problems for the classifier
        self._pixel = pd.DataFrame(features)
        self._pixel.sort_index(axis=1, inplace=True)

        # Predict if this is ground or vegetation
        try:
            predictions = self._model.predict(self._pixel)
            #self.log.debug(f"Probabilities: {self._model.predict_proba(self._pixel)}")
        except RuntimeWarning as r:
            self.log.fatal(f"Runtime error encountered: {r}")
            raise RuntimeError("Unable to classify pixel")
        except Exception as e:
            self.log.fatal(f"{e}")
            raise RuntimeError("Exception encountered in pixel classification")

        return predictions[0]

    def assess(self):
        """
        Assess the results of a classifier model
        """
        try:
            self._predictions = self._model.predict(self._xTestScaled)
            if np.all(self._predictions == 0):
                self._predictions[0] = 1
            self._confusion = confusion_matrix(self._yTest, self._predictions)
            self.log.debug(f"Confusion: \t {self._confusion}")
            self._accuracy = accuracy_score(self._yTest, self._predictions)
            self._precision = precision_score(self._yTest, self._predictions, zero_division=1)
            self._recall = recall_score(self._yTest, self._predictions)
            self._f1 = f1_score(self._yTest, self._predictions)
            self._map = accuracy_score(self._yTest, self._predictions)

            self.log.debug(f"Confusion: \t {self._confusion}")
            self.log.debug(f"Accuracy: \t {accuracy_score(self._yTest, self._predictions):.2%}")
            self.log.debug(f"Precision: \t {precision_score(self._yTest, self._predictions):.3f}")
            self.log.debug(f"Recall: \t {recall_score(self._yTest, self._predictions):.3f}")
            self.log.debug(f"F1: \t {f1_score(self._yTest, self._predictions):.2f}")
            self._assessed = True
        except Exception as e:
            self.log.error(f"Unable to assess: {e}")

class LDA(Classifier):
    name = ClassificationTechniques.LDA.name

    def __init__(self):
        super().__init__()

    def createModel(self, score: Score):
        """
        Create an LDA model
        :param score: True indicates a text output of the score
        """
        self._model = LinearDiscriminantAnalysis()
        self._model.fit(self._xTrain, self._yTrain)

        self._scores = cross_val_score(self._model, self._x, self._y)

        self._y_scores = self._model.predict_proba(self._xTest)
        self._fpr, self._tpr, self._threshold = roc_curve(self._yTest, self._y_scores[:, 1])
        self._auc = auc(self._fpr, self._tpr)


        if score:
            self.log.debug(f"LDA cross validation scores: {self._scores}")

            print("Linear Discriminate Analysis")
            self._predictions = self._model.predict(self._xTest)
            print(self._predictions)

            print("Training Score: {:.3f}".format(self._model.score(self._xTrain, self._yTrain)))
            print("Testing Score: %s" % self._model.score(self._xTest, self._yTest))

            self._confusion = confusion_matrix(self._yTest, self._predictions)
            print(f"Confusion: \t {self._confusion}")
            print(f"Accuracy: \t {accuracy_score(self._yTest, self._predictions):.2%}")
            print(f"Precision: \t {precision_score(self._yTest, self._predictions):.3f}")
            print(f"Recall: \t {recall_score(self._yTest, self._predictions):.3f}")
            print(f"F1: \t {f1_score(self._yTest, self._predictions):.2f}")


    def classify(self):
        # TODO: Raise an exception
        if self._model is None:
            return

        self.log.info("Classify by LDA")
        self._prepareData()

        # Make the predictions using the model trained
        predictions = self._model.predict(self._blobsInView)

        # Put the predictions into the blobs and mark the reason as LDA
        i = 0
        for blobName, blobAttributes in self._blobs.items():
            if blobAttributes[constants.NAME_REASON] != constants.REASON_AT_EDGE:
                blobAttributes[constants.NAME_TYPE] = predictions[i]
                blobAttributes[constants.NAME_REASON] = constants.REASON_LDA
            i = i + 1
        return

class SuppportVectorMachineClassifier(Classifier):
    name = ClassificationTechniques.SVM.name

    def __init__(self):
        super().__init__()

    def createModel(self, score: bool):
        """
        Create the model for SVM
        :param score: A boolean indicating if scores should be printed.
        :return:
        """

        # Confirm the file exists
        # if not os.path.isfile(filename):
        #     raise FileNotFoundError

        # # Load from the csv file and get the columns we care about
        # self._df = pd.read_csv(filename, usecols=["ratio", "shape", "distance", "type"])
        # # Extract the type -- there should be only two, desired and undesired
        # y = self._df.type
        # # Drop the type column
        # self._df.drop("type", axis='columns', inplace=True)
        # # Split up the data
        # X_train, X_test, y_train, y_test = train_test_split(self._df,y,train_size=0.4)

        # The default of 1000 iterations fails to converge
        # dual==True fails to converge
        self._model = LinearSVC(dual=False, max_iter=10000)
        self._model.fit(self._xTrain, self._yTrain)

        self._scores = cross_val_score(self._model, self._x, self._y)

        # Since linearSVC doesn't support the probabilities needed, use this approach
        clf = CalibratedClassifierCV(self._model)
        clf.fit(self._xTrain, self._yTrain)
        y_proba = clf.predict_proba(self._xTest)

        self._y_scores = clf.predict_proba(self._xTest)
        self._fpr, self._tpr, self._threshold = roc_curve(self._yTest, self._y_scores[:, 1])
        self._auc = auc(self._fpr, self._tpr)

        # Debug
        if score:
            self.log.debug(f"SVM cross validation scores: {self._scores}")

            print("Support Vector Machine prediction")
            print(self._model.predict(self._xTest))
            print("Training Score: {:.3f}".format(self._model.score(self._xTrain, self._yTrain)))
            print("Testing Score: %s" % self._model.score(self._xTest, self._yTest))

        return

    def classify(self):
        """
        Classify the blobs in the image
        """
        # TODO: Raise an exception
        if self._model is None:
            return

        self.log.info("Classify by support vector machine")
        self._prepareData()

        # Make the predictions using the model trained
        predictions = self._model.predict(self._blobsInView)

        # Put the predictions into the blobs and mark the reason as SVM
        i = 0
        for blobName, blobAttributes in self._blobs.items():
            if blobAttributes[constants.NAME_REASON] != constants.REASON_AT_EDGE:
                blobAttributes[constants.NAME_TYPE] = predictions[i]
                blobAttributes[constants.NAME_REASON] = constants.REASON_SVM
            i = i + 1
        return


class LogisticRegressionClassifier(Classifier):
    name = ClassificationTechniques.LOGISTIC.name

    def __init__(self):
        super().__init__()

    def createModel(self, score: bool):
        """
        Initialize the logistic regression subsystem.
        :param score:
        :param filename: A csv format file name with type, ratio, shape, and area columns
        :return:
        """
        # Confirm the file exists
        # if not os.path.isfile(filename):
        #     raise FileNotFoundError

        # # Load from the csv file and get the columns we care about
        # self._df = pd.read_csv(filename, usecols=["ratio", "shape", "distance", "type"])
        # # Extract the type -- there should be only two, desired and undesired
        # y = self._df.type
        # # Drop the type column
        # self._df.drop("type", axis='columns', inplace=True)
        # # Split up the data
        # X_train, X_test, y_train, y_test = train_test_split(self._df,y,train_size=0.4)

        self.log.debug("Creating LR Model")
        self._model = LogisticRegression(C=100, max_iter=300)
        self._model.fit(self._xTrain, self._yTrain)

        self._scores = cross_val_score(self._model, self._x, self._y)

        self._y_scores = self._model.predict_proba(self._xTest)
        self._fpr, self._tpr, self._threshold = roc_curve(self._yTest, self._y_scores[:, 1])
        self._auc = auc(self._fpr, self._tpr)

        # Debug
        if score:
            self.log.debug(f"LR Cross validation scores: {self._scores}")
            self.log.debug("Logistic regression prediction")
            self.log.debug(self._model.predict(self._xTest))
            self.log.debug("Training Score: {:.3f}".format(self._model.score(self._xTrain, self._yTrain)))
            self.log.debug("Testing Score: %s" % self._model.score(self._xTest,self._yTest))

        return

    def scatterPlotDataset(self):
        """
        Display a scatterplot Matrix of the dataset
        """
        vegetationDataframe = pd.DataFrame(self._xTrain, columns=["ratio", "shape", "distance"])
        pd.plotting.scatter_matrix(vegetationDataframe,
                                   c = self._yTrain,
                                   figsize=(15,15),
                                   marker='o',
                                   hist_kwds={'bins': 20},
                                   s = 60,
                                   alpha=.8)
        plt.show()

    def classify(self):
        """
        Use logistic regression to classify objects in the image as desired on undesired
        :return:
        """
        # TODO: Raise an exception
        if self._model is None:
            return

        self.log.info("Classify by logistic regression")
        self._prepareData()

        # Make the predictions using the model trained
        predictions = self._model.predict(self._blobsInView)

        # Put the predictions into the blobs and mark the reason as logistic regression
        i = 0
        for blobName, blobAttributes in self._blobs.items():
            if blobAttributes[constants.NAME_REASON] != constants.REASON_AT_EDGE:
                blobAttributes[constants.NAME_TYPE] = predictions[i]
                blobAttributes[constants.NAME_REASON] = constants.REASON_LOGISTIC_REGRESSION
            i = i + 1
        return

class KNNClassifier(Classifier):
    name = ClassificationTechniques.KNN.name

    def __init__(self):
        super().__init__()

    def createModel(self, score: bool):

        # Try different values for neighbors - 5 produces poor results
        self._model = KNeighborsClassifier(n_neighbors=5, weights="distance", p=1)
        #model = forest.fit(train_fold, train_y.values.ravel())
        self._model.fit(self._xTrain, pd.DataFrame(self._yTrain).values.ravel())

        self._scores = cross_val_score(self._model, self._x, self._y)

        self._y_scores = self._model.predict_proba(self._xTest)
        self._fpr, self._tpr, self._threshold = roc_curve(self._yTest, self._y_scores[:, 1])
        self._auc = auc(self._fpr, self._tpr)

        if score:
            self.log.debug(f"KNN Cross validation scores: {self._scores}")
            yPred = self._model.predict(self._xTest)
            self.log.debug(f"K Neighbors prediction:\n{yPred}")

            self.log.debug("Training Score: {:.3f}".format(self._model.score(self._xTrain, self._yTrain)))
            self.log.debug("Testing Score: {:.2f}\n".format(self._model.score(self._xTest, self._yTest)))


    def classify(self):
        if self._model is None:
            return

        # Make a dataframe out of the current view
        self._prepareData()

        # Predict the types
        predictions = self._model.predict(self._blobsInView)

        # Mark up the current view
        i = 0
        for blobName, blobAttributes in self._blobs.items():
            if blobAttributes[constants.NAME_REASON] != constants.REASON_AT_EDGE:
                blobAttributes[constants.NAME_TYPE] = predictions[i]
                blobAttributes[constants.NAME_REASON] = constants.REASON_KNN
            i = i + 1

        return


class DecisionTree(Classifier):
    name = ClassificationTechniques.DECISIONTREE.name

    def __init__(self):
        super().__init__()


    def visualize(self):
        print("Feature Importance")
        print(self._classifier.feature_importances_)
        #return
        nFeatures = self._df.shape[1]
        plt.barh(np.arange(nFeatures),
                 self._classifier.feature_importances_,
                 align="center")
        #plt.yticks(np.arange(nFeatures))
        plt.show()

    def visualizeModel(self):
        plot_tree(self._model, filled=True, max_depth=2, rounded=True, precision=3, class_names=list(self._selections))
        plt.title("Decision tree trained on crop/weed features")
        plt.show()

    def createModel(self, score: bool):
        self._model = DecisionTreeClassifier(random_state=0)
        self._model.fit(self._xTrain, self._yTrain)

        self._scores = cross_val_score(self._model, self._x, self._y)

        self._y_scores = self._model.predict_proba(self._xTest)
        self._fpr, self._tpr, self._threshold = roc_curve(self._yTest, self._y_scores[:, 1])
        self._auc = auc(self._fpr, self._tpr)

        if score:
            self.log.debug(f"Decision Tree cross validation scores: {self._scores}")

            print("Training Score: {:.3f}".format(self._model.score(self._xTrain, self._yTrain)))
            print("Testing Score: {:.2f}\n".format(self._model.score(self._xTest, self._yTest)))
        return

    def classify(self):

        self._prepareData()

        predictions = self._model.predict(self._blobsInView)
                # Mark up the current view
        i = 0
        for blobName, blobAttributes in self._blobs.items():
            if blobAttributes[constants.NAME_REASON] != constants.REASON_AT_EDGE:
                blobAttributes[constants.NAME_TYPE] = predictions[i]
                blobAttributes[constants.NAME_REASON] = constants.REASON_DECISION_TREE
            i = i + 1
        return

class RandomForest(Classifier):
    name = ClassificationTechniques.RANDOMFOREST.name

    def __init__(self):
        super().__init__()

    def createModel(self, score: bool):
        #self._classifier = RandomForestClassifier(n_estimators=1000, max_features=1, random_state=2, n_jobs=-1)
        self._model = RandomForestClassifier(n_estimators=1000, max_features=1, random_state=2, n_jobs=-1)
        self._model.fit(self._xTrain, self._yTrain)

        self._scores = cross_val_score(self._model, self._x, self._y, n_jobs=-1)

        self._y_scores = self._model.predict_proba(self._xTest)
        self._fpr, self._tpr, self._threshold = roc_curve(self._yTest, self._y_scores[:, 1])
        self._auc = auc(self._fpr, self._tpr)

        if score:
            self.log.debug(f"Random Forest cross validation scores: {self._scores}")

            print("Training Score: {:.3f}".format(self._model.score(self._xTrain, self._yTrain)))
            print("Testing Score: {:.3f}".format(self._model.score(self._xTest, self._yTest)))
        return

    def classify(self):
        self._prepareData()

        predictions = self._model.predict(self._blobsInView)
                # Mark up the current view
        i = 0
        for blobName, blobAttributes in self._blobs.items():
            if blobAttributes[constants.NAME_REASON] != constants.REASON_AT_EDGE:
                blobAttributes[constants.NAME_TYPE] = predictions[i]
                blobAttributes[constants.NAME_REASON] = constants.REASON_RANDOM_FOREST
            i = i + 1
        return

class GradientBoosting(Classifier):
    name = ClassificationTechniques.GRADIENT.name

    def __init__(self):
        super().__init__()

    def createModel(self, score: bool):
        self._model = GradientBoostingClassifier(random_state=0, max_depth=4)
        self._model.fit(self._xTrain, self._yTrain)

        self._scores = cross_val_score(self._model, self._x, self._y)

        self._y_scores = self._model.predict_proba(self._xTest)
        self._fpr, self._tpr, self._threshold = roc_curve(self._yTest, self._y_scores[:, 1])
        self._auc = auc(self._fpr, self._tpr)

        if score:
            self.log.debug(f"Gradient Boosting cross validation scores: {self._scores}")

            print("Training Score: {:.3f}".format(self._model.score(self._xTrain, self._yTrain)))
            print("Testing Score: {:.3f}".format(self._model.score(self._xTest, self._yTest)))


    def classify(self):
        super().classify(constants.REASON_GRADIENT)
        return

class ExtraTrees(Classifier):
    name = ClassificationTechniques.EXTRA.name

    def __init__(self):
        super().__init__()

    def createModel(self, score: bool):
        #X, y = make_classification(n_samples=500, n_features=10, random_state=seed, n_informative=6, n_redundant=4)
        self._model = ExtraTreesClassifier(n_estimators=100, random_state=42)
        self._model.fit(self._xTrain, self._yTrain)
        # evaluate using cross-validation
        cv = KFold(n_splits=10, random_state=42, shuffle=True)
        self._scores = cross_val_score(self._model, self._xTrain, self._yTrain, scoring='accuracy', cv=cv, n_jobs=-1)

        self._y_scores = self._model.predict_proba(self._xTest)
        self._fpr, self._tpr, self._threshold = roc_curve(self._yTest, self._y_scores[:, 1])
        self._auc = auc(self._fpr, self._tpr)

        if score:
            self.log.debug(f"Extra trees cross validation scores: {np.mean(self._scores)}")
            self.log.debug("Training Score: {:.3f}".format(self._model.score(self._xTrain, self._yTrain)))
            self.log.debug("Testing Score: {:.3f}".format(self._model.score(self._xTest, self._yTest)))

    # def createModel(self, score: bool):
    #     self._model = GradientBoostingClassifier(random_state=0, max_depth=4)
    #     self._model.fit(self._xTrain, self._yTrain)
    #
    #     self._scores = cross_val_score(self._model, self._x, self._y)
    #
    #     self._y_scores = self._model.predict_proba(self._xTest)
    #     self._fpr, self._tpr, self._threshold = roc_curve(self._yTest, self._y_scores[:, 1])
    #     self._auc = auc(self._fpr, self._tpr)
    #
    #     if score:
    #         self.log.debug(f"Gradient Boosting cross validation scores: {self._scores}")
    #
    #         print("Training Score: {:.3f}".format(self._model.score(self._xTrain, self._yTrain)))
    #         print("Testing Score: {:.3f}".format(self._model.score(self._xTest, self._yTest)))


    # def classify(self):
    #     super().classify(constants.REASON_EXTRA)
    #     return

    def classify(self):

        self._prepareData()

        predictions = self._model.predict(self._blobsInView)
                # Mark up the current view
        i = 0
        for blobName, blobAttributes in self._blobs.items():
            if blobAttributes[constants.NAME_REASON] != constants.REASON_AT_EDGE:
                blobAttributes[constants.NAME_TYPE] = predictions[i]
                blobAttributes[constants.NAME_REASON] = constants.REASON_DECISION_TREE
            i = i + 1
        return



def classifierFactory(technique: str) -> Classifier:

    classifiers = {
        RandomForest.name.upper(): RandomForest,
        GradientBoosting.name.upper(): GradientBoosting,
        LDA.name.upper(): LDA,
        MLP.name.upper(): MLP,
        SuppportVectorMachineClassifier.name.upper(): SuppportVectorMachineClassifier,
        LogisticRegressionClassifier.name.upper(): LogisticRegressionClassifier,
        KNNClassifier.name.upper(): KNNClassifier,
        DecisionTree.name.upper(): DecisionTree,
        ExtraTrees.name.upper(): ExtraTrees
    }

    return classifiers[technique]()
