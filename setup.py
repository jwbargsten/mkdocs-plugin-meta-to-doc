from setuptools import setup, find_packages
setup(
    name="mkdocs-plugin-meta-to-doc",
    version="0.12",
    packages=find_packages(),
    install_requires=[
        'mkdocs>=1.0.4',
    ],
    entry_points={
        'mkdocs.plugins': [
            'meta_to_doc = mkdocs_plugin_meta_to_doc.plugin:MetaToDoc'
        ]
    }
)
