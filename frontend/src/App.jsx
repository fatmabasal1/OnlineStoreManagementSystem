import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:5000/api";

function App() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState({ items: [], total: 0 });
  const [page, setPage] = useState("store");
  const [message, setMessage] = useState("");
  const [paymentSuccess, setPaymentSuccess] = useState(false);
  const [paymentAmount, setPaymentAmount] = useState(0);
  const [search, setSearch] = useState("");
  const [favorites, setFavorites] = useState(() => {
    const savedFavorites = localStorage.getItem("favorites");
    if (savedFavorites) {
      try {
        return JSON.parse(savedFavorites);
      } catch {
        return [];
      }
    }
    return [];
  });

  const categories = ["All Products"];

  const loadProducts = async () => {
    try {
      const response = await fetch(`${API_URL}/products`);
      const data = await response.json();
      if (!response.ok) {
        setMessage(data.message || "Could not load products");
        return;
      }
      setProducts(data);
    } catch {
      setMessage("Could not connect to the server");
    }
  };

  const loadCart = async () => {
    try {
      const response = await fetch(`${API_URL}/cart`);
      const data = await response.json();
      if (!response.ok) {
        setMessage(data.message || "Could not load cart");
        return;
      }
      setCart(data);
    } catch {
      setMessage("Could not load cart");
    }
  };

  const addToCart = async (productId) => {
    try {
      const response = await fetch(`${API_URL}/cart/items`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ product_id: productId, quantity: 1 }),
      });
      const data = await response.json();
      if (!response.ok) {
        setMessage(data.message || "Could not add product to cart");
        return;
      }
      setCart(data);
      setMessage("Product added to cart");
    } catch {
      setMessage("Could not add product to cart");
    }
  };

  const toggleFavorite = (product) => {
    setFavorites((currentFavorites) => {
      const exists = currentFavorites.some((item) => item.id === product.id);
      const updatedFavorites = exists
        ? currentFavorites.filter((item) => item.id !== product.id)
        : [...currentFavorites, product];
      localStorage.setItem("favorites", JSON.stringify(updatedFavorites));
      return updatedFavorites;
    });
  };

  const isFavorite = (productId) =>
    favorites.some((item) => item.id === productId);

  const openCheckout = () => {
    if (cart.items.length === 0) {
      setMessage("Your cart is empty");
      return;
    }
    setMessage("");
    setPaymentSuccess(false);
    setPage("checkout");
    window.scrollTo(0, 0);
  };

  const makePayment = async () => {
    const totalBeforePayment = cart.total;
    try {
      const response = await fetch(`${API_URL}/payments`, { method: "POST" });
      const data = await response.json();
      if (!response.ok) {
        setMessage(data.message || "Payment could not be completed");
        return;
      }
      setPaymentAmount(totalBeforePayment);
      setPaymentSuccess(true);
      setMessage("");
      await loadCart();
      await loadProducts();
    } catch {
      setMessage("Payment could not be completed");
    }
  };

  const handleCategoryChange = (category) => {
    if (category === "All Products") setSearch("");
    setPage("store");
    setTimeout(() => {
      document
        .getElementById("products")
        ?.scrollIntoView({ behavior: "smooth" });
    }, 50);
  };

  const filteredProducts = products.filter((product) => {
    const searchText =
      `${product.name || ""} ${product.category || ""} ${product.description || ""}`.toLowerCase();
    return searchText.includes(search.toLowerCase());
  });

  useEffect(() => {
    loadProducts();
    loadCart();
  }, []);

  const ProductImage = ({ product }) => (
    <div className="product-image-box">
      <div className="discount-badge">-20%</div>
      <img
        className="product-image"
        src={product.image_url}
        alt={product.name}
        onError={(event) => {
          event.currentTarget.style.display = "none";
          event.currentTarget.nextElementSibling.style.display = "flex";
        }}
      />
      <div className="product-letter" style={{ display: "none" }}>
        {product.name?.charAt(0)}
      </div>
      <button className="favorite" onClick={() => toggleFavorite(product)}>
        {isFavorite(product.id) ? "♥" : "♡"}
      </button>
    </div>
  );

  if (page === "checkout") {
    return (
      <div className="app">
        <header className="checkout-header">
          <div className="checkout-top">
            <button className="checkout-logo" onClick={() => setPage("store")}>
              STORE
            </button>
            <div className="checkout-title">Secure Checkout</div>
            <button className="back-store" onClick={() => setPage("store")}>
              ← Back to Store
            </button>
          </div>
        </header>
        <main className="checkout-page">
          {paymentSuccess ? (
            <div className="payment-success">
              <div className="success-check">✓</div>
              <h1>Order Confirmed!</h1>
              <p>
                Your payment has been completed successfully. Your order will
                now be prepared.
              </p>
              <div className="success-price">
                ${Number(paymentAmount).toFixed(2)}
              </div>
              <button
                onClick={() => {
                  setPaymentSuccess(false);
                  setPage("store");
                }}
              >
                Continue Shopping
              </button>
            </div>
          ) : (
            <>
              <h1 className="checkout-main-title">Checkout</h1>
              <div className="checkout-grid">
                <div className="checkout-left">
                  <div className="checkout-box">
                    <div className="checkout-box-title">
                      <span>1</span>
                      <h2>Order Summary</h2>
                    </div>
                    {cart.items.map((item) => (
                      <div className="checkout-product" key={item.id}>
                        <div className="checkout-product-image">
                          {item.name?.charAt(0)}
                        </div>
                        <div className="checkout-product-info">
                          <strong>{item.name}</strong>
                          <span>Quantity: {item.quantity}</span>
                        </div>
                        <strong>${Number(item.subtotal).toFixed(2)}</strong>
                      </div>
                    ))}
                  </div>
                  <div className="checkout-box">
                    <div className="checkout-box-title">
                      <span>2</span>
                      <h2>Payment Method</h2>
                    </div>
                    <div className="card-option">
                      <div className="card-icon">💳</div>
                      <div>
                        <strong>Card Payment</strong>
                        <p>Secure and fast payment</p>
                      </div>
                      <div className="radio-selected">✓</div>
                    </div>
                    <div className="demo-notice">
                      Payment is simulated for this project.
                    </div>
                  </div>
                </div>
                <aside className="checkout-summary">
                  <h2>Order Summary</h2>
                  <div className="summary-line">
                    <span>Products</span>
                    <strong>${Number(cart.total).toFixed(2)}</strong>
                  </div>
                  <div className="summary-line">
                    <span>Shipping</span>
                    <strong className="free">Free</strong>
                  </div>
                  <div className="summary-divider" />
                  <div className="summary-total">
                    <span>Total</span>
                    <strong>${Number(cart.total).toFixed(2)}</strong>
                  </div>
                  <button className="pay-now" onClick={makePayment}>
                    Complete Payment
                  </button>
                  {message && <div className="checkout-error">{message}</div>}
                </aside>
              </div>
            </>
          )}
        </main>
      </div>
    );
  }

  if (page === "favorites") {
    return (
      <div className="app">
        <header className="main-header">
          <div className="header-top">
            <div className="brand-area">
              <button className="store-logo" onClick={() => setPage("store")}>
                STORE
              </button>
              <span className="marketplace-text">Online Marketplace</span>
            </div>
            <div className="search-area">
              <input
                type="text"
                placeholder="Search for products, categories or brands"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
              />
              <button>⌕</button>
            </div>
            <div className="header-actions">
              <button onClick={() => setPage("favorites")}>
                ♡ <span>My Favorites</span>
                {favorites.length > 0 && <b>{favorites.length}</b>}
              </button>
              <button onClick={() => setPage("store")}>
                🛒 <span>My Cart</span>
                <b>{cart.items.length}</b>
              </button>
            </div>
          </div>
          <nav className="category-nav">
            {categories.map((category) => (
              <button
                key={category}
                className="active-category"
                onClick={() => handleCategoryChange(category)}
              >
                {category}
              </button>
            ))}
          </nav>
        </header>
        <main>
          <section className="products-section">
            <div className="section-header">
              <div>
                <span>YOUR SAVED PRODUCTS</span>
                <h2>My Favorites</h2>
              </div>
              <small>{favorites.length} products</small>
            </div>
            {favorites.length === 0 ? (
              <div className="empty-cart">
                <div>♡</div>
                <h2>Your favorites are empty</h2>
                <p>Add products to your favorites and they will appear here.</p>
                <button onClick={() => setPage("store")}>
                  Browse Products
                </button>
              </div>
            ) : (
              <div className="product-grid">
                {favorites.map((product) => (
                  <article className="market-product" key={product.id}>
                    <ProductImage product={product} />
                    <div className="market-product-info">
                      <span className="market-category">
                        {product.category}
                      </span>
                      <h3>{product.name}</h3>
                      <p>{product.description}</p>
                      <div className="rating">
                        ★★★★★{" "}
                        <span>({Number(product.rating || 0).toFixed(1)})</span>
                      </div>
                      <div className="market-product-bottom">
                        <div>
                          <strong>${Number(product.price).toFixed(2)}</strong>
                          <small>{product.stock} left in stock</small>
                        </div>
                        <button
                          onClick={() => addToCart(product.id)}
                          disabled={product.stock === 0}
                        >
                          Add to Cart
                        </button>
                      </div>
                    </div>
                  </article>
                ))}
              </div>
            )}
          </section>
        </main>
        <footer className="footer">
          <strong>STORE</strong>
          <span>Component-Based Online Store Management System</span>
        </footer>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="main-header">
        <div className="header-top">
          <div className="brand-area">
            <button
              className="store-logo"
              onClick={() => {
                setPage("store");
                setSearch("");
                window.scrollTo(0, 0);
              }}
            >
              STORE
            </button>
            <span className="marketplace-text">Online Marketplace</span>
          </div>
          <div className="search-area">
            <input
              type="text"
              placeholder="Search for products, categories or brands"
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
            <button>⌕</button>
          </div>
          <div className="header-actions">
            <button onClick={() => setPage("favorites")}>
              ♡ <span>My Favorites</span>
              {favorites.length > 0 && <b>{favorites.length}</b>}
            </button>
            <button
              onClick={() =>
                document
                  .getElementById("cart")
                  ?.scrollIntoView({ behavior: "smooth" })
              }
            >
              🛒 <span>My Cart</span>
              <b>{cart.items.length}</b>
            </button>
          </div>
        </div>
        <nav className="category-nav">
          {categories.map((category) => (
            <button
              key={category}
              className="active-category"
              onClick={() => handleCategoryChange(category)}
            >
              {category}
            </button>
          ))}
        </nav>
      </header>

      <main>
        <section className="campaign-banner">
          <div>
            <span>DISCOVER GREAT DEALS</span>
            <h1>
              Today's
              <br />
              Deals
            </h1>
            <p>Special prices on selected products</p>
            <button
              onClick={() => {
                setSearch("");
                document
                  .getElementById("products")
                  ?.scrollIntoView({ behavior: "smooth" });
              }}
            >
              Start Shopping →
            </button>
          </div>
          <div className="campaign-circle">%</div>
        </section>

        <section className="products-section" id="products">
          <div className="section-header">
            <div>
              <span>POPULAR PRODUCTS</span>
              <h2>All Products</h2>
            </div>
            <small>{filteredProducts.length} products</small>
          </div>
          <div className="product-grid">
            {filteredProducts.map((product) => (
              <article className="market-product" key={product.id}>
                <ProductImage product={product} />
                <div className="market-product-info">
                  <span className="market-category">{product.category}</span>
                  <h3>{product.name}</h3>
                  <p>{product.description}</p>
                  <div className="rating">
                    ★★★★★{" "}
                    <span>({Number(product.rating || 0).toFixed(1)})</span>
                  </div>
                  <div className="market-product-bottom">
                    <div>
                      <strong>${Number(product.price).toFixed(2)}</strong>
                      <small>{product.stock} left in stock</small>
                    </div>
                    <button
                      onClick={() => addToCart(product.id)}
                      disabled={product.stock === 0}
                    >
                      Add to Cart
                    </button>
                  </div>
                </div>
              </article>
            ))}
          </div>
          {filteredProducts.length === 0 && (
            <div className="empty-cart">
              <div>🔍</div>
              <h2>No products found</h2>
              <p>Try another search term.</p>
              <button onClick={() => setSearch("")}>Show All Products</button>
            </div>
          )}
        </section>

        <section className="shopping-cart" id="cart">
          <div className="section-header">
            <div>
              <span>YOUR SHOPPING</span>
              <h2>My Cart</h2>
            </div>
          </div>
          {cart.items.length === 0 ? (
            <div className="empty-cart">
              <div>🛒</div>
              <h2>Your cart is empty</h2>
              <p>Add products to your cart and start shopping.</p>
              <button
                onClick={() =>
                  document
                    .getElementById("products")
                    ?.scrollIntoView({ behavior: "smooth" })
                }
              >
                Browse Products
              </button>
            </div>
          ) : (
            <div className="cart-layout">
              <div className="cart-products">
                {cart.items.map((item) => (
                  <div className="cart-product" key={item.id}>
                    <div className="cart-product-image">
                      {item.name?.charAt(0)}
                    </div>
                    <div className="cart-product-info">
                      <h3>{item.name}</h3>
                      <span>Quantity: {item.quantity}</span>
                      <strong>${Number(item.price).toFixed(2)}</strong>
                    </div>
                    <strong className="cart-subtotal">
                      ${Number(item.subtotal).toFixed(2)}
                    </strong>
                  </div>
                ))}
              </div>
              <aside className="cart-summary">
                <h2>Order Summary</h2>
                <div>
                  <span>Products</span>
                  <strong>${Number(cart.total).toFixed(2)}</strong>
                </div>
                <div>
                  <span>Shipping</span>
                  <strong className="free">Free</strong>
                </div>
                <hr />
                <div className="cart-total">
                  <span>Total</span>
                  <strong>${Number(cart.total).toFixed(2)}</strong>
                </div>
                <button onClick={openCheckout}>Go to Checkout →</button>
              </aside>
            </div>
          )}
          {message && <div className="cart-message">✓ {message}</div>}
        </section>
      </main>

      <footer className="footer">
        <strong>STORE</strong>
        <span>Component-Based Online Store Management System</span>
      </footer>
    </div>
  );
}

export default App;
