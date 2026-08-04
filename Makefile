.PHONY: audit test smoke verify clean

audit:
	python3 scripts/audit.py

test:
	python3 -m unittest discover -s tests -p 'test_*.py'

smoke:
	python3 scripts/smoke_test.py

verify: audit test smoke

clean:
	rm -rf .workflow __pycache__ tests/__pycache__ scripts/__pycache__ benchmark-results
