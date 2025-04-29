# Amazon-DE-version1.0
 The first version of Amazon Data Analyst. Including ETL pipeline, scraping data.


### System Overview

The system begins by collecting data from a list of product categories on Amazon. It then proceeds to extract detailed information for each product gathered during the initial step.

### Data Processing Pipeline

Once the data is collected, it enters a processing pipeline where several key operations are performed, including:

- **Data Mapping and Standardization**: Ensuring the data is in a consistent format across various sources.
- **Data Deduplication**: Identifying and removing duplicate records to maintain data integrity.
- **Empty Data Removal**: Eliminating rows with missing or incomplete information to improve data quality.
- **New Column Generation**: Creating additional calculated or derived columns as needed for enhanced analysis.

### Data Storage and Schema Design

The processed data is then stored in a data warehouse, utilizing a **star schema** design. This schema structure facilitates efficient multidimensional analysis via OLAP (Online Analytical Processing) and is optimized for various business intelligence purposes.


