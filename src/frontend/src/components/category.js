import { Swiper, SwiperSlide, useSwiper } from "swiper/react";

function Category() {
  return (
    <>
      <section className="py-5 overflow-hidden">
        <div className="container-fluid">
          <div className="row">
            <div className="col-md-12">
              <div className="section-header d-flex flex-wrap justify-content-between mb-5">
                <h2 className="section-title">Category</h2>
                <div className="d-flex align-items-center">
                  <a href="#" className="btn-link text-decoration-none">
                    View All Categories →
                  </a>
                  <div className="swiper-buttons">
                    <button
                      className="swiper-prev category-carousel-prev btn btn-yellow"
                    >
                      ❮
                    </button>
                    <button className="swiper-next category-carousel-next btn btn-yellow">
                      ❯
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="row">
            <div className="col-md-12">
              <div className="category-carousel swiper">
                <div className="swiper-wrapper">
                  <Swiper
                    spaceBetween={50}
                    slidesPerView={4}
                    onSlideChange={() => console.log("slide change")}
                    onSwiper={(swiper) => console.log(swiper)}
                  >
                    <SwiperSlide>
                      <a
                        href="category.html"
                        className="nav-link category-item"
                      >
                        <img
                          src="images/icon-vegetables-broccoli.png"
                          alt="Category Thumbnail"
                        />
                        <h3 className="category-title">
                          Supports Small Businesses
                        </h3>
                      </a>
                    </SwiperSlide>
                    <SwiperSlide>
                      <a
                        href="category.html"
                        className="nav-link category-item "
                      >
                        <img
                          src="images/icon-animal-products-drumsticks.png"
                          alt="Category Thumbnail"
                        />
                        <h3 className="category-title">Animal Cruelty-Free</h3>
                      </a>
                    </SwiperSlide>
                    <SwiperSlide>
                      <a
                        href="category.html"
                        className="nav-link category-item "
                      >
                        <img
                          src="images/icon-vegetables-broccoli.png"
                          alt="Category Thumbnail"
                        />
                        <h3 className="category-title">Vegan</h3>
                      </a>
                    </SwiperSlide>
                    <SwiperSlide>
                      <a
                        href="category.html"
                        className="nav-link category-item "
                      >
                        <img
                          src="images/icon-vegetables-broccoli.png"
                          alt="Category Thumbnail"
                        />
                        <h3 className="category-title">Non Organinc</h3>
                      </a>
                    </SwiperSlide>
                    <SwiperSlide>
                      <a
                        href="category.html"
                        className="nav-link category-item "
                      >
                        <img
                          src="images/icon-vegetables-broccoli.png"
                          alt="Category Thumbnail"
                        />
                        <h3 className="category-title">Sustainable</h3>
                      </a>
                    </SwiperSlide>
                    ...
                  </Swiper>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

export default Category;
