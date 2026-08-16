# ShopNest Pro — Complete Step-by-Step Implementation & Setup Guide

---

## 1. What This Guide Does

This guide provides an **exhaustive, beginner-friendly, step-by-step tutorial** for setting up, running, configuring, testing, and understanding the **ShopNest Pro** e-commerce platform.

Even if you have minimal programming experience, following this guide from start to finish will enable you to:
1. Install all prerequisite software on your computer.
2. Set up a dedicated Python virtual environment.
3. Install required packages without conflicts.
4. Initialize the SQLite database and seed 63+ catalog products.
5. Launch the local web server and use the application in your browser.
6. Understand the architecture, source code files, and data flow.
7. Successfully demonstrate the project to a teacher or examiner during a viva.

---

## 2. Before You Start

### System Requirements
- **Supported Operating Systems**:
  - Windows 10 / Windows 11 (64-bit)
  - macOS 12 (Monterey) or newer
  - Linux (Ubuntu 20.04+, Debian 11+, Fedora, Arch)
- **Processor**: Intel Core i3 / AMD Ryzen 3 or higher.
- **RAM**: Minimum 4 GB (8 GB recommended).
- **Free Disk Space**: Approximately 500 MB (includes Python, dependencies, database, and media files).
- **Internet Connection**: Required only during initial software and dependency downloads. Once installed, the application runs **100% offline**.

---

## 3. Understanding the Project

ShopNest Pro is composed of three primary layers:

```
[ Frontend: HTML5 + CSS3 Glassmorphism + Bootstrap 5 + ES6 JavaScript ]
                                ▲ │
                     HTTP / AJAX│ │JSON / HTML Responses
                                │ ▼
          [ Backend: Python 3.11 + Django 5.2 Framework ]
                                ▲ │
                        ORM /   │ │SQL Queries
                     Transactions│ ▼
             [ Database & Storage: SQLite3 (db.sqlite3) ]
```

1. **Frontend**:
   - Written in semantic **HTML5** and **Vanilla CSS3** with a custom Glassmorphic design system (`backdrop-filter: blur(28px)`).
   - Uses **Bootstrap 5.3.3** for grid layouts, modal dialogs, and responsive navbar collapse.
   - Uses native **JavaScript (Fetch API)** for asynchronous add-to-cart, wishlist toggling, and theme switching without page reloads.
2. **Backend**:
   - Built on **Django 5.2**, handling URL routing, authentication, session state, financial calculations, and views.
   - Uses **Python's `Decimal` module** for all price arithmetic to eliminate floating-point rounding errors.
3. **Database**:
   - Uses **SQLite3** (`db.sqlite3`), requiring zero external database server setup or configuration.

---

## 4. Downloading the Project

### Option A: Using Git (Recommended)
1. Open your terminal or Command Prompt.
2. Run the clone command:
   ```bash
   git clone https://github.com/your-username/shopnest-ecommerce.git
   ```
3. Navigate into the cloned folder:
   ```bash
   cd shopnest-ecommerce
   ```

### Option B: Downloading ZIP from GitHub
1. Navigate to the project's GitHub repository in your browser.
2. Click the green **Code** button and select **Download ZIP**.
3. Locate the downloaded file (e.g., in your `Downloads` folder) and extract it.
4. Open the extracted `ecommerce` folder in File Explorer or Finder.

---

## 5. Installing Required Software

### Step 5.1: Python 3.11+
Python is the core programming language required to run Django.

#### Windows Installation:
1. Visit the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Download the latest Python 3.11 or 3.12 installer for Windows.
3. Run the downloaded installer.
4. **CRITICAL STEP**: On the first installer screen, check the box that says:
   $$\boxed{\checkmark}\text{ \textbf{Add Python.exe to PATH}}$$
5. Click **Install Now** and wait for the setup to finish.

#### Verification on Windows:
Open Command Prompt (`cmd`) or PowerShell and type:
```bash
python --version
```
**Expected Output**:
```text
Python 3.11.x (or Python 3.12.x)
```

