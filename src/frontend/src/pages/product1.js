import React, { useEffect, useState } from "react";
import axios from "axios";

import { usellmResponse } from "../context/llmResponse";
import { FaWandMagicSparkles } from "react-icons/fa6";

function Product({}) {
  const [product, setProduct] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const id = urlParams.get("id");

  const { llmResponse } = usellmResponse();

  console.log(id);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_ENDPOINT}/product/${id}`); // Replace with your API URL
        console.log(response);

        setProduct(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, []);

  if (loading) return <p>Loading products...</p>;
  if (error) return <p>Error fetching products: {error}</p>;

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
                    <div className="swiper-wrapper">
                      <div className="swiper-slide">
                        <img
                          src={product.image_front}
                          alt=""
                          className="thumb-image img-fluid"
                        />
                      </div>
                      <div className="swiper-slide">
                        <img
                          src="images/product-thumbnail-2.jpg"
                          alt=""
                          className="thumb-image img-fluid"
                        />
                      </div>
                      <div className="swiper-slide">
                        <img
                          src="images/product-thumbnail-3.jpg"
                          alt=""
                          className="thumb-image img-fluid"
                        />
                      </div>
                      <div className="swiper-slide">
                        <img
                          src="images/product-thumbnail-4.jpg"
                          alt=""
                          className="thumb-image img-fluid"
                        />
                      </div>
                      <div className="swiper-slide">
                        <img
                          src="images/product-thumbnail-5.jpg"
                          alt=""
                          className="thumb-image img-fluid"
                        />
                      </div>
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
                          data-image={product.image_front}
                        >
                          <img
                            src={product.image_front}
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
                  <div className="rating-container d-flex gap-0 align-items-center">
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
                  </div>
                </div>
                <div className="product-price pt-3 pb-3">
                  <strong className="text-primary display-6 fw-bold">
                    Rs. {product.price}
                  </strong>
                  <del className="ms-2">Rs. {product.price}</del>
                </div>
                <p>{product.description}</p>
                {llmResponse?.category && (
                  <>
                    <p>
                      <strong>AI Suggests </strong> <span>  <FaWandMagicSparkles/></span>
                    </p>
                  </>
                )}
                <div className="cart-wrap py-1">
                  {llmResponse?.category && (
                    <>
                      <div className="color-options product-select">
                        <div className="color-toggle" data-option-index={0}>
                          <h6 className="item-title text-uppercase text-dark">
                            Category:
                          </h6>
                          <ul className="select-list list-unstyled d-flex">
                            {llmResponse &&
                              llmResponse?.category?.split(",").map((c) => {
                                return (
                                  <li
                                    className="select-item pe-3"
                                    data-val="Orange"
                                    title="Orange"
                                  >
                                    <a href="#" className="btn btn-light">
                                      {c}
                                    </a>
                                  </li>
                                );
                              })}
                          </ul>
                        </div>
                      </div>
                      <div className="color-options product-select">
                        <div className="color-toggle" data-option-index={0}>
                          <h6 className="item-title text-uppercase text-dark">
                            Consumption:
                          </h6>
                          <ul className="select-list list-unstyled d-flex">
                            {llmResponse &&
                              llmResponse?.consumption?.split(",").map((c) => {
                                return (
                                  <li
                                    className="select-item pe-3"
                                    data-val="Orange"
                                    title="Orange"
                                  >
                                    <a href="#" className="btn btn-light">
                                      {c}
                                    </a>
                                  </li>
                                );
                              })}
                          </ul>
                        </div>
                      </div>
                      <div className="color-options product-select">
                        <div className="color-toggle" data-option-index={0}>
                          <h6 className="item-title text-uppercase text-dark">
                            Diet Type:
                          </h6>
                          <ul className="select-list list-unstyled d-flex">
                            {llmResponse &&
                              llmResponse?.dietType?.split(",").map((c) => {
                                return (
                                  <li
                                    className="select-item pe-3"
                                    data-val="Orange"
                                    title="Orange"
                                  >
                                    <a href="#" className="btn btn-light">
                                      {c}
                                    </a>
                                  </li>
                                );
                              })}
                          </ul>
                        </div>
                      </div>

                      <div className="color-options product-select">
                        <div className="color-toggle" data-option-index={0}>
                          <h6 className="item-title text-uppercase text-dark">
                            Allergic Content:
                          </h6>
                          <ul
                            className="select-list list-unstyled"
                            mt="2"
                            pd="2"
                          >
                            {llmResponse &&
                              llmResponse?.allergies?.split(",").map((c) => {
                                return (
                                  <li
                                    className="select-item pe-3"
                                    data-val="Orange"
                                    title="Orange"
                                  >
                                    <a
                                      href="#"
                                      className="btn btn-danger btn-sm"
                                    >
                                      {c}
                                    </a>
                                  </li>
                                );
                              })}
                          </ul>
                        </div>
                      </div>
                      <p>
                        Caution:{" "}
                        <span style={{ color: "red" }}>
                          {llmResponse?.caution || "No caution available"}
                        </span>
                      </p>
                    </>
                  )}

                  <div className="product-quantity pt-3">
                    <div className="stock-number text-dark">
                      <em>2 in stock</em>
                    </div>
                    <div className="stock-button-wrap">
                      <div
                        className="input-group product-qty"
                        style={{ maxWidth: 150 }}
                      >
                        <span className="input-group-btn">
                          <button
                            type="button"
                            className="quantity-left-minus btn btn-light btn-number"
                            data-type="minus"
                            data-field=""
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
                          min={1}
                          max={100}
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
                      <div className="qty-button d-flex flex-wrap pt-3">
                        <button
                          type="submit"
                          className="btn btn-primary py-3 px-4 text-uppercase me-3 mt-3"
                        >
                          Buy now
                        </button>
                        <button
                          type="submit"
                          name="add-to-cart"
                          value={1269}
                          className="btn btn-dark py-3 px-4 text-uppercase mt-3"
                        >
                          Add to cart
                        </button>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="meta-product py-2">
                  <div className="meta-item d-flex align-items-baseline">
                    <h6 className="item-title no-margin pe-2">Brand:</h6>
                    <ul className="select-list list-unstyled d-flex">
                      <li data-value="S" className="select-item">
                        <a href="#">{product.brands}</a>,
                      </li>
                    </ul>
                  </div>
                  <div className="meta-item d-flex align-items-baseline">
                    <h6 className="item-title no-margin pe-2">Category:</h6>
                    <ul className="select-list list-unstyled d-flex">
                      <li data-value="S" className="select-item">
                        <a href="#">{product.category}</a>,
                      </li>
                    </ul>
                  </div>
                  <div className="meta-item d-flex align-items-baseline">
                    <h6 className="item-title no-margin pe-2">Tags:</h6>
                    <ul className="select-list list-unstyled">
                      {product?.tags?.split(",")?.map((tag) => {
                        return (
                          <li data-value={tag} className="select-item">
                            <a href="#">{tag}</a>,
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                </div>
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
                  Description
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
                  <h5>Product Description</h5>
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
