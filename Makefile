.PHONY: flush
.PHONY: etl
.PHONY: etl_foot
.PHONY: etl_hand
.PHONY: etl_android
.PHONY: etl_iphone
.PHONY: clean_data
.PHONY: rebase

flush:
	rm continuous_data/*.csv formatted_data/*.csv
	

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
	rm formatted_data/*.csv

rebase:
	python3 rebase.py continuous_data 1