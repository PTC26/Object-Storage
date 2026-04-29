# Task 1

## File Storage

### 1. Network Attached Storage (NAS)

A centralized file storage system accessed over a network, appearing to users as a standard filesystem.

#### Advantages:
- Simple to set up and manage  
- Looks like a traditional filesystem (easy to use for applications)  
- Good for file sharing between users and systems  
- Relatively low cost for small to medium environments  

#### Disadvantages:
- Single point of failure (central server dependency)  
- Performance bottleneck under heavy load  
- Limited scalability  
- Not suitable for cloud-native or large-scale distributed systems  

---

### 2. Hadoop Distributed File System (HDFS)

A distributed file system that splits large files into blocks and distributes them across multiple machines with replication.

#### Advantages:
- Highly scalable  
- Fault tolerant due to data replication  
- Supports parallel processing of large datasets  
- Efficient for Big Data analytics workloads  

#### Disadvantages:
- Inefficient for small files  
- Complex cluster setup and maintenance  
- Requires heavy infrastructure  
- Not well suited for modern cloud-native architectures  

---

## Block Storage

A storage model that provides raw storage blocks to be formatted and managed by the operating system.

#### Advantages:
- Very high performance and low latency  
- Ideal for databases and transactional systems  
- Full control over filesystem structure  

#### Disadvantages:
- Typically attached to a single instance at a time  
- Not optimized for massive-scale distributed data  
- More complex management compared to file storage  

---

## Object Storage

A storage system where data is stored as objects (data + metadata + unique identifier) inside buckets, accessed via APIs.

#### Advantages:
- Extremely scalable (billions of objects)  
- Highly durable with built-in replication  
- Cloud-native and distributed by design  
- Simple access via HTTP APIs  
- Suitable for both small and large data objects  

#### Disadvantages:
- Higher latency compared to block storage  
- Not compatible with traditional filesystem (POSIX) operations  
- Not ideal for low-latency transactional workloads  

---

# Task 2

## What is S3?

S3 is an object storage system and API used to store and retrieve data as objects inside buckets. Instead of using a traditional hierarchical file system, S3 organizes data in a flat structure where each object is identified by a unique key. It is designed to be highly scalable, durable, and accessible over HTTP using a REST-based interface.

Although S3 originated from Amazon’s Simple Storage Service, the S3 API has become a widely adopted standard, and many storage platforms implement S3-compatible interfaces for cloud and distributed environments.

---

# Task 3

A bucket is a logical container in an S3-based object storage system used to store objects (data and files). All objects must belong to a bucket, and each object is identified by a unique key within that bucket. Buckets are used to organize data and define configurations such as access permissions and storage policies. They serve as the top-level organizational unit in S3 storage.

---

# Task 4

No, S3 does not support real folders in the traditional filesystem sense. It uses a flat storage model where all data is stored as objects inside a bucket. What appears to be folders (for example, `images/cat.jpg`) is actually part of the object’s key.

The `/` character is only used to create logical prefixes that simulate a hierarchical structure. Any folder structure shown in user interfaces is merely a visual representation, while internally all objects exist in a flat namespace within the bucket.

---

# Task 5

Yes, there are size limits in S3-compatible object storage systems.

- Max object size is usually up to 5 TB  
- Files larger than ~5 GB use multipart upload  
- Buckets can store virtually unlimited data  

In Amazon S3 these limits are standard. Other S3-compatible systems like MinIO or Ceph may use similar limits, but they can vary by implementation.

In contrast, classic filesystems are limited by physical disk capacity and the filesystem design. They store data in a hierarchical structure of folders and files on a single machine or disk. Each filesystem has its own constraints, such as maximum file size, maximum number of files, and inode limits (which control how many files and directories can exist). Unlike object storage, filesystems are tightly tied to the underlying hardware.

---

# Task 6

Several implementations provide S3-compatible object storage. The original and most widely used implementation is Amazon S3 by Amazon Web Services. In addition, there are open-source and commercial alternatives such as MinIO, Ceph (via RADOS Gateway), and cloud providers like Google Cloud and DigitalOcean that offer S3-compatible APIs. These implementations allow applications to use the same S3 interface across different storage systems.