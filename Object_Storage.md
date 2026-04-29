# בס"ד

# Object Storage

## First mission

In modern distributed systems, data storage plays a critical role in ensuring performance, scalability, and reliability. As applications grow and operate across multiple machines, different types of distributed storage solutions have been developed to meet various needs. The three main types are Object Storage, File Storage, and Block Storage. Each type is designed for specific use cases and offers different advantages and limitations. Now, we will elaborate on each of them.

---

## Object Storage

Object storage is designed to store large amounts of unstructured data such as images, videos, backups, and logs. Instead of organizing data in folders, it stores data as objects, each with a unique identifier and metadata. It is mainly used in cloud environments and accessed via APIs.

### Advantages

- Highly scalable (can store massive amounts of data)
- Very reliable due to built-in replication
- Accessible from anywhere via the internet
- Cost-effective for large-scale storage
- Ideal for cloud-native applications

### Disadvantages

- Higher latency compared to other storage types
- Not suitable for applications requiring frequent small updates
- Cannot be mounted like a traditional filesystem
- Limited support for complex file operations

---

## File Storage

File storage is designed to store and manage data in a hierarchical structure (folders and files). Distributed file systems allow multiple machines to access shared files, making them suitable for collaborative environments and big data processing.

### Advantages

- Easy to understand and use (similar to local filesystems)
- Supports shared access across multiple users and systems
- Good for structured file organization
- Suitable for big data processing

### Disadvantages

- Limited scalability compared to object storage
- Can suffer from performance bottlenecks
- More complex to maintain in large distributed systems
- Not fully optimized for cloud-native environments

---

## Block Storage

Block storage divides data into fixed-size blocks and stores them separately. It is commonly used for databases, virtual machines, and applications that require high performance and low latency.

### Advantages

- Very high performance and low latency
- Ideal for databases and transactional systems
- Flexible and efficient for frequent read/write operations
- Can be used like a traditional disk

### Disadvantages

- More complex to manage
- Does not include metadata like object storage
- Less scalable compared to object storage
- Typically more expensive

---

## Second mission

## What is S3?

Amazon S3 (Simple Storage Service) is a cloud-based storage service provided by Amazon Web Services (AWS). It is designed to store and retrieve large amounts of data from anywhere on the internet, at any time.

S3 is based on the concept of object storage, meaning that data is stored as objects rather than in a traditional file system or block storage format. Each object consists of the data itself, a unique identifier (key), and metadata that describes the object.

## How S3 Works

S3 organizes data using three main components:

- Buckets – Containers used to store objects. Each bucket has a unique name.
- Objects – The actual data (such as files, images, or videos).
- Keys – Unique identifiers for objects within a bucket.

Although keys may look like file paths (for example: `images/photo.jpg`), S3 does not use a true hierarchical file system.

## Key Features

- Scalability: S3 can store virtually unlimited amounts of data.
- Durability: Data is automatically replicated across multiple servers to prevent data loss.
- Availability: Data can be accessed from anywhere via the internet.
- Security: Supports access control, encryption, and authentication.
- Integration: Works well with many other AWS services.

## Common Use Cases

- Storing images, videos, and static website content
- Backup and recovery solutions
- Data archiving
- Big data analytics and data lakes
- Application data storage

## Advantages

- Easy to use and manage
- Highly scalable and reliable
- No need to maintain physical storage infrastructure
- Cost-effective for large-scale storage

## Disadvantages

- Higher latency compared to local or block storage
- Costs can increase with heavy usage
- Not suitable for applications requiring frequent small updates
- Not a replacement for databases or traditional file systems

---

## Third mission

## What is a Bucket?

In object storage systems such as Amazon S3, a bucket is a top-level logical container used to store and organize data objects (files and their metadata).

A bucket can be thought of as a storage namespace or repository where all objects are stored. Unlike traditional file systems, buckets do not use a true hierarchical folder structure. Instead, all data is stored in a flat structure, and any folder-like organization is simulated using object keys (names).

Each bucket must have a globally unique name within the storage system, ensuring that no two users can create buckets with the same name.

