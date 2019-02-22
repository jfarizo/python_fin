import pandas as pd
import numpy as np

print('Hello World!')

print(2+2)
print(3-1)
print(10*2)
print(12/4)

first_number = 2+3
second_number = 6*4
print('The sum of my two numbers is: ')
print(first_number + second_number)

first_name = input('Hi! What is your first name? ')
last_name = input('What is your last name? ')
print('Your full name is: ', first_name + ' ' + last_name)

d = {'a': [1, 2, 3, 4], 'b': [7, 8, 9, 10], 'c': [13, 14, 15, 16]}
df = pd.DataFrame(data=d) #notice we call upon the pandas library here
print(df)

df['new_col'] = df['a'] + df['c']
print('')
print(df.head(2))