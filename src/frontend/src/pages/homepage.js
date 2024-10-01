import Category from "../components/category";
import Category1 from "../components/category1";

function Homepage() {
  return (
    <>

      <section
        className="py-3"
        style={{
          backgroundImage: 'url("images/background-pattern.jpg")',
          backgroundRepeat: "no-repeat",
          backgroundSize: "cover",
        }}
      >
        <div className="container-fluid">
          <div className="row">
            <div className="col-md-12">
              <div className="banner-blocks">
                <div className="banner-ad large bg-info block-1">
                  <div className="swiper main-swiper">
                    <div className="swiper-wrapper">
                      <div className="swiper-slide">
                        <div className="row banner-content p-5">
                          <div className="content-wrapper col-md-7">
                            <div className="categories my-3">Faster choices</div>
                            <h3 className="display-4">
                              Easier decisions using AI personalisation
                            </h3>
                            <p>
                              Find hidden product info using smart AI results
                            </p>
                            <a
                              href="#"
                              className="btn btn-outline-dark btn-lg text-uppercase fs-6 rounded-1 px-4 py-3 mt-3"
                            >
                              Search
                            </a>
                          </div>
                          <div className="img-wrapper col-md-5">
                            <img
                              src="images/product-thumb-1.png"
                              alt="Product Thumbnail"
                              className="img-fluid"
                            />
                          </div>
                        </div>
                      </div>
                      <div className="swiper-slide">
                        <div className="row banner-content p-5">
                          <div className="content-wrapper col-md-7">
                            <div className="categories mb-3 pb-3">
                              100% natural
                            </div>
                            <h3 className="banner-title">
                              Fresh Smoothie &amp; Summer Juice
                            </h3>
                            <p>
                              Lorem ipsum dolor sit amet, consectetur adipiscing
                              elit. Dignissim massa diam elementum.
                            </p>
                            <a
                              href="#"
                              className="btn btn-outline-dark btn-lg text-uppercase fs-6 rounded-1"
                            >
                              Shop Collection
                            </a>
                          </div>
                          <div className="img-wrapper col-md-5">
                            <img
                              src="images/product-thumb-1.png"
                              alt="Product Thumbnail"
                              className="img-fluid"
                            />
                          </div>
                        </div>
                      </div>
                      <div className="swiper-slide">
                        <div className="row banner-content p-5">
                          <div className="content-wrapper col-md-7">
                            <div className="categories mb-3 pb-3">
                              100% natural
                            </div>
                            <h3 className="banner-title">
                              Heinz Tomato Ketchup
                            </h3>
                            <p>
                              Lorem ipsum dolor sit amet, consectetur adipiscing
                              elit. Dignissim massa diam elementum.
                            </p>
                            <a
                              href="#"
                              className="btn btn-outline-dark btn-lg text-uppercase fs-6 rounded-1"
                            >
                              Shop Collection
                            </a>
                          </div>
                          <div className="img-wrapper col-md-5">
                            <img
                              src="images/product-thumb-2.png"
                              alt="Product Thumbnail"
                              className="img-fluid"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="swiper-pagination" />
                  </div>
                </div>
                <div
                  className="banner-ad bg-success-subtle block-2"
                  style={{
                    background: 'url("images/ad-image-1.png") no-repeat',
                    backgroundPosition: "right bottom",
                  }}
                >
                  <div className="row banner-content p-5">
                    <div className="content-wrapper col-md-7">
                      <div className="categories sale mb-3 pb-3">Smart choices</div>
                      <h5 className="banner-title">Choose based on your preferences</h5>
                      
                    </div>
                  </div>
                </div>
                <div
                  className="banner-ad bg-danger block-3"
                  style={{
                    background: 'url("images/ad-image-2.png") no-repeat',
                    backgroundPosition: "right bottom",
                  }}
                >
                  <div className="row banner-content p-5">
                    <div className="content-wrapper col-md-7">
                      <div className="categories sale mb-3 pb-3">Get Creative</div>
                      <h5 className="item-title">Recipes based on your cravings</h5>
                     
                    </div>
                  </div>
                </div>
              </div>
              {/* / Banner Blocks */}
            </div>
          </div>
        </div>
      </section>
      <h2 className="section-title" style={{ textAlign: 'center', fontWeight: 'bold', paddingTop: '40px' }}>Our Best Features for you</h2 >
      <section className="py-5">
      
        <div className="container-fluid">
          <div className="row row-cols-1 row-cols-sm-3 row-cols-lg-5">
          
            <div className="col">
              <div className="card mb-3 border-0">
                <div className="row">
                  <div className="col-md-2 text-dark">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width={32}
                      height={32}
                      viewBox="0 0 24 24"
                    >
                      <path
                        fill="currentColor"
                        d="M21.5 15a3 3 0 0 0-1.9-2.78l1.87-7a1 1 0 0 0-.18-.87A1 1 0 0 0 20.5 4H6.8l-.33-1.26A1 1 0 0 0 5.5 2h-2v2h1.23l2.48 9.26a1 1 0 0 0 1 .74H18.5a1 1 0 0 1 0 2h-13a1 1 0 0 0 0 2h1.18a3 3 0 1 0 5.64 0h2.36a3 3 0 1 0 5.82 1a2.94 2.94 0 0 0-.4-1.47A3 3 0 0 0 21.5 15Zm-3.91-3H9L7.34 6H19.2ZM9.5 20a1 1 0 1 1 1-1a1 1 0 0 1-1 1Zm8 0a1 1 0 1 1 1-1a1 1 0 0 1-1 1Z"
                      />
                    </svg>
                  </div>
                  <div className="col-md-10">
                    <div className="card-body p-0">
                      <h5><h5><strong>Personalised Products</strong></h5></h5>
                      <p className="card-text">
                        Get your Recommendationsas per your dietry plans and goals!
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="col">
              <div className="card mb-3 border-0">
                <div className="row">
                  <div className="col-md-2 text-dark">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width={32}
                      height={32}
                      viewBox="0 0 24 24"
                    >
                      <path
                        fill="currentColor"
                        d="M19.63 3.65a1 1 0 0 0-.84-.2a8 8 0 0 1-6.22-1.27a1 1 0 0 0-1.14 0a8 8 0 0 1-6.22 1.27a1 1 0 0 0-.84.2a1 1 0 0 0-.37.78v7.45a9 9 0 0 0 3.77 7.33l3.65 2.6a1 1 0 0 0 1.16 0l3.65-2.6A9 9 0 0 0 20 11.88V4.43a1 1 0 0 0-.37-.78ZM18 11.88a7 7 0 0 1-2.93 5.7L12 19.77l-3.07-2.19A7 7 0 0 1 6 11.88v-6.3a10 10 0 0 0 6-1.39a10 10 0 0 0 6 1.39Zm-4.46-2.29l-2.69 2.7l-.89-.9a1 1 0 0 0-1.42 1.42l1.6 1.6a1 1 0 0 0 1.42 0L15 11a1 1 0 0 0-1.42-1.42Z"
                      />
                    </svg>
                  </div>
                  <div className="col-md-10">
                    <div className="card-body p-0">
                      <h5><h5><strong>Verify Claims</strong></h5></h5>
                      <p className="card-text">
                        You can Now Verify False claims on Packaging!
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="col">
              <div className="card mb-3 border-0">
                <div className="row">
                  <div className="col-md-2 text-dark">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width={32}
                      height={32}
                      viewBox="0 0 24 24"
                    >
                      <path
                        fill="currentColor"
                        d="M22 5H2a1 1 0 0 0-1 1v4a3 3 0 0 0 2 2.82V22a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1v-9.18A3 3 0 0 0 23 10V6a1 1 0 0 0-1-1Zm-7 2h2v3a1 1 0 0 1-2 0Zm-4 0h2v3a1 1 0 0 1-2 0ZM7 7h2v3a1 1 0 0 1-2 0Zm-3 4a1 1 0 0 1-1-1V7h2v3a1 1 0 0 1-1 1Zm10 10h-4v-2a2 2 0 0 1 4 0Zm5 0h-3v-2a4 4 0 0 0-8 0v2H5v-8.18a3.17 3.17 0 0 0 1-.6a3 3 0 0 0 4 0a3 3 0 0 0 4 0a3 3 0 0 0 4 0a3.17 3.17 0 0 0 1 .6Zm2-11a1 1 0 0 1-2 0V7h2ZM4.3 3H20a1 1 0 0 0 0-2H4.3a1 1 0 0 0 0 2Z"
                      />
                    </svg>
                  </div>
                  <div className="col-md-10">
                    <div className="card-body p-0">
                      <h5><h5><strong>Exhaustive Search</strong></h5></h5>
                      <p className="card-text">
                        Dynamic Searching for your products!
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="col">
              <div className="card mb-3 border-0">
                <div className="row">
                  <div className="col-md-2 text-dark">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width={32}
                      height={32}
                      viewBox="0 0 24 24"
                    >
                      <path
                        fill="currentColor"
                        d="M12 8.35a3.07 3.07 0 0 0-3.54.53a3 3 0 0 0 0 4.24L11.29 16a1 1 0 0 0 1.42 0l2.83-2.83a3 3 0 0 0 0-4.24A3.07 3.07 0 0 0 12 8.35Zm2.12 3.36L12 13.83l-2.12-2.12a1 1 0 0 1 0-1.42a1 1 0 0 1 1.41 0a1 1 0 0 0 1.42 0a1 1 0 0 1 1.41 0a1 1 0 0 1 0 1.42ZM12 2A10 10 0 0 0 2 12a9.89 9.89 0 0 0 2.26 6.33l-2 2a1 1 0 0 0-.21 1.09A1 1 0 0 0 3 22h9a10 10 0 0 0 0-20Zm0 18H5.41l.93-.93a1 1 0 0 0 0-1.41A8 8 0 1 1 12 20Z"
                      />
                    </svg>
                  </div>
                  <div className="col-md-10">
                    <div className="card-body p-0">
                      <h5><h5><strong>All product Scans</strong></h5></h5>
                      <p className="card-text">
                      Scan each product on the internet to check dietary requiremnts!
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="col">
              <div className="card mb-3 border-0">
                <div className="row">
                  <div className="col-md-2 text-dark">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width={32}
                      height={32}
                      viewBox="0 0 24 24"
                    >
                      <path
                        fill="currentColor"
                        d="M18 7h-.35A3.45 3.45 0 0 0 18 5.5a3.49 3.49 0 0 0-6-2.44A3.49 3.49 0 0 0 6 5.5A3.45 3.45 0 0 0 6.35 7H6a3 3 0 0 0-3 3v2a1 1 0 0 0 1 1h1v6a3 3 0 0 0 3 3h8a3 3 0 0 0 3-3v-6h1a1 1 0 0 0 1-1v-2a3 3 0 0 0-3-3Zm-7 13H8a1 1 0 0 1-1-1v-6h4Zm0-9H5v-1a1 1 0 0 1 1-1h5Zm0-4H9.5A1.5 1.5 0 1 1 11 5.5Zm2-1.5A1.5 1.5 0 1 1 14.5 7H13ZM17 19a1 1 0 0 1-1 1h-3v-7h4Zm2-8h-6V9h5a1 1 0 0 1 1 1Z"
                      />
                    </svg>
                  </div>
                  <div className="col-md-10">
                    <div className="card-body p-0">
                      <h5><h5><strong>Vocal for Local</strong></h5></h5>
                      <p className="card-text">
                      We flag small business to help them grow!
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
      
      <section id="latest-blog" className="py-5">
        <div className="container-fluid">
          <div className="row">
          <h2 className="section-title" style={{ textAlign: 'center', fontWeight: 'bold', paddingTop: '0px' }}>Our Push towards Sustainibility</h2>
            <div className="section-header d-flex align-items-center justify-content-between my-5">
            
             
            </div>
          </div>
          <div className="row">
            <div className="col-md-4">
              <article className="post-item card border-0 shadow-sm p-3">
                <div className="image-holder zoom-effect">
                  <a href="#">
                    <img
                      src="images/post-thumb-1.jpg"
                      alt="post"
                      className="card-img-top"
                    />
                  </a>
                </div>
                <div className="card-body">
                  <div className="post-meta d-flex text-uppercase gap-3 my-2 align-items-center">
                    
                    
                  </div>
                  <div className="post-header">
                    <h3 className="post-title">
                      <a href="#" className="text-decoration-none">
                        Carbon footprints of your favourite brands
                      </a>
                    </h3>
                    <p>
                    At Consumewisely, we flag products that minimize their carbon footprint, helping you make eco-friendly choices effortlessly. From sustainable manufacturing to lower emissions, we highlight the products that contribute less to greenhouse gases. Take control of your environmental impact and make a difference with every purchase through Consumewisely!
                    </p>
                  </div>
                </div>
              </article>

            </div>
            <div className="col-md-4">
              <article className="post-item card border-0 shadow-sm p-3">
                <div className="image-holder zoom-effect">
                  <a href="#">
                    <img
                      src="images/post-thumb-2.jpg"
                      alt="post"
                      className="card-img-top"
                    />
                  </a>
                </div>
                <div className="card-body">
                  <div className="post-meta d-flex text-uppercase gap-3 my-2 align-items-center">
                   
                   
                  </div>
                  <div className="post-header">
                    <h3 className="post-title">
                      <a href="#" className="text-decoration-none">
                        Following sutanibility in the present!
                      </a>
                    </h3>
                    <p>
                    With Consumewisely, you’re always in the know! We showcase the latest products that align with 2024’s top sustainability trends. From eco-friendly innovations to companies adopting green practices, we flag the products that are leading the way. Make sustainable choices that are not just good for you, but great for the planet!
                    </p>
                  </div>
                </div>
              </article>
            </div>
            <div className="col-md-4">
              <article className="post-item card border-0 shadow-sm p-3">
                <div className="image-holder zoom-effect">
                  <a href="#">
                    <img
                      src="images/post-thumb-3.jpg"
                      alt="post"
                      className="card-img-top"
                    />
                  </a>
                </div>
                <div className="card-body">
                  <div className="post-meta d-flex text-uppercase gap-3 my-2 align-items-center">
                   
                    
                  </div>
                  <div className="post-header">
                    <h3 className="post-title">
                      <a href="#" className="text-decoration-none">
                        Everything You Need To Know About Organic Food.
                      </a>
                    </h3>
                    <p>
                    Looking for clean, natural, and eco-friendly food options? Consumewisely flags the best organic products for you! Discover chemical-free, sustainably grown foods, and learn how they benefit both your health and the environment. Plus, find packaging solutions that minimize waste. Eat clean and live green with Consumewisely!
                    </p>
                  </div>
                </div>
              </article>
            </div>
          </div>
        </div>
      </section>

      <Category/>
      <Category1/>
       


     
    </>
  );
}

export default Homepage;
