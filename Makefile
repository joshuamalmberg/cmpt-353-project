.PHONY: flush
.PHONY: etl
.PHONY: etl_foot
.PHONY: etl_hand
.PHONY: etl_android
.PHONY: etl_iphone
.PHONY: clean_data
.PHONY: rebase
.PHONY: tset
.PHONY: features

flush:
	rm -f continuous_data/*.csv formatted_data/*.csv
	

etl:
	python3 etl.py orig_data/iphone/walk/foot/right formatted_data 0 0 0 0
	python3 etl.py orig_data/iphone/walk/foot/left formatted_data 0 0 0 1
	python3 etl.py orig_data/iphone/walk/hand/right formatted_data 0 0 1 0
	python3 etl.py orig_data/iphone/walk/hand/left formatted_data 0 0 1 1
	python3 etl.py orig_data/iphone/run/foot/right formatted_data 0 1 0 0
	python3 etl.py orig_data/iphone/run/foot/left formatted_data 0 1 0 1
	python3 etl.py orig_data/iphone/run/hand/right formatted_data 0 1 1 0
	python3 etl.py orig_data/iphone/run/hand/left formatted_data 0 1 1 1
	python3 etl.py orig_data/android/walk/foot/right formatted_data 1 0 0 0
	python3 etl.py orig_data/android/walk/foot/left formatted_data 1 0 0 1
	python3 etl.py orig_data/android/walk/hand/right formatted_data 1 0 1 0
	python3 etl.py orig_data/android/walk/hand/left formatted_data 1 0 1 1
	python3 etl.py orig_data/android/run/foot/right formatted_data 1 1 0 0
	python3 etl.py orig_data/android/run/foot/left formatted_data 1 1 0 1
	python3 etl.py orig_data/android/run/hand/right formatted_data 1 1 1 0
	python3 etl.py orig_data/android/run/hand/left formatted_data 1 1 1 1

etl_foot:
	python3 etl.py orig_data/iphone/walk/foot/right formatted_data 0 0 0 0
	python3 etl.py orig_data/iphone/walk/foot/left formatted_data 0 0 0 1
	python3 etl.py orig_data/iphone/run/foot/right formatted_data 0 1 0 0
	python3 etl.py orig_data/iphone/run/foot/left formatted_data 0 1 0 1
	python3 etl.py orig_data/android/walk/foot/right formatted_data 1 0 0 0
	python3 etl.py orig_data/android/walk/foot/left formatted_data 1 0 0 1
	python3 etl.py orig_data/android/run/foot/right formatted_data 1 1 0 0
	python3 etl.py orig_data/android/run/foot/left formatted_data 1 1 0 1

etl_hand:
	python3 etl.py orig_data/iphone/walk/hand/right formatted_data 0 0 1 0
	python3 etl.py orig_data/iphone/walk/hand/left formatted_data 0 0 1 1
	python3 etl.py orig_data/iphone/run/hand/right formatted_data 0 1 1 0
	python3 etl.py orig_data/iphone/run/hand/left formatted_data 0 1 1 1
	python3 etl.py orig_data/android/walk/hand/right formatted_data 1 0 1 0
	python3 etl.py orig_data/android/walk/hand/left formatted_data 1 0 1 1
	python3 etl.py orig_data/android/run/hand/right formatted_data 1 1 1 0
	python3 etl.py orig_data/android/run/hand/left formatted_data 1 1 1 1

etl_android:
	python3 etl.py orig_data/android/walk/foot/right formatted_data 1 0 0 0
	python3 etl.py orig_data/android/walk/foot/left formatted_data 1 0 0 1
	python3 etl.py orig_data/android/walk/hand/right formatted_data 1 0 1 0
	python3 etl.py orig_data/android/walk/hand/left formatted_data 1 0 1 1
	python3 etl.py orig_data/android/run/foot/right formatted_data 1 1 0 0
	python3 etl.py orig_data/android/run/foot/left formatted_data 1 1 0 1
	python3 etl.py orig_data/android/run/hand/right formatted_data 1 1 1 0
	python3 etl.py orig_data/android/run/hand/left formatted_data 1 1 1 1

etl_iphone:
	python3 etl.py orig_data/iphone/walk/foot/right formatted_data 0 0 0 0
	python3 etl.py orig_data/iphone/walk/foot/left formatted_data 0 0 0 1
	python3 etl.py orig_data/iphone/walk/hand/right formatted_data 0 0 1 0
	python3 etl.py orig_data/iphone/walk/hand/left formatted_data 0 0 1 1
	python3 etl.py orig_data/iphone/run/foot/right formatted_data 0 1 0 0
	python3 etl.py orig_data/iphone/run/foot/left formatted_data 0 1 0 1
	python3 etl.py orig_data/iphone/run/hand/right formatted_data 0 1 1 0
	python3 etl.py orig_data/iphone/run/hand/left formatted_data 0 1 1 1

clean_data:
	python3 remove_discontinuities.py formatted_data continuous_data
	rm -f formatted_data/*.csv

rebase:
	python3 rebase.py continuous_data 1

split_fft:
	python3 split_fft.py continuous_data




features:
	python3 build_tset.py continuous_data training_data/tset.csv

tset_android:
	make flush
	make etl_android
	make clean_data
	make rebase
	python3 build_tset.py continuous_data training_data/android_tset.csv
	
tset_iphone:
	make flush
	make etl_iphone
	make clean_data
	make rebase
	python3 build_tset.py continuous_data training_data/iphone_tset.csv

tset:
	make etl
	make clean_data
	make rebase
	make features

train:
	python3 ML_model.py training_data/tset.csv

