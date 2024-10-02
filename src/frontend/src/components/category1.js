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
                        href="#"
                        className="nav-link category-item"
                      >
                        <img
                          src="images/icon-bread-herb-flour.png"
                          
                          alt="Category Thumbnail"
                        />
                        <h3 className="category-title">
                           Organic foods and practices flagging 
                        </h3>
                      </a>
                    </SwiperSlide>
                    <SwiperSlide>
                      <a
                        href="#"
                        className="nav-link category-item "
                      >
                        <img
                          src="images/icon-wine-glass-bottle.png"
                          alt="Category Thumbnail"
                        />
                        <h3 className="category-title">Deciper false claims in a click</h3>
                      </a>
                    </SwiperSlide>
                    <SwiperSlide>
                      <a
                        href="#"
                        className="nav-link category-item "
                      >
                        <img
                          src="images/icon-soft-drinks-bottle.png"
                          alt="Category Thumbnail"
                        />
                        <h3 className="category-title">Alerts on major preservatives</h3>
                      </a>
                    </SwiperSlide>
                    <SwiperSlide>
                      <a
                        href="#"
                        className="nav-link category-item "
                      >
                        <img
                          src="images/icon-small-business.png"
                          alt="Category Thumbnail"
                        />
                        <h3 className="category-title">Small Business Tag</h3>
                      </a>
                    </SwiperSlide>
                    <SwiperSlide>
                      <a
                        href="#"
                        className="nav-link category-item "
                      >
                        <img
                          src="images/icon-vegetables-broccoli.png"
                          alt="Category Thumbnail"
                        />
                        <h3 className="category-title">Sustainablility factors flagging</h3>
                      </a>
                    </SwiperSlide>
                    <SwiperSlide>
                      <a
                        href="#"
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
