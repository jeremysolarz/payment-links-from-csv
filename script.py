import csv
import stripe
import os

# --- Configuration ---
# Set your Stripe secret API key.
# This can be set as an environment variable for security:
# os.environ['STRIPE_API_KEY'] = 'your_stripe_secret_key'
# Or you can hard-code it here for testing (not recommended for production):
stripe.api_key = os.environ.get('STRIPE_API_KEY')

# Define the input and output file names
INPUT_CSV_FILE = 'products.csv'
OUTPUT_CSV_FILE = 'payment_links.csv'

# --- CSV File Setup ---
# The input CSV file should have at least the following columns:
# 'name': The name of the product or item.
# 'amount_usd': The price of the item in USD. Other currencies can be used.

# Example of `products.csv` content:
# name,amount_usd,customer_id,order_number
# Product A,15.99,cust_123,ORD-001
# Service B,50.00,cust_456,ORD-002


def create_payment_link(product_name, amount_usd, metadata):
    """
    Creates a Stripe payment link for a given product and attaches metadata.
    The amount should be in the currency's smallest unit (e.g., cents for USD).
    """
    try:
        # Convert the amount to cents (integer)
        amount_in_cents = int(amount_usd * 100)

        # Create a product in Stripe. This is a prerequisite for creating
        # a price.
        # This will deduplicate products based on their name.
        product = stripe.Product.create(name=product_name, metadata=metadata)

        # Create a price for the product.
        price = stripe.Price.create(
            unit_amount=amount_in_cents,
            currency="eur",
            product=product.id,
        )

        # Create the payment link using the price ID.
        payment_link = stripe.PaymentLink.create(
            line_items=[
                {
                    "price": price.id,
                    "quantity": 1,
                },
            ],
            metadata=metadata,
            payment_intent_data={
                "metadata": metadata,
                "description": product_name,
            }
        )

        print(f"✅ Created payment link for '{product_name}'")
        return payment_link.url

    except stripe.error.StripeError as e:
        print(f"❌ Error creating payment link for '{product_name}': {e}")
        return None


def main():
    """
    Main function to read the CSV, create payment links, and write them
    to a new CSV.
    """
    payment_links_data = []

    try:
        with open(INPUT_CSV_FILE, mode='r', newline='',
                  encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            
            # Get the fieldnames from the input CSV
            fieldnames = reader.fieldnames if reader.fieldnames else []
            
            # Prepare fieldnames for the output CSV
            output_fieldnames = fieldnames + ['payment_link_url']

            for row in reader:
                # Get the name and amount, converting amount to a float
                name = row.get('name')
                try:
                    amount_usd = float(row.get('amount_usd', '0'))
                except (ValueError, TypeError):
                    print(f"⚠️ Skipping row due to invalid amount: {row}")
                    continue

                # Create the metadata dictionary from the entire row
                # Stripe metadata keys must be strings.
                metadata = {key: str(value) for key, value in row.items()}
                
                # Create the payment link
                payment_link_url = create_payment_link(
                    name, amount_usd, metadata)
                
                if payment_link_url:
                    row['payment_link_url'] = payment_link_url
                    payment_links_data.append(row)

    except FileNotFoundError:
        print(f"Error: The file '{INPUT_CSV_FILE}' was not found.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    # Write the new CSV file with the generated links
    if payment_links_data:
        try:
            with open(OUTPUT_CSV_FILE, mode='w', newline='',
                      encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=output_fieldnames)
                writer.writeheader()
                writer.writerows(payment_links_data)
            print(f"🎉 Successfully wrote all payment links to "
                  f"'{OUTPUT_CSV_FILE}'")
        except Exception as e:
            print(f"Error writing to file '{OUTPUT_CSV_FILE}': {e}")
    else:
        print("No payment links were created. Check your input CSV and "
              "API key.")


if __name__ == "__main__":
    main()