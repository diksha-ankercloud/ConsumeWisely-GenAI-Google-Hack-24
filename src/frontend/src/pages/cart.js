function Cart() {
  return (
<>
  <section
    className="py-5 mb-5"
    style={{ background: "url(images/background-pattern.jpg)" }}
  >
    <div className="container-fluid">
      <div className="d-flex justify-content-between">
        <h1 className="page-title pb-2">Cart</h1>
        <nav className="breadcrumb fs-6">
          <a className="breadcrumb-item nav-link" href="#">
            Home
          </a>
          <a className="breadcrumb-item nav-link" href="#">
            Pages
          </a>
          <span className="breadcrumb-item active" aria-current="page">
            Cart
          </span>
        </nav>
      </div>
    </div>
  </section>
  <section className="py-5">
    <div className="container-fluid">
      <div className="row g-5">
        <div className="col-md-8">
          <div className="table-responsive cart">
            <table className="table">
              <thead>
                <tr>
                  <th
                    scope="col"
                    className="card-title text-uppercase text-muted"
                  >
                    Product
                  </th>
                  <th
                    scope="col"
                    className="card-title text-uppercase text-muted"
                  >
                    Quantity
                  </th>
                  <th
                    scope="col"
                    className="card-title text-uppercase text-muted"
                  >
                    Subtotal
                  </th>
                  <th
                    scope="col"
                    className="card-title text-uppercase text-muted"
                  />
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td scope="row" className="py-4">
                    <div className="cart-info d-flex flex-wrap align-items-center mb-4">
                      <div className="col-lg-3">
                        <div className="card-image">
                          <img
                            src="images/product-thumb-11.jpg"
                            alt="cloth"
                            className="img-fluid"
                          />
                        </div>
                      </div>
                      <div className="col-lg-9">
                        <div className="card-detail ps-3">
                          <h5 className="card-title">
                            <a href="#" className="text-decoration-none">
                              Iphone 13
                            </a>
                          </h5>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="py-4">
                    <div className="input-group product-qty w-50">
                      <span className="input-group-btn">
                        <button
                          type="button"
                          className="quantity-left-minus btn btn-light btn-number"
                          data-type="minus"
                        >
                          <svg width={16} height={16}>
                            <use xlinkHref="#minus" />
                          </svg>
                        </button>
                      </span>
                      <input
                        type="text"
                        id="quantity"
                        name="quantity"
                        className="form-control input-number text-center"
                        defaultValue={1}
                      />
                      <span className="input-group-btn">
                        <button
                          type="button"
                          className="quantity-right-plus btn btn-light btn-number"
                          data-type="plus"
                          data-field=""
                        >
                          <svg width={16} height={16}>
                            <use xlinkHref="#plus" />
                          </svg>
                        </button>
                      </span>
                    </div>
                  </td>
                  <td className="py-4">
                    <div className="total-price">
                      <span className="money text-dark">$1500.00</span>
                    </div>
                  </td>
                  <td className="py-4">
                    <div className="cart-remove">
                      <a href="#">
                        <svg width={24} height={24}>
                          <use xlinkHref="#trash" />
                        </svg>
                      </a>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td scope="row" className="py-4">
                    <div className="cart-info d-flex flex-wrap align-items-center">
                      <div className="col-lg-3">
                        <div className="card-image">
                          <img
                            src="images/product-thumb-12.jpg"
                            alt="product"
                            className="img-fluid"
                          />
                        </div>
                      </div>
                      <div className="col-lg-9">
                        <div className="card-detail ps-3">
                          <h5 className="card-title">
                            <a href="#" className="text-decoration-none">
                              Pink watch
                            </a>
                          </h5>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td className="py-4">
                    <div className="input-group product-qty w-50">
                      <span className="input-group-btn">
                        <button
                          type="button"
                          className="quantity-left-minus btn btn-light btn-number"
                          data-type="minus"
                        >
                          <svg width={16} height={16}>
                            <use xlinkHref="#minus" />
                          </svg>
                        </button>
                      </span>
                      <input
                        type="text"
                        id="quantity"
                        name="quantity"
                        className="form-control input-number text-center"
                        defaultValue={1}
                      />
                      <span className="input-group-btn">
                        <button
                          type="button"
                          className="quantity-right-plus btn btn-light btn-number"
                          data-type="plus"
                          data-field=""
                        >
                          <svg width={16} height={16}>
                            <use xlinkHref="#plus" />
                          </svg>
                        </button>
                      </span>
                    </div>
                  </td>
                  <td className="py-4">
                    <div className="total-price">
                      <span className="money text-dark">$870.00</span>
                    </div>
                  </td>
                  <td className="py-4">
                    <div className="cart-remove">
                      <a href="#">
                        <svg width={24} height={24}>
                          <use xlinkHref="#trash" />
                        </svg>
                      </a>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div className="col-md-4">
          <div className="cart-totals bg-grey py-5">
            <h4 className="text-dark pb-4">Cart Total</h4>
            <div className="total-price pb-5">
              <table cellSpacing={0} className="table text-uppercase">
                <tbody>
                  <tr className="subtotal pt-2 pb-2 border-top border-bottom">
                    <th>Subtotal</th>
                    <td data-title="Subtotal">
                      <span className="price-amount amount text-dark ps-5">
                        <bdi>
                          <span className="price-currency-symbol">$</span>
                          2,370.00
                        </bdi>
                      </span>
                    </td>
                  </tr>
                  <tr className="order-total pt-2 pb-2 border-bottom">
                    <th>Total</th>
                    <td data-title="Total">
                      <span className="price-amount amount text-dark ps-5">
                        <bdi>
                          <span className="price-currency-symbol">$</span>
                          2,370.00
                        </bdi>
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div className="button-wrap row g-2">
              <div className="col-md-6">
                <button className="btn btn-dark py-3 px-4 text-uppercase btn-rounded-none w-100">
                  Update Cart
                </button>
              </div>
              <div className="col-md-6">
                <button className="btn btn-dark py-3 px-4 text-uppercase btn-rounded-none w-100">
                  Continue Shopping
                </button>
              </div>
              <div className="col-md-12">
                <button className="btn btn-primary py-3 px-4 text-uppercase btn-rounded-none w-100">
                  Proceed to checkout
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  <section className="py-5">
    <div className="container-fluid">
      <div
        className="bg-secondary py-5 my-5 rounded-5"
        style={{
          background: 'url("images/bg-leaves-img-pattern.png") no-repeat'
        }}
      >
        <div className="container my-5">
          <div className="row">
            <div className="col-md-6 p-5">
              <div className="section-header">
                <h2 className="section-title display-4">
                  Get <span className="text-dark">25% Discount</span> on your
                  first purchase
                </h2>
              </div>
              <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                Dictumst amet, metus, sit massa posuere maecenas. At tellus ut
                nunc amet vel egestas.
              </p>
            </div>
            <div className="col-md-6 p-5">
              <form>
                <div className="mb-3">
                  <label htmlFor="name" className="form-label">
                    Name
                  </label>
                  <input
                    type="text"
                    className="form-control form-control-lg"
                    name="name"
                    id="name"
                    placeholder="Name"
                  />
                </div>
                <div className="mb-3">
                  <label htmlFor="" className="form-label">
                    Email
                  </label>
                  <input
                    type="email"
                    className="form-control form-control-lg"
                    name="email"
                    id="email"
                    placeholder="abc@mail.com"
                  />
                </div>
                <div className="form-check form-check-inline mb-3">
                  <label className="form-check-label" htmlFor="subscribe">
                    <input
                      className="form-check-input"
                      type="checkbox"
                      id="subscribe"
                      defaultValue="subscribe"
                    />
                    Subscribe to the newsletter
                  </label>
                </div>
                <div className="d-grid gap-2">
                  <button type="submit" className="btn btn-dark btn-lg">
                    Submit
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</>

  );
}

export default Cart;

