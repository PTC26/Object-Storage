# Object Storage

## Overview

Today’s software systems are by definition *scattered* and *replicated* across various infrastructure, which better known as ***distributed architecture***. Scattering and replicating services promotes sustainability, recovery time, and removed the issue of *single point of failure*.

A key component of any system is data. Some types of data can be stored in a database, while other types require a *filesystem*. When distributing services across infrastructure *(machine)*, you can no longer rely on a standard filesystem. Over the years, systems have moved from *network attached storage (NAS)* to other distributed system such as *Hadoop distributed files system (HDFS)*. Such filesystem have proven reliable, but cannot adopt to the *cloud native* infrastructural, implemented by the majority of today’s systems.

The next generation solution to distributed storage is known as *object storage*. The upcoming tasks include both hands-on and the theory behind object storage.

## Task


- 1.Briefly research the key differences between object storage and other forms of distributed storages. Make note of advances and disadvantages of each.
- 2.What is S3?
- 3.What is a *bucket*?
- 4.Does the concept of *folders* exist in S3?
- 5.Are there size limitations? How do they compare to classic filesystem?
- 6.What implementations of S3 are there?
- 7.Deploy a working instance of [MinIO](https://min.io/) using docker.
- 8.Write *client* code, in any language, to interact with the MinIO instance.
    - Randomly create new object *(generate both random names and data)*.
    - List the existing objects.
    - Read the data of an existing object.
    - Remove an exciting object.
    - Update an existing object *(explain how versioning plays a factor in updating)*.

## Submit

Please submit your code, scripts, documentation, and screenshots in a subdirectory of the repository.