Verify that `pip` (Python package manager) is installed:
```bash
pip --version
```
**Expected Output**:
```text
pip 24.x from ... (python 3.11)
```

#### macOS Installation:
Open Terminal and install Python via Homebrew:
```bash
brew install python@3.11
```
Verify:
```bash
python3 --version
```

#### Linux (Ubuntu/Debian) Installation:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

---

## 6. Opening the Project in VS Code / Terminal

### Using Visual Studio Code:
1. Open **Visual Studio Code**.
2. Click **File** $\rightarrow$ **Open Folder...**
3. Select the folder containing `manage.py` (e.g., `shopnest-ecommerce`).
4. Open the built-in terminal: Press <kbd>Ctrl</kbd> + <kbd>`</kbd> (or go to **Terminal** $\rightarrow$ **New Terminal**).

---

## 7. Installing Dependencies

### Step 7.1: Create a Python Virtual Environment
A virtual environment isolates the project's dependencies from your global Python installation.

#### In Windows (Command Prompt / PowerShell):
```bash
python -m venv venv
```
*This creates a `venv` folder containing an isolated Python interpreter.*

#### Activate the Virtual Environment:
- **Windows (PowerShell)**:
  ```powershell
  venv\Scripts\Activate.ps1
  ```
  *(If you receive an execution policy error, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and retry).*
- **Windows (Command Prompt `cmd`)**:
  ```cmd
  venv\Scripts\activate.bat
  ```
- **macOS / Linux**:
  ```bash
  source venv/bin/activate
  ```

**How to know it worked**: Your terminal prompt will now display `(venv)` at the beginning:
```text
(venv) PS C:\path\to\shopnest-ecommerce>
```


### Step 7.2: Install Requirements
Install the required packages using `pip`:
```bash
pip install -r requirements.txt
```

#### What `requirements.txt` contains:
- `Django>=5.2`: The core full-stack framework.
- `Pillow>=10.0`: The image processing library required for product image fields.

**Expected Output**:
```text
Collecting Django>=5.2
  Downloading Django-5.2.x-py3-none-any.whl...
Collecting Pillow>=10.0
  Downloading pillow-10.x.x-...
Installing collected packages: asgiref, sqlparse, Pillow, Django
Successfully installed Django-5.2.x Pillow-10.x.x ...
```

---

## 8. Environment Variables / Configuration

Environment variables store sensitive project configuration (such as the secret key) outside the source code.

### Step 8.1: Create Your Local `.env` File
Create a `.env` file in the project root by copying `.env.example`:

#### On Windows (PowerShell / Command Prompt):
```powershell
copy .env.example .env
```

#### On macOS / Linux:
```bash
cp .env.example .env
```

### Step 8.2: Understanding Environment Variables in `.env`
Open `.env` in your text editor. It contains:

- `DJANGO_SECRET_KEY`: A unique cryptographic salt used by Django for signing session cookies and tokens.
  - *Example*: `DJANGO_SECRET_KEY=your-custom-secret-key-string-here`
- `DJANGO_DEBUG`: Set to `True` for development, `False` for production.
  - *Example*: `DJANGO_DEBUG=True`
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of hostnames or IP addresses this app will serve.
  - *Example*: `DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost`

> **IMPORTANT**: The `.env` file is listed in `.gitignore` and must **never** be committed to public Git repositories.

---

## 9. Database Setup & Initialization

Django uses migrations to generate and update SQLite database tables based on Python model classes.

### Step 9.1: Apply Migrations
Run the following command:
```bash
python manage.py migrate
```


**Expected Output**:
```text
Operations to perform:
  Apply all migrations: admin, auth, cart, contenttypes, orders, products, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying products.0001_initial... OK
  Applying products.0002_product_brand_product_created_at_and_more... OK
  Applying cart.0001_initial... OK
  Applying orders.0001_initial... OK
  Applying orders.0002_order_discount_savings_order_original_amount_and_more... OK
  Applying sessions.0001_initial... OK
