# Utilities
from src.data import Data
from pandas import DataFrame
from sklearn.externals import joblib
from src.simulator import FeatureDistributed

# Classifiers
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

# Metrics
from sklearn.metrics import roc_auc_score, f1_score, precision_score
from sklearn.metrics import make_scorer, recall_score, accuracy_score
from src.metrics import summary, specificity_score, sensitivity_score

###############################################################################
# Settings
###############################################################################
k_fold = 10
overlap = 0
test_size = 0.3
iterations = 10
class_column = -1
results = 'tests/example/'
dataset = 'datasets/seed.csv'

classifiers = {
    'gaussian_nb': GaussianNB(),
    'svc': SVC(probability=True),
    'dtree': DecisionTreeClassifier(),
    'knn': KNeighborsClassifier()
}

scorers = {
    'auc': make_scorer(roc_auc_score),
    'f1': make_scorer(f1_score, average='binary'),
    'recall': make_scorer(recall_score),
    'specificity': make_scorer(specificity_score, labels=['Target', 'Non-Target']),
    'sensitivity': make_scorer(specificity_score, labels=['Target', 'Non-Target']),
    'accuracy': make_scorer(accuracy_score),
    'precision': make_scorer(precision_score)
}

social_functions = ['borda', 'copeland', 'dowdall', 'plurality']

###############################################################################
# Application
###############################################################################
# Load data
data = Data.load(dataset, class_column)

# Simulate distribution
classif_call = list(classifiers.values())
simulator = FeatureDistributed.load(data, classif_call, overlap, test_size)

# Run Cross-Validation
ranks, scores = simulator.cross_validate(social_functions, k_fold, scorers, iterations)

# Run tests
simulator.fit()
test_ranks, test_scores = simulator.predict(social_functions, scorers)

# Here, we had evaluated the model with social choice functions, but you can
# use the simulator model to predict using your own testset, like:
#
# test_ranks, test_scores = simulator.predict(['borda'], scorers, testset)
#

###############################################################################
# Save results
###############################################################################
# Save CV scores
n = len(social_functions)
[scores[i].to_csv('{}/cv_scores_{}.csv'.format(results, social_functions[i])) for i in range(n)]

# Save rankings
[DataFrame(ranks[scf]).to_csv('{}/cv_ranks_{}.csv'.format(results, scf))
    for scf in ranks]

# Save test scores
test_ranks, test_scores = DataFrame(test_ranks).T, DataFrame(test_scores).T

test_ranks.to_csv('{}/test_ranks.csv'.format(results))
test_scores.to_csv('{}/test_scores.csv'.format(results))

# Save models
names = list(classifiers.keys())
n = len(names)

for i in range(n):
    learner = simulator.learners[i]
    joblib.dump(learner.classifier, '{}/model_{}.pkl'.format(results, names[i]))

# Create CV summary
stats = summary(scores)             # create summary
stats.index = social_functions      # line names as social choice functions' names
stats.to_csv('{}/cv_summary.csv'.format(results))
