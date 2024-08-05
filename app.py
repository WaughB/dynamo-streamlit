import streamlit as st
import boto3
from botocore.exceptions import BotoCoreError, ClientError, EndpointConnectionError
from boto3.dynamodb.conditions import Key
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize DynamoDB client for local DynamoDB
try:
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url="http://localhost:8000",  # URL for the local DynamoDB service
        region_name="us-west-2",  # Specify any region, required by boto3 but ignored by local DynamoDB
        aws_access_key_id="223344",  # Dummy values
        aws_secret_access_key="dummy-secret-key",
    )
    logger.info("Connected to DynamoDB successfully.")
except EndpointConnectionError as e:
    logger.error(
        "Could not connect to DynamoDB. Please ensure the service is running: %s", e
    )
    st.error("Could not connect to DynamoDB. Please ensure the service is running.")
    st.stop()
except BotoCoreError as e:
    logger.error("BotoCoreError occurred: %s", e)
    st.error(
        "An error occurred with the AWS SDK. Please check the logs for more details."
    )
    st.stop()


def create_products_table():
    try:
        table = dynamodb.create_table(
            TableName="Products",
            KeySchema=[{"AttributeName": "Id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "Id", "AttributeType": "N"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        table.wait_until_exists()
        logger.info("Products table created or already exists.")
        return table
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        # Table already exists
        logger.info("Products table already exists.")
        return dynamodb.Table("Products")
    except ClientError as e:
        logger.error("ClientError occurred when creating table: %s", e)
        st.error(
            "Failed to create or access the Products table. Check AWS permissions and configuration."
        )
        st.stop()
    except BotoCoreError as e:
        logger.error("BotoCoreError occurred when creating table: %s", e)
        st.error(
            "An error occurred with the AWS SDK. Please check the logs for more details."
        )
        st.stop()


def get_products():
    try:
        response = table.scan()
        logger.info("Successfully retrieved products from DynamoDB.")
        return response["Items"]
    except ClientError as e:
        logger.error("ClientError occurred when retrieving products: %s", e)
        st.error("Error retrieving products. Please try again later.")
        return []
    except BotoCoreError as e:
        logger.error("BotoCoreError occurred when retrieving products: %s", e)
        st.error("An error occurred while accessing DynamoDB. Please try again later.")
        return []


def add_product(product_id, name, price):
    try:
        table.put_item(Item={"Id": int(product_id), "Name": name, "Price": int(price)})
        logger.info(
            "Product added successfully: ID=%s, Name=%s, Price=%s",
            product_id,
            name,
            price,
        )
    except ClientError as e:
        logger.error("ClientError occurred when adding product: %s", e)
        st.error("Error adding product. Please check your input and try again.")
    except BotoCoreError as e:
        logger.error("BotoCoreError occurred when adding product: %s", e)
        st.error("An error occurred while accessing DynamoDB. Please try again later.")


# Streamlit UI
st.title("Product Catalog")

menu = ["View Products", "Add Product"]
choice = st.sidebar.selectbox("Menu", menu)

# Ensure table exists
table = create_products_table()

if choice == "View Products":
    st.subheader("Products List")
    products = get_products()
    if products:
        for product in products:
            st.write(
                f"ID: {product['Id']} | Name: {product['Name']} | Price: ${product['Price']}"
            )
    else:
        st.info("No products available.")

elif choice == "Add Product":
    st.subheader("Add New Product")
    product_id = st.text_input("Product ID")
    name = st.text_input("Product Name")
    price = st.text_input("Product Price")

    if st.button("Add Product"):
        if product_id and name and price:
            try:
                int(product_id)  # Validate ID is an integer
                float(price)  # Validate Price is a number
                add_product(product_id, name, price)
                st.success("Product added successfully!")
            except ValueError:
                st.error(
                    "Invalid input. Ensure that the ID is an integer and the price is a number."
                )
        else:
            st.error("Please fill all fields.")