```

### Step 9.2: Seed Sample Catalog (63+ Products)
The repository includes a custom Django management command that populates the database with realistic products, ratings, prices, and discounts across 12 categories:
```bash
python manage.py seed_products
```

**Expected Output**:
```text
Seeding 63 comprehensive catalog products across 12 categories...
Successfully seeded 63 products into the ShopNest database!
```

### Step 9.3: Create an Administrator Account
To access the Django Admin panel (`/admin/`), create a superuser:
```bash
python manage.py createsuperuser
```
Follow the interactive prompts:
- **Username**: `admin`
- **Email address**: `admin@example.com`
- **Password**: *(enter a secure password, e.g., `Admin@123`)*
- **Password (again)**: *(re-enter password)*

---

## 10. Starting the Application

Launch the local development server:
```bash
python manage.py runserver 127.0.0.1:8000
```

**Expected Output**:
```text
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Django version 5.2.x, using settings 'core.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## 11. Opening and Using the Application

1. Open Google Chrome, Mozilla Firefox, Microsoft Edge, or Safari.
2. Enter the following URL into your browser address bar:
   $$\textbf{http://127.0.0.1:8000}$$
3. You will be greeted by the **ShopNest Pro** homepage.

---

## 12. Complete Step-by-Step Testing Procedure

Follow this test script to verify every capability of the application:

| Step # | Test Action | Expected Result |
|---|---|---|
| **1** | Open Homepage (`/`) | Hero banner, 12 categories, Flash Deals, and product cards appear with prices and discount badges. |
| **2** | Switch Theme | Clicking the Moon/Sun button in navbar instantly toggles between Dark and Light mode. |
| **3** | Switch Currency | Clicking `INR (₹)` in navbar switches prices to `USD ($)` with proper Decimal conversion. |
| **4** | Register Account (`/users/register/`) | Enter username, email, password $\rightarrow$ Account created, success toast shown, user auto-logged in. |
| **5** | Add to Wishlist | Clicking heart icon on any product saves item via AJAX and increments navbar wishlist badge. |
| **6** | Add to Cart | Clicking **Add to Cart** updates cart count badge in navbar with pop animation. |
| **7** | View Cart (`/cart/`) | Item subtotal, discount savings, and total payable amount are calculated accurately. Quantity stepper controls (`+` / `-`) update live. |
| **8** | Proceed to Checkout (`/orders/checkout/`) | 5-step wizard displays. Fill shipping form, choose a simulated payment option (e.g. UPI / Card), and submit. |
| **9** | Order Confirmation (`/orders/confirmation/<id>/`) | Displays confirmation checkmark, Order ID, and unique Demo Reference ID (e.g. `SN-AEE947E3`). |
| **10** | Order Details & Tracking (`/orders/detail/<id>/`) | Shows 6-step lifecycle timeline stepper and item breakdown. |
| **11** | Cancel Order | Click **Cancel Order** $\rightarrow$ Confirmation modal opens $\rightarrow$ Click **Confirm Cancellation** $\rightarrow$ Order transitions to `Cancelled`, payment marked `Void`, and item quantities are restored to stock in database. |
| **12** | Django Admin (`/admin/`) | Log in as superuser $\rightarrow$ Inspect and manage Products, Orders, CartItems, and Wishlists. |

---

## 13. Understanding the Source Code Architecture

### 1. `core/` (Project Configuration)
- **`settings.py`**: Declares installed apps, template context processors (`cart.context_processors.cart_context`), SQLite database configuration, password validators, and static/media paths.
- **`urls.py`**: Master router connecting sub-applications (`products/`, `users/`, `cart/`, `orders/`, `admin/`).

### 2. `products/` (Catalog & Discovery)
- **`models.py`**:
  - `Product`: Stores title, brand, description, price, discount percentage, category, rating, and stock count. Contains `@property discounted_price` and `@property discount_amount` implementing Decimal-safe math.
  - `Wishlist`: Stores `(user, product)` pairs with unique constraints.
- **`views.py`**:
  - `home`: Handles multi-parameter filtering (category, price range, brand, stock) and multi-field sorting.
  - `product_detail`: Renders product specifications, rating stars, and related items.
  - `toggle_wishlist`: Asynchronous JSON endpoint adding/removing wishlist items.
- **`templatetags/currency_tags.py`**: Custom template filter `{% format_price %}` providing currency conversion and comma formatting.

### 3. `cart/` (Shopping Cart)
- **`models.py`**: `CartItem` model tracking user, product, and quantity. Computes `subtotal`, `original_subtotal`, and `discount_savings`.
- **`views.py`**: Handles cart listing, AJAX item addition, quantity increments/decrements, and deletions.
- **`context_processors.py`**: Automatically supplies `cart_count`, `cart_total`, `cart_original_total`, `cart_savings`, `wishlist_count`, `currency`, and `conversion_rate` to every template rendered in the application.

### 4. `orders/` (Checkout & Order Lifecycle)
- **`models.py`**:
  - `Order`: Captures customer details, address, amounts, `status` (10 choices), `payment_method`, `payment_status`, and `transaction_id`. Implements `can_be_cancelled` and atomic `cancel_order()`.
  - `OrderItem`: Stores snapshots of purchase price, original price, and purchased quantity.
- **`views.py`**:
  - `checkout_view`: Validates `CheckoutForm`, initiates database transaction, decrements inventory stock, and empties cart.
  - `cancel_order`: Restores item quantities to inventory and marks order cancelled.
  - `order_detail`: Supplies 6-stage lifecycle timeline progression steps.

### 5. `users/` (Authentication & Profile)
- **`forms.py`**: `UserRegisterForm` (extending `UserCreationForm` with email) and `UserProfileForm`.
- **`views.py`**: User registration with instant auto-login, authentication views, dashboard analytics, and currency preference switcher.

---

## 14. End-to-End Data Flow Walkthrough

```text
[User clicks "Place Demo Order"]
       │
       ▼ (HTTP POST /orders/checkout/)
[orders.views.checkout_view]
       │
       ├─► 1. Validates CheckoutForm (name, email, address, phone, payment method)
       ├─► 2. Opens transaction.atomic() database block
       │      ├─► Generates unique transaction ID: "SN-" + uuid4[:8]
       │      ├─► Creates Order record in SQLite (status='confirmed', payment_status='paid')
       │      ├─► Loops through user's CartItem records:
       │      │   ├─► Creates OrderItem with price snapshot
       │      │   └─► Decrements Product.stock: product.stock -= item.quantity
       │      └─► Deletes all CartItem records for user
       │
       ▼ (HTTP 302 Redirect to /orders/confirmation/<id>/)
[Browser loads confirmation.html displaying receipt & transaction ID]
```

---

## 15. Common Errors and Troubleshooting

### Problem 1: `'python' is not recognized as an internal or external command`
- **Why it happens**: Python was installed without enabling the "Add Python to PATH" checkbox.
- **Fix**: Re-run the Python installer $\rightarrow$ Select **Modify** $\rightarrow$ Check **Add Python to environment variables** $\rightarrow$ Click **Install**. Alternatively, restart your terminal after installation.

### Problem 2: `Error: That port is already in use.`
- **Why it happens**: Another process or background server is already running on port 8000.
- **Fix**: Specify an alternate port when running the development server:
  ```bash
  python manage.py runserver 127.0.0.1:8080
  ```
  Then open `http://127.0.0.1:8080` in your browser.

### Problem 3: `no such table: products_product` or `OperationalError`
- **Why it happens**: Database migrations have not been applied to `db.sqlite3`.
- **Fix**: Run migrations:
  ```bash
  python manage.py migrate
  ```

### Problem 4: Blank Catalog / Zero Products on Homepage
- **Why it happens**: The database is empty after running initial migrations.
- **Fix**: Run the product catalog seeder:
  ```bash
  python manage.py seed_products
  ```

---

## 16. Stopping and Restarting the Server

### How to Stop:
In the terminal window running Django, press:
- **Windows / Linux**: <kbd>Ctrl</kbd> + <kbd>C</kbd> (or <kbd>Ctrl</kbd> + <kbd>Break</kbd>)
- **macOS**: <kbd>Cmd</kbd> + <kbd>C</kbd>

### How to Restart Later:
1. Open your terminal in the project directory (`ecommerce`).
2. Activate your virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
3. Start the server:
   ```bash
   python manage.py runserver 127.0.0.1:8000
   ```

---

## 17. Demonstrating the Project to a Teacher / Examiner

Follow this 5-minute presentation sequence:

1. **Introduction**:
   - State the project title: *"ShopNest Pro — Full-Stack Django E-Commerce Platform."*
   - Highlight the architecture: Django MVT backend, SQLite database, custom Glassmorphic UI with dark/light theme switching.
2. **Catalog & Discovery Demo**:
   - Show the homepage with 12 categories, flash deals, and search bar.
   - Demonstrate dynamic filtering by Category and Price, and show multi-option sorting.
3. **Currency Conversion Demo**:
   - Click the currency toggle in the navbar to show dynamic real-time price conversion between INR (₹) and USD ($) using Decimal-safe math.
4. **Cart & Wishlist Demo**:
   - Click heart icons to demonstrate AJAX wishlist toggle without page reloads.
   - Add products to the cart and demonstrate live quantity stepper adjustment.
5. **Checkout & Lifecycle Tracking Demo**:
   - Complete checkout with a demo payment method (e.g. Instant UPI).
   - Show the generated order receipt with its unique reference ID.
   - Open **Order Details** to showcase the 6-stage lifecycle tracking stepper.
   - Click **Cancel Order** to demonstrate confirmation modal, automatic stock inventory restoration, and status transition to `Cancelled`.

---

## 18. Viva Preparation (Questions & Direct Answers)

#### Q1: What architectural pattern does Django use?
> **Answer**: Django uses the **Model-View-Template (MVT)** pattern. The **Model** defines the database schema and business logic, the **View** processes HTTP requests and queries data via the ORM, and the **Template** renders the user interface using the Django Template Language.

#### Q2: Why did you use Python's `Decimal` instead of standard `float` for prices?
> **Answer**: Standard floating-point numbers in computers suffer from binary approximation errors (e.g., `0.1 + 0.2 = 0.30000000000000004`). In e-commerce financial calculations (discounts, taxes, currency conversions), floating-point errors cause critical rounding discrepancies. `Decimal` guarantees exact base-10 arithmetic.

#### Q3: How does the order cancellation system ensure stock integrity?
> **Answer**: When an order is created, item quantities are subtracted from `Product.stock`. When an order is cancelled via `cancel_order()`, the system verifies eligibility (`pending`, `confirmed`, `processing`), loops through the order items, and restores the exact quantities back to `Product.stock` inside an atomic transaction, preventing double-restoration.

#### Q4: How is the shopping cart preserved across different devices?
> **Answer**: The cart is backed by a relational database model (`CartItem`) linked to the authenticated user (`ForeignKey(User)`). This ensures cart contents persist across browser restarts, sessions, and device switches.

---

## 19. Final Verification Checklist

Before submission or presentation, verify that:

- [ ] Python 3.11+ is installed and verified via `python --version`.
- [ ] Virtual environment is created (`venv/`) and active.
- [ ] Dependencies installed via `pip install -r requirements.txt`.
- [ ] Local environment configured via `.env` (copied from `.env.example`).
- [ ] Database migrations applied via `python manage.py migrate`.
- [ ] 63+ products seeded via `python manage.py seed_products`.
- [ ] Django system check passes cleanly with `python manage.py check`.
- [ ] Server launches at `http://127.0.0.1:8000` without errors.
- [ ] User registration, login, logout, and profile dashboard function properly.
- [ ] Cart item additions, steppers, and removals work seamlessly.
- [ ] Checkout creates orders, decrements inventory stock, and issues transaction IDs.
- [ ] Order cancellation restores stock and updates lifecycle status cleanly.
