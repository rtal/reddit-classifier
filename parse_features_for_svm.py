import argparse
import csv
import string
def remove_punctuation(title):
	exlusionSet = set(string.punctuation)
	exlusionSet.remove("\'")
	#exlusionSet.remove("-")
	title = title.replace("-", " ")
	return ''.join(c for c in title if c not in exlusionSet)


#read in files, output them into train and test as required for libshorttxt format
#label<tab>title 
def parse_files_for_libsvm_shorttxt(fileList, out_train_file, out_test_file):
	train_f = open(out_train_file, 'wb')
	test_f = open(out_test_file, 'wb')
	test_cutoff = 10
	for fileName in fileList:
		subreddit = fileName[5:-4]
		with open(fileName, 'rb') as redditFile:
			redditReader = csv.reader(redditFile)
			i = 0
			for post in redditReader:
				words = remove_punctuation(post[4])
				if i % test_cutoff == 0:
					#testX.append(dict(words))
					#testYTitles.append((words, subreddit))
					test_f.write("%s\t%s\n" %  (subreddit, words))
					
				else:
					train_f.write("%s\t%s\n"% (subreddit, words))

				i += 1
	train_f.close()
	test_f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('fileNames', nargs='*')
    parser.add_argument('--train_out', required=True)
    parser.add_argument('--test_out', required=True)
    args = parser.parse_args()
    parse_files_for_libsvm_shorttxt(args.fileNames, args.train_out, args.test_out)