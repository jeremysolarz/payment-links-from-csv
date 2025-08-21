# Payment Links from CSV

A Python script that automatically generates Stripe payment links from a CSV file containing product information. This tool reads product data from a CSV file, creates corresponding Stripe products and prices, and generates payment links for each item.

## Features

- 🔗 Automatically creates Stripe payment links for products in bulk
- 📊 Reads product data from CSV files
- 💰 Supports USD pricing (easily configurable for other currencies)
- 📝 Preserves all original CSV data as metadata in Stripe
- ✅ Error handling for invalid data and API failures
- 📄 Outputs results to a new CSV file with payment link URLs

## Prerequisites

- Python 3.6 or higher
- A Stripe account with API access
- Stripe secret API key

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd payment-links-from-csv
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Stripe API Key

Set your Stripe secret API key as an environment variable:

```bash
export STRIPE_API_KEY="sk_test_..."
```

Alternatively, you can modify the script to hard-code your API key (not recommended for production):

```python
stripe.api_key = "your_stripe_secret_key"
```

### File Configuration

By default, the script looks for:
- Input file: `products.csv`
- Output file: `payment_links.csv`

You can modify these filenames in the script by changing the `INPUT_CSV_FILE` and `OUTPUT_CSV_FILE` variables.

## CSV File Format

Your input CSV file should contain at least the following columns:

| Column | Required | Description |
|--------|----------|-------------|
| `name` | Yes | The name of the product or service |
| `amount_usd` | Yes | The price in USD (e.g., 15.99) |

Additional columns are optional and will be preserved as metadata in Stripe.

### Example CSV (`products.csv`):

```csv
name,amount_usd,customer_id,order_number
Product A,15.99,cust_123,ORD-001
Service B,50.00,cust_456,ORD-002
Consultation,120.00,cust_789,ORD-003
```

## Usage

1. Prepare your `products.csv` file with the required format
2. Set your Stripe API key as an environment variable
3. Run the script:

   ```bash
   python script.py
   ```

4. The script will:
   - Read your CSV file
   - Create Stripe products and prices
   - Generate payment links
   - Output results to `payment_links.csv`

## Output

The script generates a new CSV file (`payment_links.csv`) containing all original data plus a new `payment_link_url` column with the generated Stripe payment links.

### Example Output:

```csv
name,amount_usd,customer_id,order_number,payment_link_url
Product A,15.99,cust_123,ORD-001,https://buy.stripe.com/test_...
Service B,50.00,cust_456,ORD-002,https://buy.stripe.com/test_...
```

## Error Handling

The script includes comprehensive error handling:

- ❌ Invalid amounts are skipped with warnings
- ❌ Stripe API errors are caught and logged
- ❌ Missing CSV files result in clear error messages
- ✅ Successfully created payment links are marked with checkmarks

## Customization

### Currency

To use a different currency, modify the `currency` parameter in the `create_payment_link` function:

```python
price = stripe.Price.create(
    unit_amount=amount_in_cents,
    currency="eur",  # Change from "usd" to your preferred currency
    product=product.id,
)
```

### Metadata

All CSV columns are automatically included as metadata in Stripe objects. This allows you to track additional information like customer IDs, order numbers, etc.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the license file for details.

## Support

If you encounter any issues or have questions:

1. Check that your Stripe API key is correctly set
2. Verify your CSV file format matches the requirements
3. Review the console output for specific error messages

## Security Notes

- Never commit your Stripe API keys to version control
- Use environment variables for sensitive configuration
- Test with Stripe's test keys before using live keys
- Regularly rotate your API keys as a security best practice
