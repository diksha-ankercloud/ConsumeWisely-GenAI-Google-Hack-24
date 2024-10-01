import React, { useEffect, useState } from "react";
import axios from "axios";

import { usellmResponse } from "../context/llmResponse";
import { FaWandMagicSparkles } from "react-icons/fa6";
import { HiOutlineBadgeCheck } from "react-icons/hi";
import { MdPersonSearch } from "react-icons/md";
import { FaCommentDots } from "react-icons/fa";

function Product({}) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [productImages, setProductImages] = useState([]);
  const [productImage, setProductImage] = useState("");
  const [productDetails, setProductDetails] = useState(false);
  const [claimCheckCard, setClaimCheckCard] = useState(false);
  const [claimData, setClaimData] = useState([]);
  const [claimText, setClaimText] = useState("");
  const [personaliseCard, setPersonaliseCard] = useState(false);

  const [personalise_age, setPersonalise_age] = useState("");
  const [personalise_allergen, setPersonalise_allergen] = useState("");
  const [personalise_diet_type, setPersonalise_diet_type] = useState("");
  const [personalise_gender, setPersonalise_gender] = useState("");
  const [personalise_health_goal, setPersonalise_health_goal] = useState("");
  const [personalise_height, setPersonalise_height] = useState("");
  const [personalise_weight, setPersonalise_weight] = useState("");
  const [personalise_product_name, setPersonalise_product_name] = useState("");
  const [personaliseResponse, setPersonaliseResponse] = useState("");

  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const id = urlParams.get("id");
  const product = JSON.parse(decodeURIComponent(urlParams.get("product")));

  const { llmResponse } = usellmResponse();

  const handleProductImageSearch = async (product) => {
    const url = `${process.env.REACT_APP_API_ENDPOINT}/search_image?query=${decodeURI(
      product.name
    )}&side=back&total=5`;

    try {
      const response = await axios.get(url);
      setProductImages(response.data);
      console.log(productImages);
    } catch (error) {
      console.error("Error fetching search results:", error);
    }
  };

  const handlePersonalise = async () => {
    console.log(123456);
    const url = `${process.env.REACT_APP_API_ENDPOINT}/analyze_product`;
    const payload = {
      age: personalise_age,
      weight: personalise_weight,
      gender: personalise_gender,
      height: personalise_height,
      diet_type: personalise_diet_type,
      health_goal: personalise_health_goal,
      allergen: personalise_allergen,
      product_name: personalise_product_name,
    };

    try {
      const response = await axios.post(url, payload);
      setPersonaliseResponse(response.data);
    } catch (error) {
      console.error("Error fetching search results:", error);
    }
  };

  const checkClaim = async (claim, ingredients) => {
    const url = `${process.env.REACT_APP_CLAIM_CHECK_ENDPOINT}?claim=${claim}&ingredients=${ingredients}`;

    try {
      const response = await axios.get(url);
      setClaimData(JSON.parse(response.data));
      console.log(claimData?.verdict);
    } catch (error) {
      console.error("Error fetching search results:", error);
    }
  };

  const getProductDetails = async (product) => {
    if (productDetails) return;
    const url = `${process.env.REACT_APP_API_ENDPOINT}/check_product_and_web_search`;
    const body = { product: product.name };

    try {
      const response = await axios.post(url, body);
      setProductDetails(response.data);
    } catch (error) {
      console.error("Error fetching search results:", error);
    }
  };

  useEffect(() => {
    handleProductImageSearch(product);
    getProductDetails(product);
    setProductImage(product.image);
  }, []);

  const ingredients = productDetails?.product_info?.ingredients?.replace(
    /\*/g,
    ""
  );

  return (
    <>
      <section id="selling-product" className="single-product mt-0 mt-md-5">
        <div className="container-fluid">
          <nav className="breadcrumb">
            <a className="breadcrumb-item" href="#">
              Home
            </a>
            <a className="breadcrumb-item" href="#">
              Pages
            </a>
            <span className="breadcrumb-item active" aria-current="page">
              Single Product
            </span>
          </nav>
          <div className="row g-5">
            <div className="col-lg-7">
              <div className="row flex-column-reverse flex-lg-row">
                <div className="col-md-12 col-lg-2">
                  {/* product-thumbnail-slider */}
                  <div className="swiper product-thumbnail-slider">
                    <div className="">
                      {productImages &&
                        productImages?.map((image) => {
                          return (
                            <div className="swiper-slide">
                              <img
                                src={image?.link}
                                alt=""
                                className="thumb-image img-fluid"
                                onClick={() => setProductImage(image?.link)}
                              />
                            </div>
                          );
                        })}
                    </div>
                  </div>
                  {/* / product-thumbnail-slider */}
                </div>
                <div className="col-md-12 col-lg-10">
                  {/* product-large-slider */}
                  <div className="swiper product-large-slider">
                    <div className="swiper-wrapper">
                      <div className="swiper-slide">
                        <div
                          className="image-zoom"
                          data-scale="2.5"
                          data-image={productImage}
                          style={{ zoom: "2", marginLeft: "50px" }}
                        >
                          <img
                            src={productImage}
                            alt="product-large"
                            className="img-fluid"
                          />
                        </div>
                      </div>
                      <div className="swiper-slide">
                        <div
                          className="image-zoom"
                          data-scale="2.5"
                          data-image="images/product-large-2.jpg"
                        >
                          <img
                            src="images/product-large-2.jpg"
                            alt="product-large"
                            className="img-fluid"
                          />
                        </div>
                      </div>
                      <div className="swiper-slide">
                        <div
                          className="image-zoom"
                          data-scale="2.5"
                          data-image="images/product-large-3.jpg"
                        >
                          <img
                            src="images/product-large-3.jpg"
                            alt="product-large"
                            className="img-fluid"
                          />
                        </div>
                      </div>
                      <div className="swiper-slide">
                        <div
                          className="image-zoom"
                          data-scale="2.5"
                          data-image="images/product-large-4.jpg"
                        >
                          <img
                            src="images/product-large-4.jpg"
                            alt="product-large"
                            className="img-fluid"
                          />
                        </div>
                      </div>
                      <div className="swiper-slide">
                        <div
                          className="image-zoom"
                          data-scale="2.5"
                          data-image="images/product-large-5.jpg"
                        >
                          <img
                            src="images/product-large-5.jpg"
                            alt="product-large"
                            className="img-fluid"
                          />
                        </div>
                      </div>
                    </div>
                    <div className="swiper-pagination" />
                  </div>
                  <br></br>
                  {/* / product-large-slider */}
                </div>
              </div>
            </div>
            <div className="col-lg-5">
              <div className="product-info">
                <div className="element-header">
                  <h2 itemProp="name" className="display-6">
                    {product.name}
                  </h2>
                  {/* <div className="row">
                    <div className="col-3">
                      <button
                        type="button"
                        class="btn btn-outline-success btn-sm"
                      >
                        {" "}
                        <h5><strong>Verify Claims</strong></h5>{" "}
                        <HiOutlineBadgeCheck
                          style={{ marginBottom: "0.2rem" }}
                        />{" "}
                      </button>
                    </div>
                    <div className="col-3">
                      <button
                        type="button"
                        class="btn btn-outline-secondary btn-sm "
                      >
                        {" "}
                        Personalise{" "}
                        <MdPersonSearch
                          style={{ marginBottom: "0.2rem" }}
                        />{" "}
                      </button>
                    </div>
                    <div className="col-3">
                    <button
                        type="button"
                        class="btn btn-outline-secondary btn-sm "
                      >
                        {" "}
                        AI Scan{" "}
                        <FaWandMagicSparkles
                          style={{ marginBottom: "0.2rem" }}
                        />{" "}
                      </button>
                    </div>
                  </div> */}
                  <ul className="nav nav-pills">
                    <li className="nav-item" style={{ margin: "5px" }}>
                      <button
                        type="button"
                        class="btn btn-outline-success btn-sm"
                        onClick={() => {
                          if (claimCheckCard) setClaimCheckCard(false);
                          else setClaimCheckCard(true);
                          setPersonaliseCard(false);
                        }}
                      >
                        {" "}
                        Verify Claims{" "}
                        <HiOutlineBadgeCheck
                          style={{ marginBottom: "0.2rem" }}
                        />{" "}
                      </button>
                    </li>
                    <li className="nav-item" style={{ margin: "5px" }}>
                      <button
                        type="button"
                        class="btn btn-outline-secondary btn-sm "
                        onClick={() => {
                          if (personaliseCard) setPersonaliseCard(false);
                          else setPersonaliseCard(true);
                          setClaimCheckCard(false);
                        }}
                      >
                        {" "}
                        Personalise{" "}
                        <MdPersonSearch
                          style={{ marginBottom: "0.2rem" }}
                        />{" "}
                      </button>
                    </li>
                  </ul>
                  {claimCheckCard && (
                    <div className="card" style={{ margin: "5px" }}>
                      <div className="card-body">
                        <form className="row">
                          <div className="col-3">
                            <label
                              htmlFor="staticEmail2"
                              className="visually-hidden"
                            ></label>
                            <input
                              type="text"
                              readOnly=""
                              className="form-control-plaintext"
                              id="staticEmail2"
                              defaultValue="Write Claims:"
                            />
                          </div>
                          <div className="col-7">
                            <label
                              htmlFor="inputPassword2"
                              className="visually-hidden"
                            ></label>
                            <input
                              type="text"
                              className="form-control"
                              id="inputPassword2"
                              placeholder="No Sugar, Zero Trans Fat etc"
                              value={claimText}
                              onChange={(e) => setClaimText(e.target.value)}
                            />
                          </div>
                          <div className="col-2">
                            <span
                              className="btn btn-primary mb-3"
                              onClick={() => {
                                checkClaim(claimText, ingredients);
                              }}
                            >
                              Check
                            </span>
                          </div>
                        </form>
                        <p>
                          {claimData && claimData?.verdict == "Misleading" ? (
                            <span style={{ color: "red" }}>
                              {claimData?.verdict}
                            </span>
                          ) : (
                            <span style={{ color: "green" }}>
                              {claimData?.verdict}
                            </span>
                          )}
                        </p>
                        <p>{claimData && claimData?.why}</p>
                        <p>{claimData && claimData?.detailed_analysis}</p>
                      </div>
                    </div>
                  )}
                  {personaliseCard && (
                    <div className="card" style={{ margin: "5px" }}>
                      <div className="card-body">
                        <div>
                          {Object.keys(personaliseResponse).map((key) => (
                            <div key={key}>
                              <strong>{key}:</strong> {personaliseResponse[key]}
                            </div>
                          ))}
                        </div>
                       {!personaliseResponse &&  <div className="row">
                          <div className="col-6">
                            <div className="mb-3">
                              <label htmlFor="" className="form-label">
                                Age:
                              </label>
                              <input
                                type="email"
                                className="form-control"
                                id=""
                                placeholder="Enter Your Age"
                                value={personalise_age}
                                onChange={(e) =>
                                  setPersonalise_age(e.target.value)
                                }
                              />
                            </div>
                          </div>
                          <div className="col-6">
                            <div className="mb-3">
                              <label htmlFor="" className="form-label">
                                Weight:
                              </label>
                              <input
                                type="email"
                                className="form-control"
                                id="exampleFormControlInput1"
                                placeholder="Enter Your Weight"
                                value={personalise_weight}
                                onChange={(e) =>
                                  setPersonalise_weight(e.target.value)
                                }
                              />
                            </div>
                          </div>
                          <div className="col-6">
                            <div className="mb-3">
                              <label
                                htmlFor="exampleFormControlInput1"
                                className="form-label"
                              >
                                Gender:
                              </label>
                              <input
                                type="email"
                                className="form-control"
                                id="exampleFormControlInput1"
                                placeholder="Enter Your Gender."
                                value={personalise_gender}
                                onChange={(e) =>
                                  setPersonalise_gender(e.target.value)
                                }
                              />
                            </div>
                          </div>
                          <div className="col-6">
                            <div className="mb-3">
                              <label
                                htmlFor="exampleFormControlInput1"
                                className="form-label"
                              >
                                Height:
                              </label>
                              <input
                                type="email"
                                className="form-control"
                                id="exampleFormControlInput1"
                                placeholder="Enter Your Height"
                                value={personalise_height}
                                onChange={(e) =>
                                  setPersonalise_height(e.target.value)
                                }
                              />
                            </div>
                          </div>
                          <div className="col-6">
                            <div className="mb-3">
                              <label
                                htmlFor="exampleFormControlInput1"
                                className="form-label"
                              >
                                Diet Type:
                              </label>
                              <input
                                type="email"
                                className="form-control"
                                id="exampleFormControlInput1"
                                placeholder="Enter Diet Type"
                                value={personalise_diet_type}
                                onChange={(e) =>
                                  setPersonalise_diet_type(e.target.value)
                                }
                              />
                            </div>
                          </div>
                          <div className="col-6">
                            <div className="mb-3">
                              <label
                                htmlFor="exampleFormControlInput1"
                                className="form-label"
                              >
                                Health Goal:
                              </label>
                              <input
                                type="email"
                                className="form-control"
                                id="exampleFormControlInput1"
                                placeholder="Enter Your Health Goal"
                                value={personalise_health_goal}
                                onChange={(e) =>
                                  setPersonalise_health_goal(e.target.value)
                                }
                              />
                            </div>
                          </div>
                          <div className="col-6">
                            <div className="mb-3">
                              <label
                                htmlFor="exampleFormControlInput1"
                                className="form-label"
                              >
                                Allergen:
                              </label>
                              <input
                                type="email"
                                className="form-control"
                                id="exampleFormControlInput1"
                                placeholder="Enter Alergen"
                                value={personalise_allergen}
                                onChange={(e) =>
                                  setPersonalise_allergen(e.target.value)
                                }
                              />
                            </div>
                          </div>
                          <div className="col-6">
                            <div className="mb-3">
                              <label
                                htmlFor="exampleFormControlInput1"
                                className="form-label"
                              >
                                Product Name:
                              </label>
                              <input
                                type="email"
                                className="form-control"
                                id="exampleFormControlInput1"
                                placeholder="Enter Product Name"
                                value={personalise_product_name}
                                onChange={(e) =>
                                  setPersonalise_product_name(e.target.value)
                                }
                              />
                            </div>
                          </div>
                        </div>}
                        <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                          <button
                            class="btn btn-primary"
                            type="button"
                            onClick={() => {
                              handlePersonalise();
                            }}
                          >
                            Submit
                          </button>
                        </div>
                      </div>
                    </div>
                  )}
                  <br></br>
                  {/* <div className="rating-container d-flex gap-0 align-items-center">
                    <div className="rating" data-rating={1}>
                      <svg width={32} height={32} className="text-primary">
                        <use xlinkHref="#star-solid" />
                      </svg>
                    </div>
                    <div className="rating" data-rating={2}>
                      <svg width={32} height={32} className="text-primary">
                        <use xlinkHref="#star-solid" />
                      </svg>
                    </div>
                    <div className="rating" data-rating={3}>
                      <svg width={32} height={32} className="text-primary">
                        <use xlinkHref="#star-solid" />
                      </svg>
                    </div>
                    <div className="rating" data-rating={4}>
                      <svg width={32} height={32} className="text-secondary">
                        <use xlinkHref="#star-solid" />
                      </svg>
                    </div>
                    <div className="rating" data-rating={5}>
                      <svg width={32} height={32} className="text-secondary">
                        <use xlinkHref="#star-solid" />
                      </svg>
                    </div>
                    <span className="rating-count">(3.5)</span>
                  </div> */}
                  <br></br> <br></br>
                  <h4>
                    <strong>Allergic Contents:</strong>
                  </h4>
                  {productDetails ? (
                    <span style={{ color: "orange" }}>
                      {" "}
                      {productDetails?.product_info?.allergens}{" "}
                    </span>
                  ) : (
                    <div className="spinner-grow text-secondary" role="status">
                      <span className="visually-hidden">Loading...</span>
                    </div>
                  )}
                  <br></br> <br></br>
                  <h4>
                    <strong>Diet Preferrence:</strong>
                  </h4>
                  {productDetails ? (
                    <span>
                      {" "}
                      {productDetails?.product_info?.diet_suitability}{" "}
                    </span>
                  ) : (
                    <div className="spinner-grow text-secondary" role="status">
                      <span className="visually-hidden">Loading...</span>
                    </div>
                  )}
                  <br></br> <br></br>
                  <h4>
                    <strong>Nutritional/Harmful Ingredients:</strong>
                  </h4>
                  {productDetails ? (
                    <span>
                      {" "}
                      {
                        productDetails?.product_info?.nutritional_benefits_harms
                      }{" "}
                    </span>
                  ) : (
                    <div className="spinner-grow text-secondary" role="status">
                      <span className="visually-hidden">Loading...</span>
                    </div>
                  )}
                  <br></br> <br></br>
                  <h4>
                    <strong>Organic & Sustainable:</strong>
                  </h4>
                  {productDetails ? (
                    <span>
                      {" "}
                      {productDetails?.product_info?.sustainibility_factor}{" "}
                    </span>
                  ) : (
                    <div className="spinner-grow text-secondary" role="status">
                      <span className="visually-hidden">Loading...</span>
                    </div>
                  )}
                  <br></br> <br></br>
                  <h4>
                    <strong>Taste:</strong>
                  </h4>
                  {productDetails ? (
                    <span> {productDetails?.product_info?.taste} </span>
                  ) : (
                    <div className="spinner-grow text-secondary" role="status">
                      <span className="visually-hidden">Loading...</span>
                    </div>
                  )}
                </div>

                {/* <div className="product-price pt-3 pb-3">
                  <strong className="text-primary display-6 fw-bold">
                    Rs. {product.price}
                  </strong>
                  <del className="ms-2">Rs. {product.price}</del>
                </div> */}
              </div>
            </div>
          </div>
        </div>
      </section>
      <section className="product-info-tabs py-5">
        <div className="container-fluid">
          <div className="row">
            <div className="d-flex flex-column flex-md-row align-items-start gap-5">
              <div
                className="nav flex-row flex-wrap flex-md-column nav-pills me-3 col-lg-3"
                id="v-pills-tab"
                role="tablist"
                aria-orientation="vertical"
              >
                <button
                  className="nav-link text-start active"
                  id="v-pills-description-tab"
                  data-bs-toggle="pill"
                  data-bs-target="#v-pills-description"
                  type="button"
                  role="tab"
                  aria-controls="v-pills-description"
                  aria-selected="true"
                >
                  <h5>Ingridients</h5>
                </button>
                <button
                  className="nav-link text-start"
                  id="v-pills-additional-tab"
                  data-bs-toggle="pill"
                  data-bs-target="#v-pills-additional"
                  type="button"
                  role="tab"
                  aria-controls="v-pills-additional"
                  aria-selected="false"
                >
                  Additional Information
                </button>
                <button
                  className="nav-link text-start"
                  id="v-pills-reviews-tab"
                  data-bs-toggle="pill"
                  data-bs-target="#v-pills-reviews"
                  type="button"
                  role="tab"
                  aria-controls="v-pills-reviews"
                  aria-selected="false"
                >
                  Customer Reviews
                </button>
              </div>
              <div className="tab-content" id="v-pills-tabContent">
                <div
                  className="tab-pane fade show active"
                  id="v-pills-description"
                  role="tabpanel"
                  aria-labelledby="v-pills-description-tab"
                  tabIndex={0}
                >
                  <h5>{ingredients}</h5>
                  <p>{product.description}</p>
                </div>
                <div
                  className="tab-pane fade"
                  id="v-pills-additional"
                  role="tabpanel"
                  aria-labelledby="v-pills-additional-tab"
                  tabIndex={0}
                >
                  <p>It is Comfortable and Best</p>
                  <p>
                    Duis aute irure dolor in reprehenderit in voluptate velit
                    esse cillum dolore eu fugiat nulla pariatur. Excepteur sint
                    occaecat cupidatat non proident, sunt in culpa qui officia
                    deserunt mollit anim id est laborum. Duis aute irure dolor
                    in reprehenderit in voluptate velit esse cillum dolore eu
                    fugiat nulla pariatur. Excepteur sint occaecat cupidatat non
                    proident, sunt in culpa qui officia deserunt mollit anim id
                    est laborum.
                  </p>
                </div>
                <div
                  className="tab-pane fade"
                  id="v-pills-reviews"
                  role="tabpanel"
                  aria-labelledby="v-pills-reviews-tab"
                  tabIndex={0}
                >
                  <div className="review-box d-flex flex-wrap">
                    <div className="col-lg-6 d-flex flex-wrap gap-3">
                      <div className="col-md-2">
                        <div className="image-holder">
                          <img
                            src="images/reviewer-1.jpg"
                            alt="review"
                            className="img-fluid rounded-circle"
                          />
                        </div>
                      </div>
                      <div className="col-md-8">
                        <div className="review-content">
                          <div className="rating-container d-flex align-items-center">
                            <div className="rating" data-rating={1}>
                              <svg
                                width={24}
                                height={24}
                                className="text-primary"
                              >
                                <use xlinkHref="#star-solid" />
                              </svg>
                            </div>
                            <div className="rating" data-rating={2}>
                              <svg
                                width={24}
                                height={24}
                                className="text-primary"
                              >
                                <use xlinkHref="#star-solid" />
                              </svg>
                            </div>
                            <div className="rating" data-rating={3}>
                              <svg
                                width={24}
                                height={24}
                                className="text-primary"
                              >
                                <use xlinkHref="#star-solid" />
                              </svg>
                            </div>
                            <div className="rating" data-rating={4}>
                              <svg
                                width={24}
                                height={24}
                                className="text-secondary"
                              >
                                <use xlinkHref="#star-solid" />
                              </svg>
                            </div>
                            <div className="rating" data-rating={5}>
                              <svg
                                width={24}
                                height={24}
                                className="text-secondary"
                              >
                                <use xlinkHref="#star-solid" />
                              </svg>
                            </div>
                            <span className="rating-count">(3.5)</span>
                          </div>
                          <div className="review-header">
                            <span className="author-name">Tina Johnson</span>
                            <span className="review-date">– 03/07/2023</span>
                          </div>
                          <p>
                            Vitae tortor condimentum lacinia quis vel eros donec
                            ac. Nam at lectus urna duis convallis convallis
                          </p>
                        </div>
                      </div>
                    </div>
                    <div className="col-lg-6 d-flex flex-wrap gap-3">
                      <div className="col-md-2">
                        <div className="image-holder">
                          <img
                            src="images/reviewer-2.jpg"
                            alt="review"
                            className="img-fluid rounded-circle"
                          />
                        </div>
                      </div>
                      <div className="col-md-8">
                        <div className="review-content">
                          <div className="rating-container d-flex align-items-center">
                            <div className="rating" data-rating={1}>
                              <svg
                                width={24}
                                height={24}
                                className="text-primary"
                              >
                                <use xlinkHref="#star-solid" />
                              </svg>
                            </div>
                            <div className="rating" data-rating={2}>
                              <svg
                                width={24}
                                height={24}
                                className="text-primary"
                              >
                                <use xlinkHref="#star-solid" />
                              </svg>
                            </div>
                            <div className="rating" data-rating={3}>
                              <svg
                                width={24}
                                height={24}
                                className="text-primary"
                              >
                                <use xlinkHref="#star-solid" />
                              </svg>
                            </div>
                            <div className="rating" data-rating={4}>
                              <svg
                                width={24}
                                height={24}
                                className="text-secondary"
                              >
                                <use xlinkHref="#star-solid" />
                              </svg>
                            </div>
                            <div className="rating" data-rating={5}>
                              <svg
                                width={24}
                                height={24}
                                className="text-secondary"
                              >
                                <use xlinkHref="#star-solid" />
                              </svg>
                            </div>
                            <span className="rating-count">(3.5)</span>
                          </div>
                          <div className="review-header">
                            <span className="author-name">Jenny Willis</span>
                            <span className="review-date">– 03/06/2022</span>
                          </div>
                          <p>
                            Vitae tortor condimentum lacinia quis vel eros donec
                            ac. Nam at lectus urna duis convallis convallis
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="add-review mt-5">
                    <h3>Add a review</h3>
                    <p>
                      Your email address will not be published. Required fields
                      are marked *
                    </p>
                    <form id="form" className="form-group">
                      <div className="pb-3">
                        <div className="review-rating">
                          <span>Your rating *</span>
                          <div className="rating-container d-flex align-items-center">
                            <div className="rating" data-rating={1}>
                              <svg
                                width={24}
                                height={24}
                                className="text-primary"
                              >
                                <use xlinkHref="#star-solid" />
                              </svg>
                            </div>
                            <div className="rating" data-rating={2}>
                              <svg
                                width={24}
                                height={24}
                                className="text-primary"
                              >
                                <use xlinkHref="#star-solid" />
                              </svg>
                            </div>
                            <div className="rating" data-rating={3}>
                              <svg
                                width={24}
                                height={24}
                                className="text-primary"
                              >
                                <use xlinkHref="#star-solid" />
                              </svg>
                            </div>
                            <div className="rating" data-rating={4}>
                              <svg
                                width={24}
                                height={24}
                                className="text-secondary"
                              >
                                <use xlinkHref="#star-solid" />
                              </svg>
                            </div>
                            <div className="rating" data-rating={5}>
                              <svg
                                width={24}
                                height={24}
                                className="text-secondary"
                              >
                                <use xlinkHref="#star-solid" />
                              </svg>
                            </div>
                            <span className="rating-count">(3.5)</span>
                          </div>
                        </div>
                      </div>
                      <div className="pb-3">
                        <input
                          type="file"
                          className="form-control"
                          data-text="Choose your file"
                        />
                      </div>
                      <div className="pb-3">
                        <label>Your Review *</label>
                        <textarea
                          className="form-control"
                          placeholder="Write your review here"
                          defaultValue={""}
                        />
                      </div>
                      <div className="pb-3">
                        <label>Your Name *</label>
                        <input
                          type="text"
                          name="name"
                          placeholder="Write your name here"
                          className="form-control"
                        />
                      </div>
                      <div className="pb-3">
                        <label>Your Email *</label>
                        <input
                          type="text"
                          name="email"
                          placeholder="Write your email here"
                          className="form-control"
                        />
                      </div>
                      <div className="pb-3">
                        <label>
                          <input type="checkbox" required="" />
                          <span className="label-body">
                            Save my name, email, and website in this browser for
                            the next time.
                          </span>
                        </label>
                      </div>
                      <button
                        type="submit"
                        name="submit"
                        className="btn btn-dark btn-large text-uppercase w-100"
                      >
                        Submit
                      </button>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

export default Product;
