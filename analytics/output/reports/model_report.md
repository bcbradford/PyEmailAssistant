mnb Report

	best_params:

		alpha: 0.05

		fit_prior: False

	best_score:

		score: 0.6386987298859191

	best_cm:

		confusion_matrix: [[2153 1304]  [1675 2688]]

	best_precision:

		precision: 0.6733466933867736

	best_recall:

		recall: 0.6160898464359386

	results:

		mean_fit_time: [1.61665044 1.86750636 1.70322399 2.24093223 2.52100286 2.39220309  2.06823936 2.6398623 ]

		std_fit_time: [1.086855   1.09761102 0.98989321 0.91393458 1.01210715 0.92232582  0.92528702 1.08732453]

		mean_score_time: [0.15393667 0.18498263 0.17318907 0.19249148 0.19197664 0.24676061  0.18687472 0.20874639]

		std_score_time: [0.03109748 0.05016796 0.07722592 0.05818484 0.06265668 0.10562253  0.0413197  0.04027305]

		param_alpha: [0.05 0.05 0.75 0.75 0.1 0.1 0.15 0.15]

		param_fit_prior: [True False True False True False True False]

		params: [{'alpha': 0.05, 'fit_prior': True}, {'alpha': 0.05, 'fit_prior': False}, {'alpha': 0.75, 'fit_prior': True}, {'alpha': 0.75, 'fit_prior': False}, {'alpha': 0.1, 'fit_prior': True}, {'alpha': 0.1, 'fit_prior': False}, {'alpha': 0.15, 'fit_prior': True}, {'alpha': 0.15, 'fit_prior': False}]

		split0_test_score: [0.64428506 0.64428506 0.64428506 0.64428506 0.64428506 0.64428506  0.64428506 0.64428506]

		split1_test_score: [0.62946632 0.62946632 0.62946632 0.62946632 0.62946632 0.62946632  0.62946632 0.62946632]

		split2_test_score: [0.64001198 0.64001198 0.64001198 0.64001198 0.64001198 0.64001198  0.64001198 0.64001198]

		split3_test_score: [0.64983567 0.64993277 0.64983567 0.64993277 0.64983567 0.64993277  0.64983567 0.64993277]

		split4_test_score: [0.62970237 0.62979752 0.62970237 0.62979752 0.62970237 0.62979752  0.62970237 0.62979752]

		mean_test_score: [0.63866028 0.63869873 0.63866028 0.63869873 0.63866028 0.63869873  0.63866028 0.63869873]

		std_test_score: [0.008039   0.00804493 0.008039   0.00804493 0.008039   0.00804493  0.008039   0.00804493]

		rank_test_score: [5 1 5 1 5 1 5 1]

End Report

rfc Report

	best_params:

		max_features: sqrt

		n_estimators: 300

	best_score:

		score: 0.8395994296412856

	best_cm:

		confusion_matrix: [[2732  725]  [ 660 3703]]

	best_precision:

		precision: 0.8362691960252936

	best_recall:

		recall: 0.8487279394911758

	results:

		mean_fit_time: [ 5.07464595 13.44773636 15.98027306  2.22299056  5.55847788  8.71322842]

		std_fit_time: [0.35132675 0.20541925 0.1733445  0.04989093 0.21835743 0.07216909]

		mean_score_time: [0.20325871 0.28196907 0.37790918 0.17556906 0.25984659 0.35524697]

		std_score_time: [0.0435234  0.01138402 0.0468193  0.02110003 0.00487785 0.00821655]

		param_max_features: ['sqrt' 'sqrt' 'sqrt' 'log2' 'log2' 'log2']

		param_n_estimators: [100 300 500 100 300 500]

		params: [{'max_features': 'sqrt', 'n_estimators': 100}, {'max_features': 'sqrt', 'n_estimators': 300}, {'max_features': 'sqrt', 'n_estimators': 500}, {'max_features': 'log2', 'n_estimators': 100}, {'max_features': 'log2', 'n_estimators': 300}, {'max_features': 'log2', 'n_estimators': 500}]

		split0_test_score: [0.83982808 0.84157706 0.83747665 0.76580562 0.77795141 0.77962253]

		split1_test_score: [0.83786881 0.83967274 0.84213539 0.76152646 0.77184602 0.77859779]

		split2_test_score: [0.83540328 0.83459182 0.83271482 0.75975764 0.77120677 0.77569435]

		split3_test_score: [0.83170835 0.83589238 0.83574058 0.76266667 0.77628635 0.78073228]

		split4_test_score: [0.8443685  0.84626314 0.84554231 0.76237484 0.77768362 0.78099522]

		mean_test_score: [0.8378354  0.83959943 0.83872195 0.76242625 0.77499484 0.77912843]

		std_test_score: [0.00424522 0.00417468 0.00457589 0.00197036 0.00289494 0.00191708]

		rank_test_score: [3 1 2 6 5 4]

End Report

xgbc Report

	best_params:

		learning_rate: 0.1

		n_estimators: 300

	best_score:

		score: 0.9397002982570118

	best_cm:

		confusion_matrix: [[2957  500]  [  60 4303]]

	best_precision:

		precision: 0.8958983968353113

	best_recall:

		recall: 0.9862479944991978

	results:

		mean_fit_time: [ 7.36829686 15.57237949 17.62302961  5.67219553  9.70140076 11.57570028]

		std_fit_time: [0.71667845 2.52541567 1.22302771 0.67001829 2.09396315 0.21396884]

		mean_score_time: [1.15368505 0.74579301 0.65861382 0.6985734  0.45911002 0.27499356]

		std_score_time: [0.41025339 0.37572414 0.20571768 0.2087594  0.23608077 0.01982434]

		param_learning_rate: [0.1 0.1 0.1 0.15 0.15 0.15]

		param_n_estimators: [100 300 500 100 300 500]

		params: [{'learning_rate': 0.1, 'n_estimators': 100}, {'learning_rate': 0.1, 'n_estimators': 300}, {'learning_rate': 0.1, 'n_estimators': 500}, {'learning_rate': 0.15, 'n_estimators': 100}, {'learning_rate': 0.15, 'n_estimators': 300}, {'learning_rate': 0.15, 'n_estimators': 500}]

		split0_test_score: [0.94491002 0.94442146 0.94354727 0.94555479 0.94370861 0.94312993]

		split1_test_score: [0.94178596 0.94228665 0.94312731 0.94315847 0.94525998 0.94298667]

		split2_test_score: [0.93641933 0.9371413  0.93681619 0.93687075 0.93718352 0.93716486]

		split3_test_score: [0.93191317 0.93345956 0.93324306 0.93040194 0.93123559 0.93159609]

		split4_test_score: [0.94026398 0.94119252 0.93992354 0.93934851 0.93958447 0.93806522]

		mean_test_score: [0.93905849 0.9397003  0.93933148 0.93906689 0.93939443 0.93858855]

		std_test_score: [0.00449785 0.00391665 0.00389685 0.00526911 0.00499015 0.00426996]

		rank_test_score: [5 1 3 4 2 6]

End Report

