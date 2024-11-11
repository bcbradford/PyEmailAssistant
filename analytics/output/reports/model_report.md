mnb Report

	best_params:

		alpha: 0.05

		fit_prior: True

	best_score:

		score: 0.6345264724809507

	best_cm:

		confusion_matrix: [[1741 1000]  [1471 2277]]

	best_precision:

		precision: 0.6948428440646933

	best_recall:

		recall: 0.6075240128068303

	results:

		mean_fit_time: [1.14347768 1.3988502  1.26447272 2.109552   1.80248232 1.92378807  2.09711223 2.29532886]

		std_fit_time: [1.0682779  0.71178363 0.6839286  0.84011494 0.63860216 1.0139435  0.92694077 0.49172538]

		mean_score_time: [0.11490107 0.15251398 0.13470516 0.16079292 0.16119976 0.1705255  0.15236549 0.18619604]

		std_score_time: [0.03600246 0.04378681 0.0549797  0.02270697 0.02340982 0.05719352  0.03451411 0.05428588]

		param_alpha: [0.05 0.05 0.75 0.75 0.1 0.1 0.15 0.15]

		param_fit_prior: [True False True False True False True False]

		params: [{'alpha': 0.05, 'fit_prior': True}, {'alpha': 0.05, 'fit_prior': False}, {'alpha': 0.75, 'fit_prior': True}, {'alpha': 0.75, 'fit_prior': False}, {'alpha': 0.1, 'fit_prior': True}, {'alpha': 0.1, 'fit_prior': False}, {'alpha': 0.15, 'fit_prior': True}, {'alpha': 0.15, 'fit_prior': False}]

		split0_test_score: [0.63743007 0.63743007 0.63743007 0.63743007 0.63743007 0.63743007  0.63743007 0.63743007]

		split1_test_score: [0.63211308 0.63186514 0.63186514 0.63186514 0.63211308 0.63186514  0.63211308 0.63186514]

		split2_test_score: [0.63021688 0.63021688 0.63021688 0.63021688 0.63021688 0.63021688  0.63021688 0.63021688]

		split3_test_score: [0.62683889 0.62683889 0.62683889 0.62683889 0.62683889 0.62683889  0.62683889 0.62683889]

		split4_test_score: [0.64603344 0.64579256 0.64603344 0.64579256 0.64603344 0.64579256  0.64603344 0.64579256]

		mean_test_score: [0.63452647 0.63442871 0.63447688 0.63442871 0.63452647 0.63442871  0.63452647 0.63442871]

		std_test_score: [0.00669831 0.00663418 0.00671689 0.00663418 0.00669831 0.00663418  0.00669831 0.00663418]

		rank_test_score: [1 5 4 5 1 5 1 5]

End Report

rfc Report

	best_params:

		max_features: sqrt

		n_estimators: 500

	best_score:

		score: 0.8622213578800514

	best_cm:

		confusion_matrix: [[2220  521]  [ 445 3303]]

	best_precision:

		precision: 0.863755230125523

	best_recall:

		recall: 0.8812700106723586

	results:

		mean_fit_time: [ 4.55026083 12.33446398 15.19745393  1.96228361  4.93182631  7.92885938]

		std_fit_time: [0.22862528 1.19524035 0.13227086 0.04650148 0.06379612 0.19734455]

		mean_score_time: [0.17022133 0.32936373 0.31602411 0.14690733 0.24237781 0.34250107]

		std_score_time: [0.02582829 0.11680974 0.0147613  0.00233873 0.01088894 0.01278682]

		param_max_features: ['sqrt' 'sqrt' 'sqrt' 'log2' 'log2' 'log2']

		param_n_estimators: [100 300 500 100 300 500]

		params: [{'max_features': 'sqrt', 'n_estimators': 100}, {'max_features': 'sqrt', 'n_estimators': 300}, {'max_features': 'sqrt', 'n_estimators': 500}, {'max_features': 'log2', 'n_estimators': 100}, {'max_features': 'log2', 'n_estimators': 300}, {'max_features': 'log2', 'n_estimators': 500}]

		split0_test_score: [0.85867561 0.85776294 0.85857909 0.78063785 0.78125    0.79342042]

		split1_test_score: [0.86037987 0.86134805 0.86872394 0.78571429 0.78791753 0.79603263]

		split2_test_score: [0.85757678 0.85584525 0.85752733 0.77633478 0.78024612 0.78993224]

		split3_test_score: [0.85862647 0.85971944 0.85432016 0.77284427 0.79600387 0.78910256]

		split4_test_score: [0.86265381 0.86783703 0.87195627 0.79327079 0.79175258 0.79161372]

		mean_test_score: [0.85958251 0.86050254 0.86222136 0.78176039 0.78743402 0.79202031]

		std_test_score: [0.00177922 0.00410655 0.00685246 0.00718773 0.00603712 0.0024939 ]

		rank_test_score: [3 2 1 6 5 4]

End Report

xgbc Report

	best_params:

		learning_rate: 0.15

		n_estimators: 300

	best_score:

		score: 0.9424835758946333

	best_cm:

		confusion_matrix: [[2374  367]  [  43 3705]]

	best_precision:

		precision: 0.9098722986247544

	best_recall:

		recall: 0.9885272145144077

	results:

		mean_fit_time: [ 7.69941993 14.54509215 17.61570616  6.0944128   8.89463472 11.44369903]

		std_fit_time: [1.04396883 1.83392637 0.97681065 0.29580295 2.38698224 0.09133547]

		mean_score_time: [1.0029357  0.96553087 0.73381805 0.70417738 0.36155701 0.27305303]

		std_score_time: [0.26421574 0.17305993 0.21242664 0.23031087 0.19972434 0.02671507]

		param_learning_rate: [0.1 0.1 0.1 0.15 0.15 0.15]

		param_n_estimators: [100 300 500 100 300 500]

		params: [{'learning_rate': 0.1, 'n_estimators': 100}, {'learning_rate': 0.1, 'n_estimators': 300}, {'learning_rate': 0.1, 'n_estimators': 500}, {'learning_rate': 0.15, 'n_estimators': 100}, {'learning_rate': 0.15, 'n_estimators': 300}, {'learning_rate': 0.15, 'n_estimators': 500}]

		split0_test_score: [0.94878881 0.94839655 0.94747145 0.94829268 0.94774657 0.94781613]

		split1_test_score: [0.94195635 0.94190198 0.94163551 0.94176642 0.94125284 0.94194178]

		split2_test_score: [0.94287101 0.9426442  0.94392979 0.94285252 0.94329813 0.94253622]

		split3_test_score: [0.93650538 0.93768163 0.93743922 0.93808449 0.93902043 0.93809911]

		split4_test_score: [0.93758085 0.93993506 0.93964958 0.93867618 0.9410999  0.9396846 ]

		mean_test_score: [0.94154048 0.94211188 0.94202511 0.94193446 0.94248358 0.94201557]

		std_test_score: [0.00437064 0.00358302 0.00346744 0.0036534  0.00295923 0.00330742]

		rank_test_score: [6 2 3 5 1 4]

End Report

