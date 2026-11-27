# Question-answer content of the ML interview guide (no thesis results). Executed in m_build.py.

H1('A. Foundations of machine learning')
FIG('flow', 'd_mlflow.png', 'Machine-learning workflow without information leakage.', 450)
Q('What is machine learning, and why do you need it for white-rust detection?',
  'Machine learning builds a mapping from input features (spectra, indices, temperature, texture) to an output (disease grade or PDI) by learning from labelled examples rather than from explicit rules.',
  ['Disease changes the spectrum in many places at once (visible, red edge, NIR, SWIR, thermal), each weakly and partly redundantly; no single index captures all of it. Machine learning combines many weak, correlated signals into one decision and can represent non-linear relations, such as saturation of indices at high severity (Hastie et al., 2009; Behmann et al., 2015).',
   'Statistical models (ANOVA, discriminant analysis) describe which features respond; machine-learning models predict severity for new plots and new images, which is the operational goal.'],
  mine='Objective 1 uses statistics to understand the signal; Objectives 2 and 3 use machine learning to predict grades, PDI and pre-symptomatic infection.')
Q('What is the difference between supervised, unsupervised, semi-supervised and self-supervised learning?',
  'Supervised learning uses labelled examples; unsupervised learning finds structure without labels; semi-supervised learning combines a few labels with many unlabelled samples; self-supervised learning creates its own training signal from the data.',
  ['**Supervised:** classification (grades) and regression (PDI) with ground-truth labels.', '**Unsupervised:** clustering (k-means) and dimensionality reduction (PCA) to explore variability.',
   '**Semi-supervised:** useful when ground truth is expensive, for example labelling a few plots and propagating to similar unlabelled pixels.', '**Self-supervised:** pre-training deep networks on unlabelled images (for example predicting masked image patches), then fine-tuning with few labels.'],
  mine='Supervised learning for grades and PDI; unsupervised methods only for exploration.')
Q('Classification or regression for disease severity?',
  'Both. Grades (0, 1, 3, 5, 7, 9) are ordinal classes for management decisions; PDI is a continuous variable that keeps all severity information and avoids errors at class boundaries.',
  ['Treating ordered grades as unrelated classes ignores that confusing grade 3 with 5 is less serious than confusing 0 with 9; ordinal-aware metrics (adjacent-grade accuracy, weighted kappa) and PDI regression address this (Cohen, 1968).'],
  mine='Six-grade classification and PDI regression run in parallel.')
Q('Explain the bias–variance trade-off and overfitting.',
  'Expected prediction error = bias² + variance + irreducible noise. Simple models have high bias (underfitting); flexible models have high variance (overfitting): they fit noise in the training data and fail on new data.',
  ['Overfitting is detected as a gap between training and validation performance; it is controlled by fewer features, regularisation, simpler models, more data and early stopping (Hastie et al., 2009).'],
  eq='E[(y − ŷ)²] = Bias² + Variance + σ²', fig=('bv', 'd_biasvar.png', 'Underfitting, good fit and overfitting; training error keeps falling while test error rises.', 540),
  mine='A few hundred plot-dates versus hundreds of features makes overfitting the main risk; feature selection and nested validation control it.')
Q('What is regularisation? Explain L1 and L2.',
  'Regularisation adds a penalty on model complexity to the loss. L2 (ridge) shrinks all coefficients; L1 (LASSO) can set coefficients exactly to zero and therefore selects features.',
  ['Ridge: minimise Σ(y − Xβ)² + λΣβ² (Hoerl and Kennard, 1970); LASSO: minimise Σ(y − Xβ)² + λΣ|β| (Tibshirani, 1996); elastic net combines both. In neural networks, weight decay, dropout and early stopping play the same role (Srivastava et al., 2014).',
   'With highly correlated bands LASSO picks one band arbitrarily, which is why stable selection over repeated runs is important.'])
Q('What is the curse of dimensionality and the Hughes phenomenon?',
  'As the number of features grows, samples become sparse in feature space and distances lose meaning; with a fixed number of samples, classification accuracy first rises and then falls as features are added (Hughes, 1968).',
  ['Hyperspectral data have hundreds of highly correlated bands but field experiments have few samples; feature selection or extraction is therefore essential.'],
  mine='One band per correlated region, VIF, Boruta and ML-SFFS reduce hundreds of features to a compact set.')
