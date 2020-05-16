import setuptools

zip_safe=False

setuptools.setup(
	name="farasapy",
	version='0.0.1',
	author='MagedSaeed',
	author_email="mageedsaeed1@gmail.com",
	description="A Python Wrapper for the well Farasa toolkit",
	url="https://github.com/MagedSaeed/farasapy",
	packages=['farasa'],
	package_dir = {'farasa':'farasa'},
	package_data={'farasa':['farasa_bin/*','farasa_bin/lib/*','tmp/*']},
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: GPL",
		"Operating System :: cross-platform",
	],
)

# scripts=['farasa/__init__.py','farasa/farasa_bin/*','farasa/farasa_bin/lib/*','farasa/tmp/*'],