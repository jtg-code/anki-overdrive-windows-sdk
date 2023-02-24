from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Anki-Overdrive-Windows',
  version='0.5.3',
  description='Anki Overdrive SDK for Windows',
  long_description='See Github',
  url='https://github.com/jtg-code/anki-overdrive-windows-sdk/',  
  author='Julius Tiberius Gottschling and TKV',
  author_email='juligo1008@gmail.com',
  license=open("license.txt").read(), 
  classifiers=classifiers,
  keywords=['anki', 'anki overdrive', 'bleak', 'overdrive', 'windows', 'bluetooth'], 
  packages=find_packages(),
  install_requires=['bleak', 'asyncio', 'time', 'struct']
)