Q('Parametric vs non-parametric, generative vs discriminative models?',
  'Parametric models assume a fixed functional form or distribution with a fixed number of parameters (linear regression, LDA); non-parametric models grow with the data (k-NN, random forest, kernel SVM). Generative models model how data are produced for each class (LDA, naive Bayes); discriminative models model the decision boundary directly (logistic regression, SVM).',
  ['Parametric models need fewer samples but fail if assumptions are wrong; non-parametric models are flexible but need more data and regularisation.'])
Q('What is the "no free lunch" theorem, and what does it mean for your model choice?',
  'No algorithm is best for every problem; performance depends on the data. Therefore several model families are compared on the same validation design instead of choosing one a priori.',
  mine='SVM, random forest, k-NN, PLSR and small DNNs are compared, each with its own optimum feature set.')

H1('B. Data preparation')
Q('How do you turn images and spectra into machine-learning features?',
  'By extracting physically meaningful variables per plot: band reflectance, first and second derivatives, red-edge parameters, vegetation and disease indices, texture (GLCM), colour and canopy temperature indices.',
  ['Plot-level features average out pixel noise and match the scale of ground truth.', 'Physically meaningful features make models interpretable and transferable to other sensors (Mahlein et al., 2013; Feng et al., 2022).'],
  mine='Tier 1 extracts the same feature families from each sensor after crop masking and flower removal.')
Q('Why and how do you scale features?',
  'Distance-, margin- and gradient-based models (k-NN, SVM, neural networks) are dominated by features with large numeric ranges unless features are standardised (z-score) or min–max scaled. Tree models do not need scaling.',
  ['Scaling parameters must be computed on training data only and then applied to test data; computing them on all data is a subtle form of leakage.'])
Q('How do you handle class imbalance?',
  'With class weights inversely proportional to class size, resampling (undersampling, SMOTE oversampling; Chawla et al., 2002), stratified folds, and balanced metrics (balanced accuracy, macro-F1).',
  ['Without these measures a model can predict the majority class and still show high overall accuracy while being useless for the rare, important class (severe disease).'],
  mine='Severity grades have unequal sizes; class weights and macro-F1 are used.')
Q('What is label noise, and how do you reduce it?',
  'Errors in ground-truth labels, for example visual scores that differ between observers or dates. Noise limits achievable accuracy and biases models.',
  ['Reduce it with a standard key (Conn et al., 1990), one trained scorer, same-day scoring, several sampling points per plot and explicit grade limits (Bock et al., 2010).', 'Models such as random forest are relatively robust to moderate label noise; evaluation must account for it.'])
Q('What is pseudo-replication, and why does it matter in your data?',
  'Treating correlated observations (leaves or pixels of the same plot) as independent samples. It inflates sample size, makes p-values optimistic and causes information leakage in validation.',
  ['Solutions: aggregate to plot level, use grouped cross-validation, and exclude same-plot neighbours in neighbourhood-based methods such as ReliefF.'],
  mine='Plots are the experimental units; leaves or pixels of one plot never appear in both training and test data.')
Q('What is spatial autocorrelation, and how does it affect validation?',
  'Nearby samples are more similar than distant ones. If neighbours are split between training and test sets, the test set is not independent and accuracy is overestimated (Roberts et al., 2017).',
  ['Use spatial or block cross-validation (leave out whole plots, blocks or replications).'])
Q('How would you use data augmentation?',
  'By creating modified copies of training samples (spectral noise, brightness scaling, image rotation and flipping) to make models robust and to enlarge small datasets, mainly for deep learning. Augmentations must respect physics: for example, brightness scaling simulates illumination change, but arbitrary band shifts are not realistic.')

H1('C. Feature selection and dimensionality reduction')
Q('What are filter, wrapper and embedded feature-selection methods?',
  'Filter methods score features independently of a model (correlation, ANOVA F, mutual information, ReliefF); wrapper methods search feature subsets using a model\'s validated performance (SFS, SFFS, recursive feature elimination); embedded methods select during training (LASSO, tree-based importance).',
  ['Filters are fast but ignore interactions; wrappers optimise for a specific model but are slower and can overfit; embedded methods are a compromise (Guyon et al., 2002).'],
  mine='Filters (scalogram, ReliefF) → all-relevant selection (Boruta) → collinearity removal (VIF) → wrapper (ML-SFFS).')
Q('Explain the correlation scalogram.',
  'For every band, Pearson\'s r between the band feature (reflectance, first or second derivative) and the continuous severity (PDI) is plotted against wavelength; bands with significant and high |r| are candidates (Shukla et al., 2024).',
  ['Advantages: no class limits needed, physically interpretable, shows which spectral regions respond.', 'Limitations: univariate and linear; correlated neighbours all appear significant, so one band per correlated region must be kept.'])
