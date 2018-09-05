import argparse

from src.graphics import Boxplot, NewickTree
from src.regression import RegressionAnalysis
from src.classification import ClassificationAnalysis


def main(args):
    regression = 'regression'
    classification = 'classification'

    analysis_data = 'data/datasets.csv'
    evaluation_path = '../evaluation/tests'

    # Regression
    if args.process == regression:
        regression = RegressionAnalysis()
        regression.process(analysis_data, evaluation_path)

    elif args.evaluate == regression:
        regression = RegressionAnalysis()
        regression.evaluate()

    elif args.trees == regression:
        RegressionAnalysis.grow_trees()

    elif args.important_nodes == regression:
        RegressionAnalysis.get_important_nodes(analysis_data)

    # Classification
    elif args.process == classification:
        classification = ClassificationAnalysis()
        classification.process(analysis_data, evaluation_path)

    elif args.evaluate == classification:
        classification = ClassificationAnalysis()
        classification.evaluate()

    elif args.trees == classification:
        ClassificationAnalysis.grow_trees()

    elif args.important_nodes == classification:
        ClassificationAnalysis.get_important_nodes(analysis_data)

    # Graphics
    if args.graphics == 'bp-ranking':
        graphic = Boxplot()
        graphic.ranking()
        graphic.save('bp-ranking.png')

        graphic.type_ranking()
        graphic.save('bp-type-ranking.png')

        clusters = {}

        for name, cluster in clusters.items():
            graphic = Boxplot()
            graphic.ranking(cluster)
            graphic.save('bp-ranking-{}.png'.format(name))

            graphic.type_ranking(cluster)
            graphic.save('bp-type-ranking-{}.png'.format(name))

        if args.show:
            graphic.show()
    elif args.graphics == 'bp-performance':
        graphic = Boxplot()
        graphic.performance()
        graphic.save('bp-performance.png')

        graphic.type_performance()
        graphic.save('bp-type-performance.png')

        clusters = {}

        for name, cluster in clusters.items:
            graphic = Boxplot()
            graphic.performance(cluster)
            graphic.save('bp-performance-{}.png'.format(name))

            graphic.type_performance(cluster)
            graphic.save('bp-type-performance-{}.png'.format(name))

        if args.show:
            graphic.show()

    if args.newick is not None:
        graphic = NewickTree()
        graphic.create(args.newick)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--process",
                        dest="process",
                        default=None,
                        choices=['regression', 'classification'],
                        help="Create data sets for evaluation.")

    parser.add_argument("-e", "--evaluate",
                        dest="evaluate",
                        default=None,
                        choices=['regression', 'classification'],
                        help="Type of evaluation (regression or "
                             "classification). Evaluate data sets.")

    parser.add_argument("-t", "--make-trees",
                        dest="trees",
                        default=None,
                        choices=['regression', 'classification'],
                        help="Create trees from DecisionTree's algorithm.")

    parser.add_argument("-i", "--get-important-nodes",
                        dest="important_nodes",
                        default=None,
                        choices=['regression'],
                        help="Extract important nodes from trees.")

    parser.add_argument("-g", "--graphics",
                        dest="graphics",
                        default=None,
                        choices=['bp-ranking', 'bp-performance'],
                        help="Create a specified graphic.")

    parser.add_argument("-n", "--newick",
                        dest="newick",
                        default=None,
                        choices=['ward', 'average', 'complete'],
                        help="Display a Newick Tree.")

    parser.add_argument("-s", "--show",
                        dest="show",
                        default=False,
                        choices=['true', 'false'],
                        help="Show or not a graphic.")

    args = parser.parse_args()
    main(args)
