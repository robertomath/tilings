cubic.pdf: cubic.eps
	epstopdf $<

cubic.eps: *.py
	python demo.py

lattices_v%.zip:
	zip $@ *.py tests/*.py
