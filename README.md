# Guide to the Python Service Script

This guide details the operation of the Python service script and explains how to clone the repository and test it. The script was created to identify and mark duplicate services as inactive in a database.

## Script Operation

The Python script operates in several distinct stages, each with its specific functionality. We will highlight the most important parts of the code and explain their operation:

### Establishing a Connection to the Database

The script starts by establishing a connection to the database using the SQLAlchemy library. The `URL` environment variable is used to specify the database's URL. This is critical to ensure connectivity to the database.

```python
# Getting database URL
URL = os.environ.get('URL')

# Create a database engine using the specified URL
engine = create_engine(URL)
```

### Querying and Converting Database Data

The script queries active services from the database and orders them by case number and creation date. It then converts the query results into a list of dictionaries, mapping attributes to column names in the "tb_atendimento" table.

```python
# Query data from the tb_atendimento table
with session as sessao:
    try:
        # Query active services and order them by case and creation date
        services_query = sessao.query(Atendimento).filter(Atendimento.st_ativo == True).order_by(Atendimento.co_caso).order_by(Atendimento.dh_criacao)
        
        # Convert the result to a list of dictionaries using the `convert_dictionary` function
        services_duplicates = [convert_dictionary(data) for data in services_query.all()]
```

### Identifying and Marking Duplicate Services

The script identifies duplicate services within the same case, preventing data duplication in the database. To achieve this, it generates SQL statements to mark duplicate services as inactive. This part is crucial for maintaining data integrity in the database.

```python
for case in cases:
    # Create an empty list to store services related to a case
    services_of_case = []  

    # Add services related to the case to the list
    for service in services_duplicates:
        if service['co_caso'] == case:
            services_of_case.append(service)

    # Check if there are duplicate services
    if len(services_of_case) > 1: 

        # Create a set to store unique service texts
        unique_texts = set() 

        # Create a list to store duplicate services to be excluded
        services_excluded = []  

        for service in services_of_case:
            text = service['ds_atendimento']
            if text not in unique_texts:
                # Add the service's text to the set of unique texts
                unique_texts add(text)  
            else:
                # Add duplicate services to the list
                services_excluded.append(service)  

        # Check if there are duplicate services to be excluded
        if services_excluded:  
            for dado in services_excluded:
                with open('update_services.txt', 'a+') as arquivo:
                    text = f"UPDATE public.tb_atendimento SET st_ativo = FALSE WHERE co_seq_atendimento = {dado['co_seq_atendimento']}; \n"
                    
                    # Write SQL statements to mark services as inactive
                    arquivo.write(text)  
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
   git clone [Repository URL]
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
