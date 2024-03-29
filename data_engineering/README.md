# Data Engineering Projects

## 1. Online Retail Data - Retail Project

**Dataset**: https://www.kaggle.com/datasets/tunguz/online-retail

| Column | Description |
| --- | --- |
| InvoiceNo | Invoice number. Nominal, a 6-digit integral number uniquely assigned to each transaction. If this code starts with letter 'c', it indicates a cancellation. |
| StockCode | Product (item) code. Nominal, a 5-digit integral number uniquely assigned to each distinct product. |
| Description | Product (item) name. Nominal. |
| Quantity | The quantities of each product (item) per transaction. Numeric. |
| InvoiceDate | Invice Date and time. Numeric, the day and time when each transaction was generated. |
| UnitPrice | Unit price. Numeric, Product price per unit in sterling. |
| CustomerID | Customer number. Nominal, a 5-digit integral number uniquely assigned to each customer. |
| Country | Country name. Nominal, the name of the country where each customer resides. |	

**Pipeline**
![Pipeline](https://github.com/shahy-48/laughing-pancake/tree/main/data_engineering/docs/images/de_pipeline_retail.png)

**Data Model**
![Data Model ERD](https://github.com/shahy-48/laughing-pancake/tree/main/data_engineering/docs/images/de_pipeline_retail.png)