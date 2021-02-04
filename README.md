# ASVSP PROJEKAT

Podaci koji su se koristili za ovaj projekat su:
1. 9000+ tekstualnih datoteka
2. 2 JSON fajla
3. 1 CSV fajl

Svi prethodno navedeni podaci su skinuti sa interneta i korisceni kao takvi.

Batch obrada je podeljenje u 3 koraka:
1. Obrada ulaznih podataka i njihovo objedinjavanje u jedan CSV fajl koji ima format recenica-sentiment
2. Kreiranje recnika u obliku csv fajla koji sadrzi sve jedinstvene reci kao i broj njihovog pojavljivanja. Krajnja verzija recnika ne sadrzi reci koje se ne pojavljuju barem 20 puta.
3. Treniranje LR modela koji sluzi za sentiment analizu

Real time obrada podrazumeva sledece:
1. 3 producera koji salju podatke na 2 topica. 2 producera od tih 3 podatke citaju iz dostupnog csv fajla dok treci producer scrapeuje podatke sa IMDB sajta i salje ih.
2. Consumer uzima podatke, vrsi analizu koliko su recenice dugacke, racuna sentiment nad istim i vadi samo one recenice kojima je sentiment veci od 0.5

## Pokretanje

# Batch obrada
1. Docker-compose up u folderu docker-spark
2. docker exec -it namenode bash
3. hdfs dfs -mkdir /home
4. hdfs dfs -put /home/en /home/
5. hdfs dfs -put /home/json /home/
6. hdfs dfs -put /home/train.csv /home/
7. Otvoriti u browseru localhost:8282 u kome se nalazi airflow i pokrenuti DAG

# Real time obrada
1. Docker-compose up u Real_time_processing/docker_specification
2. docker exec -it spark-master bash
3. $SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.4 $SPARK_HOME/real_time.py zoo1:2181 subreddit-politics subreddit-worldnews
