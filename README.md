The imbalance correction and analysis is provided by the impbalance.py script.

This project is built using the cygwin subsystem installed on a windows 10 system.

Use it like so:

make analyze-imbalance INPUT=/cygdrive/d/maricopa-test/imbalance/processed/final/corrected.csv OUTPUT=imbalance.csv RATIO=30:5-10 STEPS=6 IMBALANCE=ALL-OVER

The references to specific locations will vary, of course.

Some supporting make targets

Assemble the data
make data-for-imbalance

Manually classify everything
make review-for-imbalance INPUT=/cygdrive/d/maricopa-test/imbalance/processed/final/ OUTPUT=/cygdrive/d/maricopa-test/imbalance/processed/final/corrected.csv CLASSIFICATION=/cygdrive/d/maricopa-test/imbalance/processed/final/results_dataframe.csv