## Key Characteristics of a Bucket

- Top-level container: Used to store all objects in object storage systems.
- Flat structure: Does not contain real folders; hierarchy is simulated using object keys.
- Globally unique name: Each bucket name must be unique across the entire system.
- Access control: Permissions can be configured at the bucket level to control who can read, write, or manage data.
- Region-based storage: Each bucket is created in a specific geographic region for performance and compliance reasons.

## Purpose of a Bucket

Buckets are essential for organizing and managing data in cloud storage systems. They provide a logical separation between different datasets, applications, or users, while enabling scalability, security, and centralized management of stored objects.

---

## Fourth mission

## Does the concept of folders exist in S3?

In Amazon S3, the concept of traditional folders does not truly exist.

S3 is an object storage system, which means all data is stored as objects inside a bucket in a flat structure. There is no real hierarchical file system like in a local computer or traditional file storage systems.

However, S3 provides a way to simulate folders using object keys (names). For example, an object named:

`images/cat.jpg`

may appear as if it is inside a folder called images, but in reality:

- There is no actual folder called images.
- The entire string `images/cat.jpg` is just the object’s key (its name).
- S3 simply interprets the `/` character as a visual separator to help users organize data more intuitively.

## Conclusion

Folders do not exist in a real, physical sense in Amazon S3. Instead, folder-like structures are only a logical representation created by naming conventions, while all data is stored as objects in a flat namespace.

---

## Fifth mission

In Amazon S3, there are practical size limits, but they are extremely large compared to traditional systems, making them effectively suitable for large-scale storage needs.

## Size limitations in S3

S3 allows objects (files) to be very large, up to multiple terabytes per object. In addition, there is virtually no limit on the total amount of data that can be stored in a bucket, as the system is designed to scale horizontally across distributed infrastructure.

However, instead of strict physical limits like in traditional systems, S3 limits are mainly defined by service design and API constraints rather than hardware capacity.

## Comparison with a classic filesystem

In a classic filesystem (such as NTFS or ext4):

- Storage is limited by the physical disk size.
- File size limits are usually smaller (compared to cloud systems).
- Scaling requires adding or upgrading hardware.
- Performance can degrade as storage grows large.

In contrast, S3:

- Is not bound to a single physical machine.
- Scales automatically across many servers.
- Supports extremely large objects and massive total storage capacity.
- Is designed for distributed, cloud-native environments.

## Conclusion

While both systems have size limitations, Amazon S3 offers significantly higher scalability and virtually unlimited storage capacity compared to classic filesystems, which are constrained by physical hardware and local disk limitations.

---

## Sixth mission

There isn’t just one implementation of S3—what people usually mean by “S3” is the API that was introduced by Amazon Web Services with Amazon S3. Many systems implement that same API (or something very close), so they can act like S3-compatible storage.

Here are the main types of S3 implementations:

## 1. Official implementation

### Amazon S3

- The original and most widely used
- Fully managed cloud object storage
- Highly scalable, durable, and integrated with AWS services

## 2. Self-hosted (S3-compatible) implementations

These let you run your own S3-like storage:

### MinIO

- Very popular, lightweight, high-performance
- Fully S3-compatible API

### Ceph (RADOS Gateway)

- Large-scale distributed storage system
- Provides S3-compatible access via a gateway

### OpenStack Swift

- Native API is different, but can be used similarly
- Often deployed in private clouds

### SeaweedFS

- Lightweight distributed storage with S3 API support

## 3. Cloud providers with S3-compatible APIs

Other companies offer S3-like services (often cheaper or specialized):

- Google Cloud Storage
- Azure Blob Storage
- Wasabi
- Backblaze B2
- DigitalOcean Spaces

(Some are fully S3-compatible, others are partially compatible or have their own APIs.)

## 4. Development / local testing implementations

Used for development without real cloud usage:

- LocalStack
- Moto

---

## Seventh mission

This command deploys a local instance of MinIO using Docker. The container is successfully started, and the service is accessible via API on port 9000 and through the web console on port 9001.
![Docker Command](./images/image.png)
