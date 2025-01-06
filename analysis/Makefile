#
# P O S T  M A K E F I L E
#

default:
	@echo Choose: application, data-for-imbalance, imbalance

application: review_ui.py

review_ui.py: review.ui
	pyuic5 review.ui -o review_ui.py -x


clean:
	rm -f *.log
	rm -f imbalance.csv

PYTHON=python

#
# I M B A L A N C E
#
# Imbalance analysis takes multiple steps
# 1) Copy the files to be analyzed
# 2) Classify the vegetation automatically
# 3) Correct the classifications manually
# 4) Analyze for imbalance
#

# Assemble the raw data used for imbalance
IMBALANCED?=/cygdrive/d/maricopa-test/imbalance

data-for-imbalance:
	@echo Creating image set for imbalance in $(IMBALANCED)
	cp /cygdrive/d/maricopa/corrected/2024-04-24/iphone-drip/*jpg $(IMBALANCED)
	cp /cygdrive/d/maricopa/corrected/2024-04-24/iphone-flood/*jpg $(IMBALANCED)
	cp /cygdrive/d/maricopa/corrected/2024-04-24/iphone-pivot/*jpg $(IMBALANCED)
	cp /cygdrive/d/maricopa/corrected/2024-05-01/drip-iphone/*jpg $(IMBALANCED)
	cp /cygdrive/d/maricopa/corrected/2024-05-01/pivot-iphone/*jpg $(IMBALANCED)

# The default generated classification file
CLASSIFICATION?=classification.csv
# The default corrected classification file
CORRECTED?=corrected.csv

# Make an initial pass at classifying the set so then we can go through things manually
classify-for-imbalance:
	mkdir -p $(IMBALANCED)/processed
	$(eval _INPUT = `cygpath -w $(IMBALANCED)`)
	$(eval _OUTPUT = `cygpath -w $(IMBALANCED)/processed`)
	#cd ../jetson; $(PYTHON) weeds.py -i $(INPUT) -o $(OUTPUT) -a $(INDEX) -df $(TRAINING) $(ALGFLAG) -sc -op $(OPERATION) -lg $(LOG) -d $(DECORATIONS) $(CONTOURS) -ini $(INI) $(STANDALONE) -db -alt $(ALTITUDE) -cr $(CROP) $(CORRECTIONFLAGS) -t $(THRESHOLD) -c
	#cd ../jetson; make weeds-to-db INPUT=$(IMBALANCED) OUTPUT=$(IMBALANCED)/processed
	cd ../jetson; make weeds-no-db INPUT=$(_INPUT) OUTPUT=$(_OUTPUT) THRESHOLD=TRIANGLE AREA=1200 INDEX=com2 DECORATIONS=name TRAINING=maricopa.csv SESSION=final

# The human part
# INPUT is processed images
# OUTPUT is CSV where the corrections are stored
# CLASSIFICATION is the output from the automatic classification

review-for-imbalance:
	test -n "$(INPUT)"
	test -n "$(OUTPUT)"
	test -n "$(CLASSIFICATION)"
	$(eval _INPUT = `cygpath -w $(INPUT)`)
	$(eval _OUTPUT = `cygpath -w $(OUTPUT)`)
	$(eval _CLASSIFICATION = `cygpath -w $(CLASSIFICATION)`)
	python review.py -i $(_INPUT) -o $(_OUTPUT) -a $(_CLASSIFICATION) -p processed-*.jpg -l logging.ini


# All imbalance techniques
# INPUT should be the corrected CSV specified as the OUTPUT in the review-for-imbalance rule
# OUTPUT is the csv where the results are stored
# RATIO is the target ratio, i.e., 30:5-10
# STEPS is the number of steps to use, i.e., 6
# IMBALANCE is the correction technique, or ALL-COMBINED or ALL-OVER
#
# Run this twice to get all the combined and oversampling techniques -- each time it produces imbalance.csv
# Which the R script consumes

analyze-imbalance:
	test -n "$(RATIO)"
	test -n "$(STEPS)"
	test -n "$(IMBALANCE)"
	$(eval _INPUT = `cygpath -w $(INPUT)`)
	$(eval _OUTPUT = `cygpath -w $(OUTPUT)`)
	# Originally
	# python ./imbalance.py -df ../jetson/training-from-dataframe.csv -ini ../jetson/standalone.ini -lg ../jetson/standalone-logging.ini -a ALL --classifier ALL
	python ./imbalance.py -df $(_INPUT) -ini ../jetson/standalone.ini -lg ../jetson/standalone-logging.ini -a $(IMBALANCE) --classifier ALL -o $(_OUTPUT) -ir $(RATIO)
