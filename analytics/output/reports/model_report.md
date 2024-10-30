mnb Report

	best_params:

		alpha: 0.05

		fit_prior: True

	best_score:

		score: 0.6901540954437204

	best_cm:

		confusion_matrix: [[2072 1385]  [1291 3072]]

	best_precision:

		precision: 0.6892528606686111

	best_recall:

		recall: 0.7041026816410727

	results:

		mean_fit_time: [1.71634779 1.05592208 1.83200588 2.42748537 1.5884222  1.97446899  2.27438345 2.33977985]

		std_fit_time: [1.13199828 0.22472081 0.77784948 1.05901514 0.85348889 0.8152693  1.01398303 1.17225903]

		mean_score_time: [0.14323869 0.19391074 0.14411211 0.18357563 0.18914051 0.15979328  0.2120543  0.19202485]

		std_score_time: [0.03437792 0.05707536 0.03938754 0.04912448 0.06672075 0.02410767  0.06025282 0.05063973]

		param_alpha: [0.05 0.05 0.75 0.75 0.1 0.1 0.15 0.15]

		param_fit_prior: [True False True False True False True False]

		params: [{'alpha': 0.05, 'fit_prior': True}, {'alpha': 0.05, 'fit_prior': False}, {'alpha': 0.75, 'fit_prior': True}, {'alpha': 0.75, 'fit_prior': False}, {'alpha': 0.1, 'fit_prior': True}, {'alpha': 0.1, 'fit_prior': False}, {'alpha': 0.15, 'fit_prior': True}, {'alpha': 0.15, 'fit_prior': False}]

		split0_test_score: [0.68937876 0.68937876 0.68937876 0.68937876 0.68937876 0.68937876  0.68937876 0.68937876]

		split1_test_score: [0.69321111 0.69321111 0.69321111 0.69321111 0.69321111 0.69321111  0.69321111 0.69321111]

		split2_test_score: [0.68671608 0.68652887 0.68671608 0.68652887 0.68671608 0.68652887  0.68671608 0.68652887]

		split3_test_score: [0.6919364  0.69175067 0.6919364  0.69175067 0.6919364  0.69175067  0.6919364  0.69175067]

		split4_test_score: [0.68952813 0.68952813 0.68952813 0.68952813 0.68952813 0.68952813  0.68952813 0.68952813]

		mean_test_score: [0.6901541  0.69007951 0.6901541  0.69007951 0.6901541  0.69007951  0.6901541  0.69007951]

		std_test_score: [0.002251   0.00228043 0.002251   0.00228043 0.002251   0.00228043  0.002251   0.00228043]

		rank_test_score: [1 5 1 5 1 5 1 5]

End Report

rfc Report

	best_params:

		max_features: sqrt

		n_estimators: 500

	best_score:

		score: 0.8553641563186851

	best_cm:

		confusion_matrix: [[2886  571]  [ 686 3677]]

	best_precision:

		precision: 0.8655838041431262

	best_recall:

		recall: 0.8427687371074949

	results:

		mean_fit_time: [ 4.95190544 13.14636331 15.76052408  2.20214782  5.4493011   8.6371067 ]

		std_fit_time: [0.35074629 0.91238483 0.09997727 0.08220843 0.11918135 0.22156831]

		mean_score_time: [0.17585464 0.30333004 0.34800253 0.16336694 0.29224439 0.36055975]

		std_score_time: [0.01601851 0.05016309 0.02582747 0.00082864 0.05874909 0.01947659]

		param_max_features: ['sqrt' 'sqrt' 'sqrt' 'log2' 'log2' 'log2']

		param_n_estimators: [100 300 500 100 300 500]

		params: [{'max_features': 'sqrt', 'n_estimators': 100}, {'max_features': 'sqrt', 'n_estimators': 300}, {'max_features': 'sqrt', 'n_estimators': 500}, {'max_features': 'log2', 'n_estimators': 100}, {'max_features': 'log2', 'n_estimators': 300}, {'max_features': 'log2', 'n_estimators': 500}]

		split0_test_score: [0.8484318  0.85314685 0.85072231 0.76958197 0.78605974 0.78184147]

		split1_test_score: [0.85155684 0.85244483 0.85549133 0.78154372 0.78233883 0.78550191]

		split2_test_score: [0.84372307 0.85427136 0.85726594 0.77639752 0.78931834 0.78817873]

		split3_test_score: [0.85549964 0.85310653 0.85529158 0.77214126 0.7858148  0.78885919]

		split4_test_score: [0.85887446 0.85907976 0.85804962 0.78492491 0.79512264 0.79716914]

		mean_test_score: [0.85161716 0.85440987 0.85536416 0.77691787 0.78773087 0.78831009]

		std_test_score: [0.00529545 0.00240759 0.00254545 0.00569936 0.00430573 0.00507012]

		rank_test_score: [3 2 1 6 5 4]

End Report

xgbc Report

	best_params:

		learning_rate: 0.15

		n_estimators: 100

	best_score:

		score: 0.9434185365386879

	best_cm:

		confusion_matrix: [[3014  443]  [  60 4303]]

	best_precision:

		precision: 0.9066582385166456

	best_recall:

		recall: 0.9862479944991978

	results:

		mean_fit_time: [ 7.26953473 14.49440455 16.93231363  5.43527255 10.54182301 11.12652245]

		std_fit_time: [0.94379011 2.37535871 1.25420966 0.75884276 1.95234446 0.14785717]

		mean_score_time: [0.86278114 0.93665304 0.73698568 0.63909001 0.51811194 0.26152444]

		std_score_time: [0.26194461 0.39464119 0.2646404  0.15492857 0.31417763 0.02681442]

		param_learning_rate: [0.1 0.1 0.1 0.15 0.15 0.15]

		param_n_estimators: [100 300 500 100 300 500]

		params: [{'learning_rate': 0.1, 'n_estimators': 100}, {'learning_rate': 0.1, 'n_estimators': 300}, {'learning_rate': 0.1, 'n_estimators': 500}, {'learning_rate': 0.15, 'n_estimators': 100}, {'learning_rate': 0.15, 'n_estimators': 300}, {'learning_rate': 0.15, 'n_estimators': 500}]

		split0_test_score: [0.94861878 0.94827109 0.94905869 0.94911504 0.94927938 0.94857935]

		split1_test_score: [0.94320988 0.94361936 0.94333379 0.9443452  0.94406172 0.94370861]

		split2_test_score: [0.94072658 0.94167579 0.94022484 0.9408867  0.94053165 0.9403374 ]

		split3_test_score: [0.9392205  0.93939394 0.93847416 0.93942701 0.93824456 0.93865788]

		split4_test_score: [0.94212836 0.94241843 0.94224173 0.94331873 0.94288852 0.9417102 ]

		mean_test_score: [0.94278082 0.94307572 0.94266664 0.94341854 0.94300117 0.94259869]

		std_test_score: [0.00321208 0.00294057 0.0036062  0.0033365  0.00372229 0.00341857]

		rank_test_score: [4 2 5 1 3 6]

End Report

