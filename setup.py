from setuptools import setup, find_packages

with open("README.md", encoding='utf-8') as f:
	long_description = f.read()

setup(
    name='herapheri',
    version='1.0.0',
    author='Ritwik Singh',
    packages=find_packages(),
    install_requires=[
    "click>=8.2.1",
    "duckdb>=1.3.1",
    "langchain>=0.3.26",
    "langchain-anthropic>=0.3.16",
    "langchain-google-genai>=2.1.6",
    "langchain-groq>=0.3.4",
    "langchain-openai>=0.3.27",
    "langgraph>=0.5.0",
    "langchain-community>=0.3.27",
    "langchain-core>=0.3.67",
    "python-dotenv>=1.1.1",
    "requests>=2.32.4",
    "rich>=14.0.0",
    "setuptools>=80.9.0",
    ],
    
    entry_points={
        'console_scripts': [
            'herapheri=run.main:main',
        ],
    },
    
    author_email="officialritwik098@gmail.com",
    description="HeraPheri CLI - A command-line interface for interacting with various LLM providers.",
    long_description_content_type='text/markdown',
    url="https://github.com/datasciritwik/hera-pheri/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: English",
        "Environment :: Console",
    ],
    python_requires='>=3.10',
)
        
