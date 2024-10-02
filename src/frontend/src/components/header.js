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
        <div className="container-fluid mt-3" >
          <div className="row border-bottom">
            <div className="col-sm-4 col-lg-4 text-center text-sm-start">
              <div className="main-logo">
                <a href="/">
                  <img src="images/logo.png" alt="logo" className="img-fluid" />
                </a>
              </div>
            </div>
            <div className="col-sm-6 offset-sm-1 offset-md-0 col-lg-6 d-none d-lg-block">
           
             <div className="search-bar-container position-relative">
              <div className="search-bar row bg-light p-2 my-2 rounded-4">
               <div className="col-md-3 d-none d-md-block">
                
                  </div>
                  <div className="col-11">
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
                        style={{ width: '100%' }} // Make input take full width
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
            <div className="col-2">
            <div id="google_translate_element"></div>
            </div>

    
            </div>
            {/* Other header content */}
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
                    <ul className="navbar-nav justify-content-end menu-list list-unstyled d-flex gap-md-3 mb-0">
                      <li className="nav-item active">
                        <a href="/" className="nav-link" style={{ fontSize: '16px', fontWeight: 'bold' }}>
                            Home
                        </a>
                      </li>
                      <li className="nav-item dropdown">
                        <a href="/shop" className="nav-link" style={{ fontSize: '16px', fontWeight: 'bold' }}>
                          Shop
                        </a>
                      </li>
                      <li className="nav-item">
                        <a href="/about-us" className="nav-link" style={{ fontSize: '16px', fontWeight: 'bold' }}>
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
