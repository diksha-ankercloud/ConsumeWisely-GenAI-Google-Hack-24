import React from 'react';

function AboutUs() {
  return (
    <>
      <section
        className="py-5 mb-5"
        style={{ background: "url(images/background-pattern.jpg)" }}
      >
        <div className="container-fluid">
          <div className="d-flex justify-content-between">
            <h1 className="page-title pb-2">About Us</h1>
            <nav className="breadcrumb fs-6">
              <a className="breadcrumb-item nav-link" href="#">
                Home
              </a>
              <a className="breadcrumb-item nav-link" href="#">
                Pages
              </a>
              <span className="breadcrumb-item active" aria-current="page">
                About Us
              </span>
            </nav>
          </div>
        </div>
      </section>

      <section className="company-detail py-4">
        <div className="container">
          <div className="row">
            <div className="col-md-12">
              <blockquote className="blockquote">
                <h2>ConsumeWisely: Your AI-Powered Guide to Healthier Choices</h2>
              </blockquote>
              <p className="lead">
                At ConsumeWisely, we provide <strong>real-time information</strong> on nutritional content, ingredients, and processing methods, helping you make better food choices.
              </p>
            </div>
          </div>

          <h3 className="mt-4">Scan, Analyze, Choose Better</h3>
          <div className="row mt-3">
            <div className="col-md-12">
              <p>
                <strong>Multi-Modal Access:</strong> Scan labels, search for products, or use voice commands for quick and easy access to important nutritional insights.
              </p>
              <p>
                We aim to build a transparent, scalable, and inclusive system for benchmarking brands and products, measuring AI performance across diverse domains, multiple modalities, and every language.
              </p>
            </div>
          </div>

          <h3 className="mt-5">Why Choose ConsumeWisely?</h3>
          <div className="row mt-3">
            <div className="col-md-12">
              <ul>
                <li><strong>Accurate Data:</strong> Precise data capture from product labels, ensuring you stay informed.</li>
                <li><strong>Dynamic Updates:</strong> Our database is constantly updated with the latest products in the market.</li>
                <li><strong>Exhaustive Catalog:</strong> Partnerships with leading retailers like Blinkit and BigBasket provide you with a wide array of products.</li>
                <li><strong>Insightful Augmentation:</strong> Enhanced data based on your preferences for a better understanding of the products.</li>
              </ul>
              <p>
                <strong>Personalized Health Analysis:</strong> Tailored recommendations based on your dietary needs and preferences, making it easier to find healthier options.
              </p>
            </div>
          </div>

          <div className="row mt-5">
            <div className="col-md-12">
              <p>
                Curious to know which packaged foods are best for your diet? Click the "Personalize" button to get detailed information about products that fit your lifestyle.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="py-5 my-5">
        <div className="container-fluid">
          <div
            className="bg-warning py-5 rounded-5"
            style={{ backgroundImage: 'url("images/bg-pattern-2.png")' }}
          >
            <div className="container">
              <div className="row">
                <div className="col-md-12 text-center">
                  <h2 className="my-5">Shop Smarter with the Foodmart App</h2>
                  <p className="lead">
                    Our platform empowers you to make better food choices with:
                  </p>

                  <div className="row">
                    <div className="col-md-4">
                      <h4><strong>Timely Insights</strong></h4>
                      <p>
                        Nutritional information is available when you need it most—right before you make a purchase.
                      </p>
                    </div>
                    <div className="col-md-4">
                      <h4><strong>User-Friendly Experience</strong></h4>
                      <p>
                        Intuitive design ensures all information is clear and easy to digest, minimizing cognitive load.
                      </p>
                    </div>
                    <div className="col-md-4">
                      <h4><strong>Accessibility</strong></h4>
                      <p>
                        Available across multiple interfaces and in various languages, making healthier choices accessible to everyone.
                      </p>
                    </div>
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

export default AboutUs;
