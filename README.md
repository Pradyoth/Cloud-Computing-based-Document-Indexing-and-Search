# Datacenter Scale Computing Project

#### Title : Document Indexing and Search in an E-Learning Platform

#### Team Members: Vandana Sridhar, Pradyoth Srinivasan

#### Project Overview:

This system helps users search and access resources such as e-books and other documents and additionally helps upload and store resource materials. Given a user query, this application helps in finding the appropriate and relevant resources.

For this project, we utilized REST APIs, message queues, key-value stores,Cloud storage services and virtual machines to construct our application. Additionally we incorporated the Elasticsearch service to a major portion of our application to facilitate our search and indexing platform.

#### Project Components:

1. Flask REST server – API endpoints / REST interface
2. RabbitMQ -  message/Task queue
3. Redis -  Key-value store
4. Google Cloud Storage – document store
5. Compute Engine – Virtual machines to host services
6. Elasticsearch – Index & Search facilitation


#### Process to create the Virtual Machines:

#### REST/REDIS/RABBITMQ

We programmatically constructed the virtual machines for these services.
All of the three folders ie rest, redis and RabbitMQ in the repository have a program along with their configurations and install scripts to install the virtual machine apppropriately.
To create a VM instance for either of three services[once you're in the respective directory] run:

```python3 create_instance.py```

#### WORKER NODE:

We manually constructed the virtual machine for worker through the **Google Cloud Platform**.
In google cloud platform: compute -> compute engine -> VM instances -> create

The specifications of the worker node are:

1. Ubuntu 18.04
2.region : us-central1(Iowa)
3. Zone: us-central1-b
4. Machine Type: n1-standard-2
5. Allow all http traffic under firewall
6. Set the instance's external IP to be none

Next, to install **Elasticsearch** into the worker, we referred to the following links:

https://linuxconfig.org/how-to-install-java-on-ubuntu-18-04-bionic-beaver-linux - To install JDK
https://tecadmin.net/setup-elasticsearch-on-ubuntu/ - Install Elasticsearch

#### How to Run the Program:

SSH into the REST and Worker instance and upload `client.py, server.py` and the remaining text files into the REST terminal.On the worker, upload `worker.py` . Create two terminals for REST and two for the Worker.

**Note** : Create a bucket on google cloud storage with your credentials and set the file access policy of your bucket to public.

Run `python3 client.py <endpoint-name>` [endpoint name = index|search] and `python3 server.py` on individual REST terminals and execute the worker program `python3 worker.py` on the worker consoles. We have two consoles for the worker to validate the task distribution process of the RabbitMQ task channel.










