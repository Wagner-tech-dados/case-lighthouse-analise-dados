-- Schema gerado automaticamente a partir dos arquivos CSV
-- Banco de destino: PostgreSQL
-- Nenhum dado foi limpo, corrigido ou removido neste processo.

-- Tabela originada do arquivo: addresses.csv
CREATE TABLE IF NOT EXISTS "addresses" (
    "id" INTEGER,
    "customer_id" INTEGER,
    "address_type" TEXT,
    "postal_code" TEXT,
    "street" TEXT,
    "number" INTEGER,
    "complement" TEXT,
    "district" TEXT,
    "city" TEXT,
    "state" TEXT,
    "country" TEXT,
    "is_primary" BOOLEAN
);

-- Tabela originada do arquivo: attributes.csv
CREATE TABLE IF NOT EXISTS "attributes" (
    "id" INTEGER,
    "name" TEXT,
    "data_type" TEXT
);

-- Tabela originada do arquivo: brands.csv
CREATE TABLE IF NOT EXISTS "brands" (
    "id" INTEGER,
    "name" TEXT,
    "country" TEXT,
    "is_active" BOOLEAN,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP
);

-- Tabela originada do arquivo: categories.csv
CREATE TABLE IF NOT EXISTS "categories" (
    "id" INTEGER,
    "name" TEXT,
    "slug" TEXT,
    "parent_category_id" INTEGER,
    "is_active" BOOLEAN,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP
);

-- Tabela originada do arquivo: customers.csv
CREATE TABLE IF NOT EXISTS "customers" (
    "id" INTEGER,
    "person_type" TEXT,
    "legal_name" TEXT,
    "trade_name" TEXT,
    "tax_id" INTEGER,
    "state_registration" TEXT,
    "email" TEXT,
    "phone" TEXT,
    "is_active" BOOLEAN,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP
);

-- Tabela originada do arquivo: employees.csv
CREATE TABLE IF NOT EXISTS "employees" (
    "id" INTEGER,
    "full_name" TEXT,
    "cpf" INTEGER,
    "email" TEXT,
    "role" TEXT,
    "primary_location_id" INTEGER,
    "hire_date" TIMESTAMP,
    "termination_date" TIMESTAMP,
    "is_active" BOOLEAN,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP
);

-- Tabela originada do arquivo: fiscal_invoices.csv
CREATE TABLE IF NOT EXISTS "fiscal_invoices" (
    "id" INTEGER,
    "order_id" INTEGER,
    "nfe_number" TEXT,
    "nfe_access_key" INTEGER,
    "series" INTEGER,
    "issued_at" TIMESTAMP,
    "status" TEXT,
    "total_amount" REAL,
    "xml_storage_uri" TEXT,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP
);

-- Tabela originada do arquivo: goods_receipt_items.csv
CREATE TABLE IF NOT EXISTS "goods_receipt_items" (
    "id" INTEGER,
    "goods_receipt_id" INTEGER,
    "purchase_order_item_id" INTEGER,
    "quantity_received" REAL
);

-- Tabela originada do arquivo: goods_receipts.csv
CREATE TABLE IF NOT EXISTS "goods_receipts" (
    "id" INTEGER,
    "purchase_order_id" INTEGER,
    "received_by_employee_id" INTEGER,
    "received_at" TIMESTAMP,
    "notes" TEXT,
    "created_at" TIMESTAMP
);

-- Tabela originada do arquivo: locations.csv
CREATE TABLE IF NOT EXISTS "locations" (
    "id" INTEGER,
    "name" TEXT,
    "location_type" TEXT,
    "postal_code" TEXT,
    "street" TEXT,
    "number" INTEGER,
    "complement" TEXT,
    "district" TEXT,
    "city" TEXT,
    "state" TEXT,
    "country" TEXT,
    "is_active" BOOLEAN,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP
);

-- Tabela originada do arquivo: order_items.csv
CREATE TABLE IF NOT EXISTS "order_items" (
    "id" INTEGER,
    "order_id" INTEGER,
    "product_variant_id" INTEGER,
    "quantity" INTEGER,
    "unit_price" REAL,
    "icms_rate" REAL,
    "ipi_rate" REAL,
    "line_total" REAL
);

-- Tabela originada do arquivo: orders.csv
CREATE TABLE IF NOT EXISTS "orders" (
    "id" INTEGER,
    "order_number" TEXT,
    "channel" TEXT,
    "customer_id" INTEGER,
    "salesperson_id" INTEGER,
    "location_id" INTEGER,
    "status" TEXT,
    "subtotal" REAL,
    "discount_amount" REAL,
    "total" REAL,
    "placed_at" TIMESTAMP,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP
);

