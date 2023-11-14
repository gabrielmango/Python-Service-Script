# Guide to the Python Service Script

This guide details the operation of the Python service script and explains how to clone the repository and test it. The script was created to identify and mark duplicate services as inactive in a database.

## Script Operation

The Python script operates in several distinct stages, each with its specific functionality. We will highlight the most important parts of the code and explain their operation:

### Establishing a Connection to the Database

The script starts by establishing a connection to the database using the SQLAlchemy library. The `URL` environment variable is used to specify the database's URL. This is critical to ensure connectivity to the database.


### Querying and Converting Database Data

The script queries active services from the database and orders them by case number and creation date. It then converts the query results into a list of dictionaries, mapping attributes to column names in the "tb_atendimento" table.


### Identifying and Marking Duplicate Services

The script identifies duplicate services within the same case, preventing data duplication in the database. To achieve this, it generates SQL statements to mark duplicate services as inactive. This part is crucial for maintaining data integrity in the database.

```python
unique_texts = set()
services_excluded = []

if services_list:
    for service in services_list:
        text = service[1]

        if text not in unique_texts:
            unique_texts.add(text)
        else:
            services_excluded.append(service)
    return services_excluded  
```

## Cloning the Repository

To clone the repository and run the script, follow these steps:

1. Open a terminal or command prompt.

2. Navigate to the folder where you want to clone the repository using the `cd` command:

   ```
   cd /path/to/your/folder
   ```

3. Clone the repository using the provided link:

   ```
   git clone https://github.com/gabrielmango/Python-Service-Script.git
   ```

## Preparing the Environment

Before running the script, ensure you have the following prerequisites:

- Python installed on your system.
- Install packages:

```
pip install -r requirements.txt
```

## Running the Script

Now that you have cloned the repository and prepared the environment, follow these steps to run the script:

1. Open a terminal or command prompt.

2. Navigate to the cloned repository folder:

   ```
   cd /path/to/repository/folder
   ```

3. Run the Python script:

   ```
   python main.py
   ```

The script will run and process the data in the database.

## Results

After successfully running the script, a file named `update_services.txt` will be generated in the repository folder. This file contains SQL statements to mark duplicate services as inactive in the database.

Please note that this guide assumes you have properly configured the `URL` environment variable for the database connection. Ensure you provide the database URL in your environment before running the script.

## License

This script is made available under the [MIT License](https://opensource.org/licenses/MIT). You are free to use, modify, and distribute this code in accordance with the terms of the license.

This concludes the guide to the Python service script, highlighting the important parts of the code and explaining its operation, along with the inclusion of the MIT License. You should now have a better understanding of how the script operates and how to clone the repository for testing. Make sure to review the script's source code and database settings before running it in a production environment.
