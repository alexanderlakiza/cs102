import psycopg2
from tabulate import tabulate


def fetch_all(cursor):
    colnames = [desc[0] for desc in cursor.description]
    records = cursor.fetchall()
    return [{colname: value for colname, value in zip(colnames, record)} for record in records]


conn = psycopg2.connect(host="192.168.99.100", port="5432", dbname="athletes", user="postgres", password="asecurepassword")
cursor = conn.cursor()


# 1. How old were the youngest male and female participants of the 1996 Olympics?
# 1. Answer is 14 and 12

cursor.execute("""SELECT MIN(age) FROM athletes_events WHERE sex = 'M' and year = 1996 and age != 0""")
print(tabulate(fetch_all(cursor), "keys", "psql"))
# 14

cursor.execute("""SELECT MIN(age) FROM athletes_events WHERE sex = 'F' and year = 1996 and age != 0""")
print(tabulate(fetch_all(cursor), "keys", "psql"))
# 12


# 2. What was the percentage of male gymnasts among all the male participants of the 2000 Olympics?
# Round the answer to the first decimal
# 2. Answer is 1.5%

cursor.execute(
	"""
	SELECT ROUND((COUNT(DISTINCT(athlete_id)) / (SELECT COUNT(DISTINCT(athlete_id))
    FROM athletes_events WHERE sex = 'M' and year = 2000)::numeric) * 100, 1)
        FROM athletes_events
        WHERE sex = 'M' and year = 2000 and sport = 'Gymnastics'
    """
)
print(tabulate(fetch_all(cursor), "keys", "psql"))
# 1.5


# 3. What are the mean and standard deviation of height for female basketball players participated in the 2000 Olympics?
# Round the answer to the first decimal.
# 3. Answer is 182.4 and 9.1

cursor.execute(
    """
    SELECT ROUND((AVG(temp.height)::numeric), 1) AS "avg_height",
    ROUND((STDDEV(temp.height)::numeric), 1) AS "stddev_height"
    FROM (SELECT DISTINCT athlete_id, height FROM athletes_events
    WHERE sex = 'F' and year = 2000 and height > 0 and sport = 'Basketball') AS temp
    """
)
print(tabulate(fetch_all(cursor), "keys", "psql"))
# 182.4 and 9.1


# 4. Find a sportsperson participated in the 2002 Olympics, with the highest weight among other participants of the same Olympics. What sport did he or she do?
# 4. Answer is Bobsleigh

cursor.execute(
	"""
	SELECT sport FROM athletes_events
	WHERE weight=(SELECT MAX(weight) FROM athletes_events WHERE year = 2002) and year = 2002
	"""
)
print(tabulate(fetch_all(cursor), "keys", "psql"))
# Bobsleigh


# 5. How many times did Pawe Abratkiewicz participate in the Olympics held in different years?
# 5. Answer is 3

cursor.execute(
	"""
	SELECT COUNT(DISTINCT temp.games)
	FROM (SELECT DISTINCT name, games FROM athletes_events
	WHERE name = 'Pawe Abratkiewicz') AS temp
	"""
)
print(tabulate(fetch_all(cursor), "keys", "psql"))
# 3


# 6. How many silver medals in tennis did Australia win at the 2000 Olympics?
# 6. Answer is 2

cursor.execute(
	"""
	SELECT COUNT (*) FROM athletes_events
	WHERE team = 'Australia' and year = 2000 and sport = 'Tennis' and medal ='Silver'
	"""
)
print(tabulate(fetch_all(cursor), "keys", "psql"))
# 2


# 7. Is it true that Switzerland won fewer medals than Serbia at the 2016 Olympics?
# 7. Answer is Yes

cursor.execute(
	"""
	SELECT(SELECT COUNT(*)
	FROM athletes_events
	WHERE year = 2016 and medal != 'NA' and team = 'Serbia') >
	(SELECT COUNT(*)
	FROM athletes_events
	WHERE year = 2016 and medal != 'NA' and team = 'Switzerland') AS answer
	"""
)
print(tabulate(fetch_all(cursor), "keys", "psql"))
# True