Q('Explain ReliefF in detail.',
  'ReliefF weights each feature by how well it separates a sample from its nearest neighbours of other classes compared with its nearest neighbours of the same class (Kononenko, 1994; Robnik-Šikonja and Kononenko, 2003).',
  ['For each sample, find k nearest hits (same class) and k nearest misses from each other class; increase a feature\'s weight if it differs from misses and decrease it if it differs from hits; misses are weighted by class prior.', 'It handles multi-class, noisy and overlapping classes and detects interacting features, unlike univariate tests.', 'Same-plot neighbours should be excluded to avoid pseudo-replication.'],
  eq='W_{f} ← W_{f} − Σ diff(f, x, H_{j}) / (mk) + Σ_{c≠class(x)} [P(c)/(1 − P(class(x)))] Σ diff(f, x, M_{j}(c)) / (mk)',
  mine='Classification side of band selection (six grades).')
Q('What is the variance inflation factor (VIF)?',
  'VIF_{j} = 1/(1 − R_{j}²), where R_{j}² is from regressing feature j on all others; it measures how much the variance of a coefficient is inflated by collinearity. Features are removed iteratively until all VIF < 10 (Dormann et al., 2013).',
  ['VIF is computed inside each training fold; it removes redundancy but not irrelevance.'])
Q('Explain the Boruta algorithm.',
  'Boruta adds shuffled copies of every feature ("shadow features"), trains a random forest, and confirms a feature only if its importance is significantly higher than the best shadow feature over repeated runs (Kursa and Rudnicki, 2010).',
  ['It is an all-relevant method: it keeps every feature that carries information, including weak and correlated ones, which makes it a good first filter before a minimal-set method.', 'Decisions: confirmed, tentative, rejected; p-value threshold and maximum runs are set by the user.'],
  mine='Applied separately for classification and regression to build disease-specific feature pools, as in Mustafa et al. (2023).')
Q('Explain sequential floating forward selection (SFFS).',
  'Starting from an empty set, the feature that most improves the model\'s cross-validated score is added; after each addition, earlier features are removed if that improves the score ("floating" step) (Pudil et al., 1994).',
  ['ML-SFFS uses the target model itself (SVM, random forest, k-NN) as the criterion, so each model receives its own optimum feature combination (Tian et al., 2021).', 'The smallest subset whose score is within a tolerance of the best is chosen, which reduces overfitting.'],
  fig=('sffs', 'm_sffs_lc.png', 'Forward selection and learning curve on simulated data.', 520))
Q('Explain principal component analysis and why you do not rely on it for band selection.',
  'PCA rotates correlated variables into uncorrelated components ordered by variance (Pearson, 1901). It is unsupervised: the first component often represents brightness or canopy structure rather than disease.',
  ['Components mix all bands, which makes physical interpretation and transfer to satellite bands difficult.', 'PCA is useful for data compression, noise reduction and exploration; supervised selection keeps original wavelengths related to disease.'],
  eq='Σv_{k} = λ_{k}v_{k};  variance explained = λ_{k}/Σλ', fig=('pca', 'm_pca.png', 'PCA on simulated spectra: PC1 follows brightness, PC2 follows severity.', 520))
Q('How do PLS components differ from principal components?',
  'PLS components maximise covariance between predictors and the response, so they are chosen to predict severity; principal components ignore the response (Wold et al., 2001).',
  mine='PLSR is used as a regression model and full-spectrum baseline.')
Q('Band selection or feature extraction?',
  'Band selection keeps original wavelengths (interpretable, transferable to sensors with few bands); feature extraction (PCA, MNF, PLS, autoencoders) creates new variables that mix bands. For sensor design and satellite transfer, selection is preferred.')
Q('How do you make feature selection stable?',
  'By repeating selection over resamples or folds and keeping features selected frequently (stability selection), because a single run on small data can pick different correlated features by chance.')

H1('D. Algorithms')
FIG('bound', 'm_boundaries.png', 'Decision boundaries of six classifiers on simulated data.', 540)
Q('Explain linear and logistic regression.',
  'Linear regression fits y = β₀ + Σβᵢxᵢ by least squares; logistic regression models the log-odds of a class as a linear function and outputs probabilities.',
  ['Linear models are interpretable but cannot represent non-linear relations and become unstable with collinear predictors.'],
  eq='β̂ = (XᵀX)^{−1}Xᵀy;   P(y = 1|x) = 1/(1 + e^{−(β₀ + βᵀx)})')
