from setuptools import setup

setup(name='pycrunch-engine',
      version='0.1',
      description='Automatic Test Runner Engine',
      url='http://github.com/gleb-sevruk/pycrunch',
      author='Gleb Sevruk',
      author_email='sevruk.gleb@gmail.com',
      license='MIT',
      packages=['pycrunch'],
      entry_points={
          'console_scripts': ['pycrunch-engine=pycrunch.main:run'],
      },
      install_requires=[
            'PyYAML==5.1',
            'pytest==4.6.3',
            'python-engineio==3.5.1',
            'python-socketio==3.1.2',
            'Werkzeug==0.15.2',
            'Flask==1.0.2',
            'Flask-Cors==3.0.7',
            'Flask-SocketIO==3.3.2',
            'Flask-SocketIO==3.3.2',
            'watchgod==0.4',
            'watchdog==0.9.0',
            'coverage==4.5.3',
      ],
      include_package_data=True,
      zip_safe=False)