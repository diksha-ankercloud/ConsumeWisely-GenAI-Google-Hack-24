
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
        <div className="container-fluid">
          <div className="row">
            <div className="col-md-12">
              <blockquote>
              Headline: ConsumeWise: Your AI-Powered Guide to Healthier Choices </blockquote>
              <p>
                <strong>Accurate Product Data</strong> 
                Real-time information on nutritional content, ingredients, and processing methods.
              </p>
            </div>
          </div>
          <h2>Scan, Analyze, Choose Better</h2>
          <div className="row">
            <div className="col-md-12">
               <p>Multi-Modal Access: Scan labels, search for products, or use voice commands.</p>
                </div>
           
              <p>
              We want to build a transparent, scalable, and inclusive benchmarking Brands/Products, aiming to measure and improve the performance of AI across diverse domains and multiple modalities, in every language.
              </p>
              
              <p><h2>Why Choose ConsumeWisely?</h2></p>
              <p>
                Accurate Data: Our system ensures precise data capture from product labels, keeping you informed.
                Dynamic Updates: We constantly update our database as new products hit the market.
                Exhaustive Catalog: With partnerships across leading retailers like Blinkit and BigBasket, we provide a vast array of products.
                Insightful Augmentation: From categorizing products based on your preferences to enriching the raw data for enhanced understanding.
              </p>
              <p> Personalized Health Analysis: Tailored recommendations based on your dietary needs and preferences.</p>
      
            
              <p>To some food experts, packaged foods are a cardinal sin. But some packaged foods are better than others. Curious to know which packaged foods you should add to your diet? Tap on Personalise button to get all the information about product
              </p>
          </div>
        </div>
      </section>
      <section className="py-5 my-5">
        <div className="container-fluid">
          <div
            className="bg-warning py-5 rounded-5"
            style={{
              backgroundImage: 'url("images/bg-pattern-2.png") no-repeat',
            }}
          >
            <div className="container">
              <div className="row">
                <div className="col-md-12">
                  <h2 className="my-5">Shop faster with foodmart App</h2>
                  <p>
                  <h4><strong>What We Solve For:</strong></h4>

<p> <strong>Timely Insights:</strong>Timely Insights: Our platform provides nutritional information right when you're about to make a decision.
</p>
<p><strong>User-Friendly Experience:</strong>
 Information is presented in a clear and intuitive way, reducing cognitive overload and helping you focus on the essentials.

</p>
<p><strong>Accessibility:</strong>
: Available across multiple interfaces and languages, ensuring everyone can make healthier choices.

</p>
 </p>
               
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