Q('Explain linear and canonical discriminant analysis.',
  'Fisher\'s discriminant finds linear combinations that maximise between-class relative to within-class variance (Fisher, 1936). CDA reports these canonical functions (canonical correlations, standardised coefficients, Wilks\' lambda); LDA uses them to classify, assuming Gaussian classes with equal covariance.',
  eq='maximise wᵀS_{B}w / wᵀS_{W}w;   Wilks Λ = |S_{W}|/|S_{T}|',
  mine='Two-step stepwise CDA following Bhattacharya and Chattopadhyay (2013) describes grade separability; LDA accuracy is a linear baseline.')
Q('What is quadratic discriminant analysis and naive Bayes?',
  'QDA allows a separate covariance matrix per class (curved boundaries) but needs many samples; naive Bayes assumes features are independent within a class and is very fast but unrealistic for correlated bands.')
Q('Explain k-nearest neighbours.',
  'A sample receives the majority class (or mean value) of its k nearest training samples in feature space (Cover and Hart, 1967).',
  ['Small k gives flexible, high-variance boundaries; large k gives smooth, high-bias boundaries; features must be scaled; irrelevant features degrade distances, so selection is important.'],
  mine='Included because it performed well for disease severity regression in Mustafa et al. (2023).')
Q('Explain decision trees.',
  'Recursive binary splits of the feature space; each split chooses the feature and threshold that most reduce impurity (Gini or entropy for classes, variance for regression) (Breiman et al., 1984; Quinlan, 1986).',
  eq='Gini = 1 − Σp_{k}²;   Entropy = −Σp_{k}log₂p_{k}', fig=('tree', 'm_tree.png', 'Decision tree on simulated data.', 540))
Q('Explain random forest in detail.',
  'An ensemble of decision trees, each grown on a bootstrap sample with a random subset of features considered at each split; predictions are averaged (regression) or voted (classification) (Breiman, 2001).',
  ['**Why it works:** averaging many decorrelated trees reduces variance without increasing bias.', '**Out-of-bag error:** each tree leaves out about one third of samples, giving an internal validation estimate.',
   '**Importance:** mean decrease in impurity (biased toward many-valued features) or permutation importance (more reliable).', '**Hyperparameters:** number of trees, features per split (mtry), minimum leaf size, maximum depth.', '**Limitations:** less interpretable than one tree; regression cannot extrapolate beyond the training range.'],
  fig=('rf', 'm_rf.png', 'Random forest: bootstrap samples, decorrelated trees, voting.', 520), mine='Classifier and regressor in Objective 2 and the base learner of Boruta; widely used in remote sensing (Belgiu and Drăguţ, 2016).')
Q('What is gradient boosting, and how does it differ from random forest?',
  'Boosting adds trees sequentially, each fitting the residual errors (gradient of the loss) of the current ensemble (Friedman, 2001); XGBoost and LightGBM add regularisation and efficiency (Chen and Guestrin, 2016; Ke et al., 2017). Random forest (bagging) builds trees independently to reduce variance; boosting reduces bias.',
  ['Boosting is often more accurate on large tabular data but has more hyperparameters (learning rate, depth, number of trees) and overfits small datasets more easily.'])
Q('Explain support vector machines and support vector regression.',
  'SVM finds the separating hyperplane with the maximum margin between classes; training points on the margin are support vectors; slack variables with penalty C allow misclassification; kernels map data into higher dimensions for non-linear boundaries (Cortes and Vapnik, 1995). SVR fits a function within an ε-insensitive tube.',
  ['**C:** large C fits training data closely (narrow margin, risk of overfitting); small C allows more errors (wider margin).', '**γ (RBF kernel):** large γ makes each point\'s influence local (wiggly boundary); small γ makes it smooth.',
   '**Strengths:** works well with few samples and many features (Mountrakis et al., 2011); used for early disease detection (Rumpf et al., 2010).', '**Limitations:** needs scaling and tuning; no direct probabilities; slow for very large datasets.'],
  eq='min ½‖w‖² + CΣξ_{i}  s.t.  y_{i}(wᵀφ(x_{i}) + b) ≥ 1 − ξ_{i};   K(x, x\') = exp(−γ‖x − x\'‖²)', fig=('svm', 'm_svm.png', 'Maximum-margin linear SVM and RBF-kernel SVM.', 500))
Q('What is the kernel trick?',
  'Many algorithms depend only on inner products between samples; replacing the inner product by a kernel function computes it in a high-dimensional feature space without explicitly mapping the data, allowing non-linear boundaries at linear cost.')
