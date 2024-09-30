import React, { useEffect, useState } from "react";
import axios from "axios";

function Header() {
  const [searchQuery, setSearchQuery] = useState("");
  const [results, setResults] = useState([]);
  const [showSearchModal, setShowSearchModal] = useState(false);

  const removeHtmlTags = (str) => {
    return str.replace(/<\/?[^>]+(>|$)/g, "");
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    const url = `${process.env.REACT_APP_API_ENDPOINT}/search_image?query=${searchQuery}`;

    try {
      const response = await axios.get(url);
      setShowSearchModal(true);
      setResults(response.data || []);
    } catch (error) {
      console.error("Error fetching search results:", error);
    }
  };

  const openProduct = (result) => {
    const obj = {
      name: removeHtmlTags(result.title).replace(/[^a-zA-Z0-9\s]/g, ""),
      image: result.link,
      site: result.displayLink,
    };

    window.location.href = `product?product=${JSON.stringify(obj)}`;
  };

  return (
    <>
      <header>
        <div className="container-fluid">
          <div className="row py-3 border-bottom">
            <div className="col-sm-4 col-lg-3 text-center text-sm-start">
              <div className="main-logo">
                <a href="/">
                  <img src="images/logo.png" alt="logo" className="img-fluid" />
                </a>
              </div>
            </div>
            <div className="col-sm-6 offset-sm-2 offset-md-0 col-lg-5 d-none d-lg-block">
              <div className="search-bar-container position-relative">
                <div className="search-bar row bg-light p-2 my-2 rounded-4">
                  <div className="col-md-4 d-none d-md-block">
                    <select className="form-select border-0 bg-transparent">
                      <option>All Categories</option>
                      <option>Groceries</option>
                      <option>Drinks</option>
                      <option>Chocolates</option>
                    </select>
                  </div>
                  <div className="col-11 col-md-7">
                    <form
                      id="search-form"
                      className="text-center"
                      onSubmit={handleSearch}
                    >
                      <input
                        type="text"
                        className="form-control border-0 bg-transparent"
                        placeholder="Search for more than 20,000 products"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                      />
                    </form>
                  </div>

                  <div className="col-1">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width={24}
                      height={24}
                      viewBox="0 0 24 24"
                    >
                      <path
                        fill="currentColor"
                        d="M21.71 20.29L18 16.61A9 9 0 1 0 16.61 18l3.68 3.68a1 1 0 0 0 1.42 0a1 1 0 0 0 0-1.39ZM11 18a7 7 0 1 1 7-7a7 7 0 0 1-7 7Z"
                      />
                    </svg>
                  </div>
                </div>

                {/* Search Results Dropdown */}
                {showSearchModal && (
                  <div
                    className="search-results-dropdown position-absolute w-100 bg-white shadow-sm p-3"
                    style={{
                      top: "100%",
                      left: 0,
                      zIndex: 10,
                      maxHeight: "700px",
                      overflowY: "auto",
                    }}
                  >
                    {results.length > 0 ? (
                      results.map((result) => (
                        // <div
                        //   key={result.cacheId}
                        //   className="card"
                        //   style={{
                        //     margin: "5px",
                        //     display: "flex",
                        //     cursor: "pointer",
                        //     padding: "10px",
                        //     alignItems: "center",
                        //     justifyContent: "space-between", // Ensures space between text and image
                        //   }}
                        //   onClick={() => openProduct(result)}
                        // >
                        //   <div
                        //     className="card-body d-flex align-items-center"
                        //     style={{ flex: 1 }}
                        //   >
                        //     {/* Text on the left */}
                        //     <div className="row">
                        //         <div className="col-10">
                        //         </div>
                        //     </div>
                        //     <div className="col-2">
                        //     </div>
                        //     <div
                        //       className="flex-grow-1"
                        //       style={{ textAlign: "left" }}
                        //     >
                        //       <p className="mb-1">
                        //         <strong>
                        //           {result.htmlTitle.match(/<b>(.*?)<\/b>/)
                        //             ? result.htmlTitle.match(/<b>(.*?)<\/b>/)[1]
                        //             : result.title}
                        //         </strong>
                        //       </p>
                        //       <span
                        //         className="badge badge1 bg-warning"
                        //         style={{
                        //           backgroundColor: "red", // Badge background is now red
                        //           color: "white",
                        //           padding: "5px 10px",
                        //           borderRadius: "5px",
                        //         }}
                        //       >
                        //         {result.displayLink}
                        //       </span>
                        //     </div>

                        //     {/* Image on the right */}

                        //   </div>
                        // </div>

                        <div
                          className="card"
                          style={{
                            margin: "5px",
                            display: "flex",
                            cursor: "pointer",
                            padding: "10px",

                            justifyContent: "space-between", // Ensures space between text and image
                          }}
                          onClick={() => openProduct(result)}
                        >
                          <div className="card-body">
                              <div className="row">
                                <div className="col-9">
                                <strong>
                                   {result.htmlTitle.match(/<b>(.*?)<\/b>/)
                                    ? result.htmlTitle.match(/<b>(.*?)<\/b>/)[1]
                                    : result.title}
                                </strong>
                                <br></br>
                                <span
                                className="badge bg-primary"
                                style={{
                                  backgroundColor: "red", // Badge background is now red
                                  color: "white",
                                  padding: "5px 10px",
                                  borderRadius: "5px",
                                }}
                              >
                                {result.displayLink}
                           </span>
                            </div>
                                <div className="col-3"> 
                                <img
                                src={result.image.thumbnailLink}
                                alt={result.title}
                                style={{
                                  width: "100px",
                                  height: "100px",
                                  objectFit: "cover",
                                  float : "right"
                                }}
                              />
                                </div>
                              </div>
                          </div>              
                        </div>
                      ))
                    ) : (
                      <p>No results found</p>
                    )}
                  </div>
                )}
              </div>
            </div>

            <div className="col-sm-8 col-lg-4 d-flex justify-content-end gap-5 align-items-center mt-4 mt-sm-0 justify-content-center justify-content-sm-end">
              <div className="support-box text-end d-none d-xl-block">
                <span className="fs-6 text-muted">For Support?</span>
                <h5 className="mb-0">+980-34984089</h5>
              </div>

              
              <ul className="d-flex justify-content-end list-unstyled m-0">
                <li>
                  <a href="#" className="rounded-circle bg-light p-2 mx-1">
                    <svg width={24} height={24} viewBox="0 0 24 24">
                      <use xlinkHref="#user" />
                    </svg>
                  </a>
                </li>
                <li>
                  <a href="#" className="rounded-circle bg-light p-2 mx-1">
                    <svg width={24} height={24} viewBox="0 0 24 24">
                      <use xlinkHref="#heart" />
                    </svg>
                  </a>
                </li>
                <li className="d-lg-none">
                  <a
                    href="#"
                    className="rounded-circle bg-light p-2 mx-1"
                    data-bs-toggle="offcanvas"
                    data-bs-target="#offcanvasCart"
                    aria-controls="offcanvasCart"
                  >
                    <svg width={24} height={24} viewBox="0 0 24 24">
                      <use xlinkHref="#cart" />
                    </svg>
                  </a>
                </li>
                <li className="d-lg-none">
                  <a
                    href="#"
                    className="rounded-circle bg-light p-2 mx-1"
                    data-bs-toggle="offcanvas"
                    data-bs-target="#offcanvasSearch"
                    aria-controls="offcanvasSearch"
                  >
                    <svg width={24} height={24} viewBox="0 0 24 24">
                      <use xlinkHref="#search" />
                    </svg>
                  </a>
                </li>
              </ul>
              <div className="cart text-end d-none d-lg-block dropdown">
                <button
                  className="border-0 bg-transparent d-flex flex-column gap-2 lh-1"
                  type="button"
                  data-bs-toggle="offcanvas"
                  data-bs-target="#offcanvasCart"
                  aria-controls="offcanvasCart"
                >
                  <span className="fs-6 text-muted dropdown-toggle">
                    Your Cart
                  </span>
                  <span className="cart-total fs-5 fw-bold">Rs 1290</span>
                </button>
              </div>
            </div>
            {/* Other header content */}
          </div>
        </div>
        <div className="container-fluid">
          <div className="row py-3">
            <div className="d-flex  justify-content-center justify-content-sm-between align-items-center">
              <nav className="main-menu d-flex navbar navbar-expand-lg">
                <button
                  className="navbar-toggler"
                  type="button"
                  data-bs-toggle="offcanvas"
                  data-bs-target="#offcanvasNavbar"
                  aria-controls="offcanvasNavbar"
                >
                  <span className="navbar-toggler-icon" />
                </button>
                <div
                  className="offcanvas offcanvas-end"
                  tabIndex={-1}
                  id="offcanvasNavbar"
                >
                  <div className="offcanvas-header justify-content-center">
                    <button
                      type="button"
                      className="btn-close"
                      data-bs-dismiss="offcanvas"
                      aria-label="Close"
                    />
                  </div>
                  <div className="offcanvas-body">
                    <select className="filter-categories border-0 mb-0 me-5">
                      <option>Shop by Departments</option>
                      <option>Whole Foods</option>
                      <option>Drinks</option>
                      <option>Snacks</option>
                    </select>
                    <ul className="navbar-nav justify-content-end menu-list list-unstyled d-flex gap-md-3 mb-0">
                      <li className="nav-item active">
                        <a href="/" className="nav-link">
                          Home
                        </a>
                      </li>
                      <li className="nav-item dropdown">
                        <a href="/shop" className="nav-link">
                          Shop
                        </a>
                      </li>
                  
                      <li className="nav-item">
                        <a href="/about-us" className="nav-link">
                          About us
                        </a>
                      </li>
                    </ul>
                  </div>
                </div>
              </nav>
            </div>
          </div>
        </div>
      </header>
    </>
  );
}

export default Header;
