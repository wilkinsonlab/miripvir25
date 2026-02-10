---
author: Bruno Cuevas
format: html
---

# Analysis

The analysis pipeline can be certainly complex to execute. The following tips can ease the execution.

1. There are three kinds of files in the analysis folder:
    - **analysis**: Includes statistical analysis
    - **compute**: Includes calculations scripts for time-consuming tasks (e.g. cooccurrence calculation)
    - **prep**: Includes preparation tasks, such as creating tables that will be used by other notebooks.
    - **visualization**: Includes notebooks whose major aim is to simply produce figures.
2. The whole analysis was originally run in multiple machines, depending on the needs (e.g. some tasks cannot be run in a MacBook air). Therefore, there is not really anything like an executable pipeline to run the whole analysis. However, files are numbered depending on their execution order. In principle, you should run notebooks `prep-00` before notebooks `prep-01`. 
3. There is a `conf.yaml` file that determines execution data, such as the name of the *daforfer* database (see below), or the color palette employed. 


# What is Daforfer? 

[Daforfer](https://github.com/brunocuevas/daforfer) is a very simple solution to keep the datasets of the article controlled. Instead of creating infinite `.csv` files floating around, it keeps everything under an SQL database and enables dumping the contents to an excel file. This can be very useful to keep tables under different databases (e.g. one for intermediate calculations, another one for supplementary tables, etc)