Q('Explain partial least squares regression and PLS-DA.',
  'PLSR projects predictors and response onto a few latent components that maximise their covariance and regresses on these components; it handles many collinear predictors (Wold et al., 2001). PLS-DA applies the same idea to class indicator variables.',
  ['The number of components is chosen by cross-validated RMSE; loadings and VIP scores show influential wavelengths.'],
  mine='Regression model and full-spectrum baseline, standard for spectra (Shukla et al., 2024; Guo et al., 2021).')
Q('What is Gaussian process regression?',
  'A Bayesian non-parametric method that places a prior over functions defined by a kernel and returns predictions with uncertainty intervals (Rasmussen and Williams, 2006); powerful for small datasets but computationally heavy for large ones.')
Q('Explain artificial neural networks and back-propagation.',
  'A multilayer perceptron consists of layers of neurons computing weighted sums followed by non-linear activation functions; weights are learned by minimising a loss with gradient descent, the gradients being computed layer by layer by back-propagation (Rumelhart et al., 1986).',
  ['**Activation:** ReLU (avoids vanishing gradients), sigmoid, softmax (class probabilities).', '**Loss:** cross-entropy for classes, mean squared error for regression.', '**Optimisers:** stochastic gradient descent, Adam (Kingma and Ba, 2015).',
   '**Regularisation:** dropout (Srivastava et al., 2014), batch normalisation (Ioffe and Szegedy, 2015), weight decay, early stopping.', '**Terms:** epoch = one pass over the training data; batch = samples per gradient update; learning rate = step size.'],
  eq='h = σ(Wx + b);   w ← w − η ∂L/∂w', fig=('nn', 'd_nn.png', 'Multilayer perceptron and convolutional neural network.', 540))
Q('Explain convolutional neural networks and their use for hyperspectral and UAV data.',
  'CNNs learn local filters by convolution, share weights across positions, reduce size by pooling and classify with dense layers (LeCun et al., 2015). 1-D CNNs process spectra, 2-D CNNs process images, 3-D CNNs process hyperspectral cubes jointly in space and spectrum (Paoletti et al., 2019); U-Net performs pixel-wise segmentation (Ronneberger et al., 2015); residual connections allow very deep networks (He et al., 2016).',
  ['CNNs learn features automatically but need thousands of labelled samples, are hard to interpret and may not transfer from laboratory to field (Mohanty et al., 2016; Kamilaris and Prenafeta-Boldú, 2018).'],
  mine='Not the main model because plot-level labels are few; small dense networks (DNN-F1, DNN-F2) are tested against classical models.')
Q('What are recurrent networks, LSTM and transformers?',
  'Recurrent networks process sequences; LSTM uses gates to keep long-term memory and avoid vanishing gradients (Hochreiter and Schmidhuber, 1997); transformers use self-attention to weigh all positions of a sequence or all patches of an image (Vaswani et al., 2017; Dosovitskiy et al., 2021).',
  ['In remote sensing they model satellite time series for crop mapping and could model weather sequences for disease forecasting.'])
Q('What are autoencoders, transfer learning and self-supervised learning?',
  'Autoencoders compress data into a low-dimensional code and reconstruct it (Hinton and Salakhutdinov, 2006); transfer learning reuses a model trained on a large dataset and fine-tunes it on a small one (Pan and Yang, 2010); self-supervised learning pre-trains on unlabelled data.',
  ['These approaches reduce the need for labelled disease data, which is the main bottleneck in field studies.'])
Q('What are ensembles and stacking?',
  'Combining several models improves robustness: bagging (random forest), boosting, voting and stacking, in which a meta-model learns how to combine base-model predictions (Wolpert, 1992). Extremely randomised trees add further randomness to splits (Geurts et al., 2006).')
Q('Which clustering and anomaly-detection methods would you use?',
  'k-means (MacQueen, 1967), hierarchical clustering and DBSCAN (Ester et al., 1996) for grouping; isolation forest (Liu et al., 2008) and one-class SVM (Schölkopf et al., 2001) for anomaly detection, which can be trained on healthy plots only.',
  mine='Anomaly detection is an option for pre-symptomatic detection, where infected examples are scarce and uncertain.')
Q('What is active learning, and why is it relevant for ground truth?',
  'The model selects the most informative unlabelled samples (for example those with the most uncertain predictions) for labelling, so fewer field visits achieve the same accuracy (Settles, 2009).')

H1('E. Multi-sensor fusion')
Q('What are the levels of data fusion?',
  'Pixel or data level (combine raw images, for example pansharpening), feature level (concatenate features from several sensors into one model), intermediate level (learn sensor-specific representations and join them inside a network), and decision level (combine predictions of single-sensor models by voting, averaging or stacking).',
  fig=('fusion', 'm_fusion.png', 'Early, intermediate and late fusion.', 520))
