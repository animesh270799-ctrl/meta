"""Settings of this hold-out pipeline (the 80:20 copy differs only in these lines)."""
TAG = '70-30'                      # used in output file names
LABEL = '70:30'                    # used in texts
TEST_FRAC = 0.30                   # target fraction of plots / leaves in the test set
SEED = 2026                        # fixed seed of the split search (reproducible)
FOLDS = [0]                        # one outer split: fold 0 = test plots, fold 1 = training plots
