#!/usr/local/bin/python3
import qGen

print("Default full text query\n")
print(qGen.makeQuery(0,0,0))
print("\nID query\n")
print(qGen.makeQuery(-1,0,0))
print("\nName query in C++\n")
print(qGen.makeQuery(1, "Language_Name", ["C++"]))
print("\nName query in C, C++, and Java\n")
print(qGen.makeQuery(1, "Language_Name", ["C","C++","Java"]))
