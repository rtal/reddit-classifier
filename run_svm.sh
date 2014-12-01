python parse_features_for_svm.py data/Archaeology.csv data/ArtHistory.csv --train_out train_file --test_out test_file
python libshorttext-1.1/text-train.py train_file -f
python libshorttext-1.1/text-predict.py test_file train_file.model predict_result -f