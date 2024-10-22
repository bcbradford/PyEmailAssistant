bnn Report

	best:

		score: 0

	model_1:

	model_2:

	model_3:

End Report

rfc Report

	best:

		params: {'n_estimators': 300, 'max_depth': 10, 'random_state': 42}

		confusion_matrix: [[1872 1585]  [ 458 3905]]

		score: 0.7926519841672587

	model_1:

		params: {'n_estimators': 100, 'max_depth': 10, 'random_state': 42}

		confusion_matrix: [[1778 1679]  [ 409 3954]]

		score: 0.7911164465786314

	model_2:

		params: {'n_estimators': 200, 'max_depth': 10, 'random_state': 42}

		confusion_matrix: [[1853 1604]  [ 457 3906]]

		score: 0.7912488605287147

	model_3:

		params: {'n_estimators': 300, 'max_depth': 10, 'random_state': 42}

		confusion_matrix: [[1872 1585]  [ 458 3905]]

		score: 0.7926519841672587

End Report

xgbc Report

	best:

		params: {'learning_rate': 0.1, 'n_estimators': 100, 'max_depth': 10, 'tree_method': 'hist'}

		confusion_matrix: [[3044  413]  [  50 4313]]

		score: 0.9490593024535152

	model_1:

		params: {'learning_rate': 0.1, 'n_estimators': 100, 'max_depth': 10, 'tree_method': 'hist'}

		confusion_matrix: [[3044  413]  [  50 4313]]

		score: 0.9490593024535152

	model_2:

		params: {'learning_rate': 0.1, 'n_estimators': 200, 'max_depth': 10, 'tree_method': 'hist'}

		confusion_matrix: [[3040  417]  [  56 4307]]

		score: 0.9479476174755145

	model_3:

		params: {'learning_rate': 0.1, 'n_estimators': 300, 'max_depth': 10, 'tree_method': 'hist'}

		confusion_matrix: [[3047  410]  [  60 4303]]

		score: 0.9482150727192595

End Report

