from pip.req import parse_requirements
from setuptools import setup

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='image_grabber',
    version='1.0.0',
    description='Grab the first page of images from Bing Image search.',
    author='Jeff Rand',
    author_email='jeffreyrand@gmail.com',
    install_requires=reqs,
    url='https://github.com/jeffrand/image-grabber',
    packages=['image_grabber'],
    scripts=['bin/image_grabber']
)
