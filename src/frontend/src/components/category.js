import { Swiper, SwiperSlide, useSwiper } from "swiper/react";

function Category() {
  return (
    <>
      <section className="py-5 overflow-hidden">
        <div className="container-fluid">
          <div className="row">
            <div className="col-md-12">
            <h2 className="section-title" style={{ textAlign: 'center', fontWeight: 'bold', paddingTop: '0px' }}>One Click Results from AI Quick Scan</h2>
              <div className="section-header d-flex flex-wrap justify-content-between mb-5">
                
                
                
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
                           Quick and thorough Allergy alerts
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
                        <h3 className="category-title">Highlight macro nutrients</h3>
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
                        <h3 className="category-title">Diet Suitability for jain/keto/vegan etc</h3>
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
                        <h3 className="category-title">Animal cruelty free flagging</h3>
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
