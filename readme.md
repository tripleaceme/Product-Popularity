**Case Study Title:**
📦 *Tracking Product Popularity in an E-commerce Platform*

**Background:**
Imagine you are the Analytics Engineer for a growing e-commerce marketplace, **ShopEase**, which operates in multiple states and offers thousands of products in various categories. The business wants to understand:

* Which products are the most popular
* How popularity changes over time
* Which states and categories contribute most to sales
* How seasonal trends affect product demand

**Challenge:**
You need to build a **real-time inspired analytics pipeline** that simulates order generation and answers business questions. The pipeline should:

* Generate realistic but **non-repeating** orders using a fixed product catalog
* Continuously add new customers and simulate orders every 3 hours
* Store data in MongoDB (or in S3 for the cloud version)
* Transform and model the data in Postgres/Snowflake using dbt
* Deliver actionable insights through Tableau dashboards

**Goal:**
Empower business teams to make data-driven decisions on:

* Inventory restocking
* Marketing campaigns per product & state
* Identifying underperforming categories

---

### **2. Data Model & Pipeline Flow**

```
Faker Script (Products, Customers, Orders)
     ↓ every 3 hours
MongoDB (Raw Orders)
     ↓ ETL Script (Python)
Postgres (Raw → Staging → Analytics Schema)
     ↓
dbt (Transformations & Metrics)
     ↓
Tableau (Dashboards)
```

---

### **3. Dashboard Questions & Metrics**


#### **Main Dashboard: Product Popularity Trends**

1. **Top Products**

   * Which products have been ordered the most in a given time period?
   * Metric: `Order Count` & `Total Quantity Ordered`
2. **Revenue Leaders**

   * Which products generate the most revenue?
   * Metric: `Total Sales = SUM(price * quantity)`
3. **Popularity Rank**

   * Show a rank column based on `Order Count` or `Total Sales`
4. **Category Performance**

   * Which categories dominate orders and sales?
5. **Trends Over Time**

   * Line chart of `Order Count` over time (day, month, year filter)

**Filters for this dashboard:**

* Year, Month, Product Category, Store/Branch

---

#### **Secondary Dashboard: Product Popularity by State**

1. **State-Level Map**

   * Quantity ordered per state
   * Total sales per state
2. **Product Drilldown**

   * Select a product → see how it performs across states
3. **Regional Popularity Rank**

   * Which products are #1 in each state?

**Filters for this dashboard:**

* Year, Month, Product Category, Product Name

---

#### **Possible Extra Insights**

* Repeat purchase rate per product
* New vs returning customers per product
* Seasonal product demand spikes
* Price sensitivity (changes in order count when price changes in simulation using dbt snaposhot)
