python parse_features_for_svm.py data/Archaeology.csv data/ArtHistory.csv --train_out train_file --test_out test_file
python ../text-train.py train_file
python ../text-predict.py test_file train_file.model predict_result