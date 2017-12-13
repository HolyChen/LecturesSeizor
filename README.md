# LecturesSeizor
This python script can automatically seize lectures held by School of Information and Technology, Xiamen University. The core strategy is send http requests recurrently.

## Outline
- [Pre-requirements](#Pre-requirements)
- [How-to](#How-to)
- [License](#License)

## Pre-requirements

[<img src="https://img.shields.io/badge/Python-3.x-blue.svg" alt="Python 3">](https://www.python.org/downloads/) It has been developed and tested in python 3.6.3 (Anoconda 3), your can only download the original python 3.x interpreter.

[<img src="https://img.shields.io/badge/Beautiful%20Soup-4.6.0-blue.svg" alt="BeautifulSoup 4">](https://pypi.python.org/pypi/beautifulsoup4/4.6.0) 

# How-to

1. Download the code and extract it to a directory.
2. Run the script as follows.

The script receive 3 parameters, which are, in sequence, **website**, **student ID\(sID\)**, and **password** with respective to the website and sID. The **website** is the URL of the *Management System of School of Information and Engineering*, which is unchanged for serveral years but should be removed from the code. 

```shell
python lectures-seizor "http://example.xmu.edu.cn/" your_student_id your_password
```

## License

[<img src="https://img.shields.io/badge/Lisence-GPL%20v3-brightgreen.svg" alt="GPLv3" >](http://www.gnu.org/licenses/gpl-3.0.html)

The script is licensed under GNU General Public License v3.0 \(GPLv3\).

