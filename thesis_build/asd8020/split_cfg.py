"""Settings of this hold-out pipeline (the 70:30 copy differs only in these lines)."""
TAG = '80-20'                      # used in output file names
LABEL = '80:20'                    # used in texts
TEST_FRAC = 0.20                   # target fraction of plots / leaves in the test set
SEED = 2026                        # fixed seed of the split search (reproducible)
FOLDS = [0]                        # one outer split: fold 0 = test plots, fold 1 = training plots
