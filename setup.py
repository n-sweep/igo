from setuptools import setup

setup(
    name='gobot',
    version='0.0.1',
    description='a discord/OGS utility',
    author='n_sweep',
    author_email='n@sweep.sh',
    packages=['igo'],
    install_requires=[
        'beautifulsoup4',
        'discord.py',
        'kaleido',
        'imageio',
        'numpy',
        'plotly',
        'requests',
    ]
)
