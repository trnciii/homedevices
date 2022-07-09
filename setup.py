from setuptools import setup, find_packages

setup(
	name="hui",
	version="0.3.1",
	packages=find_packages(),
	url="https://github.com/trnciii/hui",
	license="MIT",
	entry_points={
		'console_scripts': [
			'huii = hui.__main__:run',
			'hui  = hui.__main__:oneliner'
		]
	}
)