Q('Explain DNN-F1 and DNN-F2.',
  'DNN-F1 concatenates all sensor features at the input of one network (early fusion); DNN-F2 gives each sensor its own sub-network and joins their hidden representations at an intermediate layer (intermediate fusion), which can learn sensor-specific patterns first (Maimaitijiang et al., 2020).',
  mine='Both are kept very small because of the limited number of plot-dates and compared with feature-level fusion using ML-SFFS.')
Q('How do you fuse sensors with different spatial resolutions?',
  'By extracting features at a common unit (the plot or object), by resampling to a common grid with appropriate methods (nearest neighbour for masks, averaging for reflectance), or by multi-branch networks that accept inputs of different sizes.',
  mine='All features are extracted per plot after co-registration and crop masking, so resolution differences do not matter for fusion.')
Q('How do you know whether fusion really helps?',
  'By comparing fused models with the best single sensor under the same validation design and testing whether the improvement exceeds the variation between folds (Dietterich, 1998). A third sensor does not always add information (Mahlein et al., 2019).')

H1('F. Training, tuning and validation')
Q('What is the difference between parameters and hyperparameters?',
  'Parameters are learned from data (weights, split thresholds); hyperparameters are set before training and control learning (C and γ in SVM, number of trees, k, learning rate) and are chosen by validation.')
Q('How do you tune hyperparameters?',
  'Grid search, random search (Bergstra and Bengio, 2012) or Bayesian optimisation (Snoek et al., 2012), always with cross-validation inside the training data.',
  mine='Grid search with grouped inner cross-validation for each model and fold.')
Q('Explain the types of cross-validation.',
  'k-fold (random), stratified k-fold (preserves class proportions), grouped k-fold (keeps groups together), leave-one-group-out, spatial block and temporal cross-validation (Kohavi, 1995; Roberts et al., 2017).',
  fig=('cv', 'd_cv.png', 'Random, grouped and leave-one-replication-out cross-validation.', 470))
Q('What is nested cross-validation, and why is it necessary?',
  'An outer loop estimates performance on held-out data; an inner loop, inside each outer training set, performs feature selection and hyperparameter tuning. Without nesting, selection and tuning see the test data and accuracy is biased upward (Varma and Simon, 2006; Ambroise and McLachlan, 2002).',
  fig=('nested', 'm_nested.png', 'Nested leave-one-replication-out validation.', 520), mine='Leave-one-replication-out outer loop; Tier 2 band selection, Boruta, VIF, ML-SFFS and tuning inside each training set.')
Q('What is information leakage? Give examples.',
  'Any use of information from the test data before testing. Examples: scaling or selecting features on all data, tuning on the test set, leaves of the same plot in training and test, neighbouring pixels in both sets, or using future information (later-date labels) as a feature.')
Q('What is a learning curve, and what does it tell you?',
  'Training and validation scores plotted against training-set size. A large gap indicates variance (overfitting); low and converging curves indicate bias (underfitting); a plateau indicates that more data of the same kind will not help much.',
  mine='Used to judge whether more plots or more dates would improve the models.')
Q('What is early stopping?',
  'Training of iterative models (neural networks, boosting) stops when the validation loss stops improving, preventing overfitting.')
Q('How do you ensure reproducibility?',
  'Fixed random seeds, documented software versions, a scripted pipeline from raw data to results, saved fold assignments and hyperparameters, and repeated runs to show variability.')

H1('G. Evaluation metrics')
FIG('eval', 'm_eval.png', 'Confusion matrix, ROC and precision–recall curves and permutation importance on simulated data.', 540)
Q('Explain the confusion matrix and the metrics derived from it.',
  'Rows are observed classes, columns predicted classes. Overall accuracy = correct / total; precision (user\'s accuracy) = TP/(TP + FP); recall (producer\'s accuracy, sensitivity) = TP/(TP + FN); specificity = TN/(TN + FP); F1 = harmonic mean of precision and recall (Sokolova and Lapalme, 2009; Congalton, 1991).',
  eq='F1 = 2PR/(P + R);   balanced accuracy = (sensitivity + specificity)/2')
Q('Macro, micro and weighted F1: which do you use and why?',
  'Macro-F1 averages per-class F1 equally (each grade counts the same), micro-F1 pools all decisions (equals accuracy in single-label problems), weighted F1 weights by class size. Macro-F1 is preferred with unequal grades so that rare severe grades are not ignored.')
