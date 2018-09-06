install:
	pip install -r requirements.txt

train:
	python main.py --train

fetch_data:
	python main.py --fetch

store_into_db:
	python main.py --store

analyze_data:
	python main.py --analyze
