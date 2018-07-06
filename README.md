# PUSH ME IN
This is a simple script that will check a number of classes for free seats every two minutes and if it finds an empty seat it will email you. 

Dependencies:
- Python3
- Pandas
- bs4

To operate this script paste links such as [this one](https://courses.students.ubc.ca/cs/main;jsessionid=Y8iDvsOem9klxiCj2+iChKmV?pname=subjarea&tname=subjareas&req=5&dept=MATH&course=342&section=201) under the column Url in classes-url.csv. Then edit the following lines of code into an email you have access to. (this has been set up for gmail)

```python
sFrom = 'editme'
sTo = 'editme'
password = 'editme'
```
Good luck getting pushed in!
