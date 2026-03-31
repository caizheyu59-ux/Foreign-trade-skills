from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quote-translator",
    version="2.0.0",
    author="薯条 (Caizheyu)",
    author_email="your.email@example.com",
    description="报价单翻译器 - 保留原样式，仅翻译文字内容",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/quote-translator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Localization",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openpyxl>=3.0.0",
        "beautifulsoup4>=4.9.0",
        "lxml>=4.6.0",
        "python-docx>=0.8.0",
        "python-dotenv>=0.19.0",
    ],
    entry_points={
        "console_scripts": [
            "translate-quote=scripts.translate_quote:main",
        ],
    },
)
