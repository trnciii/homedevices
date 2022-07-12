from setuptools import setup, find_packages

setup(
	name="hui",
	version="0.3.3",
	packages=find_packages(),
	url="https://github.com/trnciii/hui",
	license="MIT",
	entry_points={
		'console_scripts': [
			'hui  = hui.__main__:main'
		]
	}
)