Q('What is Cohen\'s kappa, and what are its limitations?',
  'Kappa = (p_{o} − p_{e})/(1 − p_{e}) measures agreement beyond chance (Cohen, 1960). It depends on class prevalence and has been criticised as redundant with overall accuracy (Pontius and Millones, 2011); report it with per-class metrics. Weighted kappa penalises distant ordinal errors more (Cohen, 1968).')
Q('What is the Matthews correlation coefficient?',
  'A correlation between observed and predicted classes that uses all four cells of the binary confusion matrix and remains informative under class imbalance (Chicco and Jurman, 2020).')
Q('Explain ROC and precision–recall curves.',
  'The ROC curve plots sensitivity against 1 − specificity across thresholds; the area under it (AUC) is the probability that a random positive is ranked above a random negative (Fawcett, 2006). The precision–recall curve is more informative when positives are rare (Saito and Rehmsmeier, 2015).',
  mine='Used for the binary pre-symptomatic task, where the threshold sets the trade-off between missed infections and false alarms.')
Q('How do you evaluate ordinal grades?',
  'With exact accuracy and macro-F1, plus adjacent-grade (±1) accuracy, weighted kappa and mean absolute error in grade steps, which credit predictions close to the true grade.')
Q('Which regression metrics do you use?',
  'R² (explained variance), RMSE, MAE, NRMSE (RMSE/mean), bias (mean error) and RPD (SD of observations / RMSE; Chang et al., 2001).',
  eq='R² = 1 − Σ(y − ŷ)²/Σ(y − ȳ)²;   RMSE = √[Σ(y − ŷ)²/n];   RPD = SD_{y}/RMSE',
  fig=('reg', 'm_reg.png', 'Observed versus predicted values and residuals on simulated data.', 470))
Q('Can R² be negative?',
  'Yes, on test data, when predictions are worse than simply predicting the mean of the observations, for example when the observed range on a date is very narrow.')
Q('How do you compare two models statistically?',
  'McNemar\'s test on paired predictions of the same samples, or repeated cross-validation with an appropriate paired test (Dietterich, 1998); bootstrap confidence intervals for metrics.')
Q('How is map accuracy different from model accuracy?',
  'Model accuracy is measured on validation samples; map accuracy requires a probability sample of the mapped area and, for area estimates, error-adjusted estimators with confidence intervals (Olofsson et al., 2014).')

H1('H. Interpretation and uncertainty')
Q('How do you interpret machine-learning models?',
  'Global importance (impurity or permutation importance), local explanations (SHAP values; Lundberg and Lee, 2017), partial dependence plots, and for CNNs class-activation maps such as Grad-CAM (Selvaraju et al., 2017). The selected features must also make physiological sense.',
  mine='Compact, physically meaningful feature sets make interpretation direct: each feature is linked to pigment, structure, water or transpiration.')
Q('Why is permutation importance preferred over impurity importance?',
  'Impurity importance is biased toward continuous or many-valued features and is computed on training data; permutation importance measures the drop in validation performance when a feature is shuffled.')
Q('How do you estimate the uncertainty of predictions?',
  'Quantile regression forests (Meinshausen, 2006), ensembles, Monte Carlo dropout in neural networks (Gal and Ghahramani, 2016), Gaussian processes or bootstrapping; class probabilities should be calibrated (Niculescu-Mizil and Caruana, 2005).',
  mine='Uncertainty maps accompany severity maps so that users know where predictions are reliable.')

H1('I. Machine learning in my study and at satellite scale')
Q('Why did you choose a tiered feature pipeline plus classical models instead of end-to-end deep learning?',
  'Because a field experiment provides a limited number of labelled plot-dates, while deep networks need thousands of labelled images. The tiered pipeline extracts interpretable features, removes redundancy and gives each model a compact feature set; small DNNs are still tested to see whether learned fusion adds value.')
Q('Describe your complete ML pipeline step by step.',
  'Features (Tier 1) → band lists from correlation scalogram and ReliefF (Tier 2) → Boruta pools (Tier 6) → VIF < 10 → ML-SFFS per model → hyperparameter tuning → prediction of the held-out replication → metrics; repeated for each outer fold and each sensor set.')
Q('How do you prevent your model from learning variety or date instead of disease?',
  'Controls of the same varieties are measured on the same dates; variety and date are checked as factors; performance is reported per variety and per date; and features with physiological meaning are preferred over arbitrary ones.')