-- Tabela originada do arquivo: payments.csv
CREATE TABLE IF NOT EXISTS "payments" (
    "id" INTEGER,
    "order_id" INTEGER,
    "method" TEXT,
    "installments" INTEGER,
    "amount" REAL,
    "status" TEXT,
    "paid_at" TIMESTAMP,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP
);

-- Tabela originada do arquivo: product_suppliers.csv
CREATE TABLE IF NOT EXISTS "product_suppliers" (
    "product_variant_id" INTEGER,
    "supplier_id" INTEGER,
    "supplier_sku" TEXT,
    "last_quoted_cost" REAL,
    "lead_time_days" INTEGER,
    "is_preferred" BOOLEAN,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP
);

-- Tabela originada do arquivo: product_variants.csv
CREATE TABLE IF NOT EXISTS "product_variants" (
    "id" INTEGER,
    "product_id" INTEGER,
    "sku" TEXT,
    "barcode_ean" INTEGER,
    "sale_price" REAL,
    "cost_price" REAL,
    "weight_kg" REAL,
    "icms_rate" REAL,
    "ipi_rate" REAL,
    "is_active" BOOLEAN,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP
);

-- Tabela originada do arquivo: products.csv
CREATE TABLE IF NOT EXISTS "products" (
    "id" INTEGER,
    "name" TEXT,
    "description" TEXT,
    "brand_id" INTEGER,
    "category_id" INTEGER,
    "ncm_code" INTEGER,
    "unit_of_measure" TEXT,
    "is_active" BOOLEAN,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP
);

-- Tabela originada do arquivo: purchase_order_items.csv
CREATE TABLE IF NOT EXISTS "purchase_order_items" (
    "id" INTEGER,
    "purchase_order_id" INTEGER,
    "product_variant_id" INTEGER,
    "quantity_ordered" INTEGER,
    "unit_cost" REAL,
    "line_total" REAL
);

-- Tabela originada do arquivo: purchase_orders.csv
CREATE TABLE IF NOT EXISTS "purchase_orders" (
    "id" INTEGER,
    "po_number" TEXT,
    "supplier_id" INTEGER,
    "buyer_id" INTEGER,
    "destination_location_id" INTEGER,
    "status" TEXT,
    "currency" TEXT,
    "subtotal" REAL,
    "total" REAL,
    "placed_at" TIMESTAMP,
    "expected_delivery_at" TIMESTAMP,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP
);

-- Tabela originada do arquivo: return_items.csv
CREATE TABLE IF NOT EXISTS "return_items" (
    "id" INTEGER,
    "return_id" INTEGER,
    "order_item_id" INTEGER,
    "quantity" REAL,
    "action" TEXT,
    "exchange_variant_id" INTEGER,
    "unit_refund_amount" REAL
);

-- Tabela originada do arquivo: returns.csv
CREATE TABLE IF NOT EXISTS "returns" (
    "id" INTEGER,
    "return_number" TEXT,
    "order_id" INTEGER,
    "customer_id" INTEGER,
    "received_at_location_id" INTEGER,
    "status" TEXT,
    "reason" TEXT,
    "total_refund_amount" REAL,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP
);

-- Tabela originada do arquivo: stock_levels.csv
CREATE TABLE IF NOT EXISTS "stock_levels" (
    "product_variant_id" INTEGER,
    "location_id" INTEGER,
    "quantity_on_hand" REAL,
    "reorder_point" TEXT,
    "updated_at" TIMESTAMP
);

-- Tabela originada do arquivo: stock_movements.csv
CREATE TABLE IF NOT EXISTS "stock_movements" (
    "id" INTEGER,
    "product_variant_id" INTEGER,
    "location_id" INTEGER,
    "movement_type" TEXT,
    "quantity" REAL,
    "reference_table" TEXT,
    "reference_id" INTEGER,
    "employee_id" INTEGER,
    "notes" TEXT,
    "occurred_at" TIMESTAMP,
    "created_at" TIMESTAMP
);

-- Tabela originada do arquivo: suppliers.csv
CREATE TABLE IF NOT EXISTS "suppliers" (
    "id" INTEGER,
    "legal_name" TEXT,
    "trade_name" TEXT,
    "country" TEXT,
    "tax_id" TEXT,
    "tax_id_type" TEXT,
    "email" TEXT,
    "phone" INTEGER,
    "contact_name" TEXT,
    "is_active" BOOLEAN,
    "created_at" TIMESTAMP,
    "updated_at" TIMESTAMP
);

-- Tabela originada do arquivo: variant_attribute_values.csv
CREATE TABLE IF NOT EXISTS "variant_attribute_values" (
    "product_variant_id" INTEGER,
    "attribute_id" INTEGER,
    "value" TEXT
);
