mnb Report

	best_params:

		alpha: 0.05

		fit_prior: True

	best_score:

		score: 0.6420034021302222

	best_cm:

		confusion_matrix: [[2163 1327]  [1645 2696]]

	best_precision:

		precision: 0.6701466567238379

	best_recall:

		recall: 0.6210550564386086

	results:

		mean_fit_time: [1.25434241 1.49841752 1.51173692 1.37342    1.47233524 1.39543252  1.4738503  2.17098942]

		std_fit_time: [1.05561343 0.82012421 1.04016264 0.79600519 0.90444987 0.86255441  0.89981061 0.57707409]

		mean_score_time: [0.07416964 0.08316684 0.08848834 0.09566832 0.0944375  0.09826264  0.10950718 0.10941   ]

		std_score_time: [0.04312224 0.01708052 0.03636936 0.03460039 0.03276917 0.02270114  0.03498143 0.02668619]

		param_alpha: [0.05 0.05 0.75 0.75 0.1 0.1 0.15 0.15]

		param_fit_prior: [True False True False True False True False]

		params: [{'alpha': 0.05, 'fit_prior': True}, {'alpha': 0.05, 'fit_prior': False}, {'alpha': 0.75, 'fit_prior': True}, {'alpha': 0.75, 'fit_prior': False}, {'alpha': 0.1, 'fit_prior': True}, {'alpha': 0.1, 'fit_prior': False}, {'alpha': 0.15, 'fit_prior': True}, {'alpha': 0.15, 'fit_prior': False}]

		split0_test_score: [0.63996345 0.63996345 0.63975628 0.63975628 0.63996345 0.63975628  0.63996345 0.63975628]

		split1_test_score: [0.64300689 0.64300689 0.64300689 0.64300689 0.64300689 0.64300689  0.64300689 0.64300689]

		split2_test_score: [0.64724433 0.64704115 0.64715594 0.64654655 0.64714715 0.64694399  0.64704999 0.64684685]

		split3_test_score: [0.63356112 0.63365735 0.63316125 0.63316125 0.63335358 0.63335358  0.63335358 0.63335358]

		split4_test_score: [0.64624122 0.64624122 0.64624122 0.64624122 0.64624122 0.64624122  0.64624122 0.64624122]

		mean_test_score: [0.6420034  0.64198201 0.64186432 0.64174244 0.64194246 0.64186039  0.64192303 0.64184096]

		std_test_score: [0.00493694 0.00486129 0.0050725  0.00494973 0.00498771 0.0049627  0.00496755 0.00494291]

		rank_test_score: [1 2 5 8 3 6 4 7]

End Report

rfc Report

	best_params:

		max_features: sqrt

		n_estimators: 300

	best_score:

		score: 0.9931782486235914

	best_cm:

		confusion_matrix: [[3467   23]  [  28 4313]]

	best_precision:

		precision: 0.9946955719557196

	best_recall:

		recall: 0.9935498733010827

	results:

		mean_fit_time: [2.82191386 7.39276738 8.9287931  0.90433555 2.14027376 3.43135319]

		std_fit_time: [0.33096985 0.17803016 1.36583244 0.08493266 0.08791381 0.15944879]

		mean_score_time: [0.11904006 0.27468448 0.30019927 0.10375848 0.17296028 0.25613012]

		std_score_time: [0.02104375 0.06162228 0.14107116 0.02554082 0.0086991  0.00935487]

		param_max_features: ['sqrt' 'sqrt' 'sqrt' 'log2' 'log2' 'log2']

		param_n_estimators: [100 300 500 100 300 500]

		params: [{'max_features': 'sqrt', 'n_estimators': 100}, {'max_features': 'sqrt', 'n_estimators': 300}, {'max_features': 'sqrt', 'n_estimators': 500}, {'max_features': 'log2', 'n_estimators': 100}, {'max_features': 'log2', 'n_estimators': 300}, {'max_features': 'log2', 'n_estimators': 500}]

		split0_test_score: [0.99344169 0.99344169 0.99343982 0.99159424 0.99116557 0.99145543]

		split1_test_score: [0.99243614 0.99257779 0.99243398 0.99129193 0.98987594 0.99044359]

		split2_test_score: [0.99371788 0.99371788 0.99385977 0.99128945 0.99186063 0.99200685]

		split3_test_score: [0.99128447 0.99200685 0.99114286 0.99057143 0.99100129 0.99143347]

		split4_test_score: [0.99414369 0.99414704 0.99400343 0.99372146 0.99315068 0.99314677]

		mean_test_score: [0.99300477 0.99317825 0.99297597 0.9916937  0.99141082 0.99169722]

		std_test_score: [0.00102755 0.0007787  0.00106827 0.00106827 0.00107825 0.0008828 ]

		rank_test_score: [2 1 3 5 6 4]

End Report

xgbc Report

	best_params:

		learning_rate: 0.15

		n_estimators: 500

	best_score:

		score: 0.9954894312755306

	best_cm:

		confusion_matrix: [[3476   14]  [  15 4326]]

	best_precision:

		precision: 0.9967741935483871

	best_recall:

		recall: 0.9965445749827229

	results:

		mean_fit_time: [ 8.73248014 11.80047259 11.8284883   3.1596045   6.35496335  9.79123592]

		std_fit_time: [0.62627745 2.78320276 1.46669696 0.0514879  0.220918   0.40735887]

		mean_score_time: [0.88997779 0.62435999 0.43974686 0.26341381 0.27362967 0.27786546]

		std_score_time: [0.12072706 0.15038643 0.28375971 0.01267783 0.01370753 0.01167066]

		param_learning_rate: [0.1 0.1 0.1 0.15 0.15 0.15]

		param_n_estimators: [100 300 500 100 300 500]

		params: [{'learning_rate': 0.1, 'n_estimators': 100}, {'learning_rate': 0.1, 'n_estimators': 300}, {'learning_rate': 0.1, 'n_estimators': 500}, {'learning_rate': 0.15, 'n_estimators': 100}, {'learning_rate': 0.15, 'n_estimators': 300}, {'learning_rate': 0.15, 'n_estimators': 500}]

		split0_test_score: [0.99331722 0.99629313 0.99643519 0.9947331  0.99600912 0.99629101]

		split1_test_score: [0.9907447  0.99343607 0.99471655 0.99215966 0.99371788 0.99428571]

		split2_test_score: [0.99344729 0.99614671 0.99628784 0.99472107 0.99671476 0.99671382]

		split3_test_score: [0.99060097 0.99329816 0.99372325 0.99215966 0.99415205 0.99415205]

		split4_test_score: [0.99316044 0.99529177 0.9957204  0.99415205 0.99543379 0.99600457]

		mean_test_score: [0.99225412 0.99489317 0.99537665 0.99358511 0.99520552 0.99548943]

		std_test_score: [0.00129511 0.00129285 0.00102356 0.00118267 0.00112237 0.0010625 ]

		rank_test_score: [6 4 2 5 3 1]

End Report

