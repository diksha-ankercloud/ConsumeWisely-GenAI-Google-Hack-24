import logo from "./logo.svg";
import "./App.css";
import Header from "./components/header";
import Footer from "./components/footer";
import Shop from "./pages/shop"
import Homepage from "./pages/homepage";
import Product from "./pages/product";
import Cart from "./pages/cart";
import AboutUs from "./pages/about-us";
import * as ReactDOM from "react-dom/client";
import * as React from "react";
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import Chatbot from "./components/chatbot";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Homepage/>,
  },
  {
    path: "/shop",
    element: <Shop/>,
  },
  {
    path: "/product",
    element: <Product/>,
  },
  {
    path: "/cart",
    element: <Cart/>,
  },
  {
    path: "/about-us",
    element: <AboutUs/>,
  },
]);

function App() {
  return (
    <div className="App">
      <>
        <Header />
        <RouterProvider router={router} />
        <Chatbot/>
        <Footer />
      </>
    </div>
  );
}

export default App;