Q('How would you transfer your models to satellite data?',
  'Simulate satellite bands from hyperspectral spectra with the spectral response functions, retrain models on simulated bands, then train or fine-tune on satellite pixels labelled with aggregated UAV severity, and validate on independent ground data.',
  ['The difference between training and application conditions (domain shift) is handled by domain adaptation, for example recalibrating with a few local samples (Tuia et al., 2016).'])
Q('What is domain shift, and how do you handle it across seasons, sites and sensors?',
  'Domain shift is a change in data distribution between training and application (new season, site, sensor, illumination). It is detected by monitoring performance on new ground truth and handled by recalibration with a few local samples, domain adaptation, multi-season training and physically normalised features (Tuia et al., 2016).')
Q('How would you deploy the model operationally?',
  'As a scripted pipeline on a cloud platform (for example Google Earth Engine or ISRO\'s VEDAS) that ingests new images, applies the crop mask and models, writes maps with uncertainty, and is retrained each season with new ground truth; performance is tracked over time.')
Q('How would you choose ground-truth locations for a national model?',
  'Stratified random sampling across agro-climatic zones, varieties and severity levels, supplemented by active learning to target uncertain areas (Settles, 2009); UAV sentinel sites provide dense labels.')
Q('How would you explain your model to farmers or policy makers?',
  'The model learns from many examples how healthy and diseased mustard look to the sensors and recognises the same patterns in new fields; maps show where disease is likely and how severe it is, with confidence levels.')

H1('J. Rapid-fire questions')
for q, a in [
 ('What is an epoch, a batch and a learning rate?', 'Epoch: one pass over all training data; batch: samples per gradient update; learning rate: the size of each update step.'),
 ('Why ReLU?', 'It is cheap and avoids the vanishing gradients of sigmoid and tanh in deep networks.'),
 ('What is dropout?', 'Randomly switching off neurons during training so the network cannot rely on single units, which reduces overfitting (Srivastava et al., 2014).'),
 ('What is batch normalisation?', 'Normalising layer inputs within each mini-batch to stabilise and speed up training (Ioffe and Szegedy, 2015).'),
 ('What is the out-of-bag error?', 'Random-forest error estimated on the samples each tree did not see in its bootstrap sample.'),
 ('Why is accuracy misleading with imbalanced classes?', 'Predicting only the majority class gives high accuracy but no skill; use balanced accuracy or macro-F1.'),
 ('Bagging vs boosting?', 'Bagging trains models independently to reduce variance; boosting trains them sequentially to reduce bias.'),
 ('L1 vs L2?', 'L1 produces sparse coefficients (feature selection); L2 shrinks all coefficients smoothly.'),
 ('What does a high VIF mean?', 'The feature is largely explained by other features (collinearity), making coefficients unstable.'),
 ('What is stratified sampling?', 'Sampling that keeps class proportions in every subset or stratum.'),
 ('What is a hyperplane?', 'A flat decision surface of dimension one less than the feature space.'),
 ('What is a support vector?', 'A training sample on or inside the margin that defines the SVM boundary.'),
 ('What is overfitting in one sentence?', 'Learning noise in the training data so that performance on new data drops.'),
 ('What is the difference between validation and test sets?', 'Validation data are used for model selection and tuning; test data are used once for the final unbiased estimate.')]:
    Qd(q, a)

H1('K. Tough questions')
for q, a in [
 ('Your sample size is small compared with the number of features. How can your model be trusted?', 'Feature selection reduces dimensionality to a few physically meaningful features, models are compact, every selection step is nested inside training folds, whole replications are held out, and the result is checked at an independent site; learning curves show whether more data are needed.'),
 ('Why random forest and not XGBoost?', 'Random forest is robust with few samples and few hyperparameters; boosting is often stronger on large datasets but overfits small ones more easily. Both can be compared under the same nested design; the choice is empirical (no free lunch).'),
 ('Why not use all bands with PLSR?', 'PLSR with all bands is a valid baseline and is included; selected-feature models are more interpretable and transferable to sensors with few bands.'),
 ('If deep learning is state of the art, why not use it?', 'State of the art on large labelled image datasets; with a limited number of field labels, compact models on interpretable features generalise better. Small DNNs are included for comparison, and CNNs are an option when pixel-level labels accumulate.'),
 ('How do you know your accuracy is not inflated?', 'No sample of a test replication is used in scaling, selection or tuning; leaves and pixels of a plot stay together; independent-site validation measures transferability.'),
 ('What will you do if the model fails on satellite data?', 'Diagnose whether the cause is spectral (bands too broad), spatial (mixed pixels) or domain shift; then use transferable features, sub-pixel training with UAV maps and local recalibration.')]:
    Qd(q, a)
