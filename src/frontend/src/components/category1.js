import { Swiper, SwiperSlide, useSwiper } from "swiper/react";

function Category1() {
  return (
    <>
      <section className="py-5 overflow-hidden">
        <div className="container-fluid">
          
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
                           Organics
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
                        <h3 className="category-title">Flase Claims</h3>
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
                        <h3 className="category-title">Harmful ingredients</h3>
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
                        <h3 className="category-title">mall Businesses</h3>
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

export default Category1;
