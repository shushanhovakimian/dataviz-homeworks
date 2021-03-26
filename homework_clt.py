import sqlite3
import numpy as np
import time
import random
from scipy import stats
from scipy.stats import shapiro


connection = sqlite3.connect('data_db.db')
c = connection.cursor()

c.execute("DROP TABLE IF EXISTS CLT_data1")

c.execute("CREATE TABLE CLT_data1 (outputs int)")

c.execute("DROP TABLE IF EXISTS CLT_data2")

c.execute("CREATE TABLE CLT_data2(mean_values float)")

c.execute("DROP TABLE IF EXISTS CLT_data3")

c.execute("CREATE TABLE CLT_data3(pvalues float)")


means = []

while True:
    
    population = []
    #generating population of size 100
    for x in range(100):
        output = random.randint(1, 6)
        population.append(output) 
        c.execute("INSERT INTO CLT_data1 values ({})".format(output))
        
        
    #generating 50 samples of size 7 from that population   
    for x in range(50):
    		   
        sample = random.sample(population,7) 
        mean = sum(sample)/7
        means.append(mean)
        c.execute("INSERT INTO CLT_data2 values ({})".format(mean))
        if len(means) >= 3:
            pvalue = stats.shapiro(means).pvalue
            c.execute("INSERT INTO CLT_data3 values ({})".format(round(pvalue,4)))
        
     
    connection.commit()
    time.sleep(0.5)

