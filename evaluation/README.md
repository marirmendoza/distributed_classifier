# Evaluation
This application is responsible for evaluating several aggregation methods performance.  

## Command Line Usage
```bash
usage: main.py [-h] -d DATASET_PATH [-p PARAMS_FOLDER]

optional arguments:
  -h, --help            show this help message and exit
  -d DATASET_PATH, --dataset DATASET_PATH
                        Dataset's absolute/relative path.
  -p PARAMS_FOLDER, --params PARAMS_FOLDER
                        Folder where a file params.json is.
  -o OVERLAP, --overlap OVERLAP
                        % of overlaped features, value between 0.0 and 1.0.
```

## Params file
A JSON file as follow:
```javascript
{
    // Class' column in dataset (default -1)
    // -1 for last column, 0 for first column
    "class_column": -1,

    // Number of cross-validation iterations (default 10)
    "iterations": 10,

    // Random state to secure same randomness in different runs (seed)
    "random_state": 1,

    // Overlaped features
    // If float, should be between 0.0 and 1.0 and represents the percentage
    // of parts' common features. If int, should be less than or equal to the
    // number of features and represents the number of common features. If list,
    // represents the features' columns indexes. By default, the value is set to 0.
    "overlap": 0,

    // Classifiers
    // {<classifier id>: <full method call, i.e., with parameters>}
    "classifiers": {
        "nb": "sklearn.naive_bayes.GaussianNB()",
        "svc": "sklearn.svm.SVC(probability=True)",
        "dtree": "sklearn.tree.DecisionTreeClassifier()",
        "knn": "sklearn.neighbors.KNeighborsClassifier()"
    },

    // Scorer functions
    // {<scorer id>: <method call with parameters>}
    "metrics": {
        "auc": "sklearn.metrics.roc_auc_score()",
        "f1": "sklearn.metrics.f1_score(average='binary')",
        "recall": "sklearn.metrics.recall_score(labels=['Positive', 'Negative'])",
        "specificity": "src.metrics.specificity_score(labels=['Positive', 'Negative'])",
        "sensitivity": "src.metrics.sensitivity_score(labels=['Positive', 'Negative'])",
        "accuracy": "sklearn.metrics.accuracy_score()",
        "precision": "sklearn.metrics.precision_score()"
    },

    //
    // Aggregators
    //

    // For rank aggregation by voting...
    // {<scf's label>: <method's callable label>}
    // See available methods in
    // https://github.com/btrevizan/pyscf#methods
    "voter": {
        "borda": "borda",
        "copeland": "copeland",
        "plurality":  "plurality"
    },

    // For rank aggregation by combination...
    // {<combiner's label>: <full method call, i.e., with parameters>}
    "combiner": {
        "cmb_nb": "sklearn.naive_bayes.GaussianNB()",
        "cmb_svc": "sklearn.svm.SVC(probability=True)"
    },

    // For rank aggregation by arbiter choice...
    "arbiter": {
        "classes": ["ArbiterMetaDiff", "ArbiterMetaDiffInc", "ArbiterMetaDiffIncCorr"],
        "methods": {
            "gnb": "sklearn.naive_bayes.GaussianNB()",
            "svc": "sklearn.svm.SVC(probability=True)",
            "mlp": "sklearn.neural_network.MLPClassifier()",
            "dtree": "sklearn.tree.DecisionTreeClassifier()",
            "knn": "sklearn.neighbors.KNeighborsClassifier()"
        }
    },

    // For rank aggregation by math operations...
    // {<max/min>: <list of math operations from numpy>}
    // max: get the maximum value in mean and median
    // min: get the minimum value in std
    "mathematician": {
        "max": ["mean", "median"],
        "min": ["std"]
    }
}
```

## Example
To use a default parameters set, i.e., `binary.json` or `multiclass.json`, just:
```bash
python3 main.py -d datasets/cancer_last.csv
```
The program will save the **results** in `tests/cancer_last_<i>` folder.

If you want to change the test's parameters, just set a params.json path.
```bash
python3 main.py -d datasets/cancer_last.csv -p tests/cancer/params.json
```

## Results
Result files saved in *test folder*. You can find examples in `tests` folder.
- **cv_scores_\<aggr\>.csv**: scores for each Cross-Validation's iteration for a aggregator
- **cv_scores_\<classifier\>.csv**: scores for each Cross-Validation's iteration for a classifier
- **cv_summary.csv**: average scores from all *cv_scores_\<classifier\>.csv*

## Sample Datasets
This project uses a set of data samples for testing. This datasets are in `datasets/` folder.
