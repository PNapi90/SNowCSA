#!bin/bash

for i in {0..4}
do
	k=$((i+1))
	mv Exam${k}.txt Exam${i}.txt
	echo $i to